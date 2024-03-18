# Copyright 2023 Ant Group Co., Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import enum
import json
import logging
import math
import os
import uuid
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple, Union

import numpy as np
import pandas as pd

from secretflow.data import FedNdarray
from secretflow.data.core.io import read_file_meta
from secretflow.data.vertical import read_csv
from secretflow.data.vertical.dataframe import VDataFrame
from secretflow.device.device.pyu import PYU, PYUObject
from secretflow.device.device.spu import SPU, SPUObject
from secretflow.device.driver import DeviceObject, reveal, wait
from secretflow.spec.extend.data_pb2 import DeviceObjectCollection
from secretflow.spec.v1.component_pb2 import IoDef
from secretflow.spec.v1.data_pb2 import (
    DistData,
    IndividualTable,
    SystemInfo,
    TableSchema,
    VerticalTable,
)


class MetaEnum(enum.EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class BaseEnum(enum.Enum, metaclass=MetaEnum):
    def __repr__(self):
        return self.value

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return str(self) == str(other)


@enum.unique
class DistDataType(BaseEnum):
    # tables
    VERTICAL_TABLE = "sf.table.vertical_table"
    INDIVIDUAL_TABLE = "sf.table.individual"
    # models
    SS_SGD_MODEL = "sf.model.ss_sgd"
    SS_GLM_MODEL = "sf.model.ss_glm"
    SGB_MODEL = "sf.model.sgb"
    SS_XGB_MODEL = "sf.model.ss_xgb"
    SL_NN_MODEL = "sf.model.sl_nn"
    # binning rule
    BIN_RUNNING_RULE = "sf.rule.binning"
    # others preprocessing rules
    PREPROCESSING_RULE = "sf.rule.preprocessing"
    # report
    REPORT = "sf.report"
    # read data
    READ_DATA = "sf.read_data"
    # serving model file
    SERVING_MODEL = "sf.serving.model"


@enum.unique
class DataSetFormatSupported(BaseEnum):
    CSV = "csv"


SUPPORTED_VTABLE_DATA_TYPE = {
    "int8": np.int8,
    "int16": np.int16,
    "int32": np.int32,
    "int64": np.int64,
    "uint8": np.uint8,
    "uint16": np.uint16,
    "uint32": np.uint32,
    "uint64": np.uint64,
    "float16": np.float16,
    "float32": np.float32,
    "float64": np.float64,
    "bool": bool,
    "int": int,
    "float": float,
    "str": object,
}

REVERSE_DATA_TYPE_MAP = dict((v, k) for k, v in SUPPORTED_VTABLE_DATA_TYPE.items())


def check_io_def(io_def: IoDef):
    for t in io_def.types:
        if t not in DistDataType:
            raise ValueError(
                f"IoDef {io_def.name}: {t} is not a supported DistData types"
            )


def check_dist_data(data: DistData, io_def: IoDef = None):
    if io_def is not None:
        check_io_def(io_def)
        if data.type not in list(io_def.types):
            raise ValueError(
                f"DistData {data.name}: type {data.type} is not allowed according to io def {io_def.types}."
            )

    if data.type == DistDataType.INDIVIDUAL_TABLE:
        if len(data.data_refs) > 1:
            raise f"DistData {data.name}: data_refs is greater than 1 for {data.type}"


@dataclass
class DistdataInfo:
    uri: str
    format: str


def extract_distdata_info(
    db: DistData,
) -> Dict[str, DistdataInfo]:
    ret = {}

    for dr in db.data_refs:
        ret[dr.party] = DistdataInfo(dr.uri, dr.format)

    return ret


def merge_individuals_to_vtable(srcs: List[DistData], dest: DistData) -> DistData:
    # copy srcs' schema into dist
    # use for union individual tables into vtable
    vmeta = VerticalTable()
    for s in srcs:
        assert s.type == DistDataType.INDIVIDUAL_TABLE
        imeta = IndividualTable()
        assert s.meta.Unpack(imeta)
        vmeta.schemas.append(imeta.schema)
        vmeta.line_count = imeta.line_count

    dest.meta.Pack(vmeta)

    return dest


def extract_table_header(
    db: DistData,
    partitions_order: List[str] = None,
    load_features: bool = False,
    load_labels: bool = False,
    load_ids: bool = False,
    col_selects: List[str] = None,
    col_excludes: List[str] = None,
    return_schema_names: bool = False,
) -> Dict[str, Dict[str, np.dtype]]:
    """
    Args:
        db (DistData): input DistData.
        load_features (bool, optional): Whether to load feature cols. Defaults to False.
        load_labels (bool, optional): Whether to load label cols. Defaults to False.
        load_ids (bool, optional): Whether to load id cols. Defaults to False.
        col_selects (List[str], optional): Load part of cols. Applies to all cols. Defaults to None.
        col_excludes (List[str], optional): Load all cols exclude these. Applies to all cols. Defaults to None. Couldn't use with col_selects.
        return_schema_names (bool, optional): if True, also return schema names Dict[str, List[str]]
    """
    meta = (
        IndividualTable()
        if db.type.lower() == DistDataType.INDIVIDUAL_TABLE
        else VerticalTable()
    )
    db.meta.Unpack(meta)
    schemas = (
        [meta.schema]
        if db.type.lower() == DistDataType.INDIVIDUAL_TABLE
        else meta.schemas
    )
    col_selects_set = None
    if col_selects is not None:
        col_selects_set = set(col_selects)
        assert len(col_selects) == len(
            col_selects_set
        ), f"no repetition allowed in col_selects, got {col_selects}"

    if col_excludes is not None:
        col_excludes = set(col_excludes)

    if col_selects_set is not None and col_excludes is not None:
        intersection = set.intersection(col_selects_set, col_excludes)
        assert (
            len(intersection) == 0
        ), f'The following items are in both col_selects and col_excludes : {intersection}, which is not allowed.'

    ret = dict()
    schema_names = {}
    labels = {}
    features = {}
    ids = {}
    for slice, dr in zip(schemas, db.data_refs):
        smeta = dict()
        party_labels = []
        party_features = []
        party_ids = []
        if load_features:
            for t, h in zip(slice.feature_types, slice.features):
                if col_selects_set is not None:
                    if h not in col_selects_set:
                        # feature not selected, skip
                        continue
                    col_selects_set.remove(h)

                if col_excludes is not None:
                    if h in col_excludes:
                        continue

                t = t.lower()
                assert (
                    t in SUPPORTED_VTABLE_DATA_TYPE
                ), f"The feature type {t} is not supported"
                if return_schema_names:
                    party_features.append(h)
                smeta[h] = SUPPORTED_VTABLE_DATA_TYPE[t]
        if load_labels:
            for t, h in zip(slice.label_types, slice.labels):
                if col_selects_set is not None:
                    if h not in col_selects_set:
                        # label not selected, skip
                        continue
                    col_selects_set.remove(h)

                if col_excludes is not None:
                    if h in col_excludes:
                        continue

                if return_schema_names:
                    party_labels.append(h)
                smeta[h] = SUPPORTED_VTABLE_DATA_TYPE[t]
        if load_ids:
            for t, h in zip(slice.id_types, slice.ids):
                if col_selects_set is not None:
                    if h not in col_selects_set:
                        # id not selected, skip
                        continue
                    col_selects_set.remove(h)

                if col_excludes is not None:
                    if h in col_excludes:
                        continue

                if return_schema_names:
                    party_ids.append(h)

                smeta[h] = SUPPORTED_VTABLE_DATA_TYPE[t]

        # reorder items according to col selects
        if col_selects is not None and len(col_selects) > 0:
            party_labels = [i for i in col_selects if i in party_labels]
            party_features = [i for i in col_selects if i in party_features]
            party_ids = [i for i in col_selects if i in party_ids]
            ordered_smeta = {i: smeta[i] for i in col_selects if i in smeta}
            smeta = ordered_smeta

        if len(smeta):
            ret[dr.party] = smeta
            labels[dr.party] = party_labels
            features[dr.party] = party_features
            ids[dr.party] = party_ids

    def reorder_partitions(d: Dict[str, Any]):
        if partitions_order is None:
            return d
        assert set(partitions_order) == set(d.keys())
        return {k: d[k] for k in partitions_order}

    ret = reorder_partitions(ret)
    schema_names["labels"] = reorder_partitions(labels)
    schema_names["features"] = reorder_partitions(features)
    schema_names["ids"] = reorder_partitions(ids)

    if col_selects_set is not None and len(col_selects_set) > 0:
        raise AttributeError(f"unknown cols {col_selects_set} in col_selects")
    if return_schema_names:
        return ret, schema_names
    return ret


def load_table(
    ctx,
    db: DistData,
    *,
    partitions_order: List[str] = None,
    load_features: bool = False,
    load_labels: bool = False,
    load_ids: bool = False,
    col_selects: List[str] = None,  # if None, load all cols
    col_excludes: List[str] = None,
    return_schema_names: bool = False,
    nrows: int = None,
) -> VDataFrame:
    assert load_features or load_labels or load_ids, "At least one flag should be true"
    assert (
        db.type.lower() == DistDataType.INDIVIDUAL_TABLE
        or db.type.lower() == DistDataType.VERTICAL_TABLE
    ), f"path format {db.type.lower()} should be sf.table.individual or sf.table.vertical_table"
    if return_schema_names:
        v_headers, schema_names = extract_table_header(
            db,
            partitions_order=partitions_order,
            load_features=load_features,
            load_labels=load_labels,
            load_ids=load_ids,
            col_selects=col_selects,
            col_excludes=col_excludes,
            return_schema_names=True,
        )
    else:
        v_headers = extract_table_header(
            db,
            partitions_order=partitions_order,
            load_features=load_features,
            load_labels=load_labels,
            load_ids=load_ids,
            col_selects=col_selects,
            col_excludes=col_excludes,
        )
    parties_path_format = extract_distdata_info(db)
    for p in v_headers:
        assert (
            p in parties_path_format
        ), f"schema party {p} is not in dataref parties {v_headers.keys()}"
        # only support csv for now, skip type distribute
        assert (
            parties_path_format[p].format.lower() in DataSetFormatSupported
        ), f"Illegal path format: {parties_path_format[p].format.lower()}, path format of party {p} should be in DataSetFormatSupported"
    # TODO: assert system_info

    with ctx.tracer.trace_io():
        pyus = {p: PYU(p) for p in v_headers}
        filepaths = {
            pyus[p]: os.path.join(ctx.local_fs_wd, parties_path_format[p].uri)
            for p in v_headers
        }
        dtypes = {pyus[p]: v_headers[p] for p in v_headers}
        vdf = read_csv(filepaths, dtypes=dtypes, nrows=nrows)
        wait(vdf)
        shape = vdf.shape
        logging.info(f"loaded VDataFrame, shape {shape}")
        assert math.prod(shape), "empty dataset is not allowed"

    if return_schema_names:
        return vdf, schema_names
    return vdf


def load_table_select_and_exclude_pair(
    ctx,
    db: DistData,
    load_features: bool = False,
    load_labels: bool = False,
    load_ids: bool = False,
    col_selects: List[str] = None,  # if None, load all cols
    to_pandas: bool = True,
    nrows: int = None,
):
    """
    Load two tables, one is the selected, another is the complement.
    """
    trans_x = load_table(
        ctx,
        db,
        load_features=load_features,
        load_labels=load_labels,
        load_ids=load_ids,
        col_selects=col_selects,
        nrows=nrows,
    )

    remain_x = load_table(
        ctx,
        db,
        load_features=True,
        load_ids=True,
        load_labels=True,
        col_excludes=col_selects,
        nrows=nrows,
    )
    if to_pandas:
        trans_x = trans_x.to_pandas()
        remain_x = remain_x.to_pandas()
    return trans_x, remain_x


def move_feature_to_label(schema: TableSchema, label: str) -> TableSchema:
    new_schema = TableSchema()
    new_schema.CopyFrom(schema)
    if label in list(schema.features) and label not in list(schema.labels):
        new_schema.ClearField('features')
        new_schema.ClearField('feature_types')
        for k, v in zip(list(schema.features), list(schema.feature_types)):
            if k != label:
                new_schema.features.append(k)
                new_schema.feature_types.append(v)
            else:
                label_type = v
        new_schema.labels.append(label)
        new_schema.label_types.append(label_type)
    return new_schema


@dataclass
class VerticalTableWrapper:
    line_count: int
    schema_map: Dict[str, TableSchema]

    def to_vertical_table(self, order: List[str] = None):
        if order is None:
            schemas = list(self.schema_map.values())
        else:
            schemas = [self.schema_map[k] for k in order]

        return VerticalTable(schemas=schemas, line_count=self.line_count)

    @classmethod
    def from_dist_data(cls, data: DistData, line_count: int = None):
        meta = VerticalTable()
        assert data.meta.Unpack(meta)

        return cls(
            line_count=meta.line_count if line_count is None else line_count,
            schema_map={
                data_ref.party: schema
                for data_ref, schema in zip(list(data.data_refs), list(meta.schemas))
            },
        )


def dump_vertical_table(
    ctx,
    v_data: VDataFrame,
    uri: str,
    meta: VerticalTableWrapper,
    system_info: SystemInfo,
) -> DistData:
    assert isinstance(v_data, VDataFrame)
    assert v_data.aligned
    assert len(v_data.partitions) > 0
    assert math.prod(v_data.shape), "empty dataset is not allowed"

    parties_length = {}
    for device, part in v_data.partitions.items():
        parties_length[device.party] = len(part)
    assert (
        len(set(parties_length.values())) == 1
    ), f"number of samples must be equal across all devices, got {parties_length}"

    with ctx.tracer.trace_io():
        output_uri = {p: uri for p in v_data.partitions}
        output_path = {
            p: os.path.join(ctx.local_fs_wd, output_uri[p]) for p in output_uri
        }
        wait(v_data.to_csv(output_path, index=False))
        order = [p.party for p in v_data.partitions]
        file_metas = {}
        for pyu in output_path:
            file_metas[pyu] = reveal(pyu(read_file_meta)(output_path[pyu]))
        logging.info(
            f"dumped VDataFrame, file uri {output_path}, samples {parties_length}, file meta {file_metas}"
        )

    ret = DistData(
        name=uri,
        type=str(DistDataType.VERTICAL_TABLE),
        system_info=system_info,
        data_refs=[
            DistData.DataRef(uri=output_uri[p], party=p.party, format="csv")
            for p in output_uri
        ],
    )
    ret.meta.Pack(meta.to_vertical_table(order))

    return ret


def model_dumps(
    ctx,
    model_name: str,
    model_type: str,
    major_version: int,
    minor_version: int,
    objs: List[DeviceObject],
    public_info: Any,
    dist_data_uri: str,
    system_info: SystemInfo,
) -> DistData:
    # TODO: only local fs is supported at this moment.
    storage_root = ctx.local_fs_wd
    objs_uri = []
    objs_party = []
    saved_objs = []
    for i, obj in enumerate(objs):
        if isinstance(obj, PYUObject):
            device: PYU = obj.device
            uri = f"{dist_data_uri}/{i}"
            path = os.path.join(storage_root, uri)

            def dumps(path: str, obj: Any):
                import pickle
                from pathlib import Path

                # create parent folders.
                file = Path(path)
                file.parent.mkdir(parents=True, exist_ok=True)

                with open(path, "wb") as f:
                    f.write(pickle.dumps(obj))

            wait(device(dumps)(path, obj))

            saved_obj = DeviceObjectCollection.DeviceObject(
                type="pyu", data_ref_idxs=[len(objs_uri)]
            )
            saved_objs.append(saved_obj)
            objs_uri.append(uri)
            objs_party.append(device.party)
        elif isinstance(obj, SPUObject):
            device: SPU = obj.device
            uris = [f"{dist_data_uri}/{i}" for party in device.actors.keys()]
            spu_paths = [os.path.join(storage_root, uri) for uri in uris]

            device.dump(obj, spu_paths)

            saved_obj = DeviceObjectCollection.DeviceObject(
                type="spu", data_ref_idxs=[len(objs_uri) + p for p in range(len(uris))]
            )
            saved_objs.append(saved_obj)
            objs_uri.extend(uris)
            objs_party.extend(list(device.actors.keys()))
        else:
            raise RuntimeError(f"not supported objs type {type(obj)}")

    model_info = {
        "major_version": major_version,
        "minor_version": minor_version,
        "public_info": public_info,
    }

    model_meta = DeviceObjectCollection(
        objs=saved_objs,
        public_info=json.dumps(model_info),
    )

    dist_data = DistData(
        name=model_name,
        type=str(model_type),
        system_info=system_info,
        data_refs=[
            DistData.DataRef(uri=uri, party=p, format="pickle")
            for uri, p in zip(objs_uri, objs_party)
        ],
    )
    dist_data.meta.Pack(model_meta)

    return dist_data


def get_model_public_info(dist_data: DistData):
    model_meta = DeviceObjectCollection()
    assert dist_data.meta.Unpack(model_meta)
    model_info = json.loads(model_meta.public_info)
    return json.loads(model_info["public_info"])


def model_meta_info(
    dist_data: DistData,
    max_major_version: int,
    max_minor_version: int,
    model_type: str,
    # TODO: assert system_info
    # system_info: SystemInfo = None,
) -> Tuple[List[DeviceObject], str]:
    assert dist_data.type == model_type
    model_meta = DeviceObjectCollection()
    assert dist_data.meta.Unpack(model_meta)

    model_info = json.loads(model_meta.public_info)

    assert (
        isinstance(model_info, dict)
        and "major_version" in model_info
        and "minor_version" in model_info
        and "public_info" in model_info
    )

    assert (
        max_major_version >= model_info["major_version"]
        and max_minor_version >= model_info["minor_version"]
    ), "not support model version"

    return model_info["public_info"]


def model_loads(
    ctx,
    dist_data: DistData,
    max_major_version: int,
    max_minor_version: int,
    model_type: str,
    pyus: Dict[str, PYU] = None,
    spu: SPU = None,
    # TODO: assert system_info
    # system_info: SystemInfo = None,
) -> Tuple[List[DeviceObject], str]:
    # TODO: only local fs is supported at this moment.
    storage_root = ctx.local_fs_wd
    assert dist_data.type == model_type
    model_meta = DeviceObjectCollection()
    assert dist_data.meta.Unpack(model_meta)

    model_info = json.loads(model_meta.public_info)

    assert (
        isinstance(model_info, dict)
        and "major_version" in model_info
        and "minor_version" in model_info
        and "public_info" in model_info
    )

    assert (
        max_major_version >= model_info["major_version"]
        and max_minor_version >= model_info["minor_version"]
    ), "not support model version"

    objs = []
    for save_obj in model_meta.objs:
        if save_obj.type == "pyu":
            assert len(save_obj.data_ref_idxs) == 1
            data_ref = dist_data.data_refs[save_obj.data_ref_idxs[0]]
            party = data_ref.party
            if pyus is not None:
                assert party in pyus, f"party {party} not in '{','.join(pyus.keys())}'"
                pyu = pyus[party]
            else:
                pyu = PYU(party)

            assert data_ref.format == "pickle"

            def loads(path: str) -> Any:
                import pickle

                with open(path, "rb") as f:
                    # TODO: not secure, may change to json loads/dumps?
                    return pickle.loads(f.read())

            objs.append(pyu(loads)(os.path.join(storage_root, data_ref.uri)))
        elif save_obj.type == "spu":
            # TODO: only support one spu for now
            assert spu is not None
            assert len(save_obj.data_ref_idxs) > 1
            full_paths = {}
            for data_ref_idx in save_obj.data_ref_idxs:
                data_ref = dist_data.data_refs[data_ref_idx]
                assert data_ref.format == "pickle"
                party = data_ref.party
                assert party not in full_paths
                full_paths[party] = os.path.join(storage_root, data_ref.uri)
            assert set(full_paths.keys()) == set(spu.actors.keys())
            spu_paths = [full_paths[party] for party in spu.actors.keys()]
            objs.append(spu.load(spu_paths))
        else:
            raise RuntimeError(f"not supported objs type {save_obj.type}")

    return objs, model_info["public_info"]


def save_prediction_csv(
    pred_df: pd.DataFrame,
    pred_key: str,
    path: str,
    addition_df: Union[List[pd.DataFrame], List[np.array]] = None,
    addition_keys: List[str] = None,
    try_append: bool = False,
) -> None:
    x = pd.DataFrame(pred_df, columns=[pred_key])

    addition_df = [
        df if isinstance(df, pd.DataFrame) else pd.DataFrame(df) for df in addition_df
    ]

    if addition_df:
        assert addition_keys
        addition_data = pd.concat(addition_df, axis=1)
        addition_data.columns = addition_keys
        x = pd.concat([x, addition_data], axis=1)

    import os

    if try_append:
        if not os.path.isfile(path):
            x.to_csv(path, index=False)
        else:
            x.to_csv(path, mode='a', header=False, index=False)
    else:
        x.to_csv(path, index=False)


def gen_prediction_csv_meta(
    addition_headers: Dict[str, np.dtype],
    saved_ids: List[str],
    saved_labels: List[str],
    saved_features: List[str],
    pred_name: str,
    line_count: int = None,
) -> IndividualTable:
    return IndividualTable(
        schema=TableSchema(
            ids=saved_ids,
            id_types=[REVERSE_DATA_TYPE_MAP[addition_headers[k]] for k in saved_ids],
            labels=saved_labels + [pred_name],
            label_types=[
                REVERSE_DATA_TYPE_MAP[addition_headers[k]] for k in saved_labels
            ]
            + ["float"],
            feature_types=[
                REVERSE_DATA_TYPE_MAP[addition_headers[k]] for k in saved_features
            ],
            features=saved_features,
        ),
        line_count=line_count if line_count is not None else -1,
    )


class SimpleVerticalBatchReader:
    def __init__(
        self,
        ctx,
        db: DistData,
        *,
        partitions_order: List[str] = None,
        col_selects: List[str] = None,
        batch_size: int = 50000,
    ) -> None:
        assert len(col_selects) > 0, "empty dataset is not allowed"
        assert (
            db.type.lower() == DistDataType.INDIVIDUAL_TABLE
            or db.type.lower() == DistDataType.VERTICAL_TABLE
        ), f"path format {db.type.lower()} should be sf.table.individual or sf.table.vertical_table"

        v_headers = extract_table_header(
            db,
            partitions_order=partitions_order,
            load_features=True,
            load_labels=True,
            load_ids=True,
            col_selects=col_selects,
        )

        parties_path_format = extract_distdata_info(db)

        pyus = {p: PYU(p) for p in v_headers}
        self.filepaths = {
            pyus[p]: os.path.join(ctx.local_fs_wd, parties_path_format[p].uri)
            for p in v_headers
        }
        self.dtypes = {pyus[p]: v_headers[p] for p in v_headers}
        self.batch_size = batch_size
        self.total_read_cnt = 0
        self.col_selects = col_selects

    def __iter__(self):
        return self

    def __next__(self) -> VDataFrame:
        df = self.next(self.batch_size)

        if df.shape[0] == 0:
            assert self.total_read_cnt, "empty dataset is not allowed"
            # end
            raise StopIteration

        return df

    def next(self, batch_size) -> VDataFrame:
        assert batch_size > 0
        df = read_csv(
            self.filepaths,
            dtypes=self.dtypes,
            nrows=batch_size,
            skip_rows_after_header=self.total_read_cnt,
        )

        if df.shape[0]:
            self.total_read_cnt += df.shape[0]

        return df


def save_prediction_dd(
    ctx,
    uri: str,
    pyu: PYU,
    pyu_preds: Union[List[FedNdarray], FedNdarray],
    pred_name: str,
    feature_dataset,
    saved_features: List[str],
    saved_labels: List[str],
    save_ids: bool,
) -> DistData:
    # TODO: read all cols in one reader.
    addition_reader: List[SimpleVerticalBatchReader] = []
    addition_headers = {}
    saved_ids = []

    if isinstance(pyu_preds, FedNdarray):
        pyu_preds = [pyu_preds]

    def _named_features(features_name: List[str]):
        for f in features_name:
            assert (
                f not in addition_headers
            ), f"do not select {f} as saved feature, repeated with id or label"

        header = extract_table_header(
            feature_dataset,
            load_ids=True,
            load_features=True,
            load_labels=True,
            col_selects=features_name,
        )
        assert (
            len(header) == 1 and pyu.party in header
        ), f"The saved feature {features_name} can only belong to receiver party {pyu.party}, got {header.keys()}"

        addition_headers.update(header[pyu.party])
        addition_reader.append(
            SimpleVerticalBatchReader(
                ctx,
                feature_dataset,
                col_selects=list(header[pyu.party].keys()),
            )
        )

    if save_ids:
        id_header = extract_table_header(feature_dataset, load_ids=True)
        assert (
            pyu.party in id_header
        ), f"can not find id col for receiver party {pyu.party}, {id_header}"
        saved_ids = list(id_header[pyu.party].keys())
        _named_features(saved_ids)

    if saved_labels:
        _named_features(saved_labels)
    else:
        saved_labels = []

    if saved_features:
        _named_features(saved_features)
    else:
        saved_features = []

    append = False
    line_count = 0
    for pyu_pred in pyu_preds:
        assert len(pyu_pred.partitions) == 1
        assert pyu in pyu_pred.partitions

        pred_rows = pyu_pred.shape[0]
        assert pred_rows > 0
        line_count += pred_rows

        addition_df = []
        for r in addition_reader:
            pyu_df = r.next(pred_rows)
            assert len(pyu_df.partitions) == 1
            assert pyu in pyu_df.partitions
            assert pyu_df.shape[0] == pred_rows
            addition_df.append(pyu_df.partitions[pyu].values)

        wait(
            pyu(save_prediction_csv)(
                pyu_pred.partitions[pyu],
                pred_name,
                os.path.join(ctx.local_fs_wd, uri),
                addition_df,
                list(addition_headers.keys()),
                append,
            )
        )
        append = True

    pred_db = DistData(
        name=pred_name,
        type=str(DistDataType.INDIVIDUAL_TABLE),
        data_refs=[DistData.DataRef(uri=uri, party=pyu.party, format="csv")],
    )

    assert line_count, "empty dataset is not allowed"

    meta = gen_prediction_csv_meta(
        addition_headers=addition_headers,
        saved_ids=saved_ids,
        saved_labels=saved_labels,
        saved_features=saved_features,
        pred_name=pred_name,
        line_count=line_count,
    )

    pred_db.meta.Pack(meta)

    return pred_db


def any_pyu_from_spu_config(config: dict):
    return PYU(config["nodes"][0]["party"])


def generate_random_string(pyu: PYU):
    return reveal(pyu(lambda: str(uuid.uuid4()))())

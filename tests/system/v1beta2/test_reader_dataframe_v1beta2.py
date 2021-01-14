# -*- coding: utf-8 -*-
#
# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""System tests for reading rows with pandas connector."""

import numpy
import pyarrow.types
import pytest

from google.cloud.bigquery_storage_v1beta2 import types


def test_read_v1beta2(client, project_id):
    read_session = types.ReadSession()
    read_session.table = "projects/{}/datasets/{}/tables/{}".format(
        "bigquery-public-data", "new_york_citibike", "citibike_stations"
    )

    read_session.read_options.selected_fields.append("station_id")
    read_session.read_options.selected_fields.append("latitude")
    read_session.read_options.selected_fields.append("longitude")
    read_session.read_options.selected_fields.append("name")
    read_session.data_format = types.DataFormat.ARROW

    session = client.create_read_session(
        request={
            "parent": "projects/{}".format(project_id),
            "read_session": read_session,
            "max_stream_count": 1,
        }
    )

    assert len(session.streams) == 1

    streamname = session.streams[0].name

    tbl = client.read_rows(streamname, offset=0).to_arrow(session)

    assert tbl.num_columns == 4
    schema = tbl.schema
    # Use field with a name specifier as there may be ordering differences
    # when selected_fields is used
    assert pyarrow.types.is_int64(schema.field("station_id").type)
    assert pyarrow.types.is_float64(schema.field("latitude").type)
    assert pyarrow.types.is_float64(schema.field("longitude").type)
    assert pyarrow.types.is_string(schema.field("name").type)


@pytest.mark.parametrize(
    "data_format,expected_schema_type",
    ((types.DataFormat.AVRO, "avro_schema"), (types.DataFormat.ARROW, "arrow_schema")),
)
def test_read_rows_to_dataframe(client, project_id, data_format, expected_schema_type):
    read_session = types.ReadSession()
    read_session.table = "projects/{}/datasets/{}/tables/{}".format(
        "bigquery-public-data", "new_york_citibike", "citibike_stations"
    )
    read_session.data_format = data_format

    session = client.create_read_session(
        request={
            "parent": "projects/{}".format(project_id),
            "read_session": read_session,
            "max_stream_count": 1,
        }
    )
    schema_type = session._pb.WhichOneof("schema")
    assert schema_type == expected_schema_type

    stream = session.streams[0].name

    frame = client.read_rows(stream).to_dataframe(
        session, dtypes={"latitude": numpy.float16}
    )

    # Station ID is a required field (no nulls), so the datatype should always
    # be integer.
    assert frame.station_id.dtype.name == "int64"
    assert frame.latitude.dtype.name == "float16"
    assert frame.longitude.dtype.name == "float64"
    assert frame["name"].str.startswith("Central Park").any()

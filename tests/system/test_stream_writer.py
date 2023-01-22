# -*- coding: utf-8 -*-
#
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pathlib
import pytest
import time
import uuid

from google.api_core import exceptions
from google.cloud import bigquery as bq
from google.cloud import bigquery_storage as bq_store
from google.cloud.bigquery_storage import constants
from google.cloud.bigquery_storage_v1 import types

from tests.system.stream_writer_test_files.writestream_sys_test_data_pb2 import WriteStreamSystemTestData
from tests.system.stream_writer_test_files.writestream_sys_test_error_data_pb2 import (
    WriteStreamSystemTestSchemaErrorData,
)
from tests.system.stream_writer_test_files.writestream_sys_test_expanded_schema_pb2 import (
    WriteStreamSystemTestExpandedSchema,
)

TEST_PROJECT = "ucaip-sample-tests"
TEST_DATASET = "bq_storage_write_test"
BQ_CLIENT = bq.Client()
DIR = pathlib.Path(__file__).parent

# create a new table for every test, since the write stream might not realize that the table has been updated.
@pytest.fixture(autouse=True)
def temp_table():
    schema = BQ_CLIENT.schema_from_json(str(DIR / "stream_writer_test_files/write_stream_sys_test_schema.json"))
    table_id = uuid.uuid4()
    full_table_id = f"{TEST_PROJECT}.{TEST_DATASET}.{table_id}"
    table = bq.Table(full_table_id, schema=schema)
    table = BQ_CLIENT.create_table(table, exists_ok=True)
    yield table_id
    BQ_CLIENT.delete_table(table, not_found_ok=True)


class TestWriteSession:
    def test_create_write_session_without_args(self):
        write_session = bq_store.WriteSession()
        assert write_session.min_connections == 1
        assert write_session.max_connections == 20
        assert not write_session.enable_connection_pool

    def test_create_write_session_with_args(self):
        write_session = bq_store.WriteSession(min_connections=2, max_connections=18)
        assert write_session.min_connections == 2
        assert write_session.max_connections == 18


class TestWriteStream:
    def test_init_default_write_stream(self, temp_table):
        default_stream = bq_store.WriteStream(table=temp_table, dataset=TEST_DATASET)
        assert default_stream.client
        assert not default_stream.enable_connection_pool
        assert default_stream.min_connections == 1
        assert default_stream.max_connections == 20
        assert default_stream.stream
        assert default_stream.request_template
        assert default_stream.event_loop

    def test_empty_schema_error(self, temp_table):
        default_stream = bq_store.WriteStream(table=temp_table, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestData()
        row_data.string_col = "test"
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        with pytest.raises(
            RuntimeError,
            match="Schema needs to be passed in for the first write request on this stream.",
        ):
            default_stream.append_rows(rows=proto_rows)

    def test_append_rows_default(self, temp_table):
        default_stream = bq_store.WriteStream(table=temp_table, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.string_col = "test"
        row_data.int_col = 0
        row_data.float_col = 0.1
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert str(resp.error) == ""

        row_data.string_col = "test2"
        row_data.int_col = 1
        row_data.float_col = 0.2
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows)
        assert str(resp.error) == ""

    def test_append_rows_pending(self, temp_table):
        pending_stream = bq_store.WriteStream(
            table=temp_table, dataset=TEST_DATASET, stream_type=constants.PENDING
        )

        row_data = WriteStreamSystemTestData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.string_col = "test"
        row_data.int_col = 0
        row_data.float_col = 0.1
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = pending_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert str(resp.error) == ""

        row_data.string_col = "test2"
        row_data.int_col = 1
        row_data.float_col = 0.2
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = pending_stream.append_rows(rows=proto_rows)
        assert str(resp.error) == ""

        pending_stream.finalize()
        pending_stream.commit()

    # Test user errors
    def test_append_rows_invalid_row_data(self, temp_table):
        default_stream = bq_store.WriteStream(table=temp_table, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestSchemaErrorData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.wrong_col = "test"
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert resp.code == 400
        assert isinstance(resp, exceptions.InvalidArgument)
        assert "no matching field" in str(resp)

    def test_expand_schema_during_write(self, temp_table):
        table = BQ_CLIENT.get_table(f"{TEST_PROJECT}.{TEST_DATASET}.{temp_table}")
        original_schema = table.schema
        new_schema = original_schema[:]
        new_schema.append(bq.SchemaField("another_float_col", "FLOAT"))

        default_stream = bq_store.WriteStream(table=temp_table, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.string_col = "test"
        row_data.int_col = 0
        row_data.float_col = 0.1
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert str(resp.error) == ""

        table.schema = new_schema
        table = BQ_CLIENT.update_table(table, ["schema"])
        time.sleep(1)

        row_data = WriteStreamSystemTestExpandedSchema()
        proto_schema = bq_store.WriteStream.gen_proto_schema(
            WriteStreamSystemTestExpandedSchema()
        )
        row_data.string_col = "test2"
        row_data.int_col = 1
        row_data.float_col = 0.2
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert resp.code == 400
        assert isinstance(resp, exceptions.InvalidArgument)
        assert "Schema mismatch" in str(resp)

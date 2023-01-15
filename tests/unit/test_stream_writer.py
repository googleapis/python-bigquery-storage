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

import pytest
import time

from google.cloud import bigquery
from google.cloud import bigquery as bq
from google.cloud import bigquery_storage as bq_store
from google.cloud.bigquery_storage import constants
from google.cloud.bigquery_storage_v1 import types

from tests.unit.writestream_sys_test_data_pb2 import WriteStreamSystemTestData
from tests.unit.writestream_sys_test_error_data_pb2 import (
    WriteStreamSystemTestSchemaErrorData,
)
from tests.unit.writestream_sys_test_expanded_schema_pb2 import (
    WriteStreamSystemTestExpandedSchema,
)

TEST_PROJECT = "ucaip-sample-tests"
TEST_DATASET = "bq_storage_write_test"
TEST_TABLE = "system_test"
BQ_CLIENT = bq.Client()


@pytest.fixture(autouse=True)
def delay_between_tests():
    yield
    time.sleep(1)


def reset_test_table(old_schema, new_schema):
    table = bigquery.Table(
        f"{TEST_PROJECT}.{TEST_DATASET}.{TEST_TABLE}", schema=new_schema
    )
    BQ_CLIENT.delete_table(table)
    time.sleep(1)
    new_table = bigquery.Table(
        f"{TEST_PROJECT}.{TEST_DATASET}.{TEST_TABLE}", schema=old_schema
    )
    BQ_CLIENT.create_table(new_table)
    time.sleep(1)
    table = BQ_CLIENT.get_table(f"{TEST_PROJECT}.{TEST_DATASET}.{TEST_TABLE}")
    assert table.schema == old_schema


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
    def test_init_default_write_stream(self):
        default_stream = bq_store.WriteStream(table=TEST_TABLE, dataset=TEST_DATASET)
        assert default_stream.client
        assert not default_stream.enable_connection_pool
        assert default_stream.min_connections == 1
        assert default_stream.max_connections == 20
        assert default_stream.stream
        assert default_stream.request_template
        assert default_stream.event_loop

    def test_empty_schema_error(self):
        default_stream = bq_store.WriteStream(table=TEST_TABLE, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestData()
        row_data.string_col = "test"
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        with pytest.raises(
            RuntimeError,
            match="Schema needs to be passed in for the first write request on this stream.",
        ):
            default_stream.append_rows(rows=proto_rows)

    def test_append_rows_default(self):
        default_stream = bq_store.WriteStream(table=TEST_TABLE, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.string_col = "test"
        row_data.int_col = 0
        row_data.float_col = 0.1
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert resp.code == 200
        row_data.string_col = "test2"
        row_data.int_col = 1
        row_data.float_col = 0.2
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows)
        assert resp.code == 200

    def test_append_rows_pending(self):
        pending_stream = bq_store.WriteStream(
            table=TEST_TABLE, dataset=TEST_DATASET, stream_type=constants.PENDING
        )

        row_data = WriteStreamSystemTestData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.string_col = "test"
        row_data.int_col = 0
        row_data.float_col = 0.1
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = pending_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert resp.code == 200

        row_data.string_col = "test2"
        row_data.int_col = 1
        row_data.float_col = 0.2
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = pending_stream.append_rows(rows=proto_rows)
        assert resp.code == 200

        pending_stream.finalize()
        pending_stream.commit()

    # Test user errors
    def test_append_rows_invalid_row_data(self):
        default_stream = bq_store.WriteStream(table=TEST_TABLE, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestSchemaErrorData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.wrong_col = "test"
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        (req, resp) = default_stream.append_rows(rows=proto_rows, schema=proto_schema)
        assert resp.code >= 400 and resp.code < 500

    def test_expand_schema_during_write(self):
        table = BQ_CLIENT.get_table(f"{TEST_PROJECT}.{TEST_DATASET}.{TEST_TABLE}")
        original_schema = table.schema
        new_schema = original_schema[:]
        new_schema.append(bigquery.SchemaField("another_float_col", "FLOAT"))

        try:
            default_stream = bq_store.WriteStream(
                table=TEST_TABLE, dataset=TEST_DATASET
            )

            row_data = WriteStreamSystemTestData()
            proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
            row_data.string_col = "test"
            row_data.int_col = 0
            row_data.float_col = 0.1
            proto_rows = types.ProtoRows()
            proto_rows.serialized_rows.append(row_data.SerializeToString())
            (req, resp) = default_stream.append_rows(
                rows=proto_rows, schema=proto_schema
            )
            assert resp.code == 200

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
            (req, resp) = default_stream.append_rows(
                rows=proto_rows, schema=proto_schema
            )
            assert resp.code >= 400 and resp.code < 500
            # assert(isinstance(resp, exceptions.InvalidArgument))
            # assert("Schema mismatch" in str(resp))

        finally:
            # reset table schema
            reset_test_table(original_schema, new_schema)

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

from datetime import datetime
from google.cloud import bigquery_storage as bq_store
from google.cloud.bigquery_storage import constants
from google.cloud.bigquery_storage_v1 import types

from google.cloud.bigquery_storage_v1 import writer


from google.protobuf import descriptor_pb2
from tests.unit.writestream_sys_test_data_pb2 import WriteStreamSystemTestData


TEST_PROJECT = "ucaip-sample-tests"
TEST_DATASET = "bq_storage_write_test"
TEST_TABLE = "system_test"

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

    def test_append_rows_default(self):
        default_stream = bq_store.WriteStream(table=TEST_TABLE, dataset=TEST_DATASET)

        row_data = WriteStreamSystemTestData()
        proto_schema = bq_store.WriteStream.gen_proto_schema(row_data)
        row_data.string_col = "test"
        row_data.int_col = 0
        row_data.float_col = 0.1
        proto_rows = types.ProtoRows()
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        resp = default_stream.append_rows(rows=proto_rows, schema=proto_schema)

        row_data.string_col = "test2"
        row_data.int_col = 1
        row_data.float_col = 0.2
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        resp = default_stream.append_rows(rows=proto_rows)
        print(resp)

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
        resp = pending_stream.append_rows(rows=proto_rows, schema=proto_schema)

        row_data.string_col = "test2"
        row_data.int_col = 1
        row_data.float_col = 0.2
        proto_rows.serialized_rows.append(row_data.SerializeToString())
        resp = pending_stream.append_rows(rows=proto_rows)

        pending_stream.finalize()
        pending_stream.commit()
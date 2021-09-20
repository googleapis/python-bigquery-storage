# Copyright 2021 Google LLC
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

import datetime
import time
import queue

from google.cloud.bigquery_storage_v1beta2 import writer
from google.cloud.bigquery_storage_v1beta2 import types

from append_rows_benchmark import constants
from append_rows_benchmark import data_pb2


EPOCH_VALUE = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)


def main(
    append_rows_stream: writer.AppendRowsStream,
    response_queue: queue.Queue,
    end_time: float,
):
    print("worker started")
    while True:
        now = time.monotonic()
        if now >= end_time:
            print("worker done via time")
            response_queue.put(constants.DONE)
            return

        request = types.AppendRowsRequest()
        proto_data = types.AppendRowsRequest.ProtoData()
        proto_rows = types.ProtoRows()
        dense_row_generator(proto_rows)
        proto_data.rows = proto_rows
        request.proto_rows = proto_data
        try:
            print("worker sending")
            response_future = append_rows_stream.send(request)
            print("worker queueing")
            response_queue.put(response_future)
        except Exception as exc:
            # Done with writes.
            print(f"worker done via {exc}")
            response_queue.put(constants.DONE)
            return


def dense_row_generator(proto_rows):
    """Generates rows up to a predetermined size limit."""
    available = 8 * 1024 * 1024
    rows = []
    while True:
        row_bytes = b"hello world" * 20
        row = data_pb2.StressData()
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        row.bool_value = (now.minute % 2) == 0
        row.bytes_value = b"so there i was"
        row.date_value = int(now.timestamp()) // 86400
        row.datetime_value = "2016-05-19T10:38:47.046465"
        row.geography_value = "POINT(-122.350220 47.649154)"
        row.int64_value = int(now.timestamp() * 1000)
        row.numeric_value = now.strftime("%Y%m%d%H%M%S.%f")
        row.bignumeric_value = now.strftime("%Y%m%d%H%M%S.%f")
        row.float64_value = 1.23456
        row.string_value = now.isoformat()
        delta = now - EPOCH_VALUE
        row.timestamp_value = int(delta.total_seconds()) * 1000000 + int(
            delta.microseconds
        )
        row.single_struct.values.append(1)
        row.single_struct.values.append(2)
        row.single_struct.values.append(3)
        row.single_struct.values.append(4)
        row.single_struct.values.append(5)
        row.pairs.append(data_pb2.StressData.KeyValuePair(key="blah", value="foo",))
        row.pairs.append(data_pb2.StressData.KeyValuePair(key="blah2", value="foo",))
        row_bytes = row.SerializeToString()

        if available - len(row_bytes) < 0:
            break
        available = available - len(row_bytes)
        rows.append(row_bytes)

    proto_rows.serialized_rows = rows

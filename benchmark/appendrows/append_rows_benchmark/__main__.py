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

import argparse
import collections
import pathlib
import time

from google.cloud import bigquery
from google.cloud import bigquery_storage_v1beta2
from google.cloud.bigquery_storage_v1beta2 import types
from google.cloud.bigquery_storage_v1beta2 import writer
from google.protobuf import descriptor_pb2

from append_rows_benchmark import data_pb2


CURRENT_DIR = pathlib.Path(__file__).parent


def create_table(project_id, dataset_id, table_id):
    bqclient = bigquery.Client()
    schema = bqclient.schema_from_json(CURRENT_DIR / "data_bq.json")
    table = bigquery.Table(f"{project_id}.{dataset_id}.{table_id}", schema=schema)
    bqclient.create_table(table, exists_ok=True)


StreamData = collections.namedtuple(
    "StreamData", ["append_rows_stream", "stream_name", "write_client", "parent"]
)


def start_stream(project_id, dataset_id, table_id):
    write_client = bigquery_storage_v1beta2.BigQueryWriteClient()
    parent = write_client.table_path(project_id, dataset_id, table_id)
    write_stream = types.WriteStream()

    # TODO: allow for default stream, buffered, and pending types.
    write_stream.type_ = types.WriteStream.Type.COMMITTED
    write_stream = write_client.create_write_stream(
        parent=parent, write_stream=write_stream
    )
    stream_name = write_stream.name

    # Create a template with fields needed for the first request.
    request_template = types.AppendRowsRequest()

    # The initial request must contain the stream name.
    request_template.write_stream = stream_name

    # So that BigQuery knows how to parse the serialized_rows, generate a
    # protocol buffer representation of your message descriptor.
    proto_schema = types.ProtoSchema()
    proto_descriptor = descriptor_pb2.DescriptorProto()
    data_pb2.StressData.DESCRIPTOR.CopyToProto(proto_descriptor)
    proto_schema.proto_descriptor = proto_descriptor
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_data.writer_schema = proto_schema
    request_template.proto_rows = proto_data

    # Some stream types support an unbounded number of requests. Construct an
    # AppendRowsStream to send an arbitrary number of requests to a stream.
    append_rows_stream = writer.AppendRowsStream(write_client, request_template)
    return StreamData(append_rows_stream, stream_name, write_client, parent)


def wait_then_close(time_to_wait, stream: StreamData):
    start_time = time.monotonic()
    end_time = start_time + time_to_wait
    now = time.monotonic()
    while now < end_time:
        time.sleep(end_time - now)
        now = time.monotonic()

    stream.append_rows_stream.close()

    # A PENDING type stream must be "finalized" before being committed.
    # write_client.finalize_write_stream(name=write_stream.name)

    # Commit the stream you created earlier.
    batch_commit_write_streams_request = types.BatchCommitWriteStreamsRequest()
    batch_commit_write_streams_request.parent = stream.parent
    batch_commit_write_streams_request.write_streams = [stream.stream_name]
    stream.write_client.batch_commit_write_streams(batch_commit_write_streams_request)


def main(project_id, dataset_id, table_id, num_workers=8):
    create_table(project_id, dataset_id, table_id)
    # with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers + 1):
    stream = start_stream(project_id, dataset_id, table_id)
    wait_then_close(60, stream)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("full_table_id")
    parser.add_argument("--num-workers", type=int, default=8)
    args = parser.parse_args()
    main(*args.full_table_id.split("."), num_workers=args.num_workers)

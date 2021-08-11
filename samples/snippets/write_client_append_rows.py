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

from google.cloud import bigquery
from google.cloud.bigquery_storage_v1beta2.services import big_query_write
from google.cloud.bigquery_storage_v1beta2 import types
from google.protobuf import descriptor_pb2

import sample_data_pb2


bqclient = bigquery.Client()

schema = bqclient.schema_from_json("sample_data_schema.json")
table = bigquery.Table("swast-scratch.my_dataset.bqstorage_write_sample", schema=schema)
table = bqclient.create_table(table, exists_ok=True)


write_client = big_query_write.BigQueryWriteClient()
parent = write_client.table_path(
    "swast-scratch", "my_dataset", "bqstorage_write_sample"
)
write_stream = types.WriteStream()
write_stream.type_ = types.WriteStream.Type.PENDING
write_stream = write_client.create_write_stream(
    parent=parent, write_stream=write_stream
)


def write_generator():
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_rows = types.ProtoRows()
    proto_schema = types.ProtoSchema()
    proto_descriptor = descriptor_pb2.DescriptorProto()
    sample_data_pb2.SampleData.DESCRIPTOR.CopyToProto(proto_descriptor)
    proto_schema.proto_descriptor = proto_descriptor
    proto_data.writer_schema = proto_schema

    row = sample_data_pb2.SampleData()
    row.bool_col = True
    row.bytes_col = b"Hello, World!"
    row.float64_col = float("nan")
    row.int64_col = 123
    row.string_col = "Howdy!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.bool_col = False
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.bytes_col = b"See you later!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.float64_col = 1000000.01
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.int64_col = 67000
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.string_col = "Auf Wiedersehen!"
    proto_rows.serialized_rows.append(row.SerializeToString())

    proto_data.rows = proto_rows
    request = types.AppendRowsRequest()
    request.write_stream = write_stream.name
    request.proto_rows = proto_data

    yield request


requests = list(write_generator())

responses = write_client.append_rows(iter(requests))
for response in responses:
    print(response)
    break

write_client.finalize_write_stream(name=write_stream.name)

batch_commit_write_streams_request = types.BatchCommitWriteStreamsRequest()
batch_commit_write_streams_request.parent = parent
batch_commit_write_streams_request.write_streams = [write_stream.name]
write_client.batch_commit_write_streams(batch_commit_write_streams_request)

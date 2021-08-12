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
import decimal

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

    # Demonstrate data types where there isn't a protobuf scalar type.
    # https://cloud.google.com/bigquery/docs/write-api#data_type_conversions
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    date_value = datetime.date(2021, 8, 12)
    epoch_value = datetime.date(1970, 1, 1)
    delta = date_value - epoch_value
    row.date_col = delta.days
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    datetime_value = datetime.datetime(2021, 8, 12, 9, 46, 23, 987456)
    row.datetime_col = datetime_value.strftime("%Y-%m-%d %H:%M:%S.%f")
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.geography_col = "POINT(-122.347222 47.651111)"
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    numeric_value = decimal.Decimal("1.23456789101112e+6")
    row.numeric_col = str(numeric_value)
    bignumeric_value = decimal.Decimal("-1.234567891011121314151617181920e+16")
    row.bignumeric_col = str(bignumeric_value)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    time_value = datetime.time(11, 7, 48, 123456)
    row.time_col = time_value.strftime("%H:%H:%S.%f")
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    timestamp_value = datetime.datetime(
        2021, 8, 12, 16, 11, 22, 987654, tzinfo=datetime.timezone.utc
    )
    epoch_value = datetime.datetime(1970, 1, 1, tzinfo=datetime.timezone.utc)
    delta = timestamp_value - epoch_value
    row.timestamp_col = int(delta.total_seconds()) * 1000000 + int(delta.microseconds)
    proto_rows.serialized_rows.append(row.SerializeToString())

    # DESCRIPTOR is only needed in the first request.
    proto_data.rows = proto_rows
    request = types.AppendRowsRequest()
    request.offset = 6
    request.write_stream = write_stream.name
    request.proto_rows = proto_data

    yield request

    # Demonstrate STRUCT and ARRAY columns.
    proto_data = types.AppendRowsRequest.ProtoData()
    proto_rows = types.ProtoRows()

    row = sample_data_pb2.SampleData()
    row.int64_list.append(1)
    row.int64_list.append(2)
    row.int64_list.append(3)
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    row.struct_col.sub_int_col = 7
    proto_rows.serialized_rows.append(row.SerializeToString())

    row = sample_data_pb2.SampleData()
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -1
    row.struct_list.append(sub_message)
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -2
    row.struct_list.append(sub_message)
    sub_message = sample_data_pb2.SampleData.SampleStruct()
    sub_message.sub_int_col = -3
    row.struct_list.append(sub_message)
    proto_rows.serialized_rows.append(row.SerializeToString())

    proto_data.rows = proto_rows
    request = types.AppendRowsRequest()
    request.offset = 12
    request.write_stream = write_stream.name
    request.proto_rows = proto_data

    yield request


requests = list(write_generator())

responses = write_client.append_rows(iter(requests))
counter = 0
for response in responses:
    counter += 1
    print(response)

    if counter >= 3:
        break

write_client.finalize_write_stream(name=write_stream.name)

batch_commit_write_streams_request = types.BatchCommitWriteStreamsRequest()
batch_commit_write_streams_request.parent = parent
batch_commit_write_streams_request.write_streams = [write_stream.name]
write_client.batch_commit_write_streams(batch_commit_write_streams_request)

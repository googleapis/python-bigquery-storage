# Note that this file is not properly set up for pytest

from google.cloud import bigquery_storage_v1
from google.cloud.bigquery_storage_v1 import writer
from google.cloud.bigquery_storage_v1.types import storage
import sample_schema_pb2
import expanded_sample_schema_pb2
from google.protobuf import descriptor_pb2
from google.api_core import bidi
import queue as queue_module
import time
from functools import wraps
from typing import Optional
import uuid
from google.cloud import bigquery as bq
import logging

logging.basicConfig(level=logging.DEBUG)


BQ_CLIENT = bq.Client()

client = bigquery_storage_v1.BigQueryWriteClient()

# replace this with your custom table
parent = "projects/ucaip-sample-tests/datasets/bq_storage_write_test/tables/another_test"

col_val = 1

proto_schema = bigquery_storage_v1.types.ProtoSchema()
proto_descriptor = descriptor_pb2.DescriptorProto()
sample_schema_pb2.SampleSchema.DESCRIPTOR.CopyToProto(proto_descriptor)
proto_schema.proto_descriptor = proto_descriptor
proto_data = bigquery_storage_v1.types.storage.AppendRowsRequest.ProtoData()
proto_data.writer_schema = proto_schema

proto_rows = bigquery_storage_v1.types.ProtoRows()

# replace this with your custom schema
row = sample_schema_pb2.SampleSchema()
row.col1 = col_val
row.col2 = "hello"
proto_rows.serialized_rows.append(row.SerializeToString())


first_request = bigquery_storage_v1.types.storage.AppendRowsRequest(
	write_stream = f"{parent}/streams/_default",
	proto_rows = bigquery_storage_v1.types.storage.AppendRowsRequest.ProtoData(
		writer_schema = proto_schema,
		rows = proto_rows
	)
)

def create_request(col_val):
	row = sample_schema_pb2.SampleSchema()
	row.col1 = col_val
	row.col2 = "hello"
	proto_rows = bigquery_storage_v1.types.ProtoRows()
	proto_rows.serialized_rows.append(row.SerializeToString())

	next_request = bigquery_storage_v1.types.storage.AppendRowsRequest(
		write_stream = f"{parent}/streams/_default",
		proto_rows = bigquery_storage_v1.types.storage.AppendRowsRequest.ProtoData(
			rows = proto_rows
		)
	)
	return next_request

def update_schema():
	table = BQ_CLIENT.get_table("ucaip-sample-tests.bq_storage_write_test.another_test")
	original_schema = table.schema
	new_schema = original_schema[:]
	new_schema.append(bq.SchemaField("another_float_col", "FLOAT"))
	table.schema = new_schema
	table = BQ_CLIENT.update_table(table, ["schema"])
	# time.sleep(1)

def create_request_with_schema_update():
	proto_schema = bigquery_storage_v1.types.ProtoSchema()
	proto_descriptor = descriptor_pb2.DescriptorProto()
	expanded_sample_schema_pb2.ExpandedSampleSchema.DESCRIPTOR.CopyToProto(proto_descriptor)
	proto_schema.proto_descriptor = proto_descriptor
	proto_data = bigquery_storage_v1.types.storage.AppendRowsRequest.ProtoData()
	proto_data.writer_schema = proto_schema

	row = expanded_sample_schema_pb2.ExpandedSampleSchema()
	proto_schema = writer.gen_proto_schema(row)
	row.col1 = 1
	row.col2 = "hello"
	row.another_float_col = 0.1
	proto_rows = bigquery_storage_v1.types.ProtoRows()
	proto_rows.serialized_rows.append(row.SerializeToString())

	next_request = bigquery_storage_v1.types.storage.AppendRowsRequest(
		write_stream = f"{parent}/streams/_default",
		proto_rows = bigquery_storage_v1.types.storage.AppendRowsRequest.ProtoData(
			rows = proto_rows,
			writer_schema = proto_schema
		)
	)
	return next_request

append_rows_stream = writer.AppendRowsStream(client, first_request, max_reconnect_attempts = 10)
time.sleep(1)

for i in range(2,6):
	append_rows_stream.send(create_request(i))
	time.sleep(1)

update_schema()
append_rows_stream.send(create_request_with_schema_update(), max_retry = 5)
time.sleep(1)

time.sleep(605)
try:
	# test automatic reconnect
	append_rows_stream.send(create_request(2), max_retry = 5)
except Exception as e:
	# on exception, try to explicitly create a new stream
	append_rows_stream = writer.AppendRowsStream(client, first_request, max_reconnect_attempts = 10)
	append_rows_stream.send(create_request(2), max_retry = 5)


# test session-managed send_with_reconnect calls
try:
	print("using helper function and retrying with original request template")
	writer.send_with_reconnect(stream = append_rows_stream, request = first_request, max_retry = 3, max_reconnect_attempts = 10)
except Exception as e:
	print(e)

try:
	print("using helper function and retrying with a non-templated request")
	writer.send_with_reconnect(stream = append_rows_stream, request = create_request(2), max_retry = 3, max_reconnect_attempts = 10)
except Exception as e:
	print(e)

# check if we have any uncleared cache
print(append_rows_stream._requests)
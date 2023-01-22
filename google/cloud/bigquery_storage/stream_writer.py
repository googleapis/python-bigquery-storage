# Copyright 2022 Google LLC
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

import asyncio
import copy
import os
import sys

from google.api_core.retry import Retry
from google.protobuf import descriptor_pb2  # noqa: F401

from google.cloud.bigquery_storage_v1 import types
from google.cloud.bigquery_storage import base
from google.cloud.bigquery_storage import constants
from typing import Optional, Dict, Any

BUILD_SPECIFIC_GCLOUD_PROJECT = "BUILD_SPECIFIC_GCLOUD_PROJECT"


class WriteSession:
    """A manager object that keeps track of write streams and their metadata."""

    streams: Dict[str, types.ProtoSchema] = {}
    connections: Dict[str, "WriteStream"] = {}
    project = (
        None
        if not os.getenv(BUILD_SPECIFIC_GCLOUD_PROJECT)
        else os.getenv(BUILD_SPECIFIC_GCLOUD_PROJECT)
    )
    enable_connection_pool = False
    min_connections = 1
    max_connections = 20

    def __init__(
        self,
        enable_connection_pool: bool = False,
        min_connections: Optional[int] = 1,
        max_connections: Optional[int] = 20,
    ):
        """Constructs the WriteSession object.

        Args:
            enable_connection_pool (bool):
                Optional. Defaults to False. This needs to be set to True
                in order to set the min_connections and max_connections parameters.
            min_connections (int):
                Optional. Defaults to 1. Sets the minimum number of connections in the connection pool.
            max_connections (int):
                Optional. Defaults to 20. Sets the maximum number of connections in the connection pool.
        """
        self.client = base.global_base.client
        self.enable_connection_pool = enable_connection_pool
        self.min_connections = min_connections
        self.max_connections = max_connections

    def add_stream(
        self,
        table: str,
        dataset: str,
        stream_type: Optional[types.WriteStream.Type] = None,
    ):
        """Creates and adds a write stream and its metadata to the write session.

        Args:
            table (str):
                Required. The name of the table that is written to.
            dataset (str):
                Required. The name of the dataset that contains the table.
            stream_type (types.WriteStream.Type):
                Optional. If not set, the default stream will be used.

        Returns:
            stream (WriteStream): The newly created WriteStream object.
        """
        stream = WriteStream(table=table, dataset=dataset, stream_type=stream_type)

        return stream


class WriteStream(WriteSession, Retry):
    def __init__(
        self,
        table: str,
        dataset: str,
        stream_type: Optional[types.WriteStream.Type] = None,
        enable_connection_pool: bool = False,
        min_connections: Optional[int] = 1,
        max_connections: Optional[int] = 20,
        project: Optional[str] = None,
    ):
        """Constructs the WriteStream object.

        Args:
            table (str):
                Required. The name of the table that is written to.
            dataset (str):
                Required. The name of the dataset that contains the table.
            stream_type (types.WriteStream.Type):
                Optional. If not set, the default stream will be used.
            enable_connection_pool (bool):
                Optional. Defaults to False. This needs to be set to True
                in order to set the min_connections and max_connections parameters.
                This will override the global setting for the write session.
            min_connections (int):
                Optional. Defaults to 1. Sets the minimum number of connections in the connection pool.
                This will override the global setting for the write session.
            max_connections (int):
                Optional. Defaults to 20. Sets the maximum number of connections in the connection pool.
                This will override the global setting for the write session.
            project (str):
                Optional. The name of the gcloud project that contains the BQ dataset.
                This needs to be set at least once during the entire write session.

        Raises:
            RuntimeError: if the project name has never been set.
        """
        super().__init__(
            enable_connection_pool=enable_connection_pool,
            min_connections=min_connections,
            max_connections=max_connections,
        )
        if self.project is None and project is None:
            raise RuntimeError(
                "The project name has not been set yet. Please set the project in the WriteStream initializer or in the `BUILD_SPECIFIC_GCLOUD_PROJECT` environment variable."
            )
        if project is not None:
            self.project = project
        self.parent = self.client.table_path(
            project=self.project, dataset=dataset, table=table
        )
        if stream_type:
            stream_stub = types.WriteStream(type_=stream_type)
            self.stream = self.client.create_write_stream(
                parent=self.parent, write_stream=stream_stub
            )
        else:
            self.stream = self.client.get_write_stream(
                request=types.GetWriteStreamRequest(
                    name=f"{self.parent}/streams/_default"
                )
            )
        self.request_template = types.AppendRowsRequest(write_stream=self.stream.name)
        self.table = table
        self.dataset = dataset
        # lazy-load the event loop
        self._event_loop = None

    @staticmethod
    def gen_proto_schema(proto_message_class: Any):
        """Helper function that generates a proto schema from the proto message.

        Args:
            proto_message_class (Any):
                Required. The argument needs to be an instance of an auto-generated Python protocol buffer.
                For more details please see https://protobuf.dev/reference/python/python-generated/

        Returns:
            proto_schema (types.ProtoSchema)

        Raises:
            AttributeError: when the provided argument is not a protocol buffer.
        """
        try:
            proto_schema = types.ProtoSchema()
            proto_descriptor = descriptor_pb2.DescriptorProto()
            proto_message_class.DESCRIPTOR.CopyToProto(proto_descriptor)
            proto_schema.proto_descriptor = proto_descriptor
            return proto_schema
        except AttributeError as e:
            raise e

    @property
    def event_loop(self):
        if self._event_loop is None:
            self._event_loop = asyncio.get_event_loop()
        return self._event_loop

    @property
    def name(self):
        return self.stream.name

    @property
    def type_(self):
        return self.stream.type_

    @property
    def create_time(self):
        return self.stream.create_time

    @property
    def commit_time(self):
        return self.stream.commit_time

    @property
    def table_schema(self):
        return self.stream.table_schema

    @property
    def write_mode(self):
        return self.stream.write_mode

    @property
    def location(self):
        return self.stream.location

    def finalize(self) -> types.storage.FinalizeWriteStreamResponse:
        """Finalizes the current write stream"""
        if (
            self.stream.type_ == constants.PENDING
            or self.stream.type_ == constants.BUFFERED
        ):
            return self.client.finalize_write_stream(name=self.stream.name)

    def commit(self):
        """Commits the write stream."""
        batch_commit_write_streams_request = types.BatchCommitWriteStreamsRequest()
        batch_commit_write_streams_request.parent = self.parent
        batch_commit_write_streams_request.write_streams = [self.stream.name]
        return self.client.batch_commit_write_streams(
            batch_commit_write_streams_request
        )

    def _send_request(
        self, future_response: asyncio.Future, request: types.AppendRowsRequest
    ):
        response = None
        try:
            requests = [self.request_template]
            response = list(self.client.append_rows(requests=iter(requests)))
            # since we're only sending one request, we expect one response back
            assert len(response) == 1
            response = response[0]
            # (TODO) handle schema expansion/updates and retry/reconnect
            # (TODO) handle user idle case
        except Exception as e:
            response = e

        future_response.set_result(response)

    async def _append_rows(self, request: types.AppendRowsRequest):
        future_response = self.event_loop.create_future()
        self._send_request(future_response, request)
        response = await future_response
        return response

    def append_rows(
        self,
        rows: types.ProtoRows,
        offset: Optional[int] = None,
        retry: Optional[int] = 3,
        schema: Optional[types.ProtoSchema] = None,
        trace_id: Optional[str] = None,
        missing_value_interpretations: Optional[Dict] = None,
    ):
        """Sends an append_rows request to the backend. The function will automatically retry if
           backend detects that the schema has been updated.

        Args:
            rows (types.ProtoRows):
                Required. Row data in proto format.
            offset (int):
                Optional. If set, the offset will be used to index the table on reconnection.
            retry (int):
                Optional. Defaults to 3. This parameter sets the max number of retry attempts.
            schema (types.ProtoSchema):
                Optional. This parameter is required for the first append request. Subsequent
                append requests will use the same schema if this is set to None. The schema
                will be updated if a new schema is passed.
            trace_id (str):
                Optional. Id set by client to annotate its identity.
                Only initial request setting is respected.
            missing_value_interpretations (Dict):
                Optional. A map to indicate how to interpret missing value for some
                fields. Missing values are fields present in user schema but
                missing in rows. The key is the field name. The value is the
                interpretation of missing values for the field.

                For example, a map {'foo': NULL_VALUE, 'bar': DEFAULT_VALUE}
                means all missing values in field foo are interpreted as
                NULL, all missing values in field bar are interpreted as the
                default value of field bar in table schema.

                If a field is not in this map and has missing values, the
                missing values in this field are interpreted as NULL.

                This field only applies to the current request, it won't
                affect other requests on the connection.

                Currently, field name can only be top-level column name,
                can't be a struct field path like 'foo.bar'.
        Returns:
            A tuple containing a deep copy of the original request and the response wrapped
            as a Future object.
        Raises:
            RuntimeError when the schema is not passed in on the first request or when the
            append request size exceeds 10 MB.
        """
        proto_data = types.AppendRowsRequest.ProtoData()
        if schema is not None:
            proto_data.writer_schema = schema
            self.streams[self.stream.name] = schema
        else:
            if self.stream.name not in self.streams.keys():
                raise RuntimeError(
                    "Schema needs to be passed in for the first write request on this stream."
                )
            proto_data.writer_schema = self.streams[self.stream.name]

        proto_data.rows = rows
        self.request_template.offset = offset if offset else None
        self.request_template.trace_id = trace_id if trace_id else None
        self.request_template.missing_value_interpretations = (
            missing_value_interpretations if missing_value_interpretations else None
        )
        self.request_template.proto_rows = proto_data

        # raise an exception if the size of the request is greater than 10 MB
        if sys.getsizeof(self.request_template) > constants.APPEND_REQ_SIZE_CAP:
            raise RuntimeError("Individual append request size cannot exceed 10 MB.")
        return (
            copy.deepcopy(self.request_template),
            asyncio.run(self._append_rows(self.request_template)),
        )

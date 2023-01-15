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
import logging

from google.api_core.retry import Retry
from google.protobuf import descriptor_pb2  # noqa: F401

from google.cloud.bigquery_storage_v1 import types
from google.cloud.bigquery_storage import base
from google.cloud.bigquery_storage import constants
from typing import Optional, Dict

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class WriteSession(Retry):
    streams = {}  # {stream_id:append_rows_request_template}
    connections = {}  # {location (str): WriteStream}

    def __init__(
        self,
        enable_connection_pool: bool = False,
        project: Optional[str] = None,
        min_connections: Optional[int] = 1,
        max_connections: Optional[int] = 20,
    ):
        if not project and not base.global_base.project:
            raise RuntimeError(
                "The project name has not been set yet. Please set the project in the WriteSession initializer or in the `BUILD_SPECIFIC_GCLOUD_PROJECT` environment variable."
            )

        if project:
            base.global_base.project = project

        self.client = base.global_base.client
        self.project = base.global_base.project
        self.enable_connection_pool = enable_connection_pool
        self.min_connections = min_connections
        self.max_connections = max_connections

    def add_stream(
        self,
        table_name: str,
        stream_type: Optional[types.WriteStream.Type] = None,
    ):
        stream = WriteStream(types.WriteStream(type_=stream_type))
        self.streams[stream.name] = None
        return stream

    def commit_all(self):

        return


# A WriteStream can inherit from a WriteSession to access common parent fields, it should also contain type-specific logic for different stream types
class WriteStream(WriteSession):
    def __init__(
        self,
        table: str,
        dataset: str,
        stream_type: Optional[types.WriteStream.Type] = None,
        enable_connection_pool: bool = False,
        min_connections: Optional[int] = 1,
        max_connections: Optional[int] = 20,
    ):
        super().__init__(
            enable_connection_pool=enable_connection_pool,
            min_connections=min_connections,
            max_connections=max_connections,
        )
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
                request=types.GetWriteStreamRequest(name=f"{self.parent}/_default")
            )
        self.request_template = types.AppendRowsRequest(write_stream=self.stream.name)
        self.table = table
        self.dataset = dataset
        # lazy-load the event loop
        self._event_loop = None

    @staticmethod
    def gen_proto_schema(proto_message_class):
        try:
            proto_schema = types.ProtoSchema()
            proto_descriptor = descriptor_pb2.DescriptorProto()
            proto_message_class.DESCRIPTOR.CopyToProto(proto_descriptor)
            proto_schema.proto_descriptor = proto_descriptor
            return proto_schema
        except Exception as e:
            raise e

    @property
    def event_loop(self):
        if self._event_loop is None:
            self._event_loop = asyncio.get_event_loop()
        return self._event_loop

    def finalize(self):
        if (
            self.stream.type_ == constants.PENDING
            or self.stream.type_ == constants.BUFFERED
        ):
            self.client.finalize_write_stream(name=self.stream.name)

    def commit(self):
        batch_commit_write_streams_request = types.BatchCommitWriteStreamsRequest()
        batch_commit_write_streams_request.parent = self.parent
        batch_commit_write_streams_request.write_streams = [self.stream.name]
        self.client.batch_commit_write_streams(batch_commit_write_streams_request)

    def _send_request(
        self, future_response: asyncio.Future, request: types.AppendRowsRequest
    ):
        response = None
        try:
            requests = [self.request_template]
            response = self.client.append_rows(requests=iter(requests))
        except Exception as e:
            response = e

        future_response.set_result(response)

    async def _append_rows(self, request: types.AppendRowsRequest):
        future_response = self.event_loop.create_future()
        self._send_request(future_response, request)
        response = await future_response
        return response

    # this is the top-level function we intend for developers to use, and it returns a tuple: (request, future_response); users will be able to associate the response object to its originating request
    def append_rows(
        self,
        rows: types.ProtoRows,
        offset: Optional[int] = None,
        retry: Optional[int] = 3,
        schema: Optional[types.ProtoSchema] = None,
        trace_id: Optional[str] = None,
        missing_value_map: Optional[Dict] = None,
    ):
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
        self.request_template.proto_rows = proto_data

        return (
            copy.deepcopy(self.request_template),
            asyncio.run(self._append_rows(self.request_template)),
        )

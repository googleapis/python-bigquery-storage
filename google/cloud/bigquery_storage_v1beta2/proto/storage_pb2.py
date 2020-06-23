# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/bigquery_storage_v1beta2/proto/storage.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
from google.api import client_pb2 as google_dot_api_dot_client__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.cloud.bigquery_storage_v1beta2.proto import (
    arrow_pb2 as google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_arrow__pb2,
)
from google.cloud.bigquery_storage_v1beta2.proto import (
    avro_pb2 as google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_avro__pb2,
)
from google.cloud.bigquery_storage_v1beta2.proto import (
    stream_pb2 as google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_stream__pb2,
)


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/bigquery_storage_v1beta2/proto/storage.proto",
    package="google.cloud.bigquery.storage.v1beta2",
    syntax="proto3",
    serialized_options=b"\n)com.google.cloud.bigquery.storage.v1beta2B\014StorageProtoP\001ZLgoogle.golang.org/genproto/googleapis/cloud/bigquery/storage/v1beta2;storage",
    serialized_pb=b'\n9google/cloud/bigquery_storage_v1beta2/proto/storage.proto\x12%google.cloud.bigquery.storage.v1beta2\x1a\x1cgoogle/api/annotations.proto\x1a\x17google/api/client.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x37google/cloud/bigquery_storage_v1beta2/proto/arrow.proto\x1a\x36google/cloud/bigquery_storage_v1beta2/proto/avro.proto\x1a\x38google/cloud/bigquery_storage_v1beta2/proto/stream.proto"\xc8\x01\n\x18\x43reateReadSessionRequest\x12\x43\n\x06parent\x18\x01 \x01(\tB3\xe0\x41\x02\xfa\x41-\n+cloudresourcemanager.googleapis.com/Project\x12M\n\x0cread_session\x18\x02 \x01(\x0b\x32\x32.google.cloud.bigquery.storage.v1beta2.ReadSessionB\x03\xe0\x41\x02\x12\x18\n\x10max_stream_count\x18\x03 \x01(\x05"i\n\x0fReadRowsRequest\x12\x46\n\x0bread_stream\x18\x01 \x01(\tB1\xe0\x41\x02\xfa\x41+\n)bigquerystorage.googleapis.com/ReadStream\x12\x0e\n\x06offset\x18\x02 \x01(\x03")\n\rThrottleState\x12\x18\n\x10throttle_percent\x18\x01 \x01(\x05"\x9c\x01\n\x0bStreamStats\x12M\n\x08progress\x18\x02 \x01(\x0b\x32;.google.cloud.bigquery.storage.v1beta2.StreamStats.Progress\x1a>\n\x08Progress\x12\x19\n\x11\x61t_response_start\x18\x01 \x01(\x01\x12\x17\n\x0f\x61t_response_end\x18\x02 \x01(\x01"\xdb\x02\n\x10ReadRowsResponse\x12\x44\n\tavro_rows\x18\x03 \x01(\x0b\x32/.google.cloud.bigquery.storage.v1beta2.AvroRowsH\x00\x12U\n\x12\x61rrow_record_batch\x18\x04 \x01(\x0b\x32\x37.google.cloud.bigquery.storage.v1beta2.ArrowRecordBatchH\x00\x12\x11\n\trow_count\x18\x06 \x01(\x03\x12\x41\n\x05stats\x18\x02 \x01(\x0b\x32\x32.google.cloud.bigquery.storage.v1beta2.StreamStats\x12L\n\x0ethrottle_state\x18\x05 \x01(\x0b\x32\x34.google.cloud.bigquery.storage.v1beta2.ThrottleStateB\x06\n\x04rows"k\n\x16SplitReadStreamRequest\x12?\n\x04name\x18\x01 \x01(\tB1\xe0\x41\x02\xfa\x41+\n)bigquerystorage.googleapis.com/ReadStream\x12\x10\n\x08\x66raction\x18\x02 \x01(\x01"\xb1\x01\n\x17SplitReadStreamResponse\x12I\n\x0eprimary_stream\x18\x01 \x01(\x0b\x32\x31.google.cloud.bigquery.storage.v1beta2.ReadStream\x12K\n\x10remainder_stream\x18\x02 \x01(\x0b\x32\x31.google.cloud.bigquery.storage.v1beta2.ReadStream2\xf3\x06\n\x0c\x42igQueryRead\x12\xf8\x01\n\x11\x43reateReadSession\x12?.google.cloud.bigquery.storage.v1beta2.CreateReadSessionRequest\x1a\x32.google.cloud.bigquery.storage.v1beta2.ReadSession"n\x82\xd3\xe4\x93\x02\x41"</v1beta2/{read_session.table=projects/*/datasets/*/tables/*}:\x01*\xda\x41$parent,read_session,max_stream_count\x12\xde\x01\n\x08ReadRows\x12\x36.google.cloud.bigquery.storage.v1beta2.ReadRowsRequest\x1a\x37.google.cloud.bigquery.storage.v1beta2.ReadRowsResponse"_\x82\xd3\xe4\x93\x02\x44\x12\x42/v1beta2/{read_stream=projects/*/locations/*/sessions/*/streams/*}\xda\x41\x12read_stream,offset0\x01\x12\xd5\x01\n\x0fSplitReadStream\x12=.google.cloud.bigquery.storage.v1beta2.SplitReadStreamRequest\x1a>.google.cloud.bigquery.storage.v1beta2.SplitReadStreamResponse"C\x82\xd3\xe4\x93\x02=\x12;/v1beta2/{name=projects/*/locations/*/sessions/*/streams/*}\x1a\xae\x01\xca\x41\x1e\x62igquerystorage.googleapis.com\xd2\x41\x89\x01https://www.googleapis.com/auth/bigquery,https://www.googleapis.com/auth/bigquery.readonly,https://www.googleapis.com/auth/cloud-platformB\x89\x01\n)com.google.cloud.bigquery.storage.v1beta2B\x0cStorageProtoP\x01ZLgoogle.golang.org/genproto/googleapis/cloud/bigquery/storage/v1beta2;storageb\x06proto3',
    dependencies=[
        google_dot_api_dot_annotations__pb2.DESCRIPTOR,
        google_dot_api_dot_client__pb2.DESCRIPTOR,
        google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,
        google_dot_api_dot_resource__pb2.DESCRIPTOR,
        google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_arrow__pb2.DESCRIPTOR,
        google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_avro__pb2.DESCRIPTOR,
        google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_stream__pb2.DESCRIPTOR,
    ],
)


_CREATEREADSESSIONREQUEST = _descriptor.Descriptor(
    name="CreateReadSessionRequest",
    full_name="google.cloud.bigquery.storage.v1beta2.CreateReadSessionRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="parent",
            full_name="google.cloud.bigquery.storage.v1beta2.CreateReadSessionRequest.parent",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\002\372A-\n+cloudresourcemanager.googleapis.com/Project",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="read_session",
            full_name="google.cloud.bigquery.storage.v1beta2.CreateReadSessionRequest.read_session",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\002",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="max_stream_count",
            full_name="google.cloud.bigquery.storage.v1beta2.CreateReadSessionRequest.max_stream_count",
            index=2,
            number=3,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=387,
    serialized_end=587,
)


_READROWSREQUEST = _descriptor.Descriptor(
    name="ReadRowsRequest",
    full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="read_stream",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsRequest.read_stream",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\002\372A+\n)bigquerystorage.googleapis.com/ReadStream",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="offset",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsRequest.offset",
            index=1,
            number=2,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=589,
    serialized_end=694,
)


_THROTTLESTATE = _descriptor.Descriptor(
    name="ThrottleState",
    full_name="google.cloud.bigquery.storage.v1beta2.ThrottleState",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="throttle_percent",
            full_name="google.cloud.bigquery.storage.v1beta2.ThrottleState.throttle_percent",
            index=0,
            number=1,
            type=5,
            cpp_type=1,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=696,
    serialized_end=737,
)


_STREAMSTATS_PROGRESS = _descriptor.Descriptor(
    name="Progress",
    full_name="google.cloud.bigquery.storage.v1beta2.StreamStats.Progress",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="at_response_start",
            full_name="google.cloud.bigquery.storage.v1beta2.StreamStats.Progress.at_response_start",
            index=0,
            number=1,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="at_response_end",
            full_name="google.cloud.bigquery.storage.v1beta2.StreamStats.Progress.at_response_end",
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=834,
    serialized_end=896,
)

_STREAMSTATS = _descriptor.Descriptor(
    name="StreamStats",
    full_name="google.cloud.bigquery.storage.v1beta2.StreamStats",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="progress",
            full_name="google.cloud.bigquery.storage.v1beta2.StreamStats.progress",
            index=0,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        )
    ],
    extensions=[],
    nested_types=[_STREAMSTATS_PROGRESS],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=740,
    serialized_end=896,
)


_READROWSRESPONSE = _descriptor.Descriptor(
    name="ReadRowsResponse",
    full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="avro_rows",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsResponse.avro_rows",
            index=0,
            number=3,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="arrow_record_batch",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsResponse.arrow_record_batch",
            index=1,
            number=4,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="row_count",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsResponse.row_count",
            index=2,
            number=6,
            type=3,
            cpp_type=2,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="stats",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsResponse.stats",
            index=3,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="throttle_state",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsResponse.throttle_state",
            index=4,
            number=5,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="rows",
            full_name="google.cloud.bigquery.storage.v1beta2.ReadRowsResponse.rows",
            index=0,
            containing_type=None,
            fields=[],
        )
    ],
    serialized_start=899,
    serialized_end=1246,
)


_SPLITREADSTREAMREQUEST = _descriptor.Descriptor(
    name="SplitReadStreamRequest",
    full_name="google.cloud.bigquery.storage.v1beta2.SplitReadStreamRequest",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="google.cloud.bigquery.storage.v1beta2.SplitReadStreamRequest.name",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=1,
            has_default_value=False,
            default_value=b"".decode("utf-8"),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\002\372A+\n)bigquerystorage.googleapis.com/ReadStream",
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="fraction",
            full_name="google.cloud.bigquery.storage.v1beta2.SplitReadStreamRequest.fraction",
            index=1,
            number=2,
            type=1,
            cpp_type=5,
            label=1,
            has_default_value=False,
            default_value=float(0),
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1248,
    serialized_end=1355,
)


_SPLITREADSTREAMRESPONSE = _descriptor.Descriptor(
    name="SplitReadStreamResponse",
    full_name="google.cloud.bigquery.storage.v1beta2.SplitReadStreamResponse",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    fields=[
        _descriptor.FieldDescriptor(
            name="primary_stream",
            full_name="google.cloud.bigquery.storage.v1beta2.SplitReadStreamResponse.primary_stream",
            index=0,
            number=1,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
        _descriptor.FieldDescriptor(
            name="remainder_stream",
            full_name="google.cloud.bigquery.storage.v1beta2.SplitReadStreamResponse.remainder_stream",
            index=1,
            number=2,
            type=11,
            cpp_type=10,
            label=1,
            has_default_value=False,
            default_value=None,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
        ),
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=None,
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1358,
    serialized_end=1535,
)

_CREATEREADSESSIONREQUEST.fields_by_name[
    "read_session"
].message_type = (
    google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_stream__pb2._READSESSION
)
_STREAMSTATS_PROGRESS.containing_type = _STREAMSTATS
_STREAMSTATS.fields_by_name["progress"].message_type = _STREAMSTATS_PROGRESS
_READROWSRESPONSE.fields_by_name[
    "avro_rows"
].message_type = (
    google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_avro__pb2._AVROROWS
)
_READROWSRESPONSE.fields_by_name[
    "arrow_record_batch"
].message_type = (
    google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_arrow__pb2._ARROWRECORDBATCH
)
_READROWSRESPONSE.fields_by_name["stats"].message_type = _STREAMSTATS
_READROWSRESPONSE.fields_by_name["throttle_state"].message_type = _THROTTLESTATE
_READROWSRESPONSE.oneofs_by_name["rows"].fields.append(
    _READROWSRESPONSE.fields_by_name["avro_rows"]
)
_READROWSRESPONSE.fields_by_name[
    "avro_rows"
].containing_oneof = _READROWSRESPONSE.oneofs_by_name["rows"]
_READROWSRESPONSE.oneofs_by_name["rows"].fields.append(
    _READROWSRESPONSE.fields_by_name["arrow_record_batch"]
)
_READROWSRESPONSE.fields_by_name[
    "arrow_record_batch"
].containing_oneof = _READROWSRESPONSE.oneofs_by_name["rows"]
_SPLITREADSTREAMRESPONSE.fields_by_name[
    "primary_stream"
].message_type = (
    google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_stream__pb2._READSTREAM
)
_SPLITREADSTREAMRESPONSE.fields_by_name[
    "remainder_stream"
].message_type = (
    google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_stream__pb2._READSTREAM
)
DESCRIPTOR.message_types_by_name["CreateReadSessionRequest"] = _CREATEREADSESSIONREQUEST
DESCRIPTOR.message_types_by_name["ReadRowsRequest"] = _READROWSREQUEST
DESCRIPTOR.message_types_by_name["ThrottleState"] = _THROTTLESTATE
DESCRIPTOR.message_types_by_name["StreamStats"] = _STREAMSTATS
DESCRIPTOR.message_types_by_name["ReadRowsResponse"] = _READROWSRESPONSE
DESCRIPTOR.message_types_by_name["SplitReadStreamRequest"] = _SPLITREADSTREAMREQUEST
DESCRIPTOR.message_types_by_name["SplitReadStreamResponse"] = _SPLITREADSTREAMRESPONSE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

CreateReadSessionRequest = _reflection.GeneratedProtocolMessageType(
    "CreateReadSessionRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _CREATEREADSESSIONREQUEST,
        "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
        "__doc__": """Request message for ``CreateReadSession``.
  Attributes:
      parent:
          Required. The request project that owns the session, in the
          form of ``projects/{project_id}``.
      read_session:
          Required. Session to be created.
      max_stream_count:
          Max initial number of streams. If unset or zero, the server
          will provide a value of streams so as to produce reasonable
          throughput. Must be non-negative. The number of streams may be
          lower than the requested number, depending on the amount
          parallelism that is reasonable for the table. Error will be
          returned if the max count is greater than the current system
          max limit of 1,000.  Streams must be read starting from offset
          0.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.CreateReadSessionRequest)
    },
)
_sym_db.RegisterMessage(CreateReadSessionRequest)

ReadRowsRequest = _reflection.GeneratedProtocolMessageType(
    "ReadRowsRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _READROWSREQUEST,
        "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
        "__doc__": """Request message for ``ReadRows``.
  Attributes:
      read_stream:
          Required. Stream to read rows from.
      offset:
          The offset requested must be less than the last row read from
          Read. Requesting a larger offset is undefined. If not
          specified, start reading from offset zero.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.ReadRowsRequest)
    },
)
_sym_db.RegisterMessage(ReadRowsRequest)

ThrottleState = _reflection.GeneratedProtocolMessageType(
    "ThrottleState",
    (_message.Message,),
    {
        "DESCRIPTOR": _THROTTLESTATE,
        "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
        "__doc__": """Information on if the current connection is being throttled.
  Attributes:
      throttle_percent:
          How much this connection is being throttled. Zero means no
          throttling, 100 means fully throttled.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.ThrottleState)
    },
)
_sym_db.RegisterMessage(ThrottleState)

StreamStats = _reflection.GeneratedProtocolMessageType(
    "StreamStats",
    (_message.Message,),
    {
        "Progress": _reflection.GeneratedProtocolMessageType(
            "Progress",
            (_message.Message,),
            {
                "DESCRIPTOR": _STREAMSTATS_PROGRESS,
                "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
                "__doc__": """Protocol buffer.

  Attributes:
        at_response_start:
            The fraction of rows assigned to the stream that have been
            processed by the server so far, not including the rows in the
            current response message.  This value, along with
            ``at_response_end``, can be used to interpolate the progress
            made as the rows in the message are being processed using the
            following formula: ``at_response_start + (at_response_end -
            at_response_start) * rows_processed_from_response /
            rows_in_response``.  Note that if a filter is provided, the
            ``at_response_end`` value of the previous response may not
            necessarily be equal to the ``at_response_start`` value of the
            current response.
        at_response_end:
            Similar to ``at_response_start``, except that this value
            includes the rows in the current response.
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.StreamStats.Progress)
            },
        ),
        "DESCRIPTOR": _STREAMSTATS,
        "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
        "__doc__": """Estimated stream statistics for a given Stream.
  Attributes:
      progress:
          Represents the progress of the current stream.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.StreamStats)
    },
)
_sym_db.RegisterMessage(StreamStats)
_sym_db.RegisterMessage(StreamStats.Progress)

ReadRowsResponse = _reflection.GeneratedProtocolMessageType(
    "ReadRowsResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _READROWSRESPONSE,
        "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
        "__doc__": """Response from calling ``ReadRows`` may include row data, progress and
  throttling information.
  Attributes:
      rows:
          Row data is returned in format specified during session
          creation.
      avro_rows:
          Serialized row data in AVRO format.
      arrow_record_batch:
          Serialized row data in Arrow RecordBatch format.
      row_count:
          Number of serialized rows in the rows block.
      stats:
          Statistics for the stream.
      throttle_state:
          Throttling state. If unset, the latest response still
          describes the current throttling status.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.ReadRowsResponse)
    },
)
_sym_db.RegisterMessage(ReadRowsResponse)

SplitReadStreamRequest = _reflection.GeneratedProtocolMessageType(
    "SplitReadStreamRequest",
    (_message.Message,),
    {
        "DESCRIPTOR": _SPLITREADSTREAMREQUEST,
        "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
        "__doc__": """Request message for ``SplitReadStream``.
  Attributes:
      name:
          Required. Name of the stream to split.
      fraction:
          A value in the range (0.0, 1.0) that specifies the fractional
          point at which the original stream should be split. The actual
          split point is evaluated on pre-filtered rows, so if a filter
          is provided, then there is no guarantee that the division of
          the rows between the new child streams will be proportional to
          this fractional value. Additionally, because the server-side
          unit for assigning data is collections of rows, this fraction
          will always map to a data storage boundary on the server side.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.SplitReadStreamRequest)
    },
)
_sym_db.RegisterMessage(SplitReadStreamRequest)

SplitReadStreamResponse = _reflection.GeneratedProtocolMessageType(
    "SplitReadStreamResponse",
    (_message.Message,),
    {
        "DESCRIPTOR": _SPLITREADSTREAMRESPONSE,
        "__module__": "google.cloud.bigquery_storage_v1beta2.proto.storage_pb2",
        "__doc__": """Response message for ``SplitReadStream``.
  Attributes:
      primary_stream:
          Primary stream, which contains the beginning portion of
          \|original_stream|. An empty value indicates that the original
          stream can no longer be split.
      remainder_stream:
          Remainder stream, which contains the tail of
          \|original_stream|. An empty value indicates that the original
          stream can no longer be split.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1beta2.SplitReadStreamResponse)
    },
)
_sym_db.RegisterMessage(SplitReadStreamResponse)


DESCRIPTOR._options = None
_CREATEREADSESSIONREQUEST.fields_by_name["parent"]._options = None
_CREATEREADSESSIONREQUEST.fields_by_name["read_session"]._options = None
_READROWSREQUEST.fields_by_name["read_stream"]._options = None
_SPLITREADSTREAMREQUEST.fields_by_name["name"]._options = None

_BIGQUERYREAD = _descriptor.ServiceDescriptor(
    name="BigQueryRead",
    full_name="google.cloud.bigquery.storage.v1beta2.BigQueryRead",
    file=DESCRIPTOR,
    index=0,
    serialized_options=b"\312A\036bigquerystorage.googleapis.com\322A\211\001https://www.googleapis.com/auth/bigquery,https://www.googleapis.com/auth/bigquery.readonly,https://www.googleapis.com/auth/cloud-platform",
    serialized_start=1538,
    serialized_end=2421,
    methods=[
        _descriptor.MethodDescriptor(
            name="CreateReadSession",
            full_name="google.cloud.bigquery.storage.v1beta2.BigQueryRead.CreateReadSession",
            index=0,
            containing_service=None,
            input_type=_CREATEREADSESSIONREQUEST,
            output_type=google_dot_cloud_dot_bigquery__storage__v1beta2_dot_proto_dot_stream__pb2._READSESSION,
            serialized_options=b'\202\323\344\223\002A"</v1beta2/{read_session.table=projects/*/datasets/*/tables/*}:\001*\332A$parent,read_session,max_stream_count',
        ),
        _descriptor.MethodDescriptor(
            name="ReadRows",
            full_name="google.cloud.bigquery.storage.v1beta2.BigQueryRead.ReadRows",
            index=1,
            containing_service=None,
            input_type=_READROWSREQUEST,
            output_type=_READROWSRESPONSE,
            serialized_options=b"\202\323\344\223\002D\022B/v1beta2/{read_stream=projects/*/locations/*/sessions/*/streams/*}\332A\022read_stream,offset",
        ),
        _descriptor.MethodDescriptor(
            name="SplitReadStream",
            full_name="google.cloud.bigquery.storage.v1beta2.BigQueryRead.SplitReadStream",
            index=2,
            containing_service=None,
            input_type=_SPLITREADSTREAMREQUEST,
            output_type=_SPLITREADSTREAMRESPONSE,
            serialized_options=b"\202\323\344\223\002=\022;/v1beta2/{name=projects/*/locations/*/sessions/*/streams/*}",
        ),
    ],
)
_sym_db.RegisterServiceDescriptor(_BIGQUERYREAD)

DESCRIPTOR.services_by_name["BigQueryRead"] = _BIGQUERYREAD

# @@protoc_insertion_point(module_scope)

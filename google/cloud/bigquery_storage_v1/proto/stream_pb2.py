# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/cloud/bigquery_storage_v1/proto/stream.proto

from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database

# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.cloud.bigquery_storage_v1.proto import (
    arrow_pb2 as google_dot_cloud_dot_bigquery__storage__v1_dot_proto_dot_arrow__pb2,
)
from google.cloud.bigquery_storage_v1.proto import (
    avro_pb2 as google_dot_cloud_dot_bigquery__storage__v1_dot_proto_dot_avro__pb2,
)
from google.protobuf import timestamp_pb2 as google_dot_protobuf_dot_timestamp__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
    name="google/cloud/bigquery_storage_v1/proto/stream.proto",
    package="google.cloud.bigquery.storage.v1",
    syntax="proto3",
    serialized_options=b"\n$com.google.cloud.bigquery.storage.v1B\013StreamProtoP\001ZGgoogle.golang.org/genproto/googleapis/cloud/bigquery/storage/v1;storage\252\002 Google.Cloud.BigQuery.Storage.V1\312\002 Google\\Cloud\\BigQuery\\Storage\\V1",
    create_key=_descriptor._internal_create_key,
    serialized_pb=b'\n3google/cloud/bigquery_storage_v1/proto/stream.proto\x12 google.cloud.bigquery.storage.v1\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x32google/cloud/bigquery_storage_v1/proto/arrow.proto\x1a\x31google/cloud/bigquery_storage_v1/proto/avro.proto\x1a\x1fgoogle/protobuf/timestamp.proto"\xe7\x06\n\x0bReadSession\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0\x41\x03\x12\x34\n\x0b\x65xpire_time\x18\x02 \x01(\x0b\x32\x1a.google.protobuf.TimestampB\x03\xe0\x41\x03\x12\x46\n\x0b\x64\x61ta_format\x18\x03 \x01(\x0e\x32,.google.cloud.bigquery.storage.v1.DataFormatB\x03\xe0\x41\x05\x12H\n\x0b\x61vro_schema\x18\x04 \x01(\x0b\x32,.google.cloud.bigquery.storage.v1.AvroSchemaB\x03\xe0\x41\x03H\x00\x12J\n\x0c\x61rrow_schema\x18\x05 \x01(\x0b\x32-.google.cloud.bigquery.storage.v1.ArrowSchemaB\x03\xe0\x41\x03H\x00\x12\x34\n\x05table\x18\x06 \x01(\tB%\xe0\x41\x05\xfa\x41\x1f\n\x1d\x62igquery.googleapis.com/Table\x12Z\n\x0ftable_modifiers\x18\x07 \x01(\x0b\x32<.google.cloud.bigquery.storage.v1.ReadSession.TableModifiersB\x03\xe0\x41\x01\x12Y\n\x0cread_options\x18\x08 \x01(\x0b\x32>.google.cloud.bigquery.storage.v1.ReadSession.TableReadOptionsB\x03\xe0\x41\x01\x12\x42\n\x07streams\x18\n \x03(\x0b\x32,.google.cloud.bigquery.storage.v1.ReadStreamB\x03\xe0\x41\x03\x1a\x43\n\x0eTableModifiers\x12\x31\n\rsnapshot_time\x18\x01 \x01(\x0b\x32\x1a.google.protobuf.Timestamp\x1a\x44\n\x10TableReadOptions\x12\x17\n\x0fselected_fields\x18\x01 \x03(\t\x12\x17\n\x0frow_restriction\x18\x02 \x01(\t:k\xea\x41h\n*bigquerystorage.googleapis.com/ReadSession\x12:projects/{project}/locations/{location}/sessions/{session}B\x08\n\x06schema"\x9c\x01\n\nReadStream\x12\x11\n\x04name\x18\x01 \x01(\tB\x03\xe0\x41\x03:{\xea\x41x\n)bigquerystorage.googleapis.com/ReadStream\x12Kprojects/{project}/locations/{location}/sessions/{session}/streams/{stream}*>\n\nDataFormat\x12\x1b\n\x17\x44\x41TA_FORMAT_UNSPECIFIED\x10\x00\x12\x08\n\x04\x41VRO\x10\x01\x12\t\n\x05\x41RROW\x10\x02\x42\xc4\x01\n$com.google.cloud.bigquery.storage.v1B\x0bStreamProtoP\x01ZGgoogle.golang.org/genproto/googleapis/cloud/bigquery/storage/v1;storage\xaa\x02 Google.Cloud.BigQuery.Storage.V1\xca\x02 Google\\Cloud\\BigQuery\\Storage\\V1b\x06proto3',
    dependencies=[
        google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,
        google_dot_api_dot_resource__pb2.DESCRIPTOR,
        google_dot_cloud_dot_bigquery__storage__v1_dot_proto_dot_arrow__pb2.DESCRIPTOR,
        google_dot_cloud_dot_bigquery__storage__v1_dot_proto_dot_avro__pb2.DESCRIPTOR,
        google_dot_protobuf_dot_timestamp__pb2.DESCRIPTOR,
    ],
)

_DATAFORMAT = _descriptor.EnumDescriptor(
    name="DataFormat",
    full_name="google.cloud.bigquery.storage.v1.DataFormat",
    filename=None,
    file=DESCRIPTOR,
    create_key=_descriptor._internal_create_key,
    values=[
        _descriptor.EnumValueDescriptor(
            name="DATA_FORMAT_UNSPECIFIED",
            index=0,
            number=0,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="AVRO",
            index=1,
            number=1,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.EnumValueDescriptor(
            name="ARROW",
            index=2,
            number=2,
            serialized_options=None,
            type=None,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    containing_type=None,
    serialized_options=None,
    serialized_start=1318,
    serialized_end=1380,
)
_sym_db.RegisterEnumDescriptor(_DATAFORMAT)

DataFormat = enum_type_wrapper.EnumTypeWrapper(_DATAFORMAT)
DATA_FORMAT_UNSPECIFIED = 0
AVRO = 1
ARROW = 2


_READSESSION_TABLEMODIFIERS = _descriptor.Descriptor(
    name="TableModifiers",
    full_name="google.cloud.bigquery.storage.v1.ReadSession.TableModifiers",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="snapshot_time",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.TableModifiers.snapshot_time",
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
            create_key=_descriptor._internal_create_key,
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
    serialized_start=901,
    serialized_end=968,
)

_READSESSION_TABLEREADOPTIONS = _descriptor.Descriptor(
    name="TableReadOptions",
    full_name="google.cloud.bigquery.storage.v1.ReadSession.TableReadOptions",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="selected_fields",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.TableReadOptions.selected_fields",
            index=0,
            number=1,
            type=9,
            cpp_type=9,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="row_restriction",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.TableReadOptions.row_restriction",
            index=1,
            number=2,
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
            serialized_options=None,
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
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
    serialized_start=970,
    serialized_end=1038,
)

_READSESSION = _descriptor.Descriptor(
    name="ReadSession",
    full_name="google.cloud.bigquery.storage.v1.ReadSession",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.name",
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
            serialized_options=b"\340A\003",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="expire_time",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.expire_time",
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
            serialized_options=b"\340A\003",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="data_format",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.data_format",
            index=2,
            number=3,
            type=14,
            cpp_type=8,
            label=1,
            has_default_value=False,
            default_value=0,
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\005",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="avro_schema",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.avro_schema",
            index=3,
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
            serialized_options=b"\340A\003",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="arrow_schema",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.arrow_schema",
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
            serialized_options=b"\340A\003",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="table",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.table",
            index=5,
            number=6,
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
            serialized_options=b"\340A\005\372A\037\n\035bigquery.googleapis.com/Table",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="table_modifiers",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.table_modifiers",
            index=6,
            number=7,
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
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="read_options",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.read_options",
            index=7,
            number=8,
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
            serialized_options=b"\340A\001",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
        _descriptor.FieldDescriptor(
            name="streams",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.streams",
            index=8,
            number=10,
            type=11,
            cpp_type=10,
            label=3,
            has_default_value=False,
            default_value=[],
            message_type=None,
            enum_type=None,
            containing_type=None,
            is_extension=False,
            extension_scope=None,
            serialized_options=b"\340A\003",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        ),
    ],
    extensions=[],
    nested_types=[_READSESSION_TABLEMODIFIERS, _READSESSION_TABLEREADOPTIONS],
    enum_types=[],
    serialized_options=b"\352Ah\n*bigquerystorage.googleapis.com/ReadSession\022:projects/{project}/locations/{location}/sessions/{session}",
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[
        _descriptor.OneofDescriptor(
            name="schema",
            full_name="google.cloud.bigquery.storage.v1.ReadSession.schema",
            index=0,
            containing_type=None,
            create_key=_descriptor._internal_create_key,
            fields=[],
        )
    ],
    serialized_start=286,
    serialized_end=1157,
)


_READSTREAM = _descriptor.Descriptor(
    name="ReadStream",
    full_name="google.cloud.bigquery.storage.v1.ReadStream",
    filename=None,
    file=DESCRIPTOR,
    containing_type=None,
    create_key=_descriptor._internal_create_key,
    fields=[
        _descriptor.FieldDescriptor(
            name="name",
            full_name="google.cloud.bigquery.storage.v1.ReadStream.name",
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
            serialized_options=b"\340A\003",
            file=DESCRIPTOR,
            create_key=_descriptor._internal_create_key,
        )
    ],
    extensions=[],
    nested_types=[],
    enum_types=[],
    serialized_options=b"\352Ax\n)bigquerystorage.googleapis.com/ReadStream\022Kprojects/{project}/locations/{location}/sessions/{session}/streams/{stream}",
    is_extendable=False,
    syntax="proto3",
    extension_ranges=[],
    oneofs=[],
    serialized_start=1160,
    serialized_end=1316,
)

_READSESSION_TABLEMODIFIERS.fields_by_name[
    "snapshot_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_READSESSION_TABLEMODIFIERS.containing_type = _READSESSION
_READSESSION_TABLEREADOPTIONS.containing_type = _READSESSION
_READSESSION.fields_by_name[
    "expire_time"
].message_type = google_dot_protobuf_dot_timestamp__pb2._TIMESTAMP
_READSESSION.fields_by_name["data_format"].enum_type = _DATAFORMAT
_READSESSION.fields_by_name[
    "avro_schema"
].message_type = (
    google_dot_cloud_dot_bigquery__storage__v1_dot_proto_dot_avro__pb2._AVROSCHEMA
)
_READSESSION.fields_by_name[
    "arrow_schema"
].message_type = (
    google_dot_cloud_dot_bigquery__storage__v1_dot_proto_dot_arrow__pb2._ARROWSCHEMA
)
_READSESSION.fields_by_name[
    "table_modifiers"
].message_type = _READSESSION_TABLEMODIFIERS
_READSESSION.fields_by_name["read_options"].message_type = _READSESSION_TABLEREADOPTIONS
_READSESSION.fields_by_name["streams"].message_type = _READSTREAM
_READSESSION.oneofs_by_name["schema"].fields.append(
    _READSESSION.fields_by_name["avro_schema"]
)
_READSESSION.fields_by_name[
    "avro_schema"
].containing_oneof = _READSESSION.oneofs_by_name["schema"]
_READSESSION.oneofs_by_name["schema"].fields.append(
    _READSESSION.fields_by_name["arrow_schema"]
)
_READSESSION.fields_by_name[
    "arrow_schema"
].containing_oneof = _READSESSION.oneofs_by_name["schema"]
DESCRIPTOR.message_types_by_name["ReadSession"] = _READSESSION
DESCRIPTOR.message_types_by_name["ReadStream"] = _READSTREAM
DESCRIPTOR.enum_types_by_name["DataFormat"] = _DATAFORMAT
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

ReadSession = _reflection.GeneratedProtocolMessageType(
    "ReadSession",
    (_message.Message,),
    {
        "TableModifiers": _reflection.GeneratedProtocolMessageType(
            "TableModifiers",
            (_message.Message,),
            {
                "DESCRIPTOR": _READSESSION_TABLEMODIFIERS,
                "__module__": "google.cloud.bigquery_storage_v1.proto.stream_pb2",
                "__doc__": """Additional attributes when reading a table.
    
    Attributes:
        snapshot_time:
            The snapshot time of the table. If not set, interpreted as
            now.
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1.ReadSession.TableModifiers)
            },
        ),
        "TableReadOptions": _reflection.GeneratedProtocolMessageType(
            "TableReadOptions",
            (_message.Message,),
            {
                "DESCRIPTOR": _READSESSION_TABLEREADOPTIONS,
                "__module__": "google.cloud.bigquery_storage_v1.proto.stream_pb2",
                "__doc__": """Options dictating how we read a table.
    
    Attributes:
        selected_fields:
            Names of the fields in the table that should be read. If
            empty, all fields will be read. If the specified field is a
            nested field, all the sub-fields in the field will be
            selected. The output field order is unrelated to the order of
            fields in selected_fields.
        row_restriction:
            SQL text filtering statement, similar to a WHERE clause in a
            query. Aggregates are not supported.  Examples: “int_field >
            5” “date_field = CAST(‘2014-9-27’ as DATE)” “nullable_field is
            not NULL” “st_equals(geo_field, st_geofromtext(”POINT(2,
            2)“))” “numeric_field BETWEEN 1.0 AND 5.0”
    """,
                # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1.ReadSession.TableReadOptions)
            },
        ),
        "DESCRIPTOR": _READSESSION,
        "__module__": "google.cloud.bigquery_storage_v1.proto.stream_pb2",
        "__doc__": """Information about the ReadSession.
  
  Attributes:
      name:
          Output only. Unique identifier for the session, in the form ``
          projects/{project_id}/locations/{location}/sessions/{session_i
          d}``.
      expire_time:
          Output only. Time at which the session becomes invalid. After
          this time, subsequent requests to read this Session will
          return errors. The expire_time is automatically assigned and
          currently cannot be specified or updated.
      data_format:
          Immutable. Data format of the output data.
      schema:
          The schema for the read. If read_options.selected_fields is
          set, the schema may be different from the table schema as it
          will only contain the selected fields.
      avro_schema:
          Output only. Avro schema.
      arrow_schema:
          Output only. Arrow schema.
      table:
          Immutable. Table that this ReadSession is reading from, in the
          form ``projects/{project_id}/datasets/{dataset_id}/tables/{tab
          le_id}``
      table_modifiers:
          Optional. Any modifiers which are applied when reading from
          the specified table.
      read_options:
          Optional. Read options for this session (e.g. column
          selection, filters).
      streams:
          Output only. A list of streams created with the session.  At
          least one stream is created with the session. In the future,
          larger request_stream_count values *may* result in this list
          being unpopulated, in that case, the user will need to use a
          List method to get the streams instead, which is not yet
          available.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1.ReadSession)
    },
)
_sym_db.RegisterMessage(ReadSession)
_sym_db.RegisterMessage(ReadSession.TableModifiers)
_sym_db.RegisterMessage(ReadSession.TableReadOptions)

ReadStream = _reflection.GeneratedProtocolMessageType(
    "ReadStream",
    (_message.Message,),
    {
        "DESCRIPTOR": _READSTREAM,
        "__module__": "google.cloud.bigquery_storage_v1.proto.stream_pb2",
        "__doc__": """Information about a single stream that gets data out of the storage
  system. Most of the information about ``ReadStream`` instances is
  aggregated, making ``ReadStream`` lightweight.
  
  Attributes:
      name:
          Output only. Name of the stream, in the form ``projects/{proje
          ct_id}/locations/{location}/sessions/{session_id}/streams/{str
          eam_id}``.
  """,
        # @@protoc_insertion_point(class_scope:google.cloud.bigquery.storage.v1.ReadStream)
    },
)
_sym_db.RegisterMessage(ReadStream)


DESCRIPTOR._options = None
_READSESSION.fields_by_name["name"]._options = None
_READSESSION.fields_by_name["expire_time"]._options = None
_READSESSION.fields_by_name["data_format"]._options = None
_READSESSION.fields_by_name["avro_schema"]._options = None
_READSESSION.fields_by_name["arrow_schema"]._options = None
_READSESSION.fields_by_name["table"]._options = None
_READSESSION.fields_by_name["table_modifiers"]._options = None
_READSESSION.fields_by_name["read_options"]._options = None
_READSESSION.fields_by_name["streams"]._options = None
_READSESSION._options = None
_READSTREAM.fields_by_name["name"]._options = None
_READSTREAM._options = None
# @@protoc_insertion_point(module_scope)

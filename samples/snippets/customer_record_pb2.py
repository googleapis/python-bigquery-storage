# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: customer_record.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x15\x63ustomer_record.proto\"8\n\x0e\x43ustomerRecord\x12\x15\n\rcustomer_name\x18\x01 \x01(\t\x12\x0f\n\x07row_num\x18\x02 \x02(\x03')



_CUSTOMERRECORD = DESCRIPTOR.message_types_by_name['CustomerRecord']
CustomerRecord = _reflection.GeneratedProtocolMessageType('CustomerRecord', (_message.Message,), {
  'DESCRIPTOR' : _CUSTOMERRECORD,
  '__module__' : 'customer_record_pb2'
  # @@protoc_insertion_point(class_scope:CustomerRecord)
  })
_sym_db.RegisterMessage(CustomerRecord)

if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _CUSTOMERRECORD._serialized_start=25
  _CUSTOMERRECORD._serialized_end=81
# @@protoc_insertion_point(module_scope)

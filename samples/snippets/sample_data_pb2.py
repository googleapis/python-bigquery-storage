# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: sample_data.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x11sample_data.proto\"\xff\x03\n\nSampleData\x12\x10\n\x08\x62ool_col\x18\x01 \x01(\x08\x12\x11\n\tbytes_col\x18\x02 \x01(\x0c\x12\x13\n\x0b\x66loat64_col\x18\x03 \x01(\x01\x12\x11\n\tint64_col\x18\x04 \x01(\x03\x12\x12\n\nstring_col\x18\x05 \x01(\t\x12\x10\n\x08\x64\x61te_col\x18\x06 \x01(\x05\x12\x14\n\x0c\x64\x61tetime_col\x18\x07 \x01(\t\x12\x15\n\rgeography_col\x18\x08 \x01(\t\x12\x13\n\x0bnumeric_col\x18\t \x01(\t\x12\x16\n\x0e\x62ignumeric_col\x18\n \x01(\t\x12\x10\n\x08time_col\x18\x0b \x01(\t\x12\x15\n\rtimestamp_col\x18\x0c \x01(\x03\x12\x12\n\nint64_list\x18\r \x03(\x03\x12,\n\nstruct_col\x18\x0e \x01(\x0b\x32\x18.SampleData.SampleStruct\x12-\n\x0bstruct_list\x18\x0f \x03(\x0b\x32\x18.SampleData.SampleStruct\x12*\n\nrange_date\x18\x10 \x01(\x0b\x32\x16.SampleData.RangeValue\x12\x0f\n\x07row_num\x18\x11 \x02(\x03\x1a#\n\x0cSampleStruct\x12\x13\n\x0bsub_int_col\x18\x01 \x01(\x03\x1a(\n\nRangeValue\x12\r\n\x05start\x18\x01 \x01(\x05\x12\x0b\n\x03\x65nd\x18\x02 \x01(\x05')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'sample_data_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _SAMPLEDATA._serialized_start=22
  _SAMPLEDATA._serialized_end=533
  _SAMPLEDATA_SAMPLESTRUCT._serialized_start=456
  _SAMPLEDATA_SAMPLESTRUCT._serialized_end=491
  _SAMPLEDATA_RANGEVALUE._serialized_start=493
  _SAMPLEDATA_RANGEVALUE._serialized_end=533
# @@protoc_insertion_point(module_scope)

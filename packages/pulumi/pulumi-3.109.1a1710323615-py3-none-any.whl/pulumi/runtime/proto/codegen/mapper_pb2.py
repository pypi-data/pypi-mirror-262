# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: pulumi/codegen/mapper.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x1bpulumi/codegen/mapper.proto\x12\x07\x63odegen\">\n\x11GetMappingRequest\x12\x10\n\x08provider\x18\x01 \x01(\t\x12\x17\n\x0fpulumi_provider\x18\x02 \x01(\t\"\"\n\x12GetMappingResponse\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\x0c\x32Q\n\x06Mapper\x12G\n\nGetMapping\x12\x1a.codegen.GetMappingRequest\x1a\x1b.codegen.GetMappingResponse\"\x00\x42\x32Z0github.com/pulumi/pulumi/sdk/v3/proto/go/codegenb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'pulumi.codegen.mapper_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'Z0github.com/pulumi/pulumi/sdk/v3/proto/go/codegen'
  _GETMAPPINGREQUEST._serialized_start=40
  _GETMAPPINGREQUEST._serialized_end=102
  _GETMAPPINGRESPONSE._serialized_start=104
  _GETMAPPINGRESPONSE._serialized_end=138
  _MAPPER._serialized_start=140
  _MAPPER._serialized_end=221
# @@protoc_insertion_point(module_scope)

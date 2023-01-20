# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: api.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor.FileDescriptor(
  name='api.proto',
  package='api',
  syntax='proto3',
  serialized_options=b'Z\013storage/api',
  create_key=_descriptor._internal_create_key,
  serialized_pb=b'\n\tapi.proto\x12\x03\x61pi\"N\n\x0eStorageRequest\x12\x0f\n\x07\x63ommand\x18\x01 \x01(\t\x12\x0c\n\x04name\x18\x02 \x01(\t\x12\x0f\n\x07\x64\x65vices\x18\x03 \x03(\t\x12\x0c\n\x04size\x18\x04 \x01(\t\"4\n\x0cStorageReply\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x13\n\x0breturn_code\x18\x02 \x01(\x03\"M\n\x10StorageListReply\x12\x0f\n\x07message\x18\x01 \x01(\t\x12\x13\n\x0b\x64\x65vice_json\x18\x02 \x01(\t\x12\x13\n\x0breturn_code\x18\x03 \x01(\x03\x32\xe1\x03\n\x0cLocalStorage\x12\x38\n\x0c\x43reateVolume\x12\x13.api.StorageRequest\x1a\x11.api.StorageReply\"\x00\x12:\n\x0e\x43reateSnapshot\x12\x13.api.StorageRequest\x1a\x11.api.StorageReply\"\x00\x12\x36\n\x0c\x44\x65leteVolume\x12\x13.api.StorageRequest\x1a\x11.api.StorageReply\x12\x38\n\x0e\x44\x65leteSnapshot\x12\x13.api.StorageRequest\x1a\x11.api.StorageReply\x12\x36\n\x0cResizeVolume\x12\x13.api.StorageRequest\x1a\x11.api.StorageReply\x12\x39\n\x0bListVolumes\x12\x13.api.StorageRequest\x1a\x15.api.StorageListReply\x12\x39\n\x0bListDevices\x12\x13.api.StorageRequest\x1a\x15.api.StorageListReply\x12;\n\rListSnapshots\x12\x13.api.StorageRequest\x1a\x15.api.StorageListReplyB\rZ\x0bstorage/apib\x06proto3'
)




_STORAGEREQUEST = _descriptor.Descriptor(
  name='StorageRequest',
  full_name='api.StorageRequest',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='command', full_name='api.StorageRequest.command', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='name', full_name='api.StorageRequest.name', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='devices', full_name='api.StorageRequest.devices', index=2,
      number=3, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='size', full_name='api.StorageRequest.size', index=3,
      number=4, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=18,
  serialized_end=96,
)


_STORAGEREPLY = _descriptor.Descriptor(
  name='StorageReply',
  full_name='api.StorageReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='api.StorageReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='return_code', full_name='api.StorageReply.return_code', index=1,
      number=2, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=98,
  serialized_end=150,
)


_STORAGELISTREPLY = _descriptor.Descriptor(
  name='StorageListReply',
  full_name='api.StorageListReply',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  create_key=_descriptor._internal_create_key,
  fields=[
    _descriptor.FieldDescriptor(
      name='message', full_name='api.StorageListReply.message', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='device_json', full_name='api.StorageListReply.device_json', index=1,
      number=2, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=b"".decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
    _descriptor.FieldDescriptor(
      name='return_code', full_name='api.StorageListReply.return_code', index=2,
      number=3, type=3, cpp_type=2, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=None, file=DESCRIPTOR,  create_key=_descriptor._internal_create_key),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=152,
  serialized_end=229,
)

DESCRIPTOR.message_types_by_name['StorageRequest'] = _STORAGEREQUEST
DESCRIPTOR.message_types_by_name['StorageReply'] = _STORAGEREPLY
DESCRIPTOR.message_types_by_name['StorageListReply'] = _STORAGELISTREPLY
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

StorageRequest = _reflection.GeneratedProtocolMessageType('StorageRequest', (_message.Message,), {
  'DESCRIPTOR' : _STORAGEREQUEST,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.StorageRequest)
  })
_sym_db.RegisterMessage(StorageRequest)

StorageReply = _reflection.GeneratedProtocolMessageType('StorageReply', (_message.Message,), {
  'DESCRIPTOR' : _STORAGEREPLY,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.StorageReply)
  })
_sym_db.RegisterMessage(StorageReply)

StorageListReply = _reflection.GeneratedProtocolMessageType('StorageListReply', (_message.Message,), {
  'DESCRIPTOR' : _STORAGELISTREPLY,
  '__module__' : 'api_pb2'
  # @@protoc_insertion_point(class_scope:api.StorageListReply)
  })
_sym_db.RegisterMessage(StorageListReply)


DESCRIPTOR._options = None

_LOCALSTORAGE = _descriptor.ServiceDescriptor(
  name='LocalStorage',
  full_name='api.LocalStorage',
  file=DESCRIPTOR,
  index=0,
  serialized_options=None,
  create_key=_descriptor._internal_create_key,
  serialized_start=232,
  serialized_end=713,
  methods=[
  _descriptor.MethodDescriptor(
    name='CreateVolume',
    full_name='api.LocalStorage.CreateVolume',
    index=0,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='CreateSnapshot',
    full_name='api.LocalStorage.CreateSnapshot',
    index=1,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteVolume',
    full_name='api.LocalStorage.DeleteVolume',
    index=2,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='DeleteSnapshot',
    full_name='api.LocalStorage.DeleteSnapshot',
    index=3,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ResizeVolume',
    full_name='api.LocalStorage.ResizeVolume',
    index=4,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGEREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListVolumes',
    full_name='api.LocalStorage.ListVolumes',
    index=5,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGELISTREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListDevices',
    full_name='api.LocalStorage.ListDevices',
    index=6,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGELISTREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
  _descriptor.MethodDescriptor(
    name='ListSnapshots',
    full_name='api.LocalStorage.ListSnapshots',
    index=7,
    containing_service=None,
    input_type=_STORAGEREQUEST,
    output_type=_STORAGELISTREPLY,
    serialized_options=None,
    create_key=_descriptor._internal_create_key,
  ),
])
_sym_db.RegisterServiceDescriptor(_LOCALSTORAGE)

DESCRIPTOR.services_by_name['LocalStorage'] = _LOCALSTORAGE

# @@protoc_insertion_point(module_scope)

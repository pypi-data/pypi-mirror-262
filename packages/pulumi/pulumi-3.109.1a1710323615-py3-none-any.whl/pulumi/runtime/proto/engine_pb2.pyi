"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2016-2018, Pulumi Corporation.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import builtins
import google.protobuf.descriptor
import google.protobuf.internal.enum_type_wrapper
import google.protobuf.message
import sys
import typing

if sys.version_info >= (3, 10):
    import typing as typing_extensions
else:
    import typing_extensions

DESCRIPTOR: google.protobuf.descriptor.FileDescriptor

class _LogSeverity:
    ValueType = typing.NewType("ValueType", builtins.int)
    V: typing_extensions.TypeAlias = ValueType

class _LogSeverityEnumTypeWrapper(google.protobuf.internal.enum_type_wrapper._EnumTypeWrapper[_LogSeverity.ValueType], builtins.type):
    DESCRIPTOR: google.protobuf.descriptor.EnumDescriptor
    DEBUG: _LogSeverity.ValueType  # 0
    """a debug-level message not displayed to end-users (the default)."""
    INFO: _LogSeverity.ValueType  # 1
    """an informational message printed to output during resource operations."""
    WARNING: _LogSeverity.ValueType  # 2
    """a warning to indicate that something went wrong."""
    ERROR: _LogSeverity.ValueType  # 3
    """a fatal error indicating that the tool should stop processing subsequent resource operations."""

class LogSeverity(_LogSeverity, metaclass=_LogSeverityEnumTypeWrapper):
    """LogSeverity is the severity level of a log message.  Errors are fatal; all others are informational."""

DEBUG: LogSeverity.ValueType  # 0
"""a debug-level message not displayed to end-users (the default)."""
INFO: LogSeverity.ValueType  # 1
"""an informational message printed to output during resource operations."""
WARNING: LogSeverity.ValueType  # 2
"""a warning to indicate that something went wrong."""
ERROR: LogSeverity.ValueType  # 3
"""a fatal error indicating that the tool should stop processing subsequent resource operations."""
global___LogSeverity = LogSeverity

@typing_extensions.final
class LogRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    SEVERITY_FIELD_NUMBER: builtins.int
    MESSAGE_FIELD_NUMBER: builtins.int
    URN_FIELD_NUMBER: builtins.int
    STREAMID_FIELD_NUMBER: builtins.int
    EPHEMERAL_FIELD_NUMBER: builtins.int
    severity: global___LogSeverity.ValueType
    """the logging level of this message."""
    message: builtins.str
    """the contents of the logged message."""
    urn: builtins.str
    """the (optional) resource urn this log is associated with."""
    streamId: builtins.int
    """the (optional) stream id that a stream of log messages can be associated with. This allows
    clients to not have to buffer a large set of log messages that they all want to be
    conceptually connected.  Instead the messages can be sent as chunks (with the same stream id)
    and the end display can show the messages as they arrive, while still stitching them together
    into one total log message.

    0/not-given means: do not associate with any stream.
    """
    ephemeral: builtins.bool
    """Optional value indicating whether this is a status message."""
    def __init__(
        self,
        *,
        severity: global___LogSeverity.ValueType = ...,
        message: builtins.str = ...,
        urn: builtins.str = ...,
        streamId: builtins.int = ...,
        ephemeral: builtins.bool = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["ephemeral", b"ephemeral", "message", b"message", "severity", b"severity", "streamId", b"streamId", "urn", b"urn"]) -> None: ...

global___LogRequest = LogRequest

@typing_extensions.final
class GetRootResourceRequest(google.protobuf.message.Message):
    """empty."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___GetRootResourceRequest = GetRootResourceRequest

@typing_extensions.final
class GetRootResourceResponse(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    URN_FIELD_NUMBER: builtins.int
    urn: builtins.str
    """the URN of the root resource, or the empty string if one was not set."""
    def __init__(
        self,
        *,
        urn: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["urn", b"urn"]) -> None: ...

global___GetRootResourceResponse = GetRootResourceResponse

@typing_extensions.final
class SetRootResourceRequest(google.protobuf.message.Message):
    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    URN_FIELD_NUMBER: builtins.int
    urn: builtins.str
    """the URN of the root resource, or the empty string."""
    def __init__(
        self,
        *,
        urn: builtins.str = ...,
    ) -> None: ...
    def ClearField(self, field_name: typing_extensions.Literal["urn", b"urn"]) -> None: ...

global___SetRootResourceRequest = SetRootResourceRequest

@typing_extensions.final
class SetRootResourceResponse(google.protobuf.message.Message):
    """empty."""

    DESCRIPTOR: google.protobuf.descriptor.Descriptor

    def __init__(
        self,
    ) -> None: ...

global___SetRootResourceResponse = SetRootResourceResponse

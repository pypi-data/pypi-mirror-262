"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
Copyright 2016-2023, Pulumi Corporation.

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
import abc
import grpc
import pulumi.codegen.mapper_pb2

class MapperStub:
    """Mapper is a service for getting mappings from other ecosystems to Pulumi.
    This is currently unstable and experimental.
    """

    def __init__(self, channel: grpc.Channel) -> None: ...
    GetMapping: grpc.UnaryUnaryMultiCallable[
        pulumi.codegen.mapper_pb2.GetMappingRequest,
        pulumi.codegen.mapper_pb2.GetMappingResponse,
    ]
    """GetMapping tries to find a mapping for the given provider."""

class MapperServicer(metaclass=abc.ABCMeta):
    """Mapper is a service for getting mappings from other ecosystems to Pulumi.
    This is currently unstable and experimental.
    """

    @abc.abstractmethod
    def GetMapping(
        self,
        request: pulumi.codegen.mapper_pb2.GetMappingRequest,
        context: grpc.ServicerContext,
    ) -> pulumi.codegen.mapper_pb2.GetMappingResponse:
        """GetMapping tries to find a mapping for the given provider."""

def add_MapperServicer_to_server(servicer: MapperServicer, server: grpc.Server) -> None: ...

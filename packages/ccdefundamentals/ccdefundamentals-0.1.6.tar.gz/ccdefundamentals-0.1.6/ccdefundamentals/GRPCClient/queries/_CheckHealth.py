from __future__ import annotations
from ccdefundamentals.GRPCClient.service_pb2_grpc import QueriesStub
from ccdefundamentals.GRPCClient.types_pb2 import *
from ccdefundamentals.GRPCClient.health_pb2 import *
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ccdefundamentals.GRPCClient import GRPCClient
from ccdefundamentals.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
import os
import sys
from rich import print

sys.path.append(os.path.dirname("ccdefundamentals"))
from ccdefundamentals.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def check_health(self: GRPCClient):
        result = {}

        self.check_connection(sys._getframe().f_code.co_name)
        grpc_return_value: NodeHealthResponse = self.health.Check(
            request=NodeHealthRequest()
        )

        return grpc_return_value

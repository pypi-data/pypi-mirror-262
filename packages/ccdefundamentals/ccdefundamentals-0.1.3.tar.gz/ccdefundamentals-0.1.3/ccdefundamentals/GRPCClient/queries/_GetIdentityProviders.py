# ruff: noqa: F403, F405, E402
from __future__ import annotations
from ccdefundamentals.GRPCClient.types_pb2 import *
from ccdefundamentals.enums import NET
from ccdefundamentals.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)

from typing import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ccdefundamentals.GRPCClient import GRPCClient
from ccdefundamentals.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def get_identity_providers(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> list[CCD_IpInfo]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        grpc_return_value: Iterator[IpInfo] = self.stub_on_net(
            net, "GetIdentityProviders", blockHashInput
        )

        for ip in list(grpc_return_value):
            result.append(self.convertIpInfo(ip))

        return result

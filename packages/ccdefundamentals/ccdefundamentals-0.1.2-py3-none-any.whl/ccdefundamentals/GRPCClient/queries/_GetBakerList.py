# ruff: noqa: F403, F405, E402
from __future__ import annotations
from ccdefundamentals.GRPCClient.types_pb2 import *
from ccdefundamentals.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from ccdefundamentals.GRPCClient.CCD_Types import *
from ccdefundamentals.enums import NET
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ccdefundamentals.GRPCClient import GRPCClient


class Mixin(_SharedConverters):
    def get_baker_list(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> list[CCD_BakerId]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        grpc_return_value: [BakerId] = self.stub_on_net(
            net, "GetBakerList", blockHashInput
        )
        for baker in list(grpc_return_value):
            result.append(self.convertType(baker))

        return result

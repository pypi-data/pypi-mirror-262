from __future__ import annotations
from sharingiscaring.GRPCClient.types_pb2 import *

# ruff: noqa: F403, F405, E402
from sharingiscaring.enums import NET
from sharingiscaring.GRPCClient.queries._SharedConverters import (
    Mixin as _SharedConverters,
)
from typing import Iterator
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sharingiscaring.GRPCClient import GRPCClient
from sharingiscaring.GRPCClient.CCD_Types import *


class Mixin(_SharedConverters):
    def get_instance_list(
        self: GRPCClient,
        block_hash: str,
        net: Enum = NET.MAINNET,
    ) -> list[ContractAddress]:
        result = []
        blockHashInput = self.generate_block_hash_input_from(block_hash)

        grpc_return_value: Iterator[ContractAddress] = self.stub_on_net(
            net, "GetInstanceList", blockHashInput
        )
        for instance in list(grpc_return_value):
            result.append(self.convertType(instance))

        return result

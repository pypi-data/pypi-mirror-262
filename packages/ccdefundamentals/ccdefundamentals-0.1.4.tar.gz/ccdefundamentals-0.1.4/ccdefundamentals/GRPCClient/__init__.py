# ruff: noqa: F403, F405, E402
from __future__ import annotations
import sys
import os


sys.path.append(os.path.dirname("ccdefundamentals"))
from ccdefundamentals.GRPCClient.service_pb2_grpc import QueriesStub
from ccdefundamentals.env import GRPC_MAINNET, GRPC_TESTNET

from ccdefundamentals.GRPCClient.types_pb2 import *
import grpc
from ccdefundamentals.enums import NET
import sys
import os
from rich.console import Console

console = Console()

HOME_IP = os.environ.get("HOME_IP", "")

from ccdefundamentals.GRPCClient.queries._GetPoolInfo import Mixin as _GetPoolInfo
from ccdefundamentals.GRPCClient.queries._GetPoolDelegatorsRewardPeriod import (
    Mixin as _GetPoolDelegatorsRewardPeriod,
)
from ccdefundamentals.GRPCClient.queries._GetPassiveDelegatorsRewardPeriod import (
    Mixin as _GetPassiveDelegatorsRewardPeriod,
)
from ccdefundamentals.GRPCClient.queries._GetAccountList import Mixin as _GetAccountList
from ccdefundamentals.GRPCClient.queries._GetBakerList import Mixin as _GetBakerList
from ccdefundamentals.GRPCClient.queries._GetBlocksAtHeight import (
    Mixin as _GetBlocksAtHeight,
)
from ccdefundamentals.GRPCClient.queries._GetFinalizedBlocks import (
    Mixin as _GetFinalizedBlocks,
)
from ccdefundamentals.GRPCClient.queries._GetInstanceInfo import (
    Mixin as _GetInstanceInfo,
)
from ccdefundamentals.GRPCClient.queries._GetInstanceList import (
    Mixin as _GetInstanceList,
)
from ccdefundamentals.GRPCClient.queries._GetAnonymityRevokers import (
    Mixin as _GetAnonymityRevokers,
)
from ccdefundamentals.GRPCClient.queries._GetIdentityProviders import (
    Mixin as _GetIdentityProviders,
)
from ccdefundamentals.GRPCClient.queries._GetPoolDelegators import (
    Mixin as _GetPoolDelegators,
)
from ccdefundamentals.GRPCClient.queries._GetPassiveDelegators import (
    Mixin as _GetPassiveDelegators,
)
from ccdefundamentals.GRPCClient.queries._GetAccountInfo import Mixin as _GetAccountInfo
from ccdefundamentals.GRPCClient.queries._GetBlockInfo import Mixin as _GetBlockInfo
from ccdefundamentals.GRPCClient.queries._GetElectionInfo import (
    Mixin as _GetElectionInfo,
)
from ccdefundamentals.GRPCClient.queries._GetTokenomicsInfo import (
    Mixin as _GetTokenomicsInfo,
)
from ccdefundamentals.GRPCClient.queries._GetPassiveDelegationInfo import (
    Mixin as _GetPassiveDelegationInfo,
)
from ccdefundamentals.GRPCClient.queries._GetBlockTransactionEvents import (
    Mixin as _GetBlockTransactionEvents,
)
from ccdefundamentals.GRPCClient.queries._GetBlockSpecialEvents import (
    Mixin as _GetBlockSpecialEvents,
)
from ccdefundamentals.GRPCClient.queries._GetBlockPendingUpdates import (
    Mixin as _GetBlockPendingUpdates,
)
from ccdefundamentals.GRPCClient.queries._GetModuleSource import (
    Mixin as _GetModuleSource,
)
from ccdefundamentals.GRPCClient.queries._GetBlockChainParameters import (
    Mixin as _GetBlockChainParameters,
)
from ccdefundamentals.GRPCClient.queries._InvokeInstance import (
    Mixin as _InvokeInstance,
)
from ccdefundamentals.GRPCClient.queries._GetConsensusInfo import (
    Mixin as _GetConsensusInfo,
)

from ccdefundamentals.GRPCClient.queries._GetBakerEarliestWinTime import (
    Mixin as _GetBakerEarliestWinTime,
)
from ccdefundamentals.GRPCClient.queries._CheckHealth import (
    Mixin as _CheckHealth,
)


class GRPCClient(
    _GetPoolInfo,
    _GetAccountList,
    _GetBakerList,
    _GetInstanceInfo,
    _GetInstanceList,
    _GetFinalizedBlocks,
    _GetBlocksAtHeight,
    _GetIdentityProviders,
    _GetAnonymityRevokers,
    _GetPassiveDelegationInfo,
    _GetPassiveDelegators,
    _GetPoolDelegators,
    _GetPoolDelegatorsRewardPeriod,
    _GetPassiveDelegatorsRewardPeriod,
    _GetAccountInfo,
    _GetBlockInfo,
    _GetElectionInfo,
    _GetBlockTransactionEvents,
    _GetBlockSpecialEvents,
    _GetBlockPendingUpdates,
    _GetTokenomicsInfo,
    _GetModuleSource,
    _GetBlockChainParameters,
    _InvokeInstance,
    _GetConsensusInfo,
    _GetBakerEarliestWinTime,
    _CheckHealth,
):
    def __init__(self, net: str = "mainnet"):
        self.net = NET(net)
        # self.channel_mainnet: grpc.Channel
        # self.channel_testnet: grpc.Channel
        self.stub_mainnet: QueriesStub
        self.stub_testnet: QueriesStub
        # self.stub_to_net: dict[NET:QueriesStub]
        self.host_index = {NET.MAINNET: 0, NET.TESTNET: 0}
        self.hosts = {}
        self.hosts[NET.MAINNET] = GRPC_MAINNET
        self.hosts[NET.TESTNET] = GRPC_TESTNET
        self.connect()

    def connect(self):
        host = self.hosts[NET.MAINNET][self.host_index[NET.MAINNET]]["host"]
        port = self.hosts[NET.MAINNET][self.host_index[NET.MAINNET]]["port"]
        self.channel_mainnet = grpc.insecure_channel(f"{host}:{port}")
        try:
            grpc.channel_ready_future(self.channel_mainnet).result(timeout=1)
            console.log(
                f"GRPCClient for {NET.MAINNET.value} connected on: {host}:{port}"
            )
        except grpc.FutureTimeoutError:
            pass

        host = self.hosts[NET.TESTNET][self.host_index[NET.TESTNET]]["host"]
        port = self.hosts[NET.TESTNET][self.host_index[NET.TESTNET]]["port"]
        self.channel_testnet = grpc.insecure_channel(f"{host}:{port}")
        try:
            grpc.channel_ready_future(self.channel_testnet).result(timeout=1)
            console.log(
                f"GRPCClient for {NET.TESTNET.value} connected on: {host}:{port}"
            )
        except grpc.FutureTimeoutError:
            pass

        self.stub_mainnet = QueriesStub(self.channel_mainnet)
        self.stub_testnet = QueriesStub(self.channel_testnet)

        self.channel = grpc.insecure_channel(
            f"{self.hosts[self.net][self.host_index[self.net]]['host']}:{self.hosts[self.net][self.host_index[self.net]]['port']}"
        )

        self.stub = QueriesStub(self.channel)

    def stub_on_net(self, net, method_name, *args):
        self.check_connection(net)
        stub = self.stub_mainnet if net == NET.MAINNET else self.stub_testnet
        method = getattr(stub, method_name, None)

        if method:
            return method(timeout=30, *args)
        else:
            return None

    def switch_to_net(self, net: str = "mainnet"):
        # only switch when we need to connect to a different net
        if not net:
            net = NET.MAINNET.value

        if net != self.net.value:
            self.net = NET(net)
            self.connect()

    def check_connection(self, net: NET = NET.MAINNET, f=None):
        connected = {NET.MAINNET: False, NET.TESTNET: False}

        while not connected[net]:
            channel_to_check = (
                self.channel_mainnet if net == NET.MAINNET else self.channel_testnet
            )
            try:
                grpc.channel_ready_future(channel_to_check).result(timeout=1)
                connected[net] = True

            except grpc.FutureTimeoutError:
                console.log(
                    f"""GRPCClient for {net.value} Timeout for :
                      {self.hosts[net][self.host_index[net]]['host']}:
                      {self.hosts[net][self.host_index[net]]['port']}"""
                )
                self.host_index[net] += 1
                if self.host_index[net] == len(self.hosts[net]):
                    self.host_index[net] = 0
                self.connect()

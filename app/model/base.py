import struct
from abc import abstractmethod, ABC
from dataclasses import dataclass
from enum import Enum

NULLABLE_STRING = -1
TAG_BUFFER = 0


class KafkaApiKeys(Enum):
    Produce = 0
    Fetch = 1
    ListOffsets = 2
    Metadata = 3
    LeaderAndIsr = 4
    StopReplica = 5
    UpdateMetadata = 6
    ControlledShutdown = 7
    OffsetCommit = 8
    OffsetFetch = 9
    FindCoordinator = 10
    JoinGroup = 11
    Heartbeat = 12
    LeaveGroup = 13
    SyncGroup = 14
    DescribeGroups = 15
    ListGroups = 16
    SaslHandshake = 17
    ApiVersions = 18
    CreateTopics = 19
    DeleteTopics = 20
    DeleteRecords = 21
    InitProducerId = 22
    OffsetForLeaderEpoch = 23
    AddPartitionsToTxn = 24
    AddOffsetsToTxn = 25
    EndTxn = 26
    WriteTxnMarkers = 27
    TxnOffsetCommit = 28
    DescribeAcls = 29
    CreateAcls = 30
    DeleteAcls = 31
    DescribeConfigs = 32
    AlterConfigs = 33
    AlterReplicaLogDirs = 34
    DescribeLogDirs = 35
    SaslAuthenticate = 36
    CreatePartitions = 37
    CreateDelegationToken = 38
    RenewDelegationToken = 39
    ExpireDelegationToken = 40
    DescribeDelegationToken = 41
    DeleteGroups = 42
    ElectLeaders = 43
    IncrementalAlterConfigs = 44
    AlterPartitionReassignments = 45
    ListPartitionReassignments = 46
    OffsetDelete = 47
    DescribeClientQuotas = 48
    AlterClientQuotas = 49
    DescribeUserScramCredentials = 50
    AlterUserScramCredentials = 51
    Vote = 55
    BeginQuorumEpoch = 56
    EndQuorumEpoch = 57
    DescribeQuorum = 58
    AlterPartition = 60
    UpdateFeatures = 61
    Envelope = 62
    DescribeCluster = 64
    DescribeProducers = 65

    @classmethod
    def get_name(cls, api_key):
        return (
            cls(api_key).name
            if api_key in cls._value2member_map_
            else "Unknown API Key"
        )


class Serializer:
    @abstractmethod
    def to_bytes(self) -> bytes:
        pass


class Header(ABC, Serializer):
    @abstractmethod
    def size(self) -> int:
        pass


class Body(ABC, Serializer):
    pass


@dataclass
class RawBody(Body):
    _data: bytes

    def to_bytes(self) -> bytes:
        return self._data


@dataclass
class Message(Serializer):
    header: Header
    body: Body

    STRUCT_FORMAT_MESSAGE_SIZE = "!I"

    def to_bytes(self) -> bytes:
        header_bytes = self.header.to_bytes()
        body_bytes = self.body.to_bytes()
        message_size = len(header_bytes) + len(body_bytes)
        return (
            struct.pack(self.STRUCT_FORMAT_MESSAGE_SIZE, message_size)
            + header_bytes
            + body_bytes
        )

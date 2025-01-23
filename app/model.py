from dataclasses import dataclass


@dataclass
class Header:
    correlation_id: int

@dataclass
class KafkaResponse:
    message_size: int
    header: Header
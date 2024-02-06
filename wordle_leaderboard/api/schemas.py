from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class Thread:
    id: str
    snippet: str
    historyId: str


@dataclass
class Threads:
    resultSizeEstimate: int
    threads: List[Thread] = field(default_factory=list)


@dataclass
class MessagePartBody:
    size: str
    attachmentId: Optional[str] = field(default=None)
    data: Optional[str] = field(default=None)


@dataclass
class Header:
    name: str
    value: str


@dataclass
class MessagePart:
    partId: str
    mimeType: str
    filename: str
    body: MessagePartBody
    parts: List
    headers: List[Header] = field(default_factory=list)

    def __post_init__(self):
        self.headers = [Header(**header) for header in self.headers]
        if self.body:
            self.body = MessagePartBody(**self.body)


@dataclass
class Message:
    id: str
    threadId: str
    labelIds: Optional[List[str]] = field(default_factory=list)
    snippet: Optional[str] = field(default=None)
    historyId: Optional[str] = field(default=None)
    internalDate: Optional[str] = field(default=None)
    payload: Optional[MessagePart] = field(default=None)
    sizeEstimate: Optional[int] = field(default=None)
    raw: Optional[str] = field(default=None)

    def __post_init__(self):
        if self.payload:
            self.payload = MessagePart(**self.payload)


@dataclass
class Messages:
    resultSizeEstimate: Optional[int] = field(default=None)
    messages: List[Message] = field(default_factory=list)

    def __post_init__(self):
        self.messages = [Message(**message) for message in self.messages]

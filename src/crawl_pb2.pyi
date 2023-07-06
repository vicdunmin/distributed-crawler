from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Ack(_message.Message):
    __slots__ = ["content"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: str
    def __init__(self, content: _Optional[str] = ...) -> None: ...

class Comment(_message.Message):
    __slots__ = ["content", "isBad", "sequence", "url", "worker_id"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    ISBAD_FIELD_NUMBER: _ClassVar[int]
    SEQUENCE_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    WORKER_ID_FIELD_NUMBER: _ClassVar[int]
    content: str
    isBad: int
    sequence: int
    url: str
    worker_id: int
    def __init__(self, content: _Optional[str] = ..., sequence: _Optional[int] = ..., url: _Optional[str] = ..., worker_id: _Optional[int] = ..., isBad: _Optional[int] = ...) -> None: ...

class Response(_message.Message):
    __slots__ = ["content", "success"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    SUCCESS_FIELD_NUMBER: _ClassVar[int]
    content: str
    success: int
    def __init__(self, content: _Optional[str] = ..., success: _Optional[int] = ...) -> None: ...

class Task(_message.Message):
    __slots__ = ["timestamp", "url", "username"]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    URL_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    timestamp: str
    url: str
    username: str
    def __init__(self, username: _Optional[str] = ..., url: _Optional[str] = ..., timestamp: _Optional[str] = ...) -> None: ...

class Worker(_message.Message):
    __slots__ = ["number"]
    NUMBER_FIELD_NUMBER: _ClassVar[int]
    number: int
    def __init__(self, number: _Optional[int] = ...) -> None: ...

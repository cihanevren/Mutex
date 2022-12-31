from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class RequestCS(_message.Message):
    __slots__ = ["process_id", "process_timestamp"]
    PROCESS_ID_FIELD_NUMBER: _ClassVar[int]
    PROCESS_TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    process_id: int
    process_timestamp: str
    def __init__(self, process_id: _Optional[int] = ..., process_timestamp: _Optional[str] = ...) -> None: ...

class RequestEnter(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class RequestWrite(_message.Message):
    __slots__ = ["id", "line"]
    ID_FIELD_NUMBER: _ClassVar[int]
    LINE_FIELD_NUMBER: _ClassVar[int]
    id: int
    line: str
    def __init__(self, id: _Optional[int] = ..., line: _Optional[str] = ...) -> None: ...

class ResponseCS(_message.Message):
    __slots__ = ["status"]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    status: str
    def __init__(self, status: _Optional[str] = ...) -> None: ...

class ResponseEnter(_message.Message):
    __slots__ = ["granted"]
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    granted: bool
    def __init__(self, granted: bool = ...) -> None: ...

class ResponseWrite(_message.Message):
    __slots__ = ["granted"]
    GRANTED_FIELD_NUMBER: _ClassVar[int]
    granted: bool
    def __init__(self, granted: bool = ...) -> None: ...

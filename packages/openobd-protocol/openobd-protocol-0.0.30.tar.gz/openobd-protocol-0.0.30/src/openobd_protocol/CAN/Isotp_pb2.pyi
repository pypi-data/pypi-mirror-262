from openobd_protocol import Status_pb2 as _Status_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Padding(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    PADDING_UNDEFINED: _ClassVar[Padding]
    PADDING_ENABLED: _ClassVar[Padding]
    PADDING_DETECTION: _ClassVar[Padding]
    PADDING_DISABLED: _ClassVar[Padding]
    PADDING_SET_FROM_ECU: _ClassVar[Padding]
    PADDING_SET_TOWARDS_ECU: _ClassVar[Padding]
PADDING_UNDEFINED: Padding
PADDING_ENABLED: Padding
PADDING_DETECTION: Padding
PADDING_DISABLED: Padding
PADDING_SET_FROM_ECU: Padding
PADDING_SET_TOWARDS_ECU: Padding

class IsotpMessage(_message.Message):
    __slots__ = ("channel", "payload", "timeout", "ignore_response", "message_status")
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    PAYLOAD_FIELD_NUMBER: _ClassVar[int]
    TIMEOUT_FIELD_NUMBER: _ClassVar[int]
    IGNORE_RESPONSE_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_STATUS_FIELD_NUMBER: _ClassVar[int]
    channel: IsotpChannel
    payload: str
    timeout: int
    ignore_response: bool
    message_status: _Status_pb2.Status
    def __init__(self, channel: _Optional[_Union[IsotpChannel, _Mapping]] = ..., payload: _Optional[str] = ..., timeout: _Optional[int] = ..., ignore_response: bool = ..., message_status: _Optional[_Union[_Status_pb2.Status, _Mapping]] = ...) -> None: ...

class IsotpChannel(_message.Message):
    __slots__ = ("bus_name", "request_id", "response_id", "extended_request_address", "extended_response_address", "padding")
    BUS_NAME_FIELD_NUMBER: _ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: _ClassVar[int]
    RESPONSE_ID_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_REQUEST_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    EXTENDED_RESPONSE_ADDRESS_FIELD_NUMBER: _ClassVar[int]
    PADDING_FIELD_NUMBER: _ClassVar[int]
    bus_name: str
    request_id: int
    response_id: int
    extended_request_address: int
    extended_response_address: int
    padding: Padding
    def __init__(self, bus_name: _Optional[str] = ..., request_id: _Optional[int] = ..., response_id: _Optional[int] = ..., extended_request_address: _Optional[int] = ..., extended_response_address: _Optional[int] = ..., padding: _Optional[_Union[Padding, str]] = ...) -> None: ...

from dataclasses import asdict
from pydantic import BaseModel, TypeAdapter, Field, ConfigDict
from pydantic_core import ValidationError
from typing_extensions import Literal, TypeAlias, Optional, Union
from typing import Any
from fastapi import WebSocket
from json.decoder import JSONDecodeError

ClientTypes: TypeAlias = Literal['nonebot', 'koishi']
class Client(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    type: Optional[ClientTypes] = None
    mid: str
    ws: WebSocket

    closed: bool = False

class NonebotClient(Client):
    type: ClientTypes = 'nonebot'

class KoishiClient(Client):
    type: ClientTypes = 'koishi'

ActionTypes: TypeAlias = Optional[Literal['handshake', 'send/private', 'send/group', 'send/channel', 'debug/test']]
class ClientPackage(BaseModel):
    action: ActionTypes = None  # None is unkonwn
    data: Any = None

class HandshakeData(BaseModel):
    type: ClientTypes
    mid: str  # 设备 ID

class HandshakePackage(ClientPackage):
    action: ActionTypes = 'handshake'
    data: HandshakeData

class TestPackage(ClientPackage):
    action: ActionTypes = 'debug/test'

ClientPackageTypes: TypeAlias = Union[HandshakePackage, TestPackage]
def dict2pkg(received: dict):
    return TypeAdapter(ClientPackageTypes).validate_python(received)

ClientClassTypes: TypeAlias = Union[NonebotClient, KoishiClient]
def create_client(ws: WebSocket):
    pass
    # return TypeAdapter(ClientClassTypes).validate_python(unpacked)

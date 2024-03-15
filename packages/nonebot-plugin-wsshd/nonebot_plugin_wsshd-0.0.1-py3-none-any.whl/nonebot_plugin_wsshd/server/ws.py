__fastapi_entry__ = 'ws'
from dataclasses import asdict
from json.decoder import JSONDecodeError

from pydantic_core import ValidationError
from nonebot import logger
from nonebot.exception import MatcherException

from fastapi import APIRouter, Depends, Request, WebSocket

from typing_extensions import Any

from . import app
from .client import Client, dict2pkg, HandshakePackage, create_client

async def permissonChecker():
    pass

ws = APIRouter(prefix='/ws', tags=['ws', 'websocket'], dependencies=(Depends(permissonChecker, use_cache=False), ))

@ws.websocket('/')
async def ws_main(ws: WebSocket):
    await ws.accept()

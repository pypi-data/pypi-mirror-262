import importlib
from pathlib import Path
from typing import Optional

from nonebot import get_app, get_asgi
from nonebot.utils import path_to_module_name
from fastapi import FastAPI, APIRouter

app: FastAPI = get_app()

root_apirouter = APIRouter(prefix='/wsshd', tags=['wsshd'])
# 动态引入 core/server 下所有文件并添加 router
for file in Path(__file__).parent.iterdir():
    if not file.is_file():
        continue

    if file.suffix.lower() != '.py':
        continue
    
    if file == Path(__file__):
        continue

    api_module = importlib.import_module(path_to_module_name(file))
    router_name: str = (
        'router'
        if not hasattr(api_module, '__fastapi_entry__') or not issubclass(type(api_module.__fastapi_entry__), str) else
        api_module.__fastapi_entry__
    )

    api_router: Optional[APIRouter] = getattr(api_module, router_name, None)
    if not isinstance(api_router, APIRouter):
        continue

    root_apirouter.include_router(api_router)

app.include_router(root_apirouter)

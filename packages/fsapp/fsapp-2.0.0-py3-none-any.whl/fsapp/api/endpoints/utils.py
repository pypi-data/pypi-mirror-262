import structlog
from datetime import datetime
from typing import Union
from fastapi import Request
from fsapp.core.config import settings


def make_response(success_mark: bool, data: Union[dict, str]) -> dict:
    """
    Создание универсального ответа на запросы
    """
    return {
        "instance": settings.required.instance,
        "ts": datetime.now().timestamp(),
        "result": success_mark,
        "data": data
    }


async def get_request_body(request: Request) -> bytes:
    body = await request.body()
    return body


async def logging_middleware(request: Request):
    structlog.contextvars.clear_contextvars()
    body = await get_request_body(request=request)
    body_str = body.decode() if body else None
    request_logger_body = {
        'body': body_str,
        'method': request.method,
        'url': request.url.path,
    }
    structlog.contextvars.bind_contextvars(
        service=settings.required.instance.lower(),
        request=request_logger_body,
    )

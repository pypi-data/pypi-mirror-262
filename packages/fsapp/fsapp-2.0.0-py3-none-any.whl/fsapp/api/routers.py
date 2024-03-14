"""Подключаем все маршруты в один объект"""

from fastapi import APIRouter
from fsapp.api.endpoints import search
from fsapp.api.endpoints import auth

api_router = APIRouter()

api_router.include_router(search.router, tags=['SearchRoute'])
api_router.include_router(auth.router, tags=['Auth'])

__all__ = ["api_router"]

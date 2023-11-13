from typing import Any, Awaitable, Callable, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import Message
from loguru import logger

from src.dto import Student
from src.messages import ALREADY_HEADMAN_MESSAGE, MUST_BE_HEADMEN_MESSAGE

HandlerType: TypeAlias = Callable[[Message, dict[str, Any]], Awaitable[Any]]

__all__ = [
    "CheckHeadmanMiddleware",
]


class CheckHeadmanMiddleware(BaseMiddleware):
    _must_be_headman: bool

    def __init__(self, must_be_headman: bool) -> None:
        self._must_be_headman = must_be_headman
        super().__init__()

    @logger.catch
    async def __call__(self, handler: HandlerType, event: Message, data: dict[str, Any]) -> Any:
        student: Student = data["student"]

        if student.is_headman != self._must_be_headman and self._must_be_headman:
            await event.reply(MUST_BE_HEADMEN_MESSAGE)
            logger.trace("headmen commands middleware finished, user must me headman to use this command")
            return

        if student.is_headman != self._must_be_headman and not self._must_be_headman:
            await event.reply(ALREADY_HEADMAN_MESSAGE)
            logger.trace("headmen reg middleware finished, already registered as headmen")
            return

        logger.info("headman commands middleware finished")
        return await handler(event, data)

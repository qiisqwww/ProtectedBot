from collections.abc import Awaitable, Callable
from datetime import UTC, date, datetime, timedelta
from typing import Any, TypeAlias

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, TelegramObject
from loguru import logger

from src.dto.models import Student
from src.repositories.impls import (
    GroupRepositoryImpl,
    LessonRepositoryImpl,
    UniversityRepositoryImpl,
)
from src.resources import (
    YOU_CAN_NOT_ANSWER_DAY_TEMPLATE,
    YOU_CAN_NOT_ANSWER_TIME_TEMPLATE,
)
from src.services.impls import (
    GroupServiceImpl,
    LessonServiceImpl,
    UniversityServiceImpl,
)

__all__ = [
    "CheckInMiddleware",
]


HandlerType: TypeAlias = Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]]


class CheckInMiddleware(BaseMiddleware):
    async def __call__(self, handler: HandlerType, event: CallbackQuery, data: dict[str, Any]) -> Any:
        logger.info("callback middleware started")

        if event.message is None:
            return None

        logger.info(f"EVENT TYPE={type(event)}")
        student: Student = data["student"]
        lesson_len = timedelta(hours=1, minutes=30)
        now = datetime.now(tz=UTC)

        if data["callback_data"].day_of_poll != date.today():
            await event.message.edit_text(YOU_CAN_NOT_ANSWER_DAY_TEMPLATE)

        lesson_service = LessonServiceImpl(
            LessonRepositoryImpl(data["postgres_con"]),
            GroupServiceImpl(GroupRepositoryImpl(data["postgres_con"])),
            UniversityServiceImpl(UniversityRepositoryImpl(data["postgres_con"])),
        )
        today_lessons = await lesson_service.filter_by_group_id(student.group_id)

        first_lesson_time = datetime.combine(datetime.today(), today_lessons[0].start_time)

        if now > first_lesson_time + lesson_len:
            logger.info("(poll) callback middleware finished, lesson was already started")
            await event.message.edit_text(YOU_CAN_NOT_ANSWER_TIME_TEMPLATE)
            return None

        return await handler(event, data)

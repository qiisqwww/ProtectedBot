from aiogram.types import Message

from src.bot.common import RootRouter, Router
from src.bot.common.command_filter import CommandFilter, TelegramCommand
from src.bot.common.resources import main_menu
from src.modules.attendance.application.queries import GetTodayScheduleQuery
from src.modules.student_management.domain import Role, Student

from .resources.inline_buttons import choose_lesson_buttons
from .resources.templates import (
    CHOOSE_PAIR_TEMPLATE,
    NO_LESSONS_TODAY_TEMPLATE,
    WHICH_PAIR_TEMPLATE,
)

__all__ = [
    "include_get_attendance_command",
]


get_attendance_command_router = Router(
    must_be_registered=True,
    minimum_role=Role.VICE_HEADMAN,
)


def include_get_attendance_command(root_router: RootRouter) -> None:
    root_router.include_router(get_attendance_command_router)


@get_attendance_command_router.message(CommandFilter(TelegramCommand.GET_ATTENDANCE))
async def get_attendance_command(
    message: Message, student: Student, get_today_schedule_query: GetTodayScheduleQuery
) -> None:
    schedule = await get_today_schedule_query.execute(student.group_id)

    if not schedule:
        await message.answer(NO_LESSONS_TODAY_TEMPLATE)
        return

    await message.answer(CHOOSE_PAIR_TEMPLATE, reply_markup=main_menu(student.role))
    await message.answer(WHICH_PAIR_TEMPLATE, reply_markup=choose_lesson_buttons(schedule))

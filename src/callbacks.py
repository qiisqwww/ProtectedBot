import logging

from aiogram import F, Router, types
from aiogram.enums import ParseMode

from .buttons import load_attendance_kb, load_choose_lesson_kb, load_void_kb
from .dto import Lesson
from .messages import ALL_MESSAGE, NONE_MESSAGE, attendance_for_headmen_message
from .middlewares import CallbackMiddleware
from .mirea_api import MireaScheduleApi
from .services import UsersService

__all__ = [
    "callback_router",
]


callback_router = Router()
callback_router.callback_query.middleware(CallbackMiddleware())
api = MireaScheduleApi()


@callback_router.callback_query(F.data.startswith("attendance"), flags={"callback": "poll"})
async def check_in_callback(callback: types.CallbackQuery):
    callback_data = callback.data.split("_")[1]

    with UsersService() as con:
        if callback_data == "all":
            con.change_attendance(callback.from_user.id, callback_data + " 0")
            await callback.message.edit_text(ALL_MESSAGE, reply_markup=load_void_kb())
            return

        if callback_data == "none":
            con.change_attendance(callback.from_user.id, callback_data + " 0")
            await callback.message.edit_text(NONE_MESSAGE, reply_markup=load_void_kb())
            return

        data = Lesson.from_str(callback_data)

        group = con.get_group_of_id_tg(callback.from_user.id)
        lessons = await api.get_schedule(group)

        lessons_in_states = con.get_lessons(callback.from_user.id)
        already_chosen_lessons_in_numbers = []

        for idx, lesson in enumerate(lessons):
            if lesson == data:
                chosen_lesson = idx
                already_chosen_lessons_in_numbers.append(idx)
            if lessons_in_states[idx] == "1":
                already_chosen_lessons_in_numbers.append(idx)

        for i in sorted(already_chosen_lessons_in_numbers, reverse=True):
            lessons.pop(i)

        info = f"lesson {str(chosen_lesson)}"
        logging.info("commiting try")
        con.change_attendance(callback.from_user.id, info)

        await callback.message.edit_text(
            f"Вы посетите пару {data.discipline}, которая начнётся в {data.start_time}",
            reply_markup=load_attendance_kb(lessons),
        )


@callback_router.callback_query(flags={"callback": "attendance"})
async def attendance_send_callback(callback: types.CallbackQuery):
    logging.info("attendance callback handled")

    with UsersService() as con:
        group = con.get_group_of_id_tg(callback.from_user.id)
        lessons = await api.get_schedule(group)

        lesson = lessons[int(callback.data)]

        await callback.message.edit_text(
            text=f"{lesson.discipline}, {lesson.start_time}\n\n" + attendance_for_headmen_message(callback),
            reply_markup=load_choose_lesson_kb(lessons),
            parse_mode=ParseMode.HTML,
        )

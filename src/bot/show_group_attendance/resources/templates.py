from jinja2 import Template

from src.bot.common.convert_time import convert_time_from_utc
from src.modules.attendance.domain import (
    Lesson,
    LessonAttendanceForGroup,
)
from src.modules.attendance.domain.enums.visit_status import VisitStatus

__all__ = [
    "ALL_PAIRS_TEMPLATE",
    "NO_PAIRS_TEMPLATE",
    "NO_LESSONS_TODAY_TEMPLATE",
    "CHOOSE_PAIR_TEMPLATE",
    "WHICH_PAIR_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_TIME_TEMPLATE",
    "YOU_CAN_NOT_ANSWER_DAY_TEMPLATE",
    "attendance_for_headmen_template",
]

WHICH_PAIR_TEMPLATE = """
Какая пара вас интересует?"""

YOU_CAN_NOT_ANSWER_TIME_TEMPLATE = """
Вы не можете отметиться! Занятия уже начались!"""

YOU_CAN_NOT_ANSWER_DAY_TEMPLATE = """
Вы не можете отметиться за другой день!"""

ALL_PAIRS_TEMPLATE = """
Вы посетите все пары"""

NO_PAIRS_TEMPLATE = """
Вы не посетите пары """

NO_LESSONS_TODAY_TEMPLATE = """
Сегодня нет пар!"""

CHOOSE_PAIR_TEMPLATE = """
Выберите пару из списка:"""


def attendance_for_headmen_template(choosen_lesson: Lesson, group_attendance: LessonAttendanceForGroup, timezone: str) -> str:
    start_time = convert_time_from_utc(choosen_lesson.start_time, timezone)
    not_noted_count = len(tuple(filter(lambda student: not student.is_checked_in_today, group_attendance.attendance[VisitStatus.ABSENT])))
    template: str = Template(
        """{{lesson.name}} {{start_time.strftime('%H:%M')}}

Не отметились:
{% if not_noted_count > 0 -%}
    {% for student in group_attendance.attendance[VisitStatus.ABSENT] -%}
        {% if not student.is_checked_in_today -%}
            <a href="tg://user?id={{ student.telegram_id }}">{{ student.last_name }} {{ student.first_name }}</a>\n
        {%- endif %}
    {%- endfor %}
{% endif %}
Придут:
{% if group_attendance.attendance[VisitStatus.PRESENT]|length > 0 -%}
    {% for student in group_attendance.attendance[VisitStatus.PRESENT] -%}
        <a href="tg://user?id={{ student.telegram_id }}">{{ student.last_name }} {{ student.first_name }}</a>
    {%- endfor %}
{% endif %}
Не придут:
{% if group_attendance.attendance[VisitStatus.ABSENT]|length > 0 -%}
    {% for student in group_attendance.attendance[VisitStatus.ABSENT] -%}
        {% if student.is_checked_in_today -%}
            <a href="tg://user?id={{ student.telegram_id }}">{{ student.last_name }} {{ student.first_name }}</a>\n
        {%- endif %}
    {%- endfor %}
{% endif %}
Что-то еще?""",
        autoescape=True,
    ).render(start_time=start_time, group_attendance=group_attendance, lesson=choosen_lesson, VisitStatus=VisitStatus, not_noted_count=not_noted_count)

    return template

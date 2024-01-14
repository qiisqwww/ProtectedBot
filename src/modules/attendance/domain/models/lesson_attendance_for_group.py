from dataclasses import dataclass

from ..enums import VisitStatus
from .student_info import StudentInfo

__all__ = [
    "LessonAttendanceForGroup",
]


@dataclass(frozen=True, slots=True)
class LessonAttendanceForGroup:
    group_id: int
    lesson_id: int
    attendance: dict[VisitStatus, list[StudentInfo]]

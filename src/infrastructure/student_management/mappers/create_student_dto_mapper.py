from dataclasses import asdict
from datetime import date
from typing import Mapping

from src.application.student_management.repositories import CreateStudentDTO
from src.domain.edu_info import UniversityAlias
from src.domain.student_management import Role

__all__ = [
    "CreateStudentDTOMapper",
]


class CreateStudentDTOMapper:
    def to_redis_dict(self, data: CreateStudentDTO) -> Mapping:
        result = asdict(data)

        birthdate: None | date = result["birthdate"]
        result["birthdate"] = "0" if birthdate is None else birthdate.isoformat()
        result["telegram_id"] = str(result["telegram_id"])

        return result

    def from_redis_dict(self, data: Mapping) -> CreateStudentDTO:
        birthdate = None if data["birthdate"] == "0" == None else date.fromisoformat(data["birthdate"])

        return CreateStudentDTO(
            telegram_id=int(data["birthdate"]),
            name=data["name"],
            surname=data["surname"],
            birthdate=birthdate,
            role=Role(data["role"]),
            university_alias=UniversityAlias(data["university_alias"]),
            group_name=data["group_name"],
        )

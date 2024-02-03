from injector import inject

from src.modules.common.application import UseCase

from ...domain import StudentInfo
from ..repositories import StudentInfoRepository

__all__ = [
    "GetStudentsInfoFromGroupQuery",
]


class GetStudentsInfoFromGroupQuery(UseCase):
    _repository: StudentInfoRepository

    @inject
    def __init__(self, repository: StudentInfoRepository) -> None:
        self._repository = repository

    async def execute(self, group_id: int) -> list[StudentInfo]:
        return await self._repository.filter_by_group_id(group_id)

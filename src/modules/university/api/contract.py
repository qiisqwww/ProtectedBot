from src.modules.university.api.dto import University
from src.modules.university.api.enums import UniversityAlias
from src.modules.university.internal.services import UniversityService
from src.shared.services import PostgresService

__all__ = [
    "UniversityService",
]


class UniversityContract(PostgresService):
    async def find_university_by_alias(self, alias: UniversityAlias) -> University:
        university_service = UniversityService(self._con)
        return await university_service.find_by_alias(alias)

    async def get_all_universities(self) -> list[University]:
        university_service = UniversityService(self._con)
        return await university_service.all()

    async def add_universities(self) -> None:
        university_service = UniversityService(self._con)
        return await university_service.add_universities()

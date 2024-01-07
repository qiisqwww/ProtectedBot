from typing import final

from src.modules.common.domain.university_alias import UniversityAlias
from src.modules.common.infrastructure.persistence.postgres_repository import (
    PostgresRepositoryImpl,
)
from src.modules.edu_info.application.repositories.group_repository import (
    GroupRepository,
)
from src.modules.edu_info.domain.models.group import Group

__all__ = [
    "GroupRepositoryImpl",
]


@final
class GroupRepositoryImpl(PostgresRepositoryImpl, GroupRepository):
    async def find_by_name_and_uni(self, name: str, university_alias: UniversityAlias) -> Group | None:
        query = (
            "SELECT gr.id, gr.name, gr.university_id "
            "FROM groups gr "
            "JOIN universities AS un "
            "ON gr.university_id = un.id "
            "WHERE gr.name LIKE $1 AND un.alias = $2"
        )

        record = await self._con.fetchrow(query, name, university_alias)

        if record is None:
            return None

        return Group(
            id=record["id"],
            name=record["name"],
            university_id=record["university_id"],
        )

    async def find_by_id(self, group_id: int) -> Group | None:
        query = "SELECT * FROM groups WHERE id = $1"
        record = await self._con.fetchrow(query, group_id)

        if record is None:
            return None

        return Group(
            id=record["id"],
            name=record["name"],
            university_id=record["university_id"],
        )

    async def create(self, name: str, university_id: int) -> Group:
        query = "INSERT INTO groups (name, university_id) VALUES ($1, $2) RETURNING id"
        pk = await self._con.fetchval(query, name, university_id)

        return Group(
            id=pk,
            name=name,
            university_id=university_id,
        )

    async def find_by_name(self, name: str) -> Group | None:
        query = "SELECT * FROM groups WHERE name LIKE $1"
        record = await self._con.fetchrow(query, name)

        if record is None:
            return None

        return Group(
            id=record["id"],
            name=record["name"],
            university_id=record["university_id"],
        )

    #
    #
    # async def all(self) -> list[Group]:
    #     query = "SELECT * FROM groups"
    #     records = await self._con.fetch(query)
    #
    #     if records is None:
    #         raise CorruptedDatabaseError("There are no groups in table")
    #
    #     return [Group.from_mapping(record) for record in records]
    #

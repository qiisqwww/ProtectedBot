from redis.asyncio import Redis  # type: ignore

__all__ = [
    "ThrottlingService",
]


class RedisService:
    _con: Redis

    def __init__(self, con: Redis) -> None:
        self._con = con


class ThrottlingService(RedisService):
    async def set_user_throttling(self, user_id: str) -> None:
        await self._con.set(f"thr{user_id}", 0, ex=60)

    async def increase_user_throttling(self, user_id: str) -> None:
        await self._con.incr(f"thr{user_id}")

    async def get_user_throttling(self, user_id: str) -> int | None:
        return await self._con.get(f"thr{user_id}")

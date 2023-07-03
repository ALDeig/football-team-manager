from collections.abc import Sequence
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db.tables import Player 


async def add_player(session: AsyncSession, name: str, level: float):
    player = Player(name=name, level=level)
    session.add(player)
    await session.commit()


async def delete_player(session: AsyncSession, name: str):
    await session.execute(sa.delete(Player).where(Player.name == name))
    await session.commit()


async def get_players(session: AsyncSession) -> Sequence[Player]:
    players = await session.scalars(sa.select(Player))
    return players.all()


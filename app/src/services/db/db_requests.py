from collections.abc import Sequence
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from app.src.services.db.tables import Player 


async def add_player(session: AsyncSession, name: str, level: float):
    player_id = uuid4()
    player = Player(id=str(player_id), name=name, level=level)
    session.add(player)
    await session.commit()


async def delete_player(session: AsyncSession, player_id: str):
    await session.execute(sa.delete(Player).where(Player.id == player_id))
    await session.commit()


async def get_players(session: AsyncSession) -> Sequence[Player]:
    players = await session.scalars(sa.select(Player))
    return players.all()


async def update_player(session: AsyncSession, player_id: str, update_fields: dict):
    stmt = (
        sa.update(Player).
        where(Player.id == player_id).
        values(**update_fields)
    )
    await session.execute(stmt)
    await session.commit()

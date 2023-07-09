from collections import defaultdict
from random import randint, shuffle

from aiogram.types import InlineKeyboardMarkup
from app.src.dialogs.keyboards.user import kb_after_created_teams

from app.src.services.db.tables import Player


def get_response_to_creatation_team_request(
        user_id: int,
        players: list[Player],
        selected_players: list[str]) -> tuple[str, str, InlineKeyboardMarkup]:
    team_1, team_2 = create_teams(players, selected_players)
    text_team_1 = create_team_text(1, team_1, "hide")
    text_team_2 = create_team_text(2, team_2, "hide")
    kb = kb_after_created_teams(user_id, "hide")
    return text_team_1, text_team_2, kb


def create_teams(
        players: list[Player],
        selected_players: list[str]) -> tuple[dict[str, float], dict[str, float]]:
    players_dict = {}
    for player_id in selected_players:
        player, = (a for a in players if a.id == player_id)
        players_dict[player.name] = player.level

    team_1, team_2 = _form_teams(players_dict)
    return team_1, team_2


def create_team_text(team_number: int, team: dict[str, float], action: str) -> str:
    text = f"Команда {team_number}\nКоличество игроков: {len(team)}\n\n"
    if action == "show":
        text += f"Уровень - {sum(level for level in team.values())}\n\n"
    for player_name, level in team.items():
        player_text = f"<b>{player_name}</b>" 
        if action == "show":
            player_text += f" - {level}\n"
        else:
            player_text += "\n"
        text += player_text
    return text


def _form_teams(players: dict[str, float]) -> tuple[dict[str, float], dict[str, float]]:
    team_1 = []
    team_2 = []
    players_by_levels = defaultdict(list)
    for name, level in players.items():
        players_by_levels[level].append(name)
    levels = sorted(players_by_levels, reverse=True)
    for level in levels:
        players_by_level = players_by_levels[level]
        for _ in range(len(players_by_level)):
            selected_player = players_by_level.pop(randint(0, len(players_by_level) - 1))
            _append_player_in_team(team_1, team_2, players, selected_player)
    shuffle(team_1)
    shuffle(team_2)
    team_1 = {name: players[name] for name in team_1}
    team_2 = {name: players[name] for name in team_2}
    return team_1, team_2


def _append_player_in_team(
        team_1: list[str],
        team_2: list[str],
        players: dict[str, float],
        player: str) -> None:
    team_1_level = sum(players[player] for player in team_1)
    team_2_level = sum(players[player] for player in team_2)
    if team_1_level < team_2_level:
        team_1.append(player)
    else:
        team_2.append(player)

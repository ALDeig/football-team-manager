from collections import defaultdict
from random import randint, shuffle

from app.src.services.db.tables import Player


def create_teams(players: list[Player], selected_players: list[str]) -> tuple[str, str]:
    players_dict = {}
    for player_id in selected_players:
        player, = (a for a in players if a.id == player_id)
        players_dict[player.name] = player.level

    team_1, team_2 = _form_teams(players_dict)
    text_1 = _create_text(1, team_1)
    text_2 = _create_text(2, team_2)
    return text_1, text_2


def _create_text(team_number: int, team: list[str]) -> str:
    text = f"Команда {team_number}\nКоличество игроков: {len(team)}\n\n"
    for player_name in team:
        text += f"<b>{player_name}</b>\n"
    return text


def _form_teams(players: dict[str, float]) -> tuple[list[str], list[str]]:
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

from collections import defaultdict
from random import randint, shuffle

from app.src.services.db.tables import Player


def create_teams(
    num_of_teams: int, players: list[Player], selected_players_id: list[str]
) -> list[dict[str, float]]:
    players_dict = {}
    for player_id in selected_players_id:
        (player,) = (a for a in players if a.id == player_id)
        players_dict[player.name] = player.level
    players_by_levels = defaultdict(list)
    for name, level in players_dict.items():
        players_by_levels[level].append(name)
    teams = _form_teams(num_of_teams, players_dict)
    return teams


def _form_teams(num_of_teams: int, players: dict[str, float]) -> list[dict[str, float]]:
    teams = [[] for _ in range(num_of_teams)]
    players_by_levels = defaultdict(list)
    for name, level in players.items():
        players_by_levels[level].append(name)
    levels = sorted(players_by_levels, reverse=True)
    for level in levels:
        players_by_level = players_by_levels[level]
        for _ in range(len(players_by_level)):
            selected_player = players_by_level.pop(
                randint(0, len(players_by_level) - 1)
            )
            _append_player_in_team(teams, players, selected_player)
    for team in teams:
        shuffle(team)
    teams_with_level = [{name: players[name] for name in team} for team in teams]
    return teams_with_level


def _append_player_in_team(
    teams: list[list[str]], players: dict[str, float], player: str
) -> None:
    teams_level = []
    for team in teams:
        teams_level.append(sum(players[player] for player in team))
    min_level = min(teams_level)
    teams[teams_level.index(min_level)].append(player)


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

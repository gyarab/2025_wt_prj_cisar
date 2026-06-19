from ninja import NinjaAPI
from django.shortcuts import get_object_or_404
from typing import List
from .models import Team, Player, Match, Statistics
from .schemas import (
    TeamSchema, TeamCreateSchema,
    PlayerSchema, PlayerCreateSchema,
    MatchSchema, MatchCreateSchema,
    StatisticsSchema, StatisticsCreateSchema,
)

api = NinjaAPI()


# --- TEAMS ---

@api.get("/teams/", response=List[TeamSchema])
def list_teams(request):
    return Team.objects.all()


@api.get("/teams/{team_id}/", response=TeamSchema)
def get_team(request, team_id: int):
    return get_object_or_404(Team, id=team_id)


@api.post("/teams/", response=TeamSchema)
def create_team(request, payload: TeamCreateSchema):
    return Team.objects.create(**payload.dict())


@api.put("/teams/{team_id}/", response=TeamSchema)
def update_team(request, team_id: int, payload: TeamCreateSchema):
    team = get_object_or_404(Team, id=team_id)
    for k, v in payload.dict().items():
        setattr(team, k, v)
    team.save()
    return team


@api.delete("/teams/{team_id}/")
def delete_team(request, team_id: int):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return {"success": True}


# --- PLAYERS ---

@api.get("/players/", response=List[PlayerSchema])
def list_players(request, team_id: int = None):
    qs = Player.objects.select_related("team").all()
    if team_id:
        qs = qs.filter(team_id=team_id)
    return qs


@api.get("/players/{player_id}/", response=PlayerSchema)
def get_player(request, player_id: int):
    return get_object_or_404(Player.objects.select_related("team"), id=player_id)


@api.post("/players/", response=PlayerSchema)
def create_player(request, payload: PlayerCreateSchema):
    return Player.objects.create(**payload.dict())


@api.put("/players/{player_id}/", response=PlayerSchema)
def update_player(request, player_id: int, payload: PlayerCreateSchema):
    player = get_object_or_404(Player, id=player_id)
    for k, v in payload.dict().items():
        setattr(player, k, v)
    player.save()
    return player


@api.delete("/players/{player_id}/")
def delete_player(request, player_id: int):
    player = get_object_or_404(Player, id=player_id)
    player.delete()
    return {"success": True}


# --- MATCHES ---

@api.get("/matches/", response=List[MatchSchema])
def list_matches(request, team_id: int = None):
    qs = Match.objects.select_related("home_team", "away_team").order_by("-date")
    if team_id:
        qs = qs.filter(home_team_id=team_id) | qs.filter(away_team_id=team_id)
        qs = qs.order_by("-date")
    return qs


@api.get("/matches/{match_id}/", response=MatchSchema)
def get_match(request, match_id: int):
    return get_object_or_404(Match.objects.select_related("home_team", "away_team"), id=match_id)


@api.post("/matches/", response=MatchSchema)
def create_match(request, payload: MatchCreateSchema):
    return Match.objects.create(**payload.dict())


@api.put("/matches/{match_id}/", response=MatchSchema)
def update_match(request, match_id: int, payload: MatchCreateSchema):
    match = get_object_or_404(Match, id=match_id)
    for k, v in payload.dict().items():
        setattr(match, k, v)
    match.save()
    return match


@api.delete("/matches/{match_id}/")
def delete_match(request, match_id: int):
    match = get_object_or_404(Match, id=match_id)
    match.delete()
    return {"success": True}


# --- STATISTICS ---

@api.get("/statistics/", response=List[StatisticsSchema])
def list_statistics(request, match_id: int = None, player_id: int = None):
    qs = Statistics.objects.select_related("player", "match")
    if match_id:
        qs = qs.filter(match_id=match_id)
    if player_id:
        qs = qs.filter(player_id=player_id)
    return qs


@api.get("/statistics/player/{player_id}/", response=List[StatisticsSchema])
def player_statistics(request, player_id: int):
    return Statistics.objects.select_related("player", "match").filter(player_id=player_id)


@api.post("/statistics/", response=StatisticsSchema)
def create_statistics(request, payload: StatisticsCreateSchema):
    return Statistics.objects.create(**payload.dict())
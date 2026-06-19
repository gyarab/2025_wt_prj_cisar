from ninja import Schema
from typing import Optional
from datetime import datetime


class TeamSchema(Schema):
    id: int
    name: str
    stadium: str
    colours: str
    founded_year: int


class TeamCreateSchema(Schema):
    name: str
    stadium: str
    colours: str
    founded_year: int


class PlayerSchema(Schema):
    id: int
    name: str
    age: int
    position: str
    number: int
    team_id: int
    team_name: Optional[str] = None

    @staticmethod
    def resolve_team_name(obj):
        return obj.team.name if obj.team else None


class PlayerCreateSchema(Schema):
    name: str
    age: int
    position: str
    number: int
    team_id: int


class MatchSchema(Schema):
    id: int
    home_team_id: int
    home_team_name: Optional[str] = None
    away_team_id: int
    away_team_name: Optional[str] = None
    score_home: int
    score_away: int
    date: datetime
    stadium: str

    @staticmethod
    def resolve_home_team_name(obj):
        return obj.home_team.name if obj.home_team else None

    @staticmethod
    def resolve_away_team_name(obj):
        return obj.away_team.name if obj.away_team else None


class MatchCreateSchema(Schema):
    home_team_id: int
    away_team_id: int
    score_home: int
    score_away: int
    date: datetime
    stadium: str


class StatisticsSchema(Schema):
    id: int
    player_id: int
    player_name: Optional[str] = None
    player_number: Optional[int] = None
    player_position: Optional[str] = None
    match_id: int
    goals: int
    assists: int
    penalty_minutes: int

    @staticmethod
    def resolve_player_name(obj):
        return obj.player.name if obj.player else None

    @staticmethod
    def resolve_player_number(obj):
        return obj.player.number if obj.player else None

    @staticmethod
    def resolve_player_position(obj):
        return obj.player.position if obj.player else None


class StatisticsCreateSchema(Schema):
    player_id: int
    match_id: int
    goals: int
    assists: int
    penalty_minutes: int

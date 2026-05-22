from ninja import NinjaAPI
from django.shortcuts import get_object_or_404

from ..app.models import Player, Team
from ..app.schemas import PlayerSchema, PlayerCreateSchema

api = NinjaAPI()



@api.get("/player", response=list[PlayerSchema])
def player_list(request):
    return Player.objects.all()



@api.get("/player/{player_id}", response=PlayerSchema)
def player_detail(request, player_id: int):
    player = get_object_or_404(Player, id=player_id)
    return player



@api.post("/player", response=PlayerSchema)
def create_player(request, data: PlayerCreateSchema):

    team = get_object_or_404(Team, id=data.team_id)

    player = Player.objects.create(
        name=data.name,
        age=data.age,
        position=data.position,
        number=data.number,
        team=team
    )

    return player



@api.put("/player/{player_id}", response=PlayerSchema)
def update_player(request, player_id: int, data: PlayerCreateSchema):

    player = get_object_or_404(Player, id=player_id)
    team = get_object_or_404(Team, id=data.team_id)

    player.name = data.name
    player.age = data.age
    player.position = data.position
    player.number = data.number
    player.team = team

    player.save()

    return player
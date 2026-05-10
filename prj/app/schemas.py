from ninja import Schema


class PlayerSchema(Schema):
    id: int
    name: str
    age: int
    position: str
    number: int


class PlayerCreateSchema(Schema):
    name: str
    age: int
    position: str
    number: int
    team_id: int
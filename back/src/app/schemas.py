from datetime import datetime
from pydantic import BaseModel


class GameState(BaseModel):
    """gamestate schemas"""
    board: list[list[int]]
    current_player: int
    winner: str


class PlayerCreate(BaseModel):
    pseudo: str


class PlayerResponse(BaseModel):
    id: int
    pseudo: str

    class Config:
        orm_mode = True


class GameHistoryCreate(BaseModel):
    player_id: int
    opponent: str
    winner: int


class GameHistoryResponse(BaseModel):
    id: int
    player_id: int
    opponent: str
    winner: int
    date_played: datetime

    class Config:
        orm_mode = True

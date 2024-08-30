from datetime import datetime
from pydantic import BaseModel


class GameState(BaseModel):
    """gamestate schemas"""
    board: list[list[int]]
    current_player: int
    player1: str
    player2: str
    winner: str
    pieces: int


class PlayerCreate(BaseModel):
    player1: str
    player2: str


class PlayerResponse(BaseModel):
    id: int
    pseudo: str

    class Config:
        orm_mode = True


class GameHistoryCreate(BaseModel):
    winner: str
    loser: str
    pieces: int


class GameHistoryResponse(BaseModel):
    id: int
    winner: str
    loser: str
    pieces: int
    date_played: datetime

    class Config:
        orm_mode = True

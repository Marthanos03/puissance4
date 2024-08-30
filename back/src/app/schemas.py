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
    """To create a player"""
    player1: str
    player2: str


class GameHistoryCreate(BaseModel):
    """To add a game to the history"""
    winner: str
    loser: str
    pieces: int


class GameHistoryResponse(BaseModel):
    """Response after adding a game to the history"""
    id: int
    winner: str
    loser: str
    pieces: int
    date_played: datetime

    class Config:
        orm_mode = True

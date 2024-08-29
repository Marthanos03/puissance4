import json
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


Base = declarative_base()


class GameStateDB(Base):
    __tablename__ = "gamestate"

    id = Column(Integer, primary_key=True, index=True)
    board = Column(String, default=json.dumps([[0] * 7 for _ in range(6)]))
    current_player = Column(Integer, default=1)
    player1 = Column(String, default="Player 1")
    player2 = Column(String, default="Player 2")
    winner = Column(String, default="")


class GameHistory(Base):
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, index=True)
    winner = Column(String)
    loser = Column(String)
    pieces = Column(Integer, default=0)
    date_played = Column(DateTime, default=datetime.utcnow)

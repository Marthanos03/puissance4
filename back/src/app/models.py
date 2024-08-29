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
    winner = Column(Integer)


class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    pseudo = Column(String, unique=True, index=True)

    games = relationship("GameHistory", back_populates="player")


class GameHistory(Base):
    __tablename__ = "game_history"

    id = Column(Integer, primary_key=True, index=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    opponent = Column(String)
    winner = Column(Integer)
    date_played = Column(DateTime, default=datetime.utcnow)

    player = relationship("Player", back_populates="games")

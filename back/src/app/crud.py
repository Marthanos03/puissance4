import json
from sqlalchemy.orm import Session
from src.app import models, schemas, exceptions
from src.app.utils import check_winner


def start_game(db: Session):
    """To start the game"""
    state_db = db.query(models.GameStateDB).first()
    if state_db is None:
        raise exceptions.NoGameFoundException()
    return schemas.GameState(
        board=json.loads(state_db.board),
        current_player=state_db.current_player,
        player1=state_db.player1,
        player2=state_db.player2,
        winner=state_db.winner,
        pieces=state_db.pieces
    )


def play(db: Session, column: int):
    """To play"""
    state_db = db.query(models.GameStateDB).first()
    if state_db is None:
        raise exceptions.NoGameFoundException()

    board = json.loads(state_db.board)

    if column < 0 or column >= 7:
        raise exceptions.NonExistingColumnException(column)

    if board[0][column] != 0:
        raise exceptions.FullColumnException(column)

    for row in reversed(range(6)):
        if board[row][column] == 0:
            board[row][column] = state_db.current_player
            break

    if check_winner(board, row, column, state_db.current_player):
        if state_db.current_player == 1:
            state_db.winner = state_db.player1
        else:
            state_db.winner = state_db.player2
    state_db.current_player = 3 - state_db.current_player
    state_db.board = json.dumps(board)
    state_db.pieces += 1
    db.commit()

    return schemas.GameState(
        board=board,
        current_player=state_db.current_player,
        player1=state_db.player1,
        player2=state_db.player2,
        winner=state_db.winner,
        pieces=state_db.pieces
    )


def reset(db: Session):
    """To reset the game"""
    state_db = db.query(models.GameStateDB).first()
    if state_db is None:
        state_db = models.GameStateDB()
        db.add(state_db)
    state_db.board = json.dumps([[0] * 7 for _ in range(6)])
    state_db.current_player = 1
    state_db.winner = ""
    state_db.pieces = 0
    db.commit()

    return schemas.GameState(
        board=json.loads(state_db.board),
        current_player=state_db.current_player,
        player1=state_db.player1,
        player2=state_db.player2,
        winner=state_db.winner,
        pieces=state_db.pieces
    )


def create_player(db: Session, player: schemas.PlayerCreate):
    """create a new player"""
    state_db = db.query(models.GameStateDB).first()
    if state_db is None:
        state_db = models.GameStateDB()
        db.add(state_db)
    state_db.board = json.dumps([[0] * 7 for _ in range(6)])
    state_db.current_player = 1
    state_db.player1 = player.player1
    state_db.player2 = player.player2
    state_db.winner = ""
    state_db.pieces = 0
    db.commit()
    return schemas.GameState(
        board=json.loads(state_db.board),
        current_player=state_db.current_player,
        player1=state_db.player1,
        player2=state_db.player2,
        winner=state_db.winner,
        pieces=state_db.pieces
    )


def get_history(db: Session):
    """return history for a player"""
    return db.query(models.GameHistory).all()


def record_game(db: Session, game: schemas.GameHistoryCreate):
    """add a game to the history"""
    db_game = models.GameHistory(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game

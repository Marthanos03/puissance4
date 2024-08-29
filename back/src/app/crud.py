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
        winner=state_db.winner,
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
        state_db.winner = state_db.current_player

    state_db.current_player = 3 - state_db.current_player
    state_db.board = json.dumps(board)
    db.commit()

    return schemas.GameState(
        board=board,
        current_player=state_db.current_player,
        winner=state_db.winner,
    )


def reset(db: Session):
    """To reset the game"""
    state_db = db.query(models.GameStateDB).first()
    if state_db is None:
        state_db = models.GameStateDB()
        db.add(state_db)
    state_db.board = json.dumps([[0] * 7 for _ in range(6)])
    state_db.current_player = 1
    state_db.winner = 0
    db.commit()

    return schemas.GameState(
        board=json.loads(state_db.board),
        current_player=state_db.current_player,
        winner=state_db.winner,
    )


def create_player(db: Session, player: schemas.PlayerCreate):
    """create a new player"""
    db_player = db.query(models.Player).filter(models.Player.pseudo == player.pseudo).first()
    if db_player:
        raise exceptions.AlreadyExistingPseudoException(player.pseudo)
    new_player = models.Player(pseudo=player.pseudo)
    db.add(new_player)
    db.commit()
    db.refresh(new_player)
    return new_player


def get_history(db: Session, player_id: int):
    """return history for a player"""
    return db.query(models.GameHistory).filter(models.GameHistory.player_id == player_id).all()


def record_game(db: Session, game: schemas.GameHistoryCreate):
    """add a game to the history"""
    db_game = models.GameHistory(**game.dict())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


# def set_pseudo(db: Session, pseudo: str, player: int):
#     """To set pseudos"""
#     state_db = db.query(models.GameStateDB).first()
#     if state_db is None:
#         raise exceptions.NoGameFoundException()
#     if player == 1:
#         state_db.player1 = pseudo
#     elif player == 2:
#         state_db.player2 = pseudo
#     db.commit()
#     return schemas.GameState(
#         board=json.loads(state_db.board),
#         current_player=state_db.current_player,
#         winner=state_db.winner,
#     )

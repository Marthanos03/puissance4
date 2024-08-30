from typing import List
from fastapi import FastAPI, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from src.app import models, schemas, crud, exceptions
from src.app.database import engine, get_db


models.Base.metadata.create_all(bind=engine)


app = FastAPI()
origins = [
    "http://localhost:8080",
    "http://localhost:8000",
    "https://puissance4-eight.vercel.app/"
    "https://puissance4-martins-projects-0ce88cb6.vercel.app/"
    "https://puissance4-741d39802c9e.herokuapp.com/"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """home"""
    return {"message": "Bienvenue dans le jeu de Puissance 4!"}


@app.get("/game", response_model=schemas.GameState)
def get_game_state(db: Session = Depends(get_db)):
    """To start a game"""
    return crud.start_game(db)


@app.post("/play/{column}", response_model=schemas.GameState)
def play(column: int, db: Session = Depends(get_db)):
    """To play"""
    return crud.play(db, column)


@app.post("/reset", response_model=schemas.GameState)
def reset_game(db: Session = Depends(get_db)):
    """To reset the game"""
    return crud.reset(db)


@app.post("/players", response_model=schemas.GameState)
def create_new_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """Create a new player"""
    return crud.create_player(db, player)


@app.get("/games/history", response_model=List[schemas.GameHistoryResponse])
def get_games_history(db: Session = Depends(get_db)):
    """Get games of the player"""
    return crud.get_history(db)


@app.post("/games/record")
def record_game_history(game: schemas.GameHistoryCreate, db: Session = Depends(get_db)):
    """Add a game to the history"""
    return crud.record_game(db, game)


@app.exception_handler(exceptions.NoGameFoundException)
def no_game_found_exception_handler(request: Request, exc: exceptions.NoGameFoundException):
    """returns a 404 error"""
    return JSONResponse(
        status_code=404,
        content={"detail": "Game not found."},
    )


@app.exception_handler(exceptions.FullColumnException)
def full_column_exception_handler(request: Request, exc: exceptions.FullColumnException):
    """returns a 400 error"""
    return JSONResponse(
        status_code=400,
        content={"detail": f"Column {exc.column} is full"},
    )


@app.exception_handler(exceptions.NonExistingColumnException)
def non_existing_column_exception_handler(request: Request, exc: exceptions.NonExistingColumnException):
    """returns a 400 error"""
    return JSONResponse(
        status_code=400,
        content={"detail": f"Column {exc.column} does not exist."},
    )


@app.exception_handler(exceptions.AlreadyExistingPseudoException)
def already_existing_pseudo_exception_handler(request: Request, exc: exceptions.AlreadyExistingPseudoException):
    """returns a 400 error"""
    return JSONResponse(
        status_code=400,
        content={"detail": f"pseudo {exc.pseudo} already exist."},
    )


def init_db():
    """init database"""
    models.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    init_db()

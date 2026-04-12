import json
from typing import List
from pydantic import ValidationError
from fastapi import FastAPI, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
   
from domain.monster import Monster
from domain.encounter_service import EncounterService
from app.schemas import EncounterFilter, PlayerCharacterFilter

MONSTER_FILE = '../../../data/monsters.json'

@asynccontextmanager
async def lifespan(app: FastAPI):
    with open(MONSTER_FILE, 'r') as fd:
        data = json.load(fd)
        monsters = []
        invalid_monsters = []
        for m in data:
            try:
                monsters.append(Monster(**m))
            except ValidationError as ve:
                invalid_monsters.append(m)
        app.state.monsters = monsters
    print(f"Cached {len(app.state.monsters)} monsters")

    yield 

    app.state.monsters.clear()

def get_cached_monsters(request : Request):
    return request.app.state.monsters

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # your React dev server port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/')
def base():
    return {'message': 'Welcome to the DnD Encounter Creator API!'}

@app.get('/monsters')
def get_all_monsters(monsters : List[Monster] = Depends(get_cached_monsters)):
    return {'monsters': monsters}

@app.post('/encounters/generate')
def generate_encounter(encounter_filter : EncounterFilter, monsters : List[Monster] = Depends(get_cached_monsters)):
    serv = EncounterService(monsters=monsters)
    return serv.generate(encounter_filter)
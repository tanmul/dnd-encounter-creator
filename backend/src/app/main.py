import json
from typing import List
from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager
   
from domain.monster import Monster

MONSTER_FILE = '../../../data/monsters.json'

@asynccontextmanager
async def lifespan(app: FastAPI):
    with open(MONSTER_FILE, 'r') as fd:
        data = json.load(fd)
        app.state.monsters = [Monster(**m) for m in data]
    print(f"Cached {len(app.state.monsters)} monsters")

    yield 

    app.state.monsters.clear()
    

def get_monster_cache(request : Request):
    return request.app.state.monsters

app = FastAPI(lifespan=lifespan)

@app.get('/')
def base():
    return {'message': 'Welcome to the DnD Encounter Creator API!'}

@app.get('/generate')
def generate_encounter(monsters : List[Monster] = Depends(get_monster_cache)):
    return {'monsters': monsters}
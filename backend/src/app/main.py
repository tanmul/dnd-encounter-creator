import json
from typing import List
from fastapi import FastAPI, Request, Depends
from contextlib import asynccontextmanager

from dnd_monster import Monster

MONSTER_FILE = '../../../data/monsters.json'

monster_cache : List[Monster] = []
@asynccontextmanager
async def lifespan(app: FastAPI):
    if not monster_cache:
        with open(MONSTER_FILE, 'r') as fd:
            monster_list = json.load(fd)
            for monster_dict in monster_list:
                monster_cache.append(Monster(**monster_dict))
        
    yield {'monster_cache': monster_cache}

    monster_cache.clear()

def get_monster_cache(request : Request):
    return request.app.state['monster_cache']

app = FastAPI(lifespan=lifespan)

@app.get('/')
def base():
    return {'message': 'Welcome to the DnD Encounter Creator API!'}

@app.get('/generate-encounter')
def generate_encounter(monsters : List[Monster] = Depends(get_monster_cache)):
    return {'monsters': monsters}
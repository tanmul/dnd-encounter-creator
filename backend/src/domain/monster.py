from pydantic import BaseModel, Field, computed_field, model_validator, field_validator
from typing import Literal, Optional, List

CR_TO_XP = {
    '0': 10,
    '1/8': 25,
    '1/4': 50,
    '1/2': 100,
    '1': 200,
    '2': 450,
    '3': 700,
    '4': 1100,
    '5': 1800,
    '6': 2300,
    '7': 2900,
    '8': 3900,
    '9': 5000,
    '10': 5900,
    '11': 7200,
    '12': 8400,
    '13': 10000,
    '14': 11500,
    '15': 13000,
    '16': 15000,
    '17': 18000,
    '18': 20000,
    '19': 22000,
    '20': 25000,
    '21': 33000,
    '22': 41000,
    '23': 50000,
    '24': 62000,
    '25': 75000,
    '26': 90000,
    '27': 105000,
    '28': 120000,
    '29': 135000,
    '30': 155000
}

STANDARD_TYPES = Literal[
    'Aberration',
    'Beast',
    'Celestial',
    'Construct',
    'Dragon',
    'Elemental',
    'Fey',
    'Fiend',
    'Giant',
    'Humanoid',
    'Monstrosity',
    'Ooze',
    'Plant',
    'Undead',
    'Swarm of Tiny Beasts',
    'Swarm of Tiny Monstrosities',
    'Swarm of Tiny Undead',
    'Swarm of Small Fiends',
    'Swarm of Medium Fiends'
]

class Monster(BaseModel):
    model_config = {'extra': 'ignore'}

    name : str = Field(alias='name')
    sizes : List[Literal['Tiny', 'Small', 'Medium', 'Large', 'Huge', 'Gargantuan']] = Field(alias='size')
    challenge_rating : str = Field(alias='cr')
    types : List[STANDARD_TYPES] = Field(alias='type')
    alignment : str = Field(alias='alignment')
    armor_class : int = Field(alias='ac')

    @computed_field
    @property
    def xp(self) -> int:
        return CR_TO_XP.get(self.challenge_rating, 0)
    
    @model_validator(mode='before')
    @classmethod
    def flatten_and_parse_properties(cls, data):
        for key, value in data.items():
            if key == 'size': # Size can be 'Small or Medium', which we should split into a list
                data['size'] = [size.strip() for size in value.replace('or', ',').split(',')]
            elif key == 'type':
                data['type'] = [type.strip() for type in value.split('(')[0].strip().replace('or', ',').split(',')]
            elif key == 'cr':
                data['cr'] = 0 if not value else value
            else:
                data[key] = value

        return data


    
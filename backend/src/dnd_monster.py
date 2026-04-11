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

class Monster(BaseModel):
    model_config = {'extra': 'ignore'}

    name : str = Field(alias='name')
    description : str = Field(alias='description')
    category : str = Field(alias='properties.Category')
    size : Optional[List[str]] = Field(alias='properties.Size', default=None)
    type : Optional[str] = Field(alias='properties.Type', default=None)
    alignment : Optional[str] = Field(alias='properties.Alignment', default=None)
    challenge_rating : Optional[str] = Field(alias='properties.Challenge Rating', default=None)

    @computed_field
    @property
    def xp(self) -> int:
        return CR_TO_XP.get(self.challenge_rating, 0)
    
    @model_validator(mode='before')
    @classmethod
    def flatten_and_parse_properties(cls, data):
        if isinstance(data, dict):
            for key, value in data.get('properties', {}).items():
                if key == 'Challenge Rating': # Challenge Rating can be a number, need to coerce the string
                    data[f'properties.{key}'] = str(value)
                elif key == 'Size': # Size can be 'Small or Medium', which we should split into a list
                    data[f'properties.{key}'] = [size.strip() for size in value.replace('or', ',').split(',')]
                else:
                    data[f'properties.{key}'] = value

        return data


    
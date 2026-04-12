from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Literal

from domain.monster import Monster

class PlayerCharacterFilter(BaseModel):
    player_count : int = Field(alias='player_count', gt=0, default=4)
    player_level : int = Field(alias='player_level', gt=0, lt=21)

class EncounterFilter(BaseModel):
    difficulty : Literal['low', 'moderate', 'high'] = Field(alias='difficulty')
    pc_filter : PlayerCharacterFilter = Field(alias='pc_filter')

    encounter_size : Optional[int] = Field(alias='encounter_size', default=None)
    encounter_type : Literal['Balanced', 'Boss', 'Swarm'] = Field(alias='encounter_type', default='Balanced')

    monster_names: Optional[List[str]] = Field(alias='monster_names', default=None)
    monster_types: Optional[List[str]] = Field(alias='monster_types', default=None)
    monster_sizes: Optional[List[str]] = Field(alias='monster_sizes', default=None)

from .monster import Monster
from app.schemas import EncounterFilter

from typing import Optional, List, Dict
import random

XP_BUDGET_MAP = {
    1:  {'low': 50,    'moderate': 75,    'high': 100},
    2:  {'low': 100,   'moderate': 150,   'high': 200},
    3:  {'low': 150,   'moderate': 225,   'high': 400},
    4:  {'low': 250,   'moderate': 375,   'high': 500},
    5:  {'low': 500,   'moderate': 750,   'high': 1100},
    6:  {'low': 600,   'moderate': 1000,  'high': 1400},
    7:  {'low': 750,   'moderate': 1300,  'high': 1700},
    8:  {'low': 1000,  'moderate': 1700,  'high': 2100},
    9:  {'low': 1300,  'moderate': 2000,  'high': 2600},
    10: {'low': 1600,  'moderate': 2300,  'high': 3100},
    11: {'low': 1900,  'moderate': 2900,  'high': 4100},
    12: {'low': 2200,  'moderate': 3700,  'high': 4700},
    13: {'low': 2600,  'moderate': 4200,  'high': 5400},
    14: {'low': 2900,  'moderate': 4900,  'high': 6200},
    15: {'low': 3300,  'moderate': 5400,  'high': 7800},
    16: {'low': 3800,  'moderate': 6100,  'high': 9800},
    17: {'low': 4500,  'moderate': 7200,  'high': 11700},
    18: {'low': 5000,  'moderate': 8700,  'high': 14200},
    19: {'low': 5500,  'moderate': 10700, 'high': 17200},
    20: {'low': 6400,  'moderate': 13200, 'high': 22000},
}

class EncounterService():

    def __init__(self, monsters : List[Monster]):
        self._monsters = monsters

    def generate(self, encounter_filter : EncounterFilter):
        # First we need to apply all the filters so our monster pool is selective
        filtered_monsters = self._monsters
        if encounter_filter.monster_names:
            filtered_monsters = list(filter(lambda x: x.name in encounter_filter.monster_names, filtered_monsters))
        if encounter_filter.monster_sizes:
            filtered_monsters = list(filter(lambda x: bool(set(x.sizes) & set(encounter_filter.monster_sizes)), filtered_monsters))

        # Creating a xp -> monster list map using the filtered monsters
        xp_monster_map : Dict[int, List[Monster]] = {}
        for monster in filtered_monsters:
            xp_monster_map.setdefault(monster.xp, []).append(monster)
        if 0 in xp_monster_map:
            xp_monster_map.pop(0) # We don't want any 0 xp monsters

        # Now we generate the encounter using the list of monsters we have
        best_encounter = []
        best_encounter_total_xp = 0
        for _ in range(10): # We will be coming up with many encounters and choosing the one closest to the budget
            xp_budget = XP_BUDGET_MAP[encounter_filter.pc_filter.player_level][encounter_filter.difficulty] * encounter_filter.pc_filter.player_count
            current_encounter = []
            current_encounter_xp_total = 0
            used_monsters = set()
            while xp_budget >= 0:
                valid_xp_costs = [xp for xp in xp_monster_map.keys() if xp <= xp_budget]
                if not valid_xp_costs or len(used_monsters) >= len(filtered_monsters):
                    break

                # We come up with weights for the monster xp based on encounter type
                weights = [1] * len(valid_xp_costs)
                if encounter_filter.encounter_type == 'Boss':
                    weights = [xp **2 for xp in valid_xp_costs]
                elif encounter_filter.encounter_type == 'Swarm':
                    weights = [1/xp for xp in valid_xp_costs]
                
                random_xp_choice = random.choices(valid_xp_costs, weights=weights, k=1)[0]
                valid_monsters = [monster for monster in xp_monster_map[random_xp_choice] if monster.name not in used_monsters]
                if random_xp_choice <= xp_budget and valid_monsters:
                    monster = random.choice(valid_monsters)
                    monster_count_upper = int(xp_budget/random_xp_choice)
                    num_monsters = random.randint(1, monster_count_upper)
                    monster_xp_total = num_monsters * random_xp_choice
                    current_encounter_xp_total += monster_xp_total 
                    xp_budget -= monster_xp_total # Reduce the xp_budget
                    current_encounter.append((num_monsters, monster))
                    used_monsters.add(monster.name) # Don't pick the same monster again

            if current_encounter_xp_total > best_encounter_total_xp:
                best_encounter_total_xp = current_encounter_xp_total
                best_encounter = current_encounter

        return best_encounter
        
                




        
        
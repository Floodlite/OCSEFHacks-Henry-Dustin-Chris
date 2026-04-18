import random

score = 0
gameover = False
lose_reason = ""
pollution = 0.0
temp = 100.0
light_level = 100.0
water_level = 1000000.0
organic_matter = 100000.0
water_toxicity = 0.0 # pollution bleedthrough + user buildings, implement later

animal_types = 4
animals = [ # order matters, top predates on next level
    {"name": "apex_predators", "count": 10},
    {"name": "carnivores", "count": 100},
    {"name": "herbivores", "count": 1000},
    {"name": "plants", "count": 10000}
]

ORGANIC_WATER_NEED = 0.01
SUNLIGHT_GROWTH_FACTOR = 0.01
WATER_REPLENISH_RATE = 1000.0 # aquifers, rain, natural sources
ENERGY_TRANSFER_EFFICENCY = 0.1 # how much energy is transferred from one trophic level to the next
POLLUTION_EFFECT_FACTOR = 0.01
BASE_DEATH_RATE = 0.01
PREDATION_RATE = 0.02
STARVATION_RATE = 0.2
city_water_net = 0.0 # you can add pumps later to increase this, or drain it with consumption
city_pollution_production = 0.0 # buildings affect

# todo: water toxicity, human intervention options, more complex food web, random events (droughts, floods, etc), player choices and consequences, graphics and UI, endgame PSA about real world ecosystem collapse and how to help

while gameover == False:
    i = animal_types
    # game loop
    temp = random.random(70 + pollution * 0.95, 100 + pollution * 1.25) # random temp fluctuation, exacerbated by pollution/climate change
    water_level -= ORGANIC_WATER_NEED * plants * temp * 0.01 # plant consumption, boil-off rate mult
    water_level += WATER_REPLENISH_RATE + city_water_net * (pollution * (1 - POLLUTION_EFFECT_FACTOR)) # standin for water toxicity until implemented
    pollution = abs(pollution + city_pollution_production) # can't be negative
    plants += SUNLIGHT_GROWTH_FACTOR * light_level * plants * (pollution * (1 - POLLUTION_EFFECT_FACTOR))
    if pollution > 100:
        gameover = True
        lose_reason = "The ecosystem is too toxic to support life. All life has perished."
    if water_level < 0:
        gameover = True
        lose_reason = "The ecosystem has no more clean water. All life has perished."
    for animal_dict in animals:
        i -= 1
        animal = animal_dict["name"]
        count = animal_dict["count"]
        count -= BASE_DEATH_RATE * count * (pollution * POLLUTION_EFFECT_FACTOR + 1)
        if i > 1: # not plants
            count += ENERGY_TRANSFER_EFFICENCY * PREDATION_RATE * animals[i-1]["count"] # "ate" a lower tier animal
        if i != animal_types: # not apex predators
            count -= PREDATION_RATE * count * animals[i+1]["count"] # "got eaten" by a higher tier animal
        animal_dict["count"] = count
        if count < 0: # todo: give options for human intervention to save ecosystem
            gameover = True
            lose_reason = f"The {animal} population has collapsed. The ecosystem is incapable of sustaining life without human rebalancing."
        
            
    # player choices
    # filler text and display graphics
    print("Score: " + str(score))

# endgame psa
import random

round = 1
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
    {"name": "apex_predators", "count": 10.0},
    {"name": "carnivores", "count": 100.0},
    {"name": "herbivores", "count": 1000.0},
    {"name": "plants", "count": 10000.0}
]

ORGANIC_WATER_NEED = 0.01
SUNLIGHT_GROWTH_FACTOR = 0.01
WATER_REPLENISH_RATE = 1000.0 # aquifers, rain, natural sources
ENERGY_TRANSFER_EFFICENCY = 0.1 # how much energy is transferred from one trophic level to the next
POLLUTION_EFFECT_FACTOR = 0.01
BASE_DEATH_RATE = 0.01
PREDATION_RATE = 0.02
ORGANIC_MATTER_NEED = 0.01 
STARVATION_RATE = 0.2 # only works later, right now useless until intervention of dying ecosystem possible
city_water_net = 0.0 # you can add pumps later to increase this, or drain it with consumption
city_pollution_production = 0.0 # buildings affect

# todo: water toxicity, human intervention options, more complex food web, random events (droughts, floods, etc), player choices and consequences, graphics and UI, endgame PSA about real world ecosystem collapse and how to help

building_dict = {
    "factory": {
        "pollution": 100,
        "score": 30,
        "chosen": False,
    },
    "park": {
        "pollution": -20,
        "score": -10,
        "chosen": False,
    },
    "highway": {
        "pollution": 50,
        "score": 15,
        "chosen": False,
    }
}

def print_dict(dict):
    for item in dict:
        if(not dict[item]["chosen"]):
            continue
        print("_________________________")
        print(item)
        print("Pollution: " + str(dict[item]["pollution"]))
        print("Score: " + str(dict[item]["score"]))
        print("_________________________")

def print_stats():
    print("========================")
    print("Your score: " + str(score))
    print("Pollution: " + str(pollution))
    print("Temperature: " + str(temp))
    print("Light Level: " + str(light_level))
    print("Water Level: " + str(water_level))
    print("========================")
    print("Plants alive: " + str(animals["plants"]["count"]))
    print("Herbivores alive: " + str(animals["herbivores"]["count"]))
    print("Carnivores alive: "  + str(animals["carnivores"]["count"]))
    print("Apex predators alive: " + str(animals["apex_predators"]["count"]))
    print("========================")


def pick_available_buildings(dict, available_choices=3):
    building_names = []
    for item in dict:
        building_names.append(item)
        dict[item]["chosen"] = False

    random.shuffle(building_names)
    for i in range(available_choices):
        dict[building_names[i]]["chosen"] = True


while gameover == False:
    i = animal_types
    # game loop
    temp = random.randrange(start=70 + pollution * 0.95, stop=100 + pollution * 1.25, step=0.01) # random temp fluctuation, exacerbated by pollution/climate change
    water_level -= ORGANIC_WATER_NEED * animals["plants"]["count"] * temp * 0.01 # plant consumption, boil-off rate mult
    water_level += WATER_REPLENISH_RATE + city_water_net * (pollution * (1 - POLLUTION_EFFECT_FACTOR)) # standin for water toxicity until implemented
    organic_matter -= ORGANIC_MATTER_NEED * animals["plants"]["count"] # plant fertilizer consumption
    pollution = abs(pollution + city_pollution_production) # can't be negative
    animals["plants"]["count"] += SUNLIGHT_GROWTH_FACTOR * light_level * animals["plants"]["count"] * (pollution * (1 - POLLUTION_EFFECT_FACTOR))
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
        natural_deaths = BASE_DEATH_RATE * count * (pollution * POLLUTION_EFFECT_FACTOR + 1)
        count -= natural_deaths * (1 - (pollution * POLLUTION_EFFECT_FACTOR)) # pollution represents toxicity, some cannot be recycled
        organic_matter += natural_deaths 
        if i > 1: # not plants
            count += ENERGY_TRANSFER_EFFICENCY * PREDATION_RATE * animals[i-1]["count"] # "ate" a lower tier animal
        if i != animal_types: # not apex predators
            eaten = PREDATION_RATE * count * animals[i+1]["count"] # "got eaten" by a higher tier animal
            count -= eaten
            organic_matter += eaten * (1 - (pollution * POLLUTION_EFFECT_FACTOR)) # replenishes organic matter
        animal_dict["count"] = count
        if count < 0: # todo: give options for human intervention to save ecosystem
            gameover = True
            lose_reason = f"The {animal} population has collapsed. The ecosystem is incapable of sustaining life without human rebalancing."
        
            
    # player choices
    print("**** Round " + str(round) + " ****")
    print_stats()
    pick_available_buildings(building_dict, 3)
    while(True):
        print_dict(building_dict)
        player_input = input("Choose your building: ")
        player_input = player_input.lower()
        try:
            if(building_dict[player_input]["chosen"]):
                pollution += building_dict[player_input]["pollution"]
                score += building_dict[player_input]["score"]
                break
            else:
                print("Building not available this round, see above for valid choices")
                continue
        except KeyError:
            print("Invalid choice, try again")
            continue


    # filler text and display graphics
    print("Score: " + str(score))
    round += 1

# endgame psa
print("You have lost. ")
print(lose_reason)
print(f"You scored {score} points.")
input("Play again(Y/N)?")
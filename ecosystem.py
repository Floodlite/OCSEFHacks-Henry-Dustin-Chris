import random
import math

lose_reason = ""
score = 0
pollution = 0.0
temp = 100.0
light_level = 100.0
water_level = 1000000.0 # declare existence for usage in functions

events_dict = {
    "drought": {
        "city_water_net": -500.0,
        "description": "A severe drought has reduced water availability. Water will reduce by 500 units per turn for the next 5 turns.",
        "duration": 5
    },

    "industrial spill": {
        "city_pollution_production": 6.0,
        "description": "An industrial spill has occurred, increasing pollution. Pollution will increase by 6 units per turn until the spill is cleaned up after the next 4 turns.",
        "duration": 4
    }
}

modifiers_ongoning = []

events_dict = {
    "drought": {
        "city_water_net": -500.0,
        "description": "A severe drought has reduced water availability. Water will reduce by 500 units per turn for the next 5 turns.",
        "duration": 5
    },

    "industrial spill": {
        "city_pollution_production": 6.0,
        "description": "An industrial spill has occurred, increasing pollution. Pollution will increase by 6 units per turn until the spill is cleaned up after the next 4 turns.",
        "duration": 4
    }
}

modifiers_ongoning = []

building_dict = {
    "factory": {
        "pollution": 10.0,
        "score": 30,
        "water": 500.0,
        "chosen": False,
        "ability": "",
    },
    "park": {
        "pollution": -5.0,
        "score": -10,
        "water": -10.0,
        "chosen": False,
        "ability": "",
    },
    "highway": {
        "pollution": 4.5,
        "score": 6,
        "water": 200.0,
        "chosen": False,
        "count": 0,
        "ability": "Ability: Grants +2 score for each highway constructed",
    },
    "skyscraper": {
        "pollution": 6.5,
        "score": 16.0,
        "water": 100.0,
        "chosen": False,
        "ability": "",
    },
    "housing": {
        "pollution": 4,
        "score": 4,
        "water": 110.0,
        "chosen": False,
        "ability": "",
    },
    "suburbs": {
        "pollution": 1,
        "score": 4,
        "water": 240.0,
        "chosen": False,
        "ability": "",
    },
    "water pump": {
        "pollution": 1,
        "score": -2,
        "water": -150.0,
        "chosen": False,
        "ability": "",
    },
    "oil well": {
        "pollution": 9,
        "score": 12,
        "water": 100.0,
        "chosen": False,
        "ability": "None",
    },
    "restaurant": {
        "pollution": 3,
        "score": 6.5,
        "water": 110.0,
        "chosen": False,
        "count": 0,
        "ability": "Ability: Consumes 10 herbivores each turn per restaurant",
    },
}


def print_dict(dict):
    for item in dict:
        if (not dict[item]["chosen"]):
            continue
        print("_________________________")
        print(item)
        print("Pollution: " + str(dict[item]["pollution"]))
        print("Water consumption: " + str(dict[item]["pollution"]))
        print("Score: " + str(dict[item]["score"]) + " points")
        print("Ability: " + str(dict[item]["ability"]))
        print("_________________________")


def print_stats(score, pollution, temp, light_level, water_level, animals):
    print("========================")
    print("Your score: " + str(score))
    print("Pollution: " + str(pollution))
    print("Temperature: " + str(temp))
    print("Light Level: " + str(light_level))
    print("Water Level: " + str(water_level))
    print("========================")
    print("Plants alive: " + str(animals["plants"]["count"]))
    print("Herbivores alive: " + str(animals["herbivores"]["count"]))
    print("Carnivores alive: " + str(animals["carnivores"]["count"]))
    print("Apex predators alive: " + str(animals["apex_predators"]["count"]))
    print("========================")

def return_building_pollution(building):
    return str(building_dict[building]["pollution"])
def return_building_water(building):
    return str(building_dict[building]["water"])
def return_building_score(building):
    return str(building_dict[building]["score"])
def return_building_ability(building):
    return str(building_dict[building]["ability"])

def return_building_stats_long(building):
    return "Pollution: " + str(dict[building]["pollution"]) + "\nWater consumption: " + str(dict[building]["pollution"]) + "\nScore: " + str(dict[building]["score"]) + " points" + "\nAbility: " + str(building_dict[building]["ability"])
def line_break():
    return "========================"
def return_score():
    return str(score)
def return_pollution():
    return str(pollution)
def return_temperature():
    return str(temp)
def return_light():
    return str(light_level)
def return_water():
    return str(water_level)
def return_plant_count():
    return str(animals["plants"]["count"])
def return_herbivore_count():
    return str(animals["herbivores"]["count"])
def return_carnivore_count():
    return str(animals["carnivore"]["count"])

def pick_available_buildings(dict, available_choices=3):
    building_names = []
    for item in dict:
        building_names.append(item)
        dict[item]["chosen"] = False
    random.shuffle(building_names)
    for i in range(available_choices):
        dict[building_names[i]]["chosen"] = True


def highway_ability():
    global score
    global building_dict
    building_dict["highway"]["count"] += 1
    score += 2 * building_dict["highway"]["count"]
    print("Highway count: " + str(building_dict["highway"]["count"]))
def restaurant_ability():
    global animals
    global building_dict
    building_dict["restaurant"]["count"] += 1
    animals["herbivores"]["count"] -= 10 * building_dict["restaurant"]["count"]
    print("Restaurant herbivore consumption: " + str(10 * building_dict["restaurant"]["count"]))

def return_round_number():
    global round
    return "**** Round " + str(round) + " ****"
def building_error_message():
    return "Building not available this round, see above for valid choices"
def input_error_message():
     return "Invalid input, please try again"
def failure_message():
    return f"{lose_reason}\nYou have lost after {round} rounds of play with {score} points"

def random_event():
    event = random.choice(list(events_dict.keys()))
    print("Random event: " + events_dict[event]["description"])
    modifiers_ongoning.append(events_dict[event])
    print(events_dict[event]["description"])

def random_event():
    event = random.choice(list(events_dict.keys()))
    print("Random event: " + events_dict[event]["description"])
    modifiers_ongoning.append(events_dict[event])
    print(events_dict[event]["description"])


def play_game():
    round = 1
    score = 0
    gameover = False
    lose_reason = ""
    pollution = 0.0
    temp = 100.0
    light_level = 100.0
    water_level = 1000000.0
    organic_matter = 100000.0
    water_toxicity = 0.0  # pollution bleedthrough + user buildings, implement later

    animal_types = 4
    animals = { # order matters, top predates on next level down
        "apex_predators": {"count": 10.0},
        "carnivores": {"count": 100.0},
        "herbivores": {"count": 1000.0},
        "plants": {"count": 10000.0}
    }
    
    ORGANIC_WATER_NEED = 0.01
    PLANT_GROWTH_FACTOR = 0.03
    WATER_REPLENISH_RATE = 1000.0  # aquifers, rain, natural sources
    ORGANICS_REPLENISH_RATE = 100.0  # natural decay, etc from outside ecosystem entering
    ENERGY_TRANSFER_EFFICENCY = 0.1  # how much energy is transferred from one trophic level to the next
    POLLUTION_EFFECT_FACTOR = 0.01
    BASE_DEATH_RATE = 0.01
    PREDATION_RATE = 0.02
    ORGANIC_MATTER_NEED = 0.01
    STARVATION_RATE = 0.2  # only works later, right now useless until intervention of dying ecosystem possible
    city_water_net = 0.0  # you can add pumps later to increase this, or drain it with consumption
    city_pollution_production = 0.0  # buildings affect
    city_organics_production = 0.0  # composting, etc, can be negative with certain buildings

    # todo: random events, player direct intervention, maximum "living space" mechanic to reduce growth over time
    while not gameover:
        input("Beginning round " + str(round) + " logic update:")
        # game loop
        temp = random.randrange(int(70 + pollution * 0.95), int(100.0 + pollution * 1.25), 1) # random temp fluctuation, exacerbated by pollution/climate change
        
        water_level -= ORGANIC_WATER_NEED * animals["plants"]["count"] * temp * 0.01 # plant consumption, boil-off rate mult
        water_level += WATER_REPLENISH_RATE + city_water_net * (pollution * (1 - POLLUTION_EFFECT_FACTOR)) # standin for water toxicity until implemented
        organic_matter -= ORGANIC_MATTER_NEED * animals["plants"]["count"] # plant fertilizer consumption
        organic_matter += ORGANICS_REPLENISH_RATE + city_organics_production * (1 - (pollution * POLLUTION_EFFECT_FACTOR)) # city composting, etc, pollution means some wasted

        pollution = abs(pollution + city_pollution_production) # can't be negative
        animals["plants"]["count"] += PLANT_GROWTH_FACTOR * (light_level * 0.01) * animals["plants"]["count"] * (pollution * (1 - POLLUTION_EFFECT_FACTOR))
        input("Plants have grown, beginning animal population updates.")
        print(f"Plants: {animals['plants']['count']},")
        if pollution > 100:
            gameover = True
            lose_reason = "The ecosystem is too toxic to support life. All life has perished."
        if water_level < 0:
            gameover = True
            lose_reason = "The ecosystem has no more clean water. All life has perished."
        for i, (animal, animal_dict) in enumerate(animals.items(), start=1):
            count = animal_dict["count"]
            natural_deaths = BASE_DEATH_RATE * count * (pollution * POLLUTION_EFFECT_FACTOR + 1)
            print(f"Natural deaths for {animal} is {natural_deaths}.")
            count -= natural_deaths * (1 - (pollution * POLLUTION_EFFECT_FACTOR)) # pollution represents toxicity, some cannot be recycled
            organic_matter += natural_deaths 
            if i < animal_types: # not plants
                input("Predation phase...")
                input(f"Animal to prey on is {list(animals.keys())[i]} and amount of that animal alive is {list(animals.values())[i]["count"]}.")
                count += ENERGY_TRANSFER_EFFICENCY * PREDATION_RATE * list(animals.values())[i]["count"] # "ate" a lower tier animal
            if i > 1: # not apex predators
                input("Eating animals of species...")
                input(f"Animal to be consumed is {list(animals.keys())[i-1]} and amount of that animal alive is {list(animals.values())[i-1]["count"]}.")
                eaten = PREDATION_RATE * count # "got eaten" by a higher tier animal
                count -= eaten
                print("Eaten by higher tier animal: " + str(eaten))
                organic_matter += eaten * (1 - (pollution * POLLUTION_EFFECT_FACTOR))  # replenishes organic matter
            animal_dict["count"] = count
            input(f"Animal population updated for animal {animal}. i is {i}.")
            if count < 0: # todo: give options for human intervention to save ecosystem
                gameover = True
                lose_reason = f"The {animal} population has collapsed. The ecosystem is incapable of sustaining life without human rebalancing."
        input("Game logic updated.")
        print(f"Plants: {animals['plants']['count']},")
        print(f"Herbivores: {animals['herbivores']['count']},")
        print(f"Carnivores: {animals['carnivores']['count']},")
        print(f"Apex predators: {animals['apex_predators']['count']},")
    # ongoing event modifiers
        for event in modifiers_ongoning:
            event["duration"] -= 1
            if event["duration"] <= 0:
                if event["city_water_net"]: # too lazy to implement global variable search to dynamically unapply, do if leftover time
                    city_water_net -= event["city_water_net"]
                if event["city_pollution_production"]:
                    city_pollution_production -= event["city_pollution_production"]
                del event
    input("Random events updated.")
    # make new random events(open-ended dice roll, in theory scales infinitely)
    while random.random() < 0.2:
        random_event()
        input("Random event triggered.")
    # player choices
    print("**** Round " + str(round) + " ****")
    print_stats(score, pollution, temp, light_level, water_level, animals)
    pick_available_buildings(building_dict, 3)
    while (True):
        print_dict(building_dict)
        player_input = input("Choose your building: ")
        uppercase_input = player_input
        player_input = player_input.lower()
        try:
            if (building_dict[player_input]["chosen"]):
                print(uppercase_input + " built!")
                city_pollution_production += building_dict[player_input]["pollution"]
                #print(building_dict[player_input]["score"])
                score += building_dict[player_input]["score"]
                city_water_net += building_dict[player_input]["water"]
                if (player_input == "highway"):
                    highway_ability()
                if (player_input == "restaurant"):
                    building_dict["restaurant"]["count"] += 1
                if(building_dict["restaurant"]["count"] >= 1):
                    restaurant_ability()
                break
            else:
                print("Building not available this round, see above for valid choices")
                continue
        except IndexError:
            print("Invalid input, please try again")
            continue

    # filler text and display graphics
    print("Score: " + str(score))
    round += 1

    # endgame psa
    print(f"You have lost, after {round} rounds of play.")
    print(lose_reason)
    print(f"You scored {score} points.")
    return input("Play again(Y/N)? ")


while True:
    try:
        input("Beginning game loop:")
        replay = play_game()
        if replay.lower() != "y":
            print(
                """Thank you for playing. While this game is a simple simulation, it represents very real problems in the world. 
                Ecosystem collapse is a very real threat, and we all have a role to play in preventing it everyday. 
                Please consider learning more about how you can help protect our planet and its ecosystems at https://sdgs.un.org/goals/goal12."""
                )
            break
    except Exception as e:
        print("An error occurred: " + str(e))

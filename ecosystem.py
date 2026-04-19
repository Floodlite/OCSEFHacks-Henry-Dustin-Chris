import copy
import random


EVENT_TEMPLATES = {
    "drought": {
        "city_water_net": -500.0,
        "description": "A severe drought has reduced water availability for the next 5 turns.",
        "duration": 5,
    },
    "industrial spill": {
        "city_pollution_production": 6.0,
        "description": "An industrial spill is increasing pollution for the next 4 turns.",
        "duration": 4,
    },
    "nuclear meltdown": {
        "city_pollution_production": 25.0,
        "description": "A nuclear meltdown causes a sharp pollution spike this turn.",
        "duration": 1,
    },
    "overpopulation": {
        "city_pollution_production": 5.0,
        "population_multiplier": 1.35,
        "description": "Population growth surges for the next 4 turns.",
        "duration": 4,
    },
}


BUILDING_TEMPLATES = {
    "factory": {
        "pollution": 10.0,
        "score": 30.0,
        "water": 500.0,
        "ability": "High score output, but it accelerates pollution fast.",
    },
    "park": {
        "pollution": -5.0,
        "score": -10.0,
        "water": -10.0,
        "ability": "Reduces pollution at the cost of points.",
    },
    "highway": {
        "pollution": 4.5,
        "score": 6.0,
        "water": 200.0,
        "ability": "Adds bonus score and a little ongoing point generation.",
    },
    "skyscraper": {
        "pollution": 6.5,
        "score": 16.0,
        "water": 100.0,
        "ability": "Boosts the score multiplier by 10%.",
    },
    "housing": {
        "pollution": 4.0,
        "score": 4.0,
        "water": 110.0,
        "ability": "Steady growth with modest costs.",
    },
    "suburbs": {
        "pollution": 1.0,
        "score": 4.0,
        "water": 240.0,
        "ability": "Low pollution, but high water use.",
    },
    "water pump": {
        "pollution": 1.0,
        "score": -2.0,
        "water": -300.0,
        "ability": "Improves water supply, but costs points.",
    },
    "oil well": {
        "pollution": 9.0,
        "score": 12.0,
        "water": 100.0,
        "ability": "Solid score gain with heavy pollution impact.",
    },
    "restaurant": {
        "pollution": 3.0,
        "score": 6.5,
        "water": 110.0,
        "ability": "Consumes herbivores each turn once built.",
    },
}


ANIMAL_ORDER = ["apex_predators", "carnivores", "herbivores", "plants"]


def reset_building_dict():
    return {
        name: {
            **copy.deepcopy(stats),
            "chosen": False,
            "count": 0,
        }
        for name, stats in BUILDING_TEMPLATES.items()
    }


def reset_game_state():
    game_state = {
        "round": 1,
        "score": 0.0,
        "score_multiplier": 1.0,
        "gameover": False,
        "lose_reason": "",
        "status": "Playing",
        "pollution": 0.0,
        "temp": 68.0,
        "light_level": 100.0,
        "water_level": 1_000_000.0,
        "organic_matter": 100_000.0,
        "water_toxicity": 0.0,
        "animals": {
            "apex_predators": {"count": 10.0},
            "carnivores": {"count": 100.0},
            "herbivores": {"count": 1_000.0},
            "plants": {"count": 10_000.0},
        },
        "ORGANIC_WATER_NEED": 0.01,
        "PLANT_GROWTH_FACTOR": 0.05,
        "WATER_REPLENISH_RATE": 1000.0,
        "ORGANICS_REPLENISH_RATE": 100.0,
        "ENERGY_TRANSFER_EFFICIENCY": 0.1,
        "POLLUTION_EFFECT_FACTOR": 0.01,
        "BASE_DEATH_RATE": 0.01,
        "PREDATION_RATE": 0.02,
        "ORGANIC_MATTER_NEED": 0.01,
        "EVENT_CHANCE": 0.2,
        "city_water_net": 0.0,
        "city_pollution_production": 0.0,
        "city_organics_production": 0.0,
        "city_point_generation": 0.0,
        "modifiers_ongoing": [],
        "building_dict": reset_building_dict(),
        "available_buildings": [],
        "recent_events": [],
        "last_building": "",
    }
    pick_available_buildings(game_state)
    return game_state


def pick_available_buildings(game_state, available_choices=3):
    building_dict = game_state["building_dict"]
    building_names = list(building_dict.keys())
    random.shuffle(building_names)
    chosen = building_names[:available_choices]
    for name, stats in building_dict.items():
        stats["chosen"] = name in chosen
    game_state["available_buildings"] = chosen
    return chosen


def create_event(name):
    event = copy.deepcopy(EVENT_TEMPLATES[name])
    event["name"] = name
    event["remaining_duration"] = event["duration"]
    return event


def apply_event_effect(game_state, event):
    if "city_water_net" in event:
        game_state["city_water_net"] += event["city_water_net"]
    if "city_pollution_production" in event:
        game_state["city_pollution_production"] += event["city_pollution_production"]
    if "population_multiplier" in event:
        for animal in game_state["animals"].values():
            animal["count"] *= event["population_multiplier"]


def remove_event_effect(game_state, event):
    if "city_water_net" in event:
        game_state["city_water_net"] -= event["city_water_net"]
    if "city_pollution_production" in event:
        game_state["city_pollution_production"] -= event["city_pollution_production"]
    if "population_multiplier" in event:
        for animal in game_state["animals"].values():
            animal["count"] /= event["population_multiplier"]


def trigger_random_events(game_state):
    triggered = []
    while random.random() < game_state["EVENT_CHANCE"]:
        event_name = random.choice(list(EVENT_TEMPLATES.keys()))
        event = create_event(event_name)
        apply_event_effect(game_state, event)
        game_state["modifiers_ongoing"].append(event)
        triggered.append(
            {
                "name": event["name"],
                "description": event["description"],
                "duration": event["duration"],
            }
        )
    game_state["recent_events"] = triggered
    return triggered


def tick_events(game_state):
    active_events = []
    for event in game_state["modifiers_ongoing"]:
        event["remaining_duration"] -= 1
        if event["remaining_duration"] <= 0:
            remove_event_effect(game_state, event)
        else:
            active_events.append(event)
    game_state["modifiers_ongoing"] = active_events


def highway_ability(game_state, building_dict):
    building_dict["highway"]["count"] += 1
    game_state["score"] += 2.0 * building_dict["highway"]["count"]
    game_state["city_point_generation"] += 0.4 * building_dict["highway"]["count"]


def restaurant_ability(game_state, building_dict):
    herbivore_loss = 10.0 * building_dict["restaurant"]["count"]
    game_state["animals"]["herbivores"]["count"] = max(
        game_state["animals"]["herbivores"]["count"] - herbivore_loss,
        0.0,
    )


def apply_building_choice(game_state, building_name):
    building_dict = game_state["building_dict"]
    building_key = building_name.strip().lower()

    if game_state["gameover"]:
        return False, "The game is over. Start a new game to keep playing."
    if building_key not in building_dict:
        return False, "Invalid input, please try again."
    if not building_dict[building_key]["chosen"]:
        return False, "Building not available this round, see above for valid choices."

    building = building_dict[building_key]
    game_state["last_building"] = building_key
    game_state["city_pollution_production"] += building["pollution"]
    game_state["score"] += building["score"] * game_state["score_multiplier"]
    game_state["city_point_generation"] += building["score"] * 0.2
    game_state["city_water_net"] += building["water"]

    if building_key == "highway":
        highway_ability(game_state, building_dict)
    else:
        building["count"] += 1

    if building_key == "restaurant":
        restaurant_ability(game_state, building_dict)
    if building_key == "skyscraper":
        game_state["score_multiplier"] += 0.1

    advance_round(game_state)
    if not game_state["gameover"]:
        game_state["round"] += 1
        pick_available_buildings(game_state)
    return True, f"{building_key.title()} built."


def advance_round(game_state):
    trigger_random_events(game_state)

    game_state["temp"] = random.randrange(
        int(70 + game_state["pollution"] * 0.95),
        int(100.0 + game_state["pollution"] * 1.25) + 1,
        1,
    )
    game_state["light_level"] = random.randrange(
        max(int(80 - game_state["pollution"] * 0.8), 10),
        max(int(120 - game_state["pollution"]), 20) + 1,
        1,
    )

    plants = game_state["animals"]["plants"]["count"]
    pollution_factor = max(0.0, 1.0 - game_state["pollution"] * game_state["POLLUTION_EFFECT_FACTOR"])

    game_state["water_level"] -= (
        game_state["ORGANIC_WATER_NEED"] * plants * game_state["temp"] * 0.01
    )
    game_state["water_level"] += (
        game_state["WATER_REPLENISH_RATE"] + game_state["city_water_net"]
    ) * pollution_factor
    game_state["organic_matter"] -= game_state["ORGANIC_MATTER_NEED"] * plants
    game_state["organic_matter"] += (
        game_state["ORGANICS_REPLENISH_RATE"] + game_state["city_organics_production"]
    ) * pollution_factor
    game_state["score"] += game_state["city_point_generation"] * game_state["score_multiplier"]

    game_state["pollution"] = max(
        game_state["pollution"] + game_state["city_pollution_production"],
        0.0,
    )

    grown = (
        game_state["PLANT_GROWTH_FACTOR"]
        * (game_state["light_level"] * 0.01)
        * plants
        * pollution_factor
    )
    game_state["animals"]["plants"]["count"] += grown

    if game_state["building_dict"]["restaurant"]["count"] > 0:
        restaurant_ability(game_state, game_state["building_dict"])

    for index, animal_name in enumerate(ANIMAL_ORDER):
        count = game_state["animals"][animal_name]["count"]
        natural_deaths = game_state["BASE_DEATH_RATE"] * count * (
            game_state["pollution"] * game_state["POLLUTION_EFFECT_FACTOR"] + 1
        )
        count -= natural_deaths * pollution_factor
        game_state["organic_matter"] += natural_deaths

        if index < len(ANIMAL_ORDER) - 1:
            prey_name = ANIMAL_ORDER[index + 1]
            prey_count = game_state["animals"][prey_name]["count"]
            count += (
                game_state["ENERGY_TRANSFER_EFFICIENCY"]
                * game_state["PREDATION_RATE"]
                * prey_count
            )

        if index > 0:
            predator_name = ANIMAL_ORDER[index - 1]
            predator_count = game_state["animals"][predator_name]["count"]
            eaten = game_state["PREDATION_RATE"] * predator_count
            count -= eaten
            game_state["organic_matter"] += eaten * pollution_factor

        game_state["animals"][animal_name]["count"] = count

        if count <= 0:
            game_state["gameover"] = True
            game_state["lose_reason"] = (
                f"The {animal_name.replace('_', ' ')} population has collapsed. "
                "The ecosystem is incapable of sustaining life without human rebalancing."
            )

    if game_state["pollution"] > 100:
        game_state["gameover"] = True
        game_state["lose_reason"] = "The ecosystem is too toxic to support life."
    elif game_state["water_level"] < 0:
        game_state["gameover"] = True
        game_state["lose_reason"] = "The ecosystem has run out of clean water."
    elif game_state["organic_matter"] < 0:
        game_state["gameover"] = True
        game_state["lose_reason"] = "The ecosystem has exhausted its organic matter reserves."

    tick_events(game_state)

    if game_state["gameover"]:
        game_state["status"] = "Game Over"
        game_state["available_buildings"] = []
        for stats in game_state["building_dict"].values():
            stats["chosen"] = False


def serialize_game_state(game_state):
    return {
        "round": game_state["round"],
        "score": round(game_state["score"], 1),
        "score_multiplier": round(game_state["score_multiplier"], 2),
        "status": game_state["status"],
        "gameover": game_state["gameover"],
        "lose_reason": game_state["lose_reason"],
        "pollution": round(game_state["pollution"], 1),
        "water_level": round(game_state["water_level"], 1),
        "temperature": round(game_state["temp"], 1),
        "light_level": round(game_state["light_level"], 1),
        "organic_matter": round(game_state["organic_matter"], 1),
        "city_pollution_production": round(game_state["city_pollution_production"], 1),
        "city_water_net": round(game_state["city_water_net"], 1),
        "city_point_generation": round(game_state["city_point_generation"], 1),
        "animals": {
            name: round(data["count"], 1)
            for name, data in game_state["animals"].items()
        },
        "available_buildings": [
            {
                "name": name,
                "pollution": game_state["building_dict"][name]["pollution"],
                "score": game_state["building_dict"][name]["score"],
                "water": game_state["building_dict"][name]["water"],
                "ability": game_state["building_dict"][name]["ability"],
                "count": game_state["building_dict"][name]["count"],
            }
            for name in game_state["available_buildings"]
        ],
        "built_counts": {
            name: stats["count"] for name, stats in game_state["building_dict"].items()
        },
        "recent_events": game_state["recent_events"],
        "active_events": [
            {
                "name": event["name"],
                "description": event["description"],
                "remaining_duration": event["remaining_duration"],
            }
            for event in game_state["modifiers_ongoing"]
        ],
        "last_building": game_state["last_building"],
    }


if __name__ == "__main__":
    state = reset_game_state()
    print("Starting local console test.")
    while not state["gameover"]:
        print(serialize_game_state(state))
        choice = input("Choose a building: ")
        ok, message = apply_building_choice(state, choice)
        print(message)
    print(state["lose_reason"])

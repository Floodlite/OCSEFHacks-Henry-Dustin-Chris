import random

score = 0
gameover = False
pollution = 0
temp = 100
light_level = 100
water_level = 100
organic_matter = 100000

plants = 10000
herbivores = 1000
carnivores = 100
apex_predators = 10

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
    print("Plants alive: " + str(plants))
    print("Herbivores alive: " + str(herbivores))
    print("Carnivores alive: "  + str(carnivores))
    print("Apex predators alive: " + str(apex_predators))
    print("========================")

"""
def pick_available_buildings(dict, available_choices=3):
    building_names = []
    for item in dict:
        building_names.append(item)

    total_buildings = len(building_names)
    for i in range(available_choices):
        chosen_index = ""
"""

while gameover == False:
    # game loop

    print_stats()
    # player choices
    while(True):
        player_input = input("Choose your building (enter 'view' to see choices): ")
        player_input = player_input.lower()
        if(player_input == "view"):
            print_dict(building_dict)
            continue
        try:
            pollution += building_dict[player_input]["pollution"]
            score += building_dict[player_input]["score"]
            break
        except KeyError:
            print("Invalid choice, try again")
            continue


    # filler text and display graphics
    print("Score: " + str(score))

# endgame psa
import random

round = 1
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
    print("Plants alive: " + str(plants))
    print("Herbivores alive: " + str(herbivores))
    print("Carnivores alive: "  + str(carnivores))
    print("Apex predators alive: " + str(apex_predators))
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
    # game loop

    # player choices
    print("**** Round " + str(round) + " ****")
    print_stats()
    pick_available_buildings(building_dict, 1)
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
score = 0
gameover = False
pollution = 0
temp = 100
light_level = 100
water_level = 100
organic_matter = 100000

plants = 10000,
herbivores = 1000,
carnivores = 100,
apex_predators = 10

building_dict = {
    "Factory": {
        "pollution": 100,
        "score": 20,
    },
    "Park": {
        "pollution": -20,
        "score": -5,
    }
}

def print_dict(dict):
    for item in dict:
        print("_________________________")
        print(item)
        print("Pollution: " + str(dict[item]["pollution"]))
        print("Score: " + str(dict[item]["score"]))


def print_stats():
    print("Score: " + str(score))
    print("Pollution: " + str(pollution))
    print("Temperature: " + str(temp))
    print("Light Level: " + str(light_level))
    print("Water Level: " + str(water_level))
    print("========================")
    print("Plants alive: " + str(plants))
    print("Herbivores alive: " + str(herbivores))
    print("Carnivores alive: "  + str(carnivores))
    print("Apex predators alive: " + str(apex_predators))

while gameover == False:
    # game loop

    # player choices
    while(True):
        player_input = input("Choose your building (enter 'view' to se choices): ")
        if(player_input == "view"):
            print_dict(building_dict)
            continue
        try:
            pollution += building_dict["pollution"]
            score += building_dict["score"]
        except KeyError:
            print("Invalid choice")
            continue


    # filler text and display graphics
    print("Score: " + str(score))

# endgame psa
score = 0
gameover = False
lose_reason = ""
pollution = 0
temp = 100
light_level = 100
water_level = 1000000
organic_matter = 100000
water_toxicity = 0 # pollution bleedthrough + user buildings

animals = [ # order matters, top predates on next level
    {"name": "apex_predators", "count": 10},
    {"name": "carnivores", "count": 100},
    {"name": "herbivores", "count": 1000},
    {"name": "plants", "count": 10000}
]

ORGANIC_WATER_NEED = 0.01
SUNLIGHT_GROWTH_FACTOR = 0.01
WATER_REPLENISH_RATE = 1000 # aquifers, rain, natural sources
ENERGY_TRANSFER_EFFICENCY = 0.1 # how much energy is transferred from one trophic level to the next
POLLUTION_EFFECT_FACTOR = 0.01
BASE_DEATH_RATE = 0.01
city_water_net = 0 # you can add pumps later to increase this, or drain it with consumption
city_pollution_production = 0 # buildings affect

# todo: forgot what, come back later

while gameover == False:
    # game loop
    water_level -= organic_matter * ORGANIC_WATER_NEED * SUNLIGHT_GROWTH_FACTOR * plants
    water_level += WATER_REPLENISH_RATE + city_water_net
    plants += SUNLIGHT_GROWTH_FACTOR * plants
    if water_level < 0:
        gameover = True
        lose_reason = "The ecosystem has no more clean water. All life has perished."
    for animal_dict in animals:
        animal = animal_dict["name"]
        count = animal_dict["count"]
        count -= BASE_DEATH_RATE * count * (pollution * POLLUTION_EFFECT_FACTOR + 1)
        animal_dict["count"] = count
    # player choices
    # filler text and display graphics
    print("Score: " + str(score))

# endgame psa
# DONT TOUCH
from RREngine import *

engine = RRE()

xClassCar = engine.loadCar("5c8f386c-47f1-4ac8-8160-7b4ed936fb85")

xClassCar2 = engine.genCar("X")

tracks = engine.loadedTracks()
print(tracks)

race = engine.initRace([xClassCar, xClassCar2], tracks[randint(0, len(tracks)-1)], 10)

# print(race.info(True))

# print(xClassCar.stats())
print(race.info(True))
race.race()

file = open("raceResults.json", "w")
file.write(race.rawResults(True))
file.close()
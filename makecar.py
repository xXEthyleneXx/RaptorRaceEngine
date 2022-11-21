# Raptor Race Engine
import RREngine
import sqlite3
import json
# Make a car from the preset classes
engine = RREngine.RRE()

def main():

    carClass = getClass()
    carnum = int(input("Number of cars? : "))

    for num in range(0, carnum+1):
        make_car(carClass)



def getClass():
    classes = json.loads(open("classes.json", "r").read())
    classkeys = classes.keys()
    while True:
        print('Enter a car class [D,C,B,A,S,X]?')
        userInput = input(": ")
        if userInput.upper() in classkeys:
            return userInput.upper()
        else:
            print('Invalid Car Class')
        
def make_car(carClass):
    car = engine.genCar(carClass)
    carstats = car.stats()
    db = sqlite3.connect('cars/cars.sqlite')
    dc = db.cursor()
    dc.execute(f"""INSERT INTO cars (uuid, speed, acceleration, braking, traction, creationDate, class) VALUES ("{carstats["uuid"]}", {carstats["speed"]}, {carstats["acceleration"]}, {carstats["braking"]}, {carstats["traction"]}, "{carstats["creationDate"]}", "{carstats["class"]}")""")
    db.commit()
    db.close()

if __name__ == "__main__":
    main()
# DONT TOUCH
# Raptor Race Engine for dragQueenRacing Devon Edwards 11.3.2022

import json
import logging
import time
import datetime
from random import randint
from cryptography.fernet import Fernet
import uuid
import os
import sqlite3

# RaptorRaceEngine
class RRE(object):

    _classes = None
    _trackLib = None

    def __init__(self):
        # Setting Up Logging
        logging.basicConfig(filename="RRE.log", filemode="w", level=logging.DEBUG)

        # Loading Class Defaults from Class File
        starttime = time.time()
        logging.info("[RRE][__init__] Loading Classes")
        self._classes = json.loads(open("classes.json", "r").read())
        endtime = time.time()
        logging.info(f"[RRE][__init__] {len(self._classes)} Classes Loaded in {round(endtime-starttime, 4)} Sec")

        # Loading Track Libaray from trackLib File
        starttime = time.time()
        logging.info("[RRE][__init__] Loading TrackLib")
        self._trackLib = json.loads(open("../trackLib.json", "r").read())
        endtime = time.time()
        logging.info(f"[RRE][__init__] {len(self._trackLib['tracks'])} Tracks Loaded {len(self._trackLib['tSections'])} Track Sections loaded in {round(endtime-starttime, 4)}")

    def loadedClasses(self):
        # Return Classes List
        return list(self._classes.keys())

    def loadedTracks(self):
        # Returns Tracks List
        return list(self._trackLib["tracks"].keys())

    def loadedTSections(self):
        # Returns tSections List
        return list(self._trackLib["tSections"].keys())

    def genCar(self, cClass):
        rrc = RRC()
        status = rrc._genCar(cClass)
        if status == True:
            return rrc
        else:
            return False

    def loadCar(self, carUUID):
        rrc = RRC()
        status = rrc._loadCar(carUUID)
        if status == True:
            return rrc
        else:
            return False
    def saveCar(self, car):
        if isinstance(car, RRC):
            car._saveCar()
            return True
        else:
            return False

    def initRace(self, cars, track, laps):
        logging.info("[RRE][initRace] Starting raceCars")
        if isinstance(cars, list):
            logging.info(f"[RRE][initRace] Cars Valid Type")
            if isinstance(track, str):
                logging.info(f"[RRE][initRace] Track Valid Type")
                if isinstance(laps, int):
                    logging.info(f"[RRE][initRace] Laps Valid Type")
                    if laps > 0:
                        logging.info(f"[RRE][initRace] Settings Laps to {laps}")
                    else:
                        logging.error(f"[RRE][initRace] Laps can't be less than One")
                        return False
                    if track in self._trackLib["tracks"]:
                        logging.info(f"[RRE][initRace] Setting Track to {track}")
                    else:
                        logging.error(f"[RRE][initRace] Invalid Track Name {track}")
                        return False
                    cCount = 1
                    for car in cars:
                        logging.info(f"[RRE][initRace] Testing Car {cCount}")
                        if isinstance(car, RRC):
                            logging.info(f"[RRE][initRace] Car {car.stats()} In Race")
                            cCount += 1
                        else:
                            logging.error(f"[RRE][initRace] Invalid Car {cCount}")
                            return False
                    race = RR()
                    status = race.raceSetup(cars, track, laps)
                    if status == True:
                        return race
                    else:
                        return False
            else:
                return False
        else:
            return False

# RaptorRaceCar
class RRC(RRE):

    _car = None

    def __init__(self):
        logging.info("[RRC][__init__] Initializing")
        RRE.__init__(self)
        logging.info("[RRC][__init__] Initialized")

    def _loadCar(self, carUUID):
            logging.info("[RRC][_loadCar] Starting loadCar")
            try:
                car = open(f"cars/{carUUID}/car.rrc").read()
                logging.info(f"[RRC][_loadCar] Opened cars/{carUUID}/car.rrc File")
            except FileNotFoundError:
                logging.error(f"[RRC][_loadCar] Failed to Open cars/{carUUID}/car.rrc File")
                return False
            try:
                key = open(f"cars/{carUUID}/car.key").read()
                logging.info(f"[RRC][_loadCar] Opened cars/{carUUID}/car.key File")
            except FileNotFoundError:
                logging.error(f"[RRC][_loadCar] Failed to Open cars/{carUUID}/car.key File")
                return False
            logging.info(f"[RRC][_loadCar] Enabling Encryption Key")
            ferent = Fernet(key.encode())
            logging.info(f"[RRC][_loadCar] Decrypting Car and Loading Stats")
            self._car = json.loads(ferent.decrypt(car.encode()).decode())
            logging.info(f"[RRC][_loadCar] Finished loadCar")
            return True

    def _saveCar(self):
        starttime = time.time()
        logging.info("[RRC][_saveCar] Starting saveCar")
        try:
            os.mkdir("cars")
            logging.info("[RRC][_saveCar] Created Folder cars/")
        except FileExistsError:
            logging.info("[RRC][_saveCar] Folder cars/ Exists")
            pass
        try:
            os.mkdir(f"cars/{self._car['uuid']}")
            logging.info(f"[RRC][_saveCar] Created Folder cars/{self._car['uuid']}/")
        except FileExistsError:
            logging.error(f"[RRC][_saveCar] Car {self._car['uuid']} Already Exists")
            return False
        

        data = json.dumps(self._car)
        logging.info(f"[RRC][_saveCar] Dumping Car Data into String")

        logging.info(f"[RRC][_saveCar] Generating Encryption Key")
        key = Fernet.generate_key()
        logging.info(f"[RRC][_saveCar] Enabling Encryption Key")
        fernet = Fernet(key)

        logging.info(f"[RRC][_saveCar] Creating cars/{self._car['uuid']}/car.key File")
        file = open(f"cars/{self._car['uuid']}/car.key", "w")
        logging.info(f"[RRC][_saveCar] Writing Encryption Key to cars/{self._car['uuid']}/car.key")
        file.write(key.decode())
        logging.info(f"[RRC][_saveCar] Saving cars/{self._car['uuid']}/car.key File")
        file.close()

        logging.info(f"[RRC][_saveCar] Encrypting Data")
        encData = fernet.encrypt(data.encode())
        logging.info(f"[RRC][_saveCar] Creating cars/{self._car['uuid']}/car.rrc File")
        file = open(f"cars/{self._car['uuid']}/car.rrc", "w")
        logging.info(f"[RRC][_saveCar] Writing Encrypted Data cars/{self._car['uuid']}/car.rrc File")
        file.write(encData.decode())
        logging.info(f"[RRC][_saveCar] Saving cars/{self._car['uuid']}/car.rrc File")
        file.close()
        endtime = time.time()
        logging.info(f"[RRC][_saveCar] saveCar Finished in {round(endtime-starttime, 3)} Sec")

        return True

    def _genCar(self, cClass):
        logging.info("[RRC][genCar] Starting Car Generation")
        if cClass.upper() in self._classes:
            cClass = cClass.upper()

            logging.info("[RRC][genCar] Aquiring Car Speed")
            carSpeed = self.__genCarValue(cClass)
            logging.info(f"[RRC][genCar] Car Speed {carSpeed}")

            logging.info("[RRC][genCar] Aquiring Car Acceleration")
            carAcceleration = self.__genCarValue(cClass)
            logging.info(f"[RRC][genCar] Car Acceleration {carAcceleration}")

            logging.info("[RRC][genCar] Aquiring Car Braking")
            carBraking = self.__genCarValue(cClass)
            logging.info(f"[RRC][genCar] Car Braking {carBraking}")

            logging.info("[RRC][genCar] Aquiring Car Traction")
            carTraction = self.__genCarValue(cClass)
            logging.info(f"[RRC][genCar] Car Traction {carTraction}")
            
            carUUID = str(uuid.uuid4())
            logging.info(f"[RRC][genCar] Finished Generation carUUID {carUUID}")
            self._car = {
                "c":cClass,
                "s":carSpeed,
                "a":carAcceleration,
                "b":carBraking,
                "t":carTraction,
                "uuid":carUUID,
                "creationDate":datetime.datetime.now().strftime("%x-%X")
            }
            return True
        else:
            logging.error("[RRC][genCar] Invalid cClass ID")
            return False
    
    def stats(self):
        return {
            "class":self._car["c"],
            "speed":self._car["s"]["valueValue"],
            "acceleration":self._car["a"]["valueValue"],
            "braking":self._car["b"]["valueValue"],
            "traction":self._car["t"]["valueValue"],
            "uuid":self._car["uuid"],
            "creationDate":self._car["creationDate"]
        }

    def __genCarValue(self, cClass):
        # Base Value
        bV = self._classes[cClass]
        # Value Percent Deviation
        vPD = randint(1, 40)
        # Value Percent Deviaiton Percent
        vPDPercent = vPD/100
        # Min Value
        minV = bV/2
        # Max Value
        maxV = bV+(minV*vPDPercent)
        # Value
        v = randint(bV*100, maxV*100)/100
        # Value Deviation
        vD = randint(0,1)
        if (vD == 0):
            vD = randint(1, 15)/100
        else:
            vD = (randint(1, 15)/100)*-1
        # Deviate Value
        dV = round(v+(v*vD), 3)
        # Value Value
        vV = round((dV/4)*0.25, 3)
        return {
            "baseValue":bV,
            "valuePercentDeviation":vPD,
            "valuePercentDeviationPercent":vPDPercent,
            "maxV":maxV,
            "value":v,
            "valueDeviation":vD,
            "deviateValue":dV,
            "valueValue":vV
        }
# RaptorRace
class RR(RRC):

    __cars = None
    __track = None
    __laps = None
    __results = None

    def __init__(self):
        RRC.__init__(self)
        
    def raceSetup(self, cars, track, laps):
        self.__cars = cars
        cStatus = self._setCars()
        self.__track = track
        tStatus = self._setTrack()
        self.__laps = laps
        lStatus = True
        if cStatus == True and tStatus == True and lStatus == True:
            return True
        else:
            return False

    def _setCars(self):
        cars = {}
        for car in self.__cars:
            cars[f"{car.stats()['uuid']}"] = car.stats()
        self.__cars = cars
        return True

    def _setTrack(self):
        self.__track = self._trackLib["tracks"][self.__track]
        return True

    def cars(self):
        return self.__cars
        
    def track(self):
        return self.__track

    def laps(self):
        return self.__laps

    def info(self, j=False):
        info = {
                "cars":self.__cars,
                "track":self.__track,
                "laps":self.__laps
            }
        if j == False:
            return info
        else:
            return json.dumps(info, indent=4)

    def race(self, iterations=2):
        allScores = {}
        iterations = range(0, iterations)
        for iteration in iterations:
            laps = range(0, self.__laps)
            lapScores = {}
            for lap in laps:
                sections = range(0, len(self.__track["sections"]))
                sectionScores = []
                for section in sections:
                    carScores = {}
                    for car in self.__cars:
                        score = {}
                        # Speed Calculator
                        deviationPercent = randint(0, 25)/100
                        if (randint(0, 1)) == 1:
                            deviationPercent = deviationPercent*-1
                        tSectionDefaults = self._trackLib["tSections"][self.__track["sections"][section]]
                        dS = tSectionDefaults["lib"][0]
                        Score = round(((self.__cars[car]["speed"] * dS)/10), 3)
                        ScoreAD = round(Score+(Score*deviationPercent), 3)
                        sD = round(ScoreAD-dS, 3)

                        score["speed"] = {}
                        score["speed"]["dP"] = deviationPercent
                        score["speed"]["dS"] = dS
                        score["speed"]["s"] = Score
                        score["speed"]["sAD"] = ScoreAD
                        score["speed"]["sD"] = sD

                        carScores[car] = score
                    sectionScores.append({f"{self.__track['sections'][section]}":carScores})
                lapScores[f"lap{lap}"] = sectionScores
            allScores[f"iter{iteration}"] = lapScores
        
        self.__results = allScores

    def rawResults(self, j=True):
        if self.__results != None:
            if j == True:
                return json.dumps(self.__results, indent=4)
            else:
                return self.__results
        else:
            return False
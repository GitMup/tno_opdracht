from abc import ABC
import pandas as pd
from frenemies import Friend, Foe
import random


class PatriotSubsystem(ABC):
    pass


class Radar(PatriotSubsystem):
    def __init__(self):
        self.readings = pd.read_csv("radar_data.csv",sep=';',header=None, dtype=str)

    def scan(self,time: int):
        """Scan the area for friend or foe for the given time step

        :return:
        """
        print("Warning, radar has detected a strange object!")
        return [int(reading,2) for reading in self.readings.iloc[time].values]

class MissileLauncher(PatriotSubsystem):
    def launch(self):
        """you pass butter

        :return:
        """
        pk_ratio = 0.8
        print("Launching missile...")
        if random.random() < pk_ratio:
            print("Foe destroyed, hooray!")
        else:
            print("Oh no, it was a miss!")


class IFF(PatriotSubsystem):
    def identify(self, radar_readings:list):
        """Identify friend or foe from radar reading at the given time step

        :param radar_readings:
             List of readings in binary format
        :return:
            Actor object specifying friend or foe
        """
        print("Identifying...")
        if sum([1 for reading in radar_readings if reading%2==0]) > len(radar_readings)/2:
            print("Foe detected, yikes!")
            return Foe()
        else:
            print("Friend detected, pfiew!")
            return Friend()


class Patriot:
    def __init__(self):
        self.radar = Radar()
        self.iff = IFF()
        self.missile_launcher = MissileLauncher()

    def react(self, time: int):
        """React to radar reading of a strange object at a certain time step

        :param time:
            the time step (row in radar_data.csv) to react to
        :return:
        """
        strange_object = self.iff.identify(self.radar.scan(time))
        if strange_object.code:
            self.missile_launcher.launch()




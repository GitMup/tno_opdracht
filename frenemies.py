from abc import ABC

class StrangeObjects(ABC):
    code  = None

class Friend(StrangeObjects):
    code = False

class Foe(StrangeObjects):
    code = True
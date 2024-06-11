import random
import logging
from abc import abstractmethod, ABC
from dataclasses import dataclass

from linecache import getline

logger = logging.getLogger("patriot")


@dataclass
class Target:
    """This class hold all information that the Radar, IFF and missile launcher need to know and set about a target."""

    scan_signature: list[str]
    disposition: str = "non hostile"
    action_taken: str = "no action taken"
    neutralized: str = "intact"

    def __str__(self):
        return f"A {self.disposition} flying object detected, {self.action_taken}, target {self.neutralized}."


class Sensor(ABC):
    """An abstract class for all different kind of sensors"""

    @abstractmethod
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        """Attach an observer to this Sensor

        :param observer:
            An observer that has to take action if this Sensor detects something
        :return:
        """
        self._observers.append(observer)

    def notify(self, target: Target):
        """Notify all observer that a target has been acquired

        :param target:
            Target object
        :return:
        """
        for observer in self._observers:
            observer.update(target)


class Radar(Sensor):
    """This is the radar. It holds the

    :param csv_path:
        Path to the csv file containing the radar readings
    """

    def __init__(self, csv_path: str):
        super().__init__()
        self.csv_path = csv_path

    def update(self, line) -> Target:
        """Scan the area for friend or foe for the given time step

        :return:
            Target object that has been detected by the radar
        """
        target = Target(line.strip("\n").split(";"))
        self.notify(target)
        return target


class IFF(Sensor):
    """This thing identifies whether a target is friendly or hostile"""

    def __init__(self):
        super().__init__()

    def update(self, target: Target):
        """Identify friend or foe from radar reading at the given time step

        :param target:
            Target object that has been detected by sensor
        """
        uneven = [int(number[-1]) for number in target.scan_signature]
        if sum(uneven) > 5:
            target.disposition = "hostile"
            self.notify(target)
        return target


class MissileLauncher:
    """This thing launches missiles at targets to try and neutralize them in case they are hostile.

    First tells the Target object which action was taken against it and then determines if it was destroyed based on
    a random number and a threshold.

    """

    pk_ratio = 0.8

    def update(
        self,
        target,
    ):
        """Launch a missile at a target.

        :param target:
            Target object to launch a missile at
        :return:
            The Target at which was launched
        """
        target.action_taken = "launched a missile"
        if random.random() <= self.pk_ratio:
            target.neutralized = "neutralized"
        else:
            target.neutralized = "failed to neutralize, please hide"
        return target

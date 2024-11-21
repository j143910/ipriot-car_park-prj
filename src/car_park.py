from sensor import Sensor
from display import Display
from pathlib import Path
from datetime import datetime
import json


class CarPark:
    """
    Provides a car park containing sensors displays and recording licence plates
    """
    def __init__(self, location="Unknown", capacity=0, plates=None, sensors=None,
                 displays=None, log_file=Path("log.txt"), config_file="config.json"):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []
        self.sensors = sensors or []
        self.displays = displays or []
        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)
        self.log_file.touch(exist_ok=True)
        self.config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        self.config_file.touch(exist_ok=True)

    def __str__(self):
        return f"Car park at {self.location}, with {self.capacity} bays"

    @property
    def available_bays(self):
        """
        Getter for available bays
        :return: returns number of bays or 0 if car park is full
        """
        return self.capacity - len(self.plates) if len(self.plates) < self.capacity else 0

    def register(self, component):
        """
        Adds a Sensor or Display to the car park
        :param component: Either a Sensor or Display object
        :return:
        """
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")
        elif isinstance(component, Sensor):
            self.sensors.append(component)
        elif isinstance(component, Display):
            self.displays.append(component)

    def _log_car_activity(self, plate, action):
        """
        Adds an action of a car and current time to log file
        :param plate: licence plate number
        :param action: entering or exiting
        :return:
        """
        with self.log_file.open("a") as f:
            f.write(f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    def add_car(self, plate):
        """
        Adds car to the car park
        :param plate: licence plate number
        :return:
        """
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, "entered")

    def remove_car(self, plate):
        """
        Removes car from the car park
        :param plate: licence plate number
        :return:
        """
        self.plates.remove(plate)
        self.update_displays()
        self._log_car_activity(plate, "exited")

    def update_displays(self):
        """
        Updates all displays in the car park
        :return:
        """
        # data to display on all displays
        data = {"available_bays": self.available_bays, "temperature": 25}
        for display in self.displays:
            display.update(data)

    def write_config(self):
        """
        Writes the car park config settings to a json file
        :return:
        """
        with open(self.config_file, "w") as f:
            json.dump({"location": self.location,
                        "capacity": self.capacity,
                        "log_file": str(self.log_file)}, f)

    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        """
        Create CarPark instance from a json file
        :param config_file: path to config file
        :return: A CarPark instance configured by a json file
        """
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(config["location"], config["capacity"], log_file=config["log_file"])


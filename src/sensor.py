from abc import ABC, abstractmethod
import random


class Sensor(ABC):
    """
    Abstract class for sensors
    """
    def __init__(self, id, car_park, is_active=False):
        self.id = id
        self.car_park = car_park
        self.is_active = is_active

    def __str__(self):
        return f"Sensor {self.id} is {'Active' if self.is_active else 'Inactive'}"

    def _scan_plate(self):
        """
        Scans car licence plate number
        :return:
        """
        # Generates a fake licence plate number
        return 'FAKE-' + format(random.randint(0, 999), "03d")

    def detect_vehicle(self):
        """
        Detects vehicle entry or exit
        :return:
        """
        plate = self._scan_plate()
        self.update_car_park(plate)

    @abstractmethod
    def update_car_park(self, plate):
        """
        Abstract method to add or remove a car from the car park
        :param plate: licence plate number
        :return:
        """
        pass


class EntrySensor(Sensor):
    def update_car_park(self, plate):
        """
        Adds a car to the car park
        :param plate: licence plate number
        :return:
        """
        self.car_park.add_car(plate)
        print(f"Incoming 🚘 vehicle detected. Plate: {plate}")


class ExitSensor(Sensor):
    def _scan_plate(self):
        """
        Override method to select a car from car park
        :return:
        """
        # select a random licence plate number from the car park
        return random.choice(self.car_park.plates)

    def update_car_park(self, plate):
        """
        Removes a car from the car park
        :param plate: licence plate number
        :return:
        """
        self.car_park.remove_car(plate)
        print(f"Outgoing 🚗 vehicle detected. Plate: {plate}")


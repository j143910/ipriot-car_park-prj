class Sensor:
    def __init__(self, id, car_park, is_active = False):
        self.id = id
        self.car_park = car_park
        self.is_active = is_active

    def __str__(self):
        return f"""Sensor {self.id} is {'Active' if self.is_active else 'Inactive' }"""

class EntrySensor(Sensor):
    ...

class ExitSensor(Sensor):
    ...
import unittest
from sensor import EntrySensor
from sensor import ExitSensor
from sensor import Sensor
from car_park import CarPark


class TestDisplay(unittest.TestCase):
    def setUp(self):
        self.car_park = CarPark("123 Example Street", 100, ["fake-123"])
        self.entry_sensor = EntrySensor(1, self.car_park, True)
        self.exit_sensor = ExitSensor(2, self.car_park, True)

    def test_entry_sensor_initialized_with_all_attributes(self):
        self.assertIsInstance(self.entry_sensor, Sensor)
        self.assertEqual(self.entry_sensor.id, 1)
        self.assertEqual(self.entry_sensor.car_park, self.car_park)
        self.assertEqual(self.entry_sensor.is_active, True)
        self.assertIsInstance(self.entry_sensor.car_park, CarPark)

    def test_exit_sensor_initialized_with_all_attributes(self):
        self.assertIsInstance(self.exit_sensor, Sensor)
        self.assertEqual(self.exit_sensor.id, 2)
        self.assertEqual(self.exit_sensor.car_park, self.car_park)
        self.assertEqual(self.exit_sensor.is_active, True)
        self.assertIsInstance(self.exit_sensor.car_park, CarPark)

    def test_entry_sensor_detect_vehicle(self):
        self.assertEqual(len(self.car_park.plates), 1)
        self.entry_sensor.detect_vehicle()
        self.assertEqual(len(self.car_park.plates), 2)

    def test_exit_sensor_detect_vehicle(self):
        self.assertEqual(len(self.car_park.plates), 1)
        self.exit_sensor.detect_vehicle()
        self.assertEqual(len(self.car_park.plates), 0)
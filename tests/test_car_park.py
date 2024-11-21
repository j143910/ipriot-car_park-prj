import unittest
from pathlib import Path
from car_park import CarPark


class TestCarPark(unittest.TestCase):
    def setUp(self):
        self.log_file_path = "new_log.txt"
        self.config_file_path = "config.json"
        self.car_park = CarPark("123 Example Street", 100, log_file=self.log_file_path, config_file=self.config_file_path)
        self.car_park.write_config()

    def test_car_park_initialized_with_all_attributes(self):
        self.assertIsInstance(self.car_park, CarPark)
        self.assertEqual(self.car_park.location, "123 Example Street")
        self.assertEqual(self.car_park.capacity, 100)
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.sensors, [])
        self.assertEqual(self.car_park.displays, [])
        self.assertEqual(self.car_park.available_bays, 100)
        self.assertEqual(self.car_park.log_file, Path(self.log_file_path))

    def test_add_car(self):
        self.car_park.add_car("FAKE-001")
        self.assertEqual(self.car_park.plates, ["FAKE-001"])
        self.assertEqual(self.car_park.available_bays, 99)

    def test_remove_car(self):
        self.car_park.add_car("FAKE-001")
        self.car_park.remove_car("FAKE-001")
        self.assertEqual(self.car_park.plates, [])
        self.assertEqual(self.car_park.available_bays, 100)

    def test_overfill_the_car_park(self):
        for i in range(100):
            self.car_park.add_car(f"FAKE-{i}")
        self.assertEqual(self.car_park.available_bays, 0)
        self.car_park.add_car("FAKE-100")
        # Overfilling the car park should not change the number of available bays
        self.assertEqual(self.car_park.available_bays, 0)

        # Removing a car from an overfilled car park should not change the number of available bays
        self.car_park.remove_car("FAKE-100")
        self.assertEqual(self.car_park.available_bays, 0)

    def test_removing_a_car_that_does_not_exist(self):
        with self.assertRaises(ValueError):
            self.car_park.remove_car("NO-1")

    def test_register_raises_type_error(self):
        with self.assertRaises(TypeError):
            self.car_park.register("Not a Sensor or Display")

    def test_log_file_created(self):
        new_carpark = CarPark("123 Example Street", 100, log_file=self.log_file_path)
        self.assertTrue(Path(self.log_file_path).exists())

    def test_car_logged_when_entering(self):
        new_carpark = CarPark("123 Example Street", 100, log_file=self.log_file_path)
        new_carpark.add_car("NEW-001")
        with new_carpark.log_file.open() as f:
            last_line = f.readlines()[-1]
        self.assertIn("NEW-001", last_line)  # check plate entered
        self.assertIn("entered", last_line)  # check description
        self.assertIn("\n", last_line)  # check entry has a new line

    def test_car_logged_when_exiting(self):
        new_carpark = CarPark("123 Example Street", 100, log_file=self.log_file_path)
        new_carpark.add_car("NEW-001")
        new_carpark.remove_car("NEW-001")
        with new_carpark.log_file.open() as f:
            last_line = f.readlines()[-1]
        self.assertIn("NEW-001", last_line)  # check plate entered
        self.assertIn("exited", last_line)  # check description
        self.assertIn("\n", last_line)  # check entry has a new line

    def test_initialize_car_park_with_json(self):
        new_carpark = CarPark.from_config(self.config_file_path)
        self.assertEqual(new_carpark.location, self.car_park.location)
        self.assertEqual(new_carpark.capacity, self.car_park.capacity)
        self.assertEqual(new_carpark.log_file, self.car_park.log_file)

    def tearDown(self):
        Path(self.log_file_path).unlink(missing_ok=True)
        Path(self.config_file_path).unlink(missing_ok=True)


if __name__ == "__main__":
   unittest.main()


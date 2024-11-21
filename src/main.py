from car_park import CarPark
from sensor import EntrySensor, ExitSensor
from display import Display


def main():
    car_park = CarPark("moondalup", 100, log_file="moondalup.log")
    entry_sensor = EntrySensor(1, car_park, True)
    exit_sensor = ExitSensor(2, car_park, True)
    display = Display(1, car_park, "Welcome to Moondalup", True)
    car_park.register(entry_sensor)
    car_park.register(exit_sensor)
    car_park.register(display)
    for _ in range(10):
        entry_sensor.detect_vehicle()
    for _ in range(2):
        exit_sensor.detect_vehicle()
    car_park.write_config()

if __name__ == '__main__':
    main()


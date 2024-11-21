class Display:
    """
    Provides a way to display car park info
    """
    def __init__(self, id, car_park, message="", is_on=False):
        self.id = id
        self.message = message
        self.is_on = is_on
        self.car_park = car_park

    def __str__(self):
        return f"Display {self.id}: {self.message}"

    def update(self, data):
        """
        Shows messages
        :param data: data to display
        :return:
        """
        if "message" in data:
            # Updates the display message
            self.message = data["message"]
        for key, value in data.items():
            print(f"{key}: {value}")


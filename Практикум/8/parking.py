
class Parking:
    def __init__(self, name: str, capacity: int):
        self.name = name
        self.capacity = capacity
        self.available_spots = list(range(1, capacity + 1))  # Список вільних місць
        self.occupied_spots = {}

    def is_full(self):
        return len(self.available_spots) == 0

    def assign_spot(self, vehicle):
        if not self.is_full():
            spot = self.available_spots.pop(0)
            self.occupied_spots[spot] = vehicle
            return spot
        return None

    def release_spot(self, spot):
        if spot in self.occupied_spots:
            del self.occupied_spots[spot]
            self.available_spots.append(spot)

    def __str__(self):
        return f"Parking {self.name}: {len(self.occupied_spots)}/{self.capacity} spots occupied."

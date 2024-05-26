class VehicleType:
    """
    Represents a vehicle type with name, capacity, and cost per kilometer.
    """
    def __init__(self, name: str, capacity: int, cost_per_km: float):
        self.name = name
        self.capacity = capacity
        self.cost_per_km = cost_per_km
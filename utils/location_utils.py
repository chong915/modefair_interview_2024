class CustomerLocation:
    """
    Represents a customer location with coordinates, demand, and ID.
    """
    def __init__(self, customer_id: str, latitude: float, longitude: float, demand: int):
        self.customer_id = customer_id
        self.latitude = latitude
        self.longitude = longitude
        self.demand = demand


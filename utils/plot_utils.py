import matplotlib.pyplot as plt
from typing import Dict
from utils.location_utils import CustomerLocation
from utils.vehicle_utils import VehicleType


def plot_locations(locations: Dict[str, CustomerLocation]) -> None:
    """
    Plots the initial locations of customers and depot.

    Args:
    locations (dict): A dictionary of CustomerLocation objects.
    """
    plt.figure(figsize=(10, 5))
    for loc in locations.values():
        plt.scatter(loc.latitude, loc.longitude, s=100)
        plt.text(loc.latitude, loc.longitude, f'{loc.customer_id} ({loc.demand})', fontsize=12, ha='right')

    depot = locations["Depot"]
    plt.scatter(depot.latitude, depot.longitude, c='red', s=100)  # Highlight depot
    plt.text(depot.latitude, depot.longitude, f'{depot.customer_id} ({depot.demand})', fontsize=12, ha='right', color='red')
    plt.title('Customer Locations')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.grid()
    plt.show()


def plot_optimized_routes(routes: Dict[tuple, Dict[str, list]], vehicle_types_dict: Dict[str, VehicleType], locations: Dict[str, CustomerLocation]) -> None:
    """
    Plots the optimized routes.

    Args:
    routes (dict): Dictionary containing route information.
    vehicle_types_dict (dict): Dictionary containing VehicleType objects.
    locations (dict): Dictionary containing CustomerLocation objects.
    """
    plt.figure(figsize=(10, 5))
    vehicle_colors = {vehicle: color for vehicle, color in zip(vehicle_types_dict.keys(), ['b', 'g', 'r', 'c', 'm', 'y', 'k'])}

    # Plot depot
    depot = locations["Depot"]
    plt.scatter(depot.latitude, depot.longitude, c='red', s=100, label='Depot')

    plotted_vehicle_types = set()  # To keep track of which vehicle types have been added to the legend

    for route_info in routes.values():
        route = route_info["route"]
        vehicle = route_info["vehicle"].name
        color = vehicle_colors[vehicle]
        route_points = [locations[str(location_id)] for location_id in route]  # Convert IDs to strings
        latitudes = [depot.latitude] + [point.latitude for point in route_points] + [depot.latitude]
        longitudes = [depot.longitude] + [point.longitude for point in route_points] + [depot.longitude]

        if vehicle not in plotted_vehicle_types:
            plt.plot(latitudes, longitudes, color, marker='o', label=vehicle)
            plotted_vehicle_types.add(vehicle)
        else:
            plt.plot(latitudes, longitudes, color, marker='o')

    plt.title('Optimized Routes')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    plt.legend()
    plt.grid()
    plt.show()  # This will keep the plot window open

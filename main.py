import matplotlib.pyplot as plt
import numpy as np
from typing import Dict, List, Tuple

import argparse

from utils.plot_utils import plot_optimized_routes, plot_locations
from utils.distance_utils import calculate_distance, is_symmetric
from utils.location_utils import CustomerLocation
from utils.vehicle_utils import VehicleType
from data.locations import locations
from data.vehicle_types import vehicle_types


class CombinedSavingsAlgorithm:
    """
    Implements the Combined Savings Algorithm for optimizing vehicle routes.
    """
    def __init__(self, locations: Dict[str, CustomerLocation], vehicle_types: Dict[str, VehicleType], pause_interval: float):
        self.locations = locations
        self.vehicle_types = vehicle_types
        self.location_keys = list(locations.keys())
        self.cost_matrix = self.calculate_cost_matrix()
        self.pause_interval = pause_interval

        # Initialize routes and vehicles
        self.routes = {tuple([i + 1]): {"route": [i + 1], "vehicle": self.find_smallest_vehicle(locations[self.location_keys[i + 1]].demand)} for i in range(len(locations) - 1)}
        self.merge_count = 0

    def calculate_cost_matrix(self) -> np.ndarray:
        """
        Calculates the cost matrix (distance matrix) for all locations.

        Returns:
        np.ndarray: The cost matrix.
        """
        n_customers = len(self.locations)
        cost_matrix = np.zeros((n_customers, n_customers))

        for i in range(n_customers):
            for j in range(n_customers):
                loc1 = self.locations[self.location_keys[i]]
                loc2 = self.locations[self.location_keys[j]]
                cost_matrix[i][j] = calculate_distance(loc1, loc2)

        return cost_matrix

    def find_smallest_vehicle(self, demand: int) -> VehicleType:
        """
        Finds the smallest vehicle that can handle the given demand, sorted by cost per kilometer.

        Args:
        demand (int): The demand to be handled.

        Returns:
        VehicleType: The smallest vehicle that can handle the demand.
        """
        sorted_vehicle_types = sorted(self.vehicle_types.values(), key=lambda v: v.cost_per_km)
        for vehicle in sorted_vehicle_types:
            if demand <= vehicle.capacity:
                return vehicle
        return None

    def calculate_route_distance(self, route: List[int]) -> float:
        """
        Calculates the total distance of a given route.

        Args:
        route (list): The route to calculate the distance for.

        Returns:
        float: The total distance of the route.
        """
        distance = 0
        for i in range(len(route) - 1):
            distance += self.cost_matrix[route[i]][route[i + 1]]
        distance += self.cost_matrix[0][route[0]] + self.cost_matrix[route[-1]][0]
        return distance

    def combine_routes(self, route1: List[int], route2: List[int]) -> List[int]:
        """
        Combines two routes into the best possible route by minimizing the distance.

        Args:
        route1 (list): The first route.
        route2 (list): The second route.

        Returns:
        list: The best combined route.
        """
        # Create four possible merged routes
        merged_routes = [
            list(route1) + list(route2),
            list(route2) + list(route1),
            list(route1)[::-1] + list(route2),
            list(route1) + list(route2)[::-1],
        ]

        # Find the merged route with the minimum total distance
        min_distance = float('inf')
        best_route = None
        for route in merged_routes:
            distance = self.calculate_route_distance(route)
            if distance < min_distance:
                min_distance = distance
                best_route = route
        return best_route

    def optimize_routes(self) -> None:
        """
        Optimizes the routes by combining them based on savings.
        """
        n_customers = len(self.locations) - 1  # excluding depot
        savings = []

        # Calculate savings for combining routes
        print("Calculating savings for combining routes:")
        for i in range(n_customers):
            for j in range(i + 1, n_customers):
                savings_ij = self.cost_matrix[0][i + 1] + self.cost_matrix[0][j + 1] - self.cost_matrix[i + 1][j + 1]
                savings.append((savings_ij, i + 1, j + 1))

        # Sort savings in descending order
        savings.sort(reverse=True, key=lambda x: x[0])

        # Combine routes based on savings
        print("\nCombining routes based on savings:")
        for saving, i, j in savings:
            print(f"\nCurrently processing savings for combining routes {i} and {j} with saving {saving:.3f} km...")
            print("----------------------------------------------------------")
            # Find the routes containing customers i and j
            route_i_key = next((key for key, value in self.routes.items() if i in value["route"]), None)
            route_j_key = next((key for key, value in self.routes.items() if j in value["route"]), None)

            if route_i_key and route_j_key and route_i_key != route_j_key:
                route_i = self.routes[route_i_key]["route"]
                route_j = self.routes[route_j_key]["route"]

                print(f"Routes {route_i} and {route_j} are considered for merging.")
                total_demand = sum(self.locations[self.location_keys[customer]].demand for customer in route_i + route_j)
                combined_vehicle = self.find_smallest_vehicle(total_demand)
                if not combined_vehicle:
                    print(f"Skipping combination of routes {route_i} and {route_j} due to insufficient vehicle capacity.")
                    continue  # Skip if no vehicle can handle the combined demand

                best_route = self.combine_routes(route_i, route_j)
                original_distance_i = self.calculate_route_distance(route_i)
                original_distance_j = self.calculate_route_distance(route_j)
                original_cost = (original_distance_i * self.routes[route_i_key]["vehicle"].cost_per_km +
                                 original_distance_j * self.routes[route_j_key]["vehicle"].cost_per_km)
                new_cost = self.calculate_route_distance(best_route) * combined_vehicle.cost_per_km

                print(f"Best merged route: {best_route}")
                print(f"Original distance for route {route_i}: {original_distance_i:.3f} km")
                print(f"Original distance for route {route_j}: {original_distance_j:.3f} km")
                print(f"Original cost for routes {route_i} and {route_j}: RM {original_cost:.2f}")
                print(f"New cost for merged route {best_route}: RM {new_cost:.2f}")

                if new_cost < original_cost:
                    # Combine routes if it reduces the cost
                    print(f"Merging route {route_i} and route {route_j} into {best_route} with vehicle {combined_vehicle.name}")
                    del self.routes[route_i_key]
                    del self.routes[route_j_key]
                    self.routes[tuple(best_route)] = {"route": best_route, "vehicle": combined_vehicle}
                    self.plot_current_routes()
                else:
                    print(f"No cost reduction achieved by merging routes {route_i} and {route_j}.")
            print("----------------------------------------------------------")

    def plot_current_routes(self) -> None:
        """
        Plots the current state of routes during the optimization process.
        """
        self.merge_count += 1
        plt.figure(figsize=(10, 8))
        vehicle_colors = {vehicle: color for vehicle, color in zip(self.vehicle_types.keys(), ['b', 'g', 'r', 'c', 'm', 'y', 'k'])}

        # Plot depot
        depot = self.locations["Depot"]
        plt.scatter(depot.latitude, depot.longitude, c='red', s=100, label='Depot')

        # Keep track of plotted vehicle types for legend
        plotted_vehicle_types = set()

        for route_info in self.routes.values():
            route = route_info["route"]
            vehicle = route_info["vehicle"].name
            color = vehicle_colors[vehicle]
            route_points = [self.locations[self.location_keys[stop]] for stop in route]
            latitudes = [depot.latitude] + [point.latitude for point in route_points] + [depot.latitude]
            longitudes = [depot.longitude] + [point.longitude for point in route_points] + [depot.longitude]

            if vehicle not in plotted_vehicle_types:
                plt.plot(latitudes, longitudes, color, marker='o', label=vehicle)
                plotted_vehicle_types.add(vehicle)
            else:
                plt.plot(latitudes, longitudes, color, marker='o')

        plt.title(f'Current Routes After Merge {self.merge_count}')
        plt.xlabel('Latitude')
        plt.ylabel('Longitude')
        plt.legend()
        plt.grid()
        plt.pause(self.pause_interval)  # Use plt.pause() for non-blocking plots
        plt.close()  # Close the figure to avoid too many open figures


    def print_optimized_routes(self) -> None:
        """
        Prints the optimized routes, their distances, and costs.
        """
        total_distance = 0
        total_cost = 0
        route_details = []

        for idx, route_info in enumerate(self.routes.values(), start=1):
            route = route_info["route"]
            vehicle = route_info["vehicle"]
            route_distance = self.calculate_route_distance(route)
            route_cost = route_distance * vehicle.cost_per_km
            total_distance += route_distance
            total_cost += route_cost
            demand = sum(self.locations[self.location_keys[customer]].demand for customer in route)
            
            route_str = f"Vehicle {idx} ({vehicle.name}):\n"
            route_str += f"Round Trip Distance: {route_distance:.3f} km, Cost: RM {route_cost:.2f}, Demand: {demand}\n"
            route_str += f"Depot"
            for i in range(len(route)):
                next_stop = self.location_keys[route[i]]
                if i == 0:
                    route_str += f" -> {next_stop} ({self.cost_matrix[0][route[i]]:.3f} km)"
                else:
                    route_str += f" -> {next_stop} ({self.cost_matrix[route[i-1]][route[i]]:.3f} km)"
            route_str += f" -> Depot ({self.cost_matrix[route[-1]][0]:.3f} km)\n"
            route_details.append(route_str)
        
        print('\n\n--------------------------------------------------')
        print(f"Total Distance = {total_distance:.3f} km")
        print(f"Total Cost = RM {total_cost:.2f}")
        for route_detail in route_details:
            print(route_detail)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Optimize vehicle routes using the Combined Savings Algorithm")
    parser.add_argument('--pause-interval', type=float, default=1.0, help="Pause interval for plotting each route merge")
    args = parser.parse_args()

    # Run the plotting function
    plot_locations(locations)

    # Create an instance of the algorithm and optimize routes
    algorithm = CombinedSavingsAlgorithm(locations, vehicle_types, args.pause_interval)
    algorithm.optimize_routes()
    algorithm.print_optimized_routes()

    # Plot the optimized routes
    plot_optimized_routes(algorithm.routes, vehicle_types, locations)
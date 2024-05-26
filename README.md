# ModeFair Take Home Assessment

## Directory Structure
```
project/
│
├── data/
│ ├── locations.py
│ └── vehicle_types.py
│
├── utils/
│ ├── init.py
│ ├── plot_utils.py
│ ├── distance_utils.py
│ └── vehicle_utils.py
│
├──.gitignore
├── README.md 
├── main.py
└── requirements.txt
```



## Problem Definition

### Background

You are a logistics manager for a delivery company tasked with optimizing the routing of a fleet of vehicles to efficiently deliver goods to various customer locations. Your goal is to optimize the delivery cost while ensuring that all delivery locations are visited and all demands are met.

### Task

Your task is to develop an algorithm or program that attempts to find the best route for a fleet of vehicles of different types so that the deliveries are completed at the lowest cost while satisfying all hard constraints.

### Important Notes

- Ensure that your solution is dynamic and scalable to support a larger number of customers beyond the provided test data. During the interview, you might be asked to add more customers to the test dataset (e.g., adding one more customer to the list or adding one more row of data if you are importing the dataset from a file).
- Your solution should be able to select the type of vehicle for each route to minimize the cost.

### Requirements

#### Hard Constraints

- Each delivery location must be visited exactly once.
- The total demand of each vehicle route must not exceed its maximum capacity.

#### Soft Constraints

- Minimize the cost required to meet all demands.

#### Assumptions

- The vehicles start and end their routes at the same depot location.
- Each vehicle only travels one round trip (depart from the depot and back to the depot).
- There is no limit on the number of vehicles.
- Travel times between any two locations are the same in both directions.
- Deliveries can be made at any time; there are no time windows for deliveries.
- Vehicle travel distance is calculated using the Euclidean distance formula:
$${Distance(km)} = 100 \times \sqrt{(\text{Longitude}_2 - \text{Longitude}_1)^2 + (\text{Latitude}_2 - \text{Latitude}_1)^2}$$

## Proposed Algorithm

I'm using the Combined Savings (CS) algorithm to solve the Fleet Size and Mix Vehicle Routing Problem (FSMVRP). This algorithm is an extension of the Clarke and Wright Savings algorithm, adapted to consider the varying costs and capacities of different vehicle types. Here's a brief description of how it works:

1. **Initialization**:
   - Each customer is initially assigned to a separate route, serviced by the smallest vehicle that can handle their demand.

2. **Savings Calculation**:
   - Calculate the savings for combining each pair of routes. The savings is defined as the reduction in the total travel distance when two routes are combined into one.

3. **Combine Routes**:
   - Iteratively combine routes in the order of the highest savings, ensuring that the combined demand does not exceed the capacity of the chosen vehicle.

4. **Vehicle Selection**:
   - For each combined route, select the smallest vehicle that can handle the total demand to minimize the cost.

5. **Optimization**:
   - The process continues until no more feasible combinations can be made that reduce the overall cost.

## Paper Reference

The methodology implemented in this project is based on the paper:

**The Fleet Size and Mix Vehicle Routing Problem**  
*Bruce Golden, Arjang Assad, Larry Levy, Filip Gheysens*  
University of Maryland at College Park, College Park, MD 20742, U.S.A.


## How to Run

To run the FSMVRP solver with various arguments, follow these steps:

1. Ensure you have Python installed on your system. (I'm using Python 3.11.6)
2. Install the required packages using the following command:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the `main.py` script with the desired arguments:

### Arguments
- `--pause-interval`: Set the pause interval for plotting each route merge (default is `0.1` seconds).


### Example Usage
```bash
python main.py --pause-interval 1
```

### Example Input Data
`data/locations.py`

Dictionary Structure:
- `Customer_id`: A unique identifier for each customer location (string).
- `latitude`: The latitude coordinate of the customer location (float).
- `longitude`: The longitude coordinate of the customer location (float).
- `demand`: The demand at the customer location (integer).

```python
locations = {
    "Depot": CustomerLocation("Depot", 4.4184, 114.0932, 0),
    "1": CustomerLocation("1", 4.3555, 113.9777, 5),
    "2": CustomerLocation("2", 4.3976, 114.0049, 8),
    "3": CustomerLocation("3", 4.3163, 114.0764, 3),
    "4": CustomerLocation("4", 4.3184, 113.9932, 6),
    "5": CustomerLocation("5", 4.4024, 113.9896, 5),
    "6": CustomerLocation("6", 4.4142, 114.0127, 8),
    "7": CustomerLocation("7", 4.4804, 114.0734, 3),
    "8": CustomerLocation("8", 4.3818, 114.2034, 6),
    "9": CustomerLocation("9", 4.4935, 114.1828, 5),
    "10": CustomerLocation("10", 4.4932, 114.1322, 8),
}
```

Dictionary Structure:
- `vehicle name`: The name of the vehicle type (string).
- `capacity`: The capacity of the vehicle (integer).
- `cost`: The cost per kilometer of using the vehicle (float).

`data/vehicles_types.py`
```python
from utils.vehicle_utils import VehicleType

vehicle_types = {
    "Type A": VehicleType("Type A", 25, 1.2),  # Small vehicle
    "Type B": VehicleType("Type B", 30, 1.5)  # Large vehicle
}
```


## Video Demonstration


## Documentation
######################## IMPORTANT ########################
""" Do not rename the variables or functions.
Do not change the function parameters.
Do not add input() calls inside airport_manager.py.
The file must be importable by the tests. """
###########################################################


airport_info = ("OUL", 1, "14-09-2026")

allowed_gates = {"A1", "A2", "A3", "A4", "B1", "B2"}

restricted_destinations = {"Moscow", "Pyongyang"}

flights = {
    "AY450": {
        "destination": "Helsinki",
        "departure": "08:30",
        "gate": "A2",
        "capacity": 5,
        "passengers": ["Alice Wong", "David Kim", "Fatima Ali"],
    },
    "SK271": {
        "destination": "Stockholm",
        "departure": "10:15",
        "gate": "B1",
        "capacity": 4,
        "passengers": ["Chen Wei", "George Smith"],
    },
    "LH2491": {
        "destination": "Munich",
        "departure": "12:40",
        "gate": "A4",
        "capacity": 5,
        "passengers": ["Hana Lee", "Maria Garcia", "Noah Wilson"],
    },
}


## Logic to find if a flight exists
def find_flight(flights, flight_number):
    if not isinstance(flight_number, str):
        return None

    normalized_number = flight_number.strip().casefold()

    for stored_number in flights:
        if str(stored_number).strip().casefold() == normalized_number:
            return stored_number

    return None


## Logic to find if a passenger exists
def passenger_exists(passengers, passenger_name):
    if not isinstance(passenger_name, str):
        return False

    normalized_name = " ".join(passenger_name.split()).casefold()

    return any(
        " ".join(str(passenger).split()).casefold() == normalized_name
        for passenger in passengers
    )


## Logic to check in a passenger
def check_in_passenger(
    flights,
    flight_number,
    passenger_name,
    restricted_destinations
):
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    if not isinstance(passenger_name, str) or not passenger_name.strip():
        return "EMPTY_NAME"

    normalized_name = " ".join(passenger_name.split()).title()
    flight = flights[flight_key]

    if passenger_exists(flight["passengers"], normalized_name):
        return "DUPLICATE"

    if len(flight["passengers"]) >= flight["capacity"]:
        return "FULL"

    destination = str(flight["destination"]).strip().casefold()
    restricted = {
        str(place).strip().casefold()
        for place in restricted_destinations
    }

    if destination in restricted:
        return "RESTRICTED"

    flight["passengers"].append(normalized_name)
    return "OK"


## Logic to remove a passenger from a flight
def remove_passenger(
    flights,
    flight_number,
    passenger_name
):
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    passengers = flights[flight_key]["passengers"]

    for index, passenger in enumerate(passengers):
        if passenger_exists([passenger], passenger_name):
            passengers.pop(index)
            return "OK"

    return "PASSENGER_NOT_FOUND"


# Logic to change the gate of a flight
def change_gate(
    flights,
    flight_number,
    new_gate,
    allowed_gates
):
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return "FLIGHT_NOT_FOUND"

    if not isinstance(new_gate, str):
        return "INVALID_GATE"

    normalized_gate = new_gate.strip().casefold()
    matching_gate = next(
        (
            gate
            for gate in allowed_gates
            if str(gate).strip().casefold() == normalized_gate
        ),
        None,
    )

    if matching_gate is None:
        return "INVALID_GATE"

    flights[flight_key]["gate"] = matching_gate
    return "OK"


# Logic to get the status of a flight
def flight_status(flight):
    passenger_count = len(flight["passengers"])
    capacity = flight["capacity"]

    if passenger_count >= capacity:
        return "FULL"

    if passenger_count / capacity >= 0.75:
        return "ALMOST FULL"

    return "AVAILABLE"



# Logic to get the sorted manifest of a flight
def sorted_manifest(
    flights,
    flight_number
):
    flight_key = find_flight(flights, flight_number)

    if flight_key is None:
        return None

    return sorted(flights[flight_key]["passengers"])


# Logic to get the total number of passengers across all flights
def total_passengers(flights):
    return sum(len(flight["passengers"]) for flight in flights.values())


# Logic to check if any flight is full
def any_full_flight(flights):
    return any(flight_status(flight) == "FULL" for flight in flights.values())



# Logic to check if all flights have at least one passenger
def all_flights_have_passengers(flights):
    return all(bool(flight["passengers"]) for flight in flights.values())

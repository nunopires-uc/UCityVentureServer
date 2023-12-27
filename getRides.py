import json
from Ride import Ride  # Import the User class from User.py
from datetime import datetime

def load_rides_from_file(filename):
    try:
        with open(filename, 'r') as f:
            if f.read(1):  # read the first character to check if the file is empty
                f.seek(0)  # reset the file pointer to the beginning of the file
                return json.load(f)
            else:
                return []  # Return an empty list if the file is empty
    except FileNotFoundError:
        return []  # Return an empty list if the file does not exist
    except json.JSONDecodeError:
        return []  # Return an empty list if the file is empty or not valid JSON


def save_rides_to_file(rides, filename):
    with open(filename, 'w') as f:
        # assuming rides is a list of dicts that do not have a serialize() method
        json.dump(rides, f, indent=4)


def save_rides_in_memory(docs, filename):

    rides_to_save = []

    for doc in docs:
        doc_data = doc.to_dict()
        new_ride = Ride(
            destination=doc_data.get('destination'),
            info=doc_data.get('info'),
            license=doc_data.get('license'),
            origin=doc_data.get('origin'),
            origin_lat=doc_data.get('originLat'),
            origin_lon=doc_data.get('originLon'),
            provider=doc_data.get('provider'),
            ride_capacity=doc_data.get('rideCapacity'),
            ride_passengers=doc_data.get('ridePassangers'),
            state=doc_data.get('state'),
            time=doc_data.get('time'),
            id=doc.id
        )
        rides_to_save.append(new_ride)

    rides_to_save_dicts = [ride.to_dict() for ride in rides_to_save]
    
    # Save the list of ride dicts to file
    save_rides_to_file(rides_to_save_dicts, filename)

def update_rides_in_memory(docs, filename):
    # Load existing rides from file
    existing_rides = load_rides_from_file(filename)
    #print(existing_rides)
    existing_ids = {ride['id'] for ride in existing_rides}
    #print(existing_ids)

    rides_to_save = []

    for doc in docs:
        doc_data = doc.to_dict()
        ride_id = doc.id
        # Check if the ride is not already in memory
        if ride_id not in existing_ids:
            # Instantiate a Ride object for the new document and serialize it
            new_ride = Ride(
                destination=doc_data.get('destination'),
                info=doc_data.get('info'),
                license=doc_data.get('license'),
                origin=doc_data.get('origin'),
                origin_lat=doc_data.get('originLat'),
                origin_lon=doc_data.get('originLon'),
                provider=doc_data.get('provider'),
                ride_capacity=doc_data.get('rideCapacity'),
                ride_passengers=doc_data.get('ridePassangers'),
                state=doc_data.get('state'),
                time=doc_data.get('time'),
                id=doc.id
            )
            rides_to_save.append(new_ride)

    # If we found new rides, add them to existing ones and save to file
    #print(rides_to_save)

    if rides_to_save:
        rides_to_save_dicts = [ride.to_dict() for ride in rides_to_save]
        # Combine with existing rides and serialize
        new_rides = existing_rides + rides_to_save_dicts
        save_rides_to_file(new_rides, filename)



def check_for_matches(ride_list, id_passenger, id_provider):

    today_str = datetime.now().strftime("%d-%m-%Y")
    print(today_str)
    for ride in ride_list:


        ride_date_str = ride['time'].split(' ')[0]
        print(ride_date_str)
        # If the ride date is not today, continue to the next iteration
        # Check if the current provider matches the given ID_PROVIDER
        if ride['provider'] == id_provider:
            if ride_date_str == today_str:
            # Check if ID_PASSENGER matches any in the list
                if not id_passenger or id_passenger in ride['ride_passengers']:
                    return 1  # Match found
    return -1  # No match found
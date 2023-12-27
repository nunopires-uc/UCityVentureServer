class Ride:
    def __init__(self, destination=None, info=None, license=None, origin=None, origin_lat=None, origin_lon=None, provider=None, ride_capacity=0, ride_passengers=None, state=None, time=None, id=None):
        self.destination = destination
        self.info = info
        self.license = license
        self.origin = origin
        self.origin_lat = origin_lat
        self.origin_lon = origin_lon
        self.provider = provider
        self.ride_capacity = ride_capacity
        self.ride_passengers = ride_passengers if ride_passengers is not None else []
        self.state = state
        self.time = time
        self.id = id

    def get_id(self):
        return self.id

    def set_id(self, id):
        self.id = id

    def get_destination(self):
        return self.destination

    def set_destination(self, destination):
        self.destination = destination

    def get_info(self):
        return self.info

    def set_info(self, info):
        self.info = info

    def get_license(self):
        return self.license

    def set_license(self, license):
        self.license = license

    def get_origin(self):
        return self.origin

    def set_origin(self, origin):
        self.origin = origin

    def get_origin_lat(self):
        return self.origin_lat

    def set_origin_lat(self, origin_lat):
        self.origin_lat = origin_lat

    def get_origin_lon(self):
        return self.origin_lon

    def set_origin_lon(self, origin_lon):
        self.origin_lon = origin_lon

    def get_provider(self):
        return self.provider

    def set_provider(self, provider):
        self.provider = provider

    def get_ride_capacity(self):
        return self.ride_capacity

    def set_ride_capacity(self, ride_capacity):
        self.ride_capacity = ride_capacity

    def get_ride_passengers(self):
        return self.ride_passengers

    def set_ride_passengers(self, ride_passengers):
        self.ride_passengers = ride_passengers

    def get_state(self):
        return self.state

    def set_state(self, state):
        self.state = state

    def get_time(self):
        return self.time

    def set_time(self, time):
        self.time = time

    def __str__(self):
        return f"Ride(destination='{self.destination}', info='{self.info}', license='{self.license}', " \
               f"origin='{self.origin}', origin_lat={self.origin_lat}, origin_lon={self.origin_lon}, " \
               f"provider='{self.provider}', ride_capacity={self.ride_capacity}, ride_passengers={self.ride_passengers}, " \
               f"state='{self.state}', time='{self.time}')"
    
    def serialize(self):
        """Serialize the object to a dictionary."""
        return {
            'id': self.id,
            'destination': self.destination,
            'info': self.info,
            'license': self.license,
            'origin': self.origin,
            'origin_lat': self.origin_lat,
            'origin_lon': self.origin_lon,
            'provider': self.provider,
            'ride_capacity': self.ride_capacity,
            'ride_passengers': self.ride_passengers,
            'state': self.state,
            'time': self.time
        }
    
    def to_dict(self):
        # Return a dictionary representation of the Ride instance
        return {
            "destination": self.destination,
            "info": self.info,
            "license": self.license,
            "origin": self.origin,
            "origin_lat": self.origin_lat,
            "origin_lon": self.origin_lon,
            "provider": self.provider,
            "ride_capacity": self.ride_capacity,
            "ride_passengers": self.ride_passengers,
            "state": self.state,
            "time": self.time,
            "id": self.id
        }

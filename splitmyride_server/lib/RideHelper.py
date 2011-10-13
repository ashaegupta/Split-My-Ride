from model.Ride import Ride
from model.User import User
import simplejson

class RideHelper(object):
    
    @classmethod
    def add_ride(klass, user_id, origin, dest_lat, dest_lon, departure_time):
        
        ## Convert the origin and destination dictionaries into a string
        origin_dict = {}
        destination_dict = {}
        origin_dict = simplejson.loads(origin)
        origin_1 = origin_dict.get('origin_1')
        origin_2 = origin_dict.get('origin_2')

        doc = {
            Ride.A_USER_ID:user_id,
            Ride.A_ORIGIN_1:origin_1,
            Ride.A_ORIGIN_2:origin_2,
            Ride.A_DESTINATION_LAT:dest_lat,
            Ride.A_DESTINATION_LON:dest_lon,
            Ride.A_TIMESTAMP_DEPARTURE:departure_time
        }

        ride_id = Ride.create_or_update_ride(doc)

        if not ride_id:
            return ApiResponse.RIDE_COULD_NOT_CREATE
        else:
            return ride_id
        
    @classmethod
    def get_matches(klass, ride_id):
        rides = []
        users = {}
        user_ids = []
                
        # Get all rides that match ride_id specs
        rides = Ride.get_matches(ride_id)
        
        # Get list of user_ids in rides  
        for ride in rides:
            user_id = ride.get(Ride.A_USER_ID) 
            if user_id:
                user_ids.append(user_id)
        
        # Make batch call to get all user info
        users = User.get_by_user_ids(user_ids)
        
        # Get the rides that match
        rides = Ride.get_matches(ride_id)
        
        # Append each ride with user info
        if not rides:
            return ApiResponse.RIDE_COULD_NOT_CREATE
        
        else:
            for ride in rides:
                del ride[klass.A_OBJECT_ID]
                user_id = ride.get(Ride.A_USER_ID)
                ride["user"] = users.get(user_id)
            return rides

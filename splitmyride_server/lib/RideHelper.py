import simplejson
from model.Ride import Ride
from model.User import User

class RideHelper(object):
    
    @classmethod
    def add_ride(klass, user_id, origin, destination, time):
        
        ## Convert the origin and destination dictionaries into a string
        origin_dict = {}
        destination_dict = {}
        origin_dict = simplejson.loads(origin)
        desitination_dict = simplejson.loads(destination)
        
        doc = {
            Ride.A_USER_ID:user_id
            Ride.A_ORIGIN_1:origin_dict.get('origin_1'),
            Ride.A_ORIGIN_2:origin_dict.get('origin_2'),
            Ride.A_DESTINATION_1:destination_dict.get('destination_1'),
            Ride.A_DESTINATION_2:destination_dict.get('destination_2'),
            Ride.A_DESTINATION_3:destination_dict.get('destination_3'),
            Ride.A_DESTINATION_4:destination_dict.get('destination_4'),
            Ride.A_TIME_ST:time
        }        
        return simplejson.dumps(Ride.create_or_update_ride(doc))
        
    @classmethod
    def get_matches(klass, ride_id):
        
        # 1. Review logic here. Do I need to initialize all dicts within a dict?
        # 2. I'm using two different databases here user and rides, but should I also store all the
        # user info associated with each ride in the ride database, to avoid having to do a database merge and to 
        # make one less call to a database?
        # 3. I know dictionaries are not ordered, but how can I rank the entries? Another key=value?
        # 4. How do I make the query?
        # 5. 
        
        matches = {}
        rides = {}
        users = {}
        user_ids = []
                
        # Get all rides that match ride_id specs
        rides = Ride.get_rides(ride_id)
        
        # Get list of user_ids in rides  
        for ride in rides:
            user_id = ride.get('user_id')
            user_ids.add(user_id)
        
        # Make batch call to get all user info
        users = User.get_users(user_ids)
        
        # Create matches dict that holds ride and user info
        for ride in rides:
            if ride.get("status")==1:
                user_id = ride.get("user_id")
                user = {}
                user = users.get(user_id)
                
                if user.get("status")==1:
                    ride_id = ride.get("ride_id")
                    match_key = ride_id+"&"+user_id             ## Can I actually make the key, the best match rank?
                    
                    match[match_key] = {}
                    match[match_key] = {ride_id:ride, user_id:user}

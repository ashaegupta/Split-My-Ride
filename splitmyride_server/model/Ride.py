import sys
sys.path.append("../")
import logging
import uuid
import datetime
import time
import MongoMixIn
import splitmyride_settings
from utils import utils

class Ride(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'ride'
    
    if splitmyride_settings.ON_TEST:
        MONGO_COLLECTION_NAME = 'ride_c_test'
    else:
        MONGO_COLLECTION_NAME = 'ride_c'
    
    A_RIDE_ID               = 'ride_id'
    A_USER_ID               = 'user_id'                          
    A_ORIGIN_1              = 'origin_1'
    A_ORIGIN_2              = 'origin_2'
    A_DESTINATION_LON       = 'dest_lon'
    A_DESTINATION_LAT       = 'dest_lat'
    A_LOC                   = 'loc'             # loc = [float(lat), float(lon)]
    A_TIMESTAMP_CREATED     = 'ts_c'
    A_TIMESTAMP_DEPARTURE   = 'ts_d'
    A_TIMESTAMP_EXPIRES     = 'ts_e'
    A_MATCH                 = 'match'
    A_STATUS                = 'status'
    
    STATUS_PENDING          = 0
    STATUS_MATCHED          = 1
    STATUS_EXPIRED          = 2
    
    DEFAULT_EXPIRY_WINDOW_IN_SECONDS    = 60*60    # one hour
    MAX_WAIT_TIME_IN_SECONDS            = 15*60    # 15 mins
    
    MAX_DISTANCE_IN_KMS                 = 1.2
    

    # This method sets-up the indexes for the database, it needs to be run once from the shell for
    # each instance of the database
    @classmethod
    def setup_mongo_indexes(klass):
        from pymongo import GEO2D
        coll = klass.mdbc()
        coll.ensure_index([ (klass.A_LOC, GEO2D)], unique=False)
    
    @classmethod
    def create_or_update_ride(klass, doc=None):
        if not doc: doc = {}
        
        # Create ride_id if doesn't already exist
        ride_id = doc.get(klass.A_RIDE_ID)       
        if not ride_id:                          
            ride_id = uuid.uuid4().hex
        spec = {klass.A_RIDE_ID:ride_id}
        
        # Create loc
        lon = doc.get(klass.A_DESTINATION_LON)
        lat = doc.get(klass.A_DESTINATION_LAT)
        if lon and lat:
            doc[klass.A_LOC] = [float(lon), float(lat)]
            del doc[klass.A_DESTINATION_LON]
            del doc[klass.A_DESTINATION_LAT]

        
        # Store the time that this object was created, if it does not already exist
        if not doc.get(klass.A_TIMESTAMP_CREATED):
            doc[klass.A_TIMESTAMP_CREATED] = int(time.time())
        
        # Convert time into datetime and create expiry, if doesn't already exist
        if not doc.get(klass.A_TIMESTAMP_EXPIRES):
            doc[klass.A_TIMESTAMP_EXPIRES] = doc.get(klass.A_TIMESTAMP_DEPARTURE) + klass.DEFAULT_EXPIRY_WINDOW_IN_SECONDS
        
        # Initiate status to pending if it does not exist
        if not doc.get(klass.A_STATUS):
            doc[klass.A_STATUS] = klass.STATUS_PENDING
            
        try:
            klass.mdbc().update(spec=spec, document={"$set": doc}, upsert=True, safe=True)
        except Exception, e:
            logging.error("COULD NOT UPSERT document in model.Ride Exception: %s" % e.message)
            return False
        return ride_id


    @classmethod
    def get_ride(klass, ride_id):
        spec = {klass.A_RIDE_ID:ride_id}
        ride_to_match = klass.mdbc().find_one(spec)
        return ride_to_match
    
    @classmethod
    def get_matches(klass, ride_id):
        rides = []
        
        print ride_id
        
        # Get info for the ride to match
        ride_to_match = klass.get_ride(ride_id)
        print "ride_to_match"
        print ride_to_match
        
        # Run a query to find matches
        if ride_to_match:
            query = {
                # not the current ride
                klass.A_RIDE_ID:{
                    "$ne":ride_id
                },
                # status pending
                klass.A_STATUS:klass.STATUS_PENDING,
                # must match origin exactly
                klass.A_ORIGIN_1:ride_to_match.get(klass.A_ORIGIN_1),
                klass.A_ORIGIN_2:ride_to_match.get(klass.A_ORIGIN_2),
                # get an ordered list close to desired lat and lon
                klass.A_LOC: {
                    "$near":ride_to_match.get(klass.A_LOC),
                },
                # add time window
                klass.A_TIMESTAMP_DEPARTURE: {
                    "$gt":ride_to_match.get(klass.A_TIMESTAMP_DEPARTURE) - klass.MAX_WAIT_TIME_IN_SECONDS,
                    "$lte":ride_to_match.get(klass.A_TIMESTAMP_DEPARTURE) + klass.MAX_WAIT_TIME_IN_SECONDS
                }
            }
            cursor = klass.mdbc().find(query)
            rides = klass.list_from_cursor(cursor)
        
            if rides:
                rides = klass.filter_rides_by_max_distance(rides, ride_to_match.get(klass.A_LOC))
        
        return rides
    
    @classmethod
    def filter_rides_by_max_distance(klass, rides, distance_from):
        filtered_rides = []
        for ride in rides:
            loc = ride.get(klass.A_LOC)
            print "LOC"
            print loc
            distance = utils.distance_between_two_points(distance_from, loc)
            print distance
            if distance <= klass.MAX_DISTANCE_IN_KMS:
                filtered_rides.append(ride)
        return filtered_rides
    
    @classmethod
    def clear_expired_rides(klass):
        today = datetime.datetime.now()
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
    A_MATCH_RIDE_ID         = 'match_id'
    A_PENDING_RIDE_ID       = 'pend_match_id'
    A_REJECTED_RIDE_ID      = 'rejected_ride_id'
    A_REJECTED_RIDE_IDS     = 'rejected_ride_ids'       # list of ids
    A_STATUS                = 'status'
    A_MATCH_REJECTED_ITEM   = 'rejected_item'
    A_MATCH_REJECTED_ALL    = 'rejected_all'
    
    STATUS_PREPENDING       = 0 # Ride has no pending matches (no requests to match with this ride have been made)
    STATUS_PENDING          = 1 # Ride has one pending match (one request to match with this ride has been made)
    STATUS_MATCHED          = 2 # Ride has been matched (both parties accepted)
    STATUS_EXPIRED          = 3 # Ride is past the expiry window from when it was created

    ACTION_REQUEST          = 'request'
    ACTION_ACCEPT           = 'accept'
    ACTION_DECLINE          = 'decline'
    
    DEFAULT_EXPIRY_WINDOW_IN_SECONDS    = 60*30    # 30 mins
    MAX_WAIT_TIME_IN_SECONDS            = 60*15    # 15 mins
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
        
        document = {}
        
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
        if doc.get(klass.A_TIMESTAMP_DEPARTURE) and not doc.get(klass.A_TIMESTAMP_EXPIRES):
            doc[klass.A_TIMESTAMP_EXPIRES] = doc.get(klass.A_TIMESTAMP_DEPARTURE) + klass.DEFAULT_EXPIRY_WINDOW_IN_SECONDS
        
        # Initiate status to pending if it does not exist
        if not doc.get(klass.A_STATUS):
            doc[klass.A_STATUS] = klass.STATUS_PREPENDING
            
        # add one or more ride ids to a set of rejected rides
        addToSet = {}
        rejected_ride_ids = doc.get(klass.A_REJECTED_RIDE_ID)
        if rejected_ride_ids:
            del doc[klass.A_REJECTED_RIDE_ID]
            if type(rejected_ride_ids) == list:
                addToSet[klass.A_REJECTED_RIDE_IDS] = {"$each":rejected_ride_ids}
            else:
                addToSet[klass.A_REJECTED_RIDE_IDS] = rejected_ride_ids

        if doc:
            document['$set'] = doc
        if addToSet:
            document['$addToSet'] = addToSet

        try:
            klass.mdbc().update(spec=spec, document=document, upsert=True, safe=True)
        except Exception, e:
            logging.error("COULD NOT UPSERT document in model.Ride Exception: %s" % e.message)
            return False
        return ride_id


    @classmethod
    def get_ride(klass, ride_id):
        spec = {klass.A_RIDE_ID:ride_id}
        ride_to_match = klass.find_one(spec, remove_object_id=True)
        return ride_to_match
    
    @classmethod
    def get_matches(klass, ride_to_match):
        rides = []
        
        # Run a query to find matches
        if ride_to_match:
            query = {
                # not the current ride
                klass.A_RIDE_ID:{
                    "$ne":ride_to_match.get(klass.A_RIDE_ID)
                },
                # status pending
                klass.A_STATUS:klass.STATUS_PREPENDING,
                # must match origin exactly
                klass.A_ORIGIN_1:ride_to_match.get(klass.A_ORIGIN_1),
                klass.A_ORIGIN_2:ride_to_match.get(klass.A_ORIGIN_2),
                # get an ordered list close to desired lat and lon
                klass.A_LOC: {
                    "$near":ride_to_match.get(klass.A_LOC),
                },
                # add time window
                klass.A_TIMESTAMP_DEPARTURE: {
                    "$gt": ride_to_match.get(klass.A_TIMESTAMP_DEPARTURE) - klass.MAX_WAIT_TIME_IN_SECONDS,
                    "$lte":ride_to_match.get(klass.A_TIMESTAMP_DEPARTURE) + klass.MAX_WAIT_TIME_IN_SECONDS
                }
            }
            cursor = klass.mdbc().find(query)
            rides = klass.list_from_cursor(cursor, remove_object_id=True)
            if rides:
                rides = klass.filter_rides_by_max_distance(rides, ride_to_match.get(klass.A_LOC))
        return rides    
    
    @classmethod
    def filter_rides_by_max_distance(klass, rides, distance_from):
        filtered_rides = []
        for ride in rides:
            loc = ride.get(klass.A_LOC)
            distance = utils.distance_between_two_points(distance_from, loc)
            if distance <= klass.MAX_DISTANCE_IN_KMS:
                filtered_rides.append(ride)
        return filtered_rides
    
    @classmethod
    def create_match(klass, ride_id, match_ride_id):
        ride_doc = {
            klass.A_RIDE_ID: ride_id,
            klass.A_STATUS: klass.STATUS_MATCHED,
            klass.A_PENDING_RIDE_ID: None,
            klass.A_MATCH_RIDE_ID: match_ride_id
        }
        
        match_doc = {
            klass.A_RIDE_ID: match_ride_id,
            klass.A_STATUS: klass.STATUS_MATCHED,
            klass.A_PENDING_RIDE_ID: None,
            klass.A_MATCH_RIDE_ID: ride_id
        }
        return klass.create_or_update_ride_and_match(ride_doc, match_doc)

    @classmethod
    def request_match(klass, ride_id, match_ride_id):
        ride_doc = {
            klass.A_RIDE_ID: ride_id,
            klass.A_STATUS: klass.STATUS_PENDING,
            klass.A_PENDING_RIDE_ID: match_ride_id,
        }
        
        match_doc = {
            klass.A_RIDE_ID: match_ride_id,
            klass.A_STATUS: klass.STATUS_PENDING,
            klass.A_PENDING_RIDE_ID: ride_id,
        }
        return klass.create_or_update_ride_and_match(ride_doc, match_doc)

    @classmethod
    def decline_match(klass, ride_id, match_ride_id):
        ride_doc = {
            klass.A_RIDE_ID: ride_id,
            klass.A_STATUS: klass.STATUS_PREPENDING,
            klass.A_PENDING_RIDE_ID: None,
            klass.A_REJECTED_RIDE_ID: match_ride_id
        }
        
        match_doc = {
            klass.A_RIDE_ID: match_ride_id,
            klass.A_STATUS: klass.STATUS_PREPENDING,
            klass.A_PENDING_RIDE_ID: None,
            klass.A_REJECTED_RIDE_ID: ride_id
        }
        return klass.create_or_update_ride_and_match(ride_doc, match_doc)

    @classmethod
    def create_or_update_ride_and_match(klass, ride_doc, match_doc):
        ride_update_success = klass.create_or_update_ride(ride_doc)
        match_update_success = klass.create_or_update_ride(match_doc)
        
        if not (ride_update_success or match_update_success): 
            return False
        return True

    @classmethod
    def update_status_of_expired_rides(klass):
        curr_time = int(time.time())
        
        # find all rides that are expired
        query = {
            klass.A_TIMESTAMP_EXPIRES:{
            "$lt":curr_time
            }
        }
        cursor = klass.mdbc().find(query)
        
        # update all expired rides
        if cursor:
            for c in cursor:
                if klass.A_RIDE_ID and klass.A_STATUS in c:
                    update_doc = {
                        klass.A_RIDE_ID: c[klass.A_RIDE_ID],
                        klass.A_STATUS: klass.STATUS_EXPIRED
                    }
                    klass.create_or_update_ride(update_doc)
        
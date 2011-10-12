import sys
sys.path.append("../")
import logging
import uuid
import datetime
import time


class Ride(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'ride'
    MONGO_COLLECTION_NAME   = 'ride_c'
    
    A_RIDE_ID               = 'ride_id'
    A_USER_ID               = 'user_id'                          
    A_ORIGIN_1              = 'origin_1'
    A_ORIGIN_2              = 'origin_2'
    A_DESTINATION_1         = 'destination_1'
    A_DESTINATION_2         = 'destination_2'
    A_DESTINATION_3         = 'destination_3'
    A_DESTINATION_4         = 'destination_4'
    A_TIMESTAMP_CREATED     = 'ts_c'
    A_TIMESTAMP_DEPARTURE   = 'ts_d'
    A_TIMESTAMP_EXPIRES     = 'ts_e'
    A_MATCH                 = 'match' #0 if odoes not have a match, #RIDE_ID of match, if match exists
    A_STATUS                = 'status'
    
    STATUS_PENDING          = 0
    STATUS_MATCHED          = 1
    #STATUS_???              = 2     #TODO ADD all possible states of being matched
    STATUS_EXPIRED          = 3
    
    DEFAULT_EXPIRY_WINDOW_IN_SECONDS = 60*60    # one hour

    ### Do I need to do this?
    @classmethod
    def setup_mongo_indexes(klass):
        coll = klass.mdbc()
    
    @classmethod
    def create_or_update_ride(klass, doc=None):      
        if not doc: doc = {}
        
        # Create ride_id if doesn't already exist
        ride_id = doc.get(klass.A_RIDE_ID)       
        if not ride_id:                          
            ride_id = uuid.uuid4().hex
        spec = {klass.A_RIDE_ID:ride_id}
        
        # Store the time that this object was created, if it does not already exist
        if not doc.get(klass.A_TIMESTAMP_CREATED):
            doc[klass.A_TIMESTAMP_CREATED] = int(time.time())
        
        # Convert time into datetime and create expiry, if doesn't already exist
        if not doc.get(klass.A_TIMESTAMP_EXPIRES):
            doc[klass.A_TIMESTAMP_EXPIRES] = doc.get(klass.A_TIMESTAMP_DEPARTURE) + DEFAULT_EXPIRY_WINDOW_IN_SECONDS
        
        # Set match to be 0 if doesn't already exist
        match = doc.get(klass.A_MATCH)
        if not match:
            doc[klass.A_MATCH] = 0
                
        try:
            klass.mdbc().update(spec=spec, document={"$set": doc}, upsert=True, safe=True)
        except Exception, e:
            logging.error("COULD NOT UPSERT document in model.Ride Exception: %s" % e.message)
            return False
        return ride_id


    @classmethod
    def get_matches(klass, ride_id):
        rides = {}
        
        # Get info for the ride to match
        spec = {klass.A_RIDE_ID:ride_id}
        ride_to_match = klass.mdbc().find_one(spec)                
        
        if ride_to_match:
	    pass 
        # Find matches 
            # rides that are minimum matches
            # NOT THIS RIDE_ID
            # DON"T HAVE AN EXPIRED TIME
            # HAVE A TIME THAT IS WITHIN AN HOUR OF THIS LEAVE TIME
            # ARE LEAVING FROM THE ORIGIN_1 and ORIGIN_2
            # ARE GOING TO THE SAME DESTINATION_1 and DESTINATION_2
            # 
        
        # May dict rides, where key=ride_id and value={ride_info}
        return rides
    
    @classmethod
    def clear_expired_rides(klass):
        
        today = datetime.datetime.now() 
        
       

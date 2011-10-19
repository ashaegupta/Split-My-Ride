from model.Ride import Ride
from model.User import User
import simplejson
from lib import ApiResponse
from lib.UserHelper import UserHelper   
from lib.TwilioHelper import TwilioHelper

class RideHelper(object):
    
    @classmethod
    def create_or_update_ride(klass, user_id, origin, dest_lon, dest_lat, departure_time):
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
            Ride.A_DESTINATION_LON:dest_lon,
            Ride.A_DESTINATION_LAT:dest_lat,
            Ride.A_TIMESTAMP_DEPARTURE:departure_time
        }

        ride_id = Ride.create_or_update_ride(doc)

        if not ride_id:
            return ApiResponse.RIDE_COULD_NOT_CREATE
        else:
            return ride_id
        
    @classmethod
    def get_ride(klass, ride_id):
        ride = Ride.get_ride(ride_id)
        if not ride:
            return ApiResponse.RIDE_NOT_FOUND
        else:
            del ride[Ride.A_OBJECT_ID]
            return ride
    
    # Return the appropriate match(es) depending on the ride_id status
    #       if status = STATUS_PREPENDING, return complete list of potential matches
    #       if status = STATUS_PENDING, return a list with pending match on top along with other possible matches
    #       if status = STATUS_MATCHED, return the matched ride
    @classmethod
    def get_matches(klass, ride_id):        
        ride_doc = klass.get_ride(ride_id)
        status = ride_doc.get(Ride.A_STATUS)
        
        if status==0:
            return klass.get_matches_for_status_prepending(ride_doc)
        elif status==1:
            return klass.get_matches_for_status_pending(ride_doc)
        elif status==2:
            return klass.get_matches_for_status_matched(ride_doc)
        else:
            return ApiResponse.RIDE_NO_MATCHES_FOUND
    
    @classmethod
    def get_matches_for_status_prepending(klass, ride_doc):
        rides = []
        users = {}
        user_ids = []
                
        # Get all rides that match ride_doc specs
        rides = Ride.get_matches(ride_doc)
        
        # Get list of user_ids in rides  
        for ride in rides:
            user_id = ride.get(Ride.A_USER_ID)
            if user_id:
                user_ids.append(user_id)
        
        # Make batch call to get all user info
        users = UserHelper.get_users_by_id(user_ids)
        
        # Get the rides that match
        rides = Ride.get_matches(ride_doc)
        
        # Append each ride with user info
        if not rides:
            return ApiResponse.RIDE_NO_MATCHES_FOUND
        
        else:
            for ride in rides:
                del ride[Ride.A_OBJECT_ID]
                user_id = ride.get(Ride.A_USER_ID)
                ride['user'] = users.get(user_id)
            return rides

    @classmethod
    def get_matches_for_status_pending(klass, ride_doc):
        rides = []
        
        # first ensure status is pending
        if ride_doc.get(Ride.A_STATUS)!=1: return klass.get_matches_for_status_prepending(ride_doc)
        
        # get the match ride and user info
        pending_ride_id = ride_doc.get(Ride.A_PENDING_RIDE_ID)
        if not pending_ride_id: return klass.get_matches_for_status_prepending(ride_doc)
        
        rides.append(klass.get_ride_and_user_docs_from_ride_id(pending_ride_id))
        
        # Add other potential matches with prepending status
        prepending_rides = klass.get_matches_for_status_prepending(ride_doc)
        rides.append(prepending_rides)
        
        return rides
    
    @classmethod
    def get_matches_for_status_matched(klass, ride_doc):
        # first ensure status is matched
        if ride_doc.get(Ride.A_STATUS)!=2: return ApiResponse.RIDE_STATUS_INCORRECT
            
        # get the match ride and user info
        match_ride_id = ride_doc.get(Ride.A_MATCH_RIDE_ID)    
        if not match_ride_id: return ApiResponse.RIDE_NOT_FOUND
        
        return klass.get_ride_and_user_docs_from_ride_id(match_ride_id)

    @classmethod
    def get_ride_and_user_docs_from_ride_id(klass, ride_id):
        if not ride_id: return ApiResponse.RIDE_RIDE_ID_NOT_FOUND
        
        ride_doc = klass.get_ride(ride_id)
        if not ride_doc: return ApiResponse.RIDE_NOT_FOUND
        
        user_id = ride_doc.get(Ride.A_USER_ID)
        if not user_id: return ApiResponse.RIDE_USER_ID_NOT_FOUND
        
        user_doc = UserHelper.get_user_by_id(user_id)        
        if not user_doc: return ApiResponse.RIDE_USER_NOT_FOUND
        
        ride_doc['user']=user_doc
        return ride_doc
    
    
    @classmethod
    def do_match_action(klass, action, curr_user_ride_id, match_ride_id):
        # Complete appropriate SMS action
        if action == 'request':
            return klass.request_match(curr_user_ride_id, match_ride_id)
        elif action == 'accept':
            return klass.accept_match(curr_user_ride_id, match_ride_id)
        elif action == 'decline':
            return klass.decline_match(curr_user_ride_id, match_ride_id)
        else: 
            return ApiResponse.RIDE_NO_ACTION
    
    @classmethod
    def request_match(klass, curr_user_ride_id, match_ride_id):
        # update the status of both ride ids to be STATUS_PENDING
        curr_update_doc = klass.get_ride(curr_user_ride_id)
        curr_update_doc[Ride.A_STATUS] = 1
        curr_update_doc[Ride.A_PENDING_RIDE_ID] = match_ride_id
        
        match_update_doc = klass.get_ride(match_ride_id)
        match_update_doc[Ride.A_STATUS] = 1
        match_update_doc[Ride.A_PENDING_RIDE_ID] = curr_user_ride_id
                
        curr_update_success = Ride.create_or_update_ride(curr_update_doc)
        match_update_success = Ride.create_or_update_ride(match_update_doc)
        
        if not (curr_update_success or match_update_success):
             return ApiResponse.RIDE_COULD_NOT_REQUEST_MATCH
        
        curr_ride_doc = klass.get_ride_and_user_docs_from_ride_id(curr_user_ride_id)        
        if not curr_ride_doc: return ApiResponse.RIDE_COULD_NOT_REQUEST_MATCH
        # get name of the curr_user
        from_first_name = curr_ride_doc.get('user').get(User.A_FIRST_NAME)
        from_last_name = curr_ride_doc.get('user').get(User.A_LAST_NAME)
        
        # get the phone number of the match_id
        match_doc = klass.get_ride_and_user_docs_from_ride_id(match_ride_id) 
        if not match_doc: return ApiResponse.RIDE_COULD_NOT_REQUEST_MATCH
        to_first_name = match_doc.get('user').get(User.A_FIRST_NAME)
        to_last_name = match_doc.get('user').get(User.A_LAST_NAME)
        to_phone_number = match_doc.get('user').get(User.A_PHONE)

        # send sms and return twilio response
        note = "Hi %s, great news! %s wants to split a ride with you! Go to the app to check out details!" % (to_first_name, from_first_name +" "+ from_last_name)
        if not TwilioHelper.send_sms(note, to_phone_number): return ApiResponse.RIDE_COULD_NOT_REQUEST_MATCH
        return ApiResponse.RIDE_MATCH_REQUESTED
    
    @classmethod
    def accept_match(klass, curr_user_ride_id, match_ride_id):
        # ensure that both rides have STATUS_PENDING
        curr_doc = klass.get_ride_and_user_docs_from_ride_id(curr_user_ride_id)
        match_doc = klass.get_ride_and_user_docs_from_ride_id(match_ride_id) 
        
        if curr_doc.get(Ride.A_STATUS)!=1 or match_doc.get(Ride.A_STATUS)!=1:
             return ApiResponse.RIDE_COULD_NOT_ACCEPT_MATCH
        
        # update the status of both ride ids to be MATCHED
        curr_update_doc = klass.get_ride(curr_user_ride_id)
        curr_update_doc[Ride.A_STATUS] = 2
        curr_update_doc[Ride.A_PENDING_RIDE_ID] = ""
        curr_update_doc[Ride.A_MATCH_RIDE_ID] = match_ride_id
        
        match_update_doc = klass.get_ride(match_ride_id)
        match_update_doc[Ride.A_STATUS] = 2
        match_update_doc[Ride.A_PENDING_RIDE_ID] = ""
        match_update_doc[Ride.A_MATCH_RIDE_ID] = curr_user_ride_id
        
        curr_update_success = Ride.create_or_update_ride(curr_update_doc)
        match_update_success = Ride.create_or_update_ride(match_update_doc)
        if not (curr_update_success or match_update_success): return ApiResponse.RIDE_COULD_NOT_ACCEPT_MATCH
        
        # get first names of both users and to_phone_number
        from_first_name = curr_doc.get('user').get(User.A_FIRST_NAME)
        to_first_name = match_doc.get('user').get(User.A_FIRST_NAME)
        to_phone_number = match_doc.get('user').get(User.A_PHONE)
        
        # send the sms to accept the ride request
        note = "Hi %s! %s has accepted your request to split a ride! Wahoo!" % (to_first_name, from_first_name)
        if not TwilioHelper.send_sms(note, to_phone_number): ApiResponse.RIDE_COULD_NOT_ACCEPT_MATCH     
        return ApiResponse.RIDE_MATCH_ACCEPTED
        
    
    @classmethod
    def decline_match(klass, curr_user_ride_id, match_ride_id):
        # ensure that both rides have STATUS_PENDING
        curr_doc = klass.get_ride_and_user_docs_from_ride_id(curr_user_ride_id)
        match_doc = klass.get_ride_and_user_docs_from_ride_id(match_ride_id) 
        
        if curr_doc.get(Ride.A_STATUS)!=1 or match_doc.get(Ride.A_STATUS)!=1:
             return ApiResponse.RIDE_COULD_NOT_DECLINE_MATCH
        
        # update the status of both ride ids to be UNMATCHED and add ride_ids to blacklists
        curr_update_doc = klass.get_ride(curr_user_ride_id)
        curr_update_doc[Ride.A_STATUS] = 0
        curr_update_doc[Ride.A_PENDING_RIDE_ID] = ""
        curr_update_doc[Ride.A_MATCH_BLACKLIST_ITEM] = match_ride_id
        
        match_update_doc = klass.get_ride(match_ride_id)
        match_update_doc[Ride.A_STATUS] = 0
        match_update_doc[Ride.A_PENDING_RIDE_ID] = ""
        match_update_doc[Ride.A_MATCH_BLACKLIST_ITEM] = curr_user_ride_id
        
        curr_update_success = Ride.create_or_update_ride(curr_update_doc)
        match_update_success = Ride.create_or_update_ride(match_update_doc)
        if not (curr_update_success or match_update_success): return ApiResponse.RIDE_COULD_NOT_DECLINE_MATCH
        return ApiResponse.RIDE_MATCH_DECLINED
    
    '''
    # helper method to update ride status
    @classmethod
    def update_match_status(klass, ride_id_to_update, ride_id_to_include, action, curr_status, new_status)
        ride_doc = klass.get_ride_and_user_docs_from_ride_id(ride_id_to_update)
        
        if curr_doc.get(Ride.A_STATUS)!=curr_status: return ApiResponse.RIDE_COULD_NOT_DECLINE_MATCH
        
        # update the status of both ride ids to be UNMATCHED and add ride_ids to blacklists
        update_doc = klass.get_ride(user_id)
        curr_update_doc[Ride.A_STATUS] = 0
        curr_update_doc[Ride.A_PENDING_RIDE_ID] = ""
        curr_update_doc[Ride.A_MATCH_BLACKLIST_ITEM] = match_ride_id
        
        match_update_doc = klass.get_ride(match_ride_id)
        match_update_doc[Ride.A_STATUS] = 0
        match_update_doc[Ride.A_PENDING_RIDE_ID] = ""
        match_update_doc[Ride.A_MATCH_BLACKLIST_ITEM] = curr_user_ride_id
        
        curr_update_success = Ride.create_or_update_ride(curr_update_doc)
        match_update_success = Ride.create_or_update_ride(match_update_doc)
    '''
        
from model.Ride import Ride
from model.User import User
from lib import ApiResponse
from lib.UserHelper import UserHelper   
from lib.TwilioHelper import TwilioHelper

class RideHelper(object):
    
    @classmethod
    def create_or_update_ride(klass, user_id, origin_venue, dest_lon, dest_lat, departure_time, origin_pick_up=None):
        
        doc = {
            Ride.A_USER_ID:user_id,
            Ride.A_ORIGIN_VENUE:origin_venue,
            Ride.A_ORIGIN_PICK_UP:origin_pick_up,
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
            return ride
    
    # Return the appropriate match(es) depending on the ride_id status
    #       if status = STATUS_PREPENDING, return complete list of potential matches
    #       if status = STATUS_PENDING, return a list with pending match on top along with other possible matches
    #       if status = STATUS_MATCHED, return the matched ride
    @classmethod
    def get_matches(klass, ride_id):        
        ride_doc = klass.get_ride(ride_id)
        status = ride_doc.get(Ride.A_STATUS)
        
        if status == Ride.STATUS_PREPENDING:
            return klass.get_matches_for_status_prepending(ride_doc)
        elif status == Ride.STATUS_PENDING:
            return klass.get_matches_for_status_pending(ride_doc)
        elif status == Ride.STATUS_MATCHED:
            return klass.get_matches_for_status_matched(ride_doc)
        else:
            return ApiResponse.RIDE_NO_MATCHES_FOUND
    
    @classmethod
    def get_matches_for_status_prepending(klass, ride_doc):
        # Get all rides that match ride_doc specs
        rides = Ride.get_matches(ride_doc)
        if not rides:
            return ApiResponse.RIDE_NO_MATCHES_FOUND
        
        # Get list of user_ids in rides  
        user_ids = [r.get(Ride.A_USER_ID) for r in rides]
        
        # Make batch call to get all user info
        users = UserHelper.get_users_by_id(user_ids)
        
        # Append each ride with user info
        for ride in rides:
            user_id = ride.get(Ride.A_USER_ID)
            ride['user'] = users.get(user_id)
        return rides

    @classmethod
    def get_matches_for_status_pending(klass, ride_doc):
        rides = []
        
        # get the match ride and user info
        pending_ride_id = ride_doc.get(Ride.A_PENDING_RIDE_ID)
        if pending_ride_id: 
            rides.append(klass.format_ride(pending_ride_id))
        
        # Add other potential matches with prepending status
        prepending_rides = klass.get_matches_for_status_prepending(ride_doc)
        rides.append(prepending_rides)
        
        return rides
    
    @classmethod
    def get_matches_for_status_matched(klass, ride_doc):
        # get the match ride and user info
        match_ride_id = ride_doc.get(Ride.A_MATCH_RIDE_ID)    
        if not match_ride_id: 
            return ApiResponse.RIDE_NOT_FOUND
        
        return [klass.format_ride(match_ride_id)]
    
    @classmethod
    def format_ride(klass, ride_doc_or_ride_id):
        if type(ride_doc_or_ride_id) != dict:
            ride_doc = klass.get_ride(ride_doc_or_ride_id)
            if not ride_doc: 
                return ApiResponse.RIDE_NOT_FOUND
        else:
            ride_doc = ride_doc_or_ride_id
        
        user_id = ride_doc.get(Ride.A_USER_ID)
        if not user_id: return ApiResponse.RIDE_USER_ID_NOT_FOUND
        
        user_doc = UserHelper.get_user_by_id(user_id)        
        if not user_doc: return ApiResponse.RIDE_USER_NOT_FOUND
        
        ride_doc['user']=user_doc
        return ride_doc
    
    @classmethod
    def do_action(klass, action, ride_id, match_ride_id):
        if action == Ride.ACTION_REQUEST:
            return klass.request_match(ride_id, match_ride_id)
        elif action == Ride.ACTION_ACCEPT:
            return klass.accept_match(ride_id, match_ride_id)
        elif action == Ride.ACTION_DECLINE:
            return klass.decline_match(ride_id, match_ride_id)
        else: 
            return ApiResponse.RIDE_NO_ACTION
    
    @classmethod
    def request_match(klass, ride_id, match_ride_id):
        ride = klass.get_ride(ride_id)
        match = klass.get_ride(match_ride_id)
        
        match_currently_pending_id = match.get(Ride.A_PENDING_RIDE_ID)
        
        if match_currently_pending_id and match_currently_pending_id != ride_id:
            return ApiResponse.RIDE_CURRENTLY_PENDING

        # update the status of both ride ids to be STATUS_PENDING
        requested = Ride.request_match(ride_id, match_ride_id)
        if not requested:
             return ApiResponse.RIDE_COULD_NOT_REQUEST_MATCH
        
        klass.notify_users(ride, match, action=Ride.ACTION_REQUEST)
        return ApiResponse.RIDE_MATCH_REQUESTED


    @classmethod
    def accept_match(klass, ride_id, match_ride_id):
        ride = klass.get_ride(ride_id)
        match = klass.get_ride(match_ride_id)

        # ensure that both rides have STATUS_PENDING
        if (ride.get(Ride.A_STATUS) != Ride.STATUS_PENDING or 
            match.get(Ride.A_STATUS) != Ride.STATUS_PENDING):
            return ApiResponse.RIDE_COULD_NOT_ACCEPT_MATCH
        
        matched = Ride.create_match(ride_id, match_ride_id)
        if not matched:
            return ApiResponse.RIDE_COULD_NOT_ACCEPT_MATCH
        
        klass.notify_users(ride, match, action=Ride.ACTION_ACCEPT)
        return ApiResponse.RIDE_MATCH_ACCEPTED
        
    
    @classmethod
    def decline_match(klass, ride_id, match_ride_id):
        ride = klass.get_ride(ride_id)
        match = klass.get_ride(match_ride_id)
        # ensure that both rides have STATUS_PENDING
        
        if (ride.get(Ride.A_STATUS) != Ride.STATUS_PENDING or 
            match.get(Ride.A_STATUS) != Ride.STATUS_PENDING):
            return ApiResponse.RIDE_COULD_NOT_DECLINE_MATCH
        
        declined = Ride.decline_match(ride_id, match_ride_id)
        if not declined:
            return ApiResponse.RIDE_COULD_NOT_DECLINE_MATCH

        klass.notify_users(ride, match, action=Ride.ACTION_DECLINE)
        return ApiResponse.RIDE_MATCH_DECLINED

    @classmethod
    def notify_users(klass, ride, match, action):
        ride = klass.format_ride(ride)
        match = klass.format_ride(match)

        # get name of the curr_user
        from_first_name = ride.get('user').get(User.A_FIRST_NAME)
        from_last_name = ride.get('user').get(User.A_LAST_NAME)
        
        # get the phone number of the match_id
        to_first_name = match.get('user').get(User.A_FIRST_NAME)
        to_phone_number = match.get('user').get(User.A_PHONE)

        if action == Ride.ACTION_REQUEST:
            note = "Hi %s, great news! %s wants to split a ride with you! Go to the app to check out details!" % (to_first_name, from_first_name +" "+ from_last_name)
        elif action == Ride.ACTION_ACCEPT:
            note = "Hi %s! %s has accepted your request to split a ride! Wahoo!" % (to_first_name, from_first_name)
        elif action == Ride.ACTION_DECLINE:
            note = "Sorry %s, %s has declined to split a ride." % (to_first_name,
                                                                   from_first_name)

        # send sms and return twilio response
        twilio_resp = TwilioHelper.send_sms(note, to_phone_number)
        if not twilio_resp:
            return ApiResponse.RIDE_COULD_NOT_REQUEST_MATCH

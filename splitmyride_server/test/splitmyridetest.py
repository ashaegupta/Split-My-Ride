# Test file
import splitmyride_settings
# this will ensure that we only deal with test database collections from this file
splitmyride_settings.ON_TEST = True

from lib.UserHelper import UserHelper
from lib.RideHelper import RideHelper
import time
import datetime
from model.Ride import Ride
from model.User import User
from model.Terminal import Terminal
from test.test_data import test_data

def purge_test_database():
    User.mdbc().remove()
    Ride.mdbc().remove()
    Terminal.mdbc().remove()
    User.setup_mongo_indexes()
    Ride.setup_mongo_indexes()
    Terminal.setup_mongo_indexes()
    
def test_all():
    purge_test_database()
    add_users()
    get_users()
    prepending_ride_id = add_rides()
    rides = get_matches(prepending_ride_id)
    print rides
    
    ride_requested = get_ride_by_phone(rides, test_data.user_4.get('phone'))
    ride_requested_id = ride_requested.get(Ride.A_RIDE_ID)
    print ride_request_id
    #request_match(prepending_ride_id, ride_requested_id)
    #get_matches(prepending_ride_id)
    #get_matches(ride_requested_id)
    
def get_ride_by_phone(rides, phone):
    for ride in rides:
        for k, v in ride.iteritems():
            if k=="user":
                if v.get(User.A_PHONE)==phone:
                    return ride
    return ""
    
def add_users():
    # Create a new user
    
    first_name = test_data.user_1.get('first_name')
    last_name = test_data.user_1.get('last_name')
    phone = test_data.user_1.get('phone')
    image_url = test_data.user_1.get('img_url')

    # Store the user
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id
    
    # Create a new user
    first_name = test_data.user_2.get('first_name')
    last_name = test_data.user_2.get('last_name')
    phone = test_data.user_2.get('phone')
    image_url = test_data.user_2.get('img_url')
    
    # Store the user
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id

    # Create a new user
    first_name = test_data.user_3.get('first_name')
    last_name = test_data.user_3.get('last_name')
    phone = test_data.user_3.get('phone')
    image_url = test_data.user_3.get('img_url')
    
    # Store the user
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id

    # Create a new user
    first_name = test_data.user_4.get('first_name')
    last_name = test_data.user_4.get('last_name')
    phone = test_data.user_4.get('phone')
    image_url = test_data.user_4.get('img_url')

    # Store the user to match
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id

def get_users(): 
    # Get the user info
    phone = test_data.user_1.get('phone')
    print "get user with phone number: " 
    print phone
    print UserHelper.get_user_by_phone(phone)

    phone = test_data.user_4.get('phone')
    print "get user with phone number: " 
    print phone
    print UserHelper.get_user_by_phone(phone)

def add_rides(): 
    # Using user_1 add a ride that will be used to search for matches
    phone = test_data.user_1.get('phone')
    user = UserHelper.get_user_by_phone(phone)
    user_id = user.get(User.A_USER_ID)
    dt = datetime.datetime.now()
    departure_timestamp = time.mktime(dt.timetuple())
    dest_lat = 40.65 
    dest_lon = 73.78
    origin = """ {
        "origin_1":"jfk",
        "origin_2":"Terminal A"
        } """
    ride_id = RideHelper.create_or_update_ride(user_id, origin, dest_lon, dest_lat, departure_timestamp)
        
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "ride to match"
    print ride
    print "ride to match id"
    print ride_id
    ride_to_match_id = ride_id

    # Check for a ride that does not exist
    ride_id = "10291032491203"
    ride = RideHelper.get_ride(ride_id)
    print "should return an error, no ride exists"
    print ride
    
    # Switch users to user_4
    phone = test_data.user_4.get('phone')
    user = UserHelper.get_user_by_phone(phone)
    user_id = user.get("user_id")
    print "current user:"
    print user

    # Create another ride that will leave in 2 hrs for user_4
    ride_id = RideHelper.create_or_update_ride(user_id, origin, dest_lon, dest_lat, departure_timestamp+60*2*60)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride that will leave 2 hrs later"
    print ride

    # Create another ride that will go to a far away destination for user_4
    ride_id = RideHelper.create_or_update_ride(user_id, origin, dest_lon+10, dest_lat+10, departure_timestamp)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with far away destination"
    print ride

    # Create another ride that will be an ideal match, only .5 degrees further for user_4
    ride_id = RideHelper.create_or_update_ride(user_id, origin, dest_lon+0.005, dest_lat+0.005, departure_timestamp)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with only .5 degrees distance from ride to match"
    print ride

    # Switch to user 3
    phone = test_data.user_3.get('phone')
    user = UserHelper.get_user_by_phone(phone)
    user_id = user.get(User.A_USER_ID)

    # Create another ride that will be an ideal match with only .5 degrees further for user_3
    ride_id = RideHelper.create_or_update_ride(user_id, origin, dest_lon+0.003,  dest_lat+0.003, departure_timestamp+10*60)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with only .3 degrees distance from ride to match"
    print ride

    # Create another ride that leaves from a different origin for user_3
    origin = """{
            "origin_1":"lga",
            "origin_2":"Terminal B"
        }"""
    ride_id = RideHelper.create_or_update_ride(user_id, origin, dest_lon, dest_lat, departure_timestamp)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with different origin, same max distance"
    print ride
    return ride_to_match_id

def get_matches(ride_to_match_id):
    # Get matches
    print "ride to match_id"
    print ride_to_match_id
    rides = RideHelper.get_matches(ride_to_match_id)
    print "rides"
    print rides
    return rides

def request_match(curr_user_ride_id, match_ride_id):
    resp = RideHelper.request_match(curr_user_ride_id, match_ride_id)
    print "requested match"
    print resp
    return resp

def get_matches(curr_user_ride_id):
    resp = RideHelper.get_matches(curr_user_ride_id)
    doc = RideHelper.get_ride_and_user_docs_from_ride_id(curr_user_ride_id)
    print "get matches for %s" % doc.get("user").get(User.A_FIRST_NAME)
    print resp
    return resp

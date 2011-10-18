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
    ride_to_match_id = add_rides()
    get_matches(ride_to_match_id)
    
def add_users():
    # Create a new user
    first_name = "Helen"
    last_name = "Sadowski"
    phone = "7804552743"
    image_url = "asdf.jpg"

    # Store the user
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id
    
    # Create a new user
    first_name = "Michael"
    last_name = "Gupta"
    phone = "9051112222"
    image_url = "asdf.jpg"

    # Store the user
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id

    # Create a new user
    first_name = "Asha"
    last_name = "Gupta"
    phone = "6507042373"
    image_url = "asdf.jpg"

    # Store the user
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id

    # Create a new user
    first_name = "Shreyans"
    last_name = "Bhansali"
    phone = "1111111111"
    image_url = "asdf.jpg"

    # Store the user to match
    user_id = UserHelper.add_user(first_name=first_name, last_name=last_name, phone=phone, image_url=image_url)
    print user_id

def get_users(): 
    # Get the user info
    phone = "6507042373"
    print "get user with phone number: " 
    print phone
    print UserHelper.get_user_by_phone(phone)

    phone = "1111111111"
    print "get user with phone number: " 
    print phone
    print UserHelper.get_user_by_phone(phone)

def add_rides(): 
    # Create a ride to be matched
    phone = "6507042373"
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
    ride_id = RideHelper.add_ride(user_id, origin, dest_lon, dest_lat, departure_timestamp)
        
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
    
    # Switch users
    user = UserHelper.get_user_by_phone("1111111111")
    user_id = user.get("user_id")
    print "current user:"
    print user

    # Create another ride that will leave in 2 hrs
    ride_id = RideHelper.add_ride(user_id, origin, dest_lon, dest_lat, departure_timestamp+60*2*60)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride that will leave 2 hrs later"
    print ride

    # Create another ride that will go to a far away destination
    ride_id = RideHelper.add_ride(user_id, origin, dest_lon+10, dest_lat+10, departure_timestamp)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with far away destination"
    print ride

    # Create another ride that will be an ideal match, only .5 degrees further
    ride_id = RideHelper.add_ride(user_id, origin, dest_lon+0.005, dest_lat+0.005, departure_timestamp)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with only .5 degrees distance from ride to match"
    print ride

    # Get another user
    user = UserHelper.get_user_by_phone("9051112222")
    user_id = user.get(User.A_USER_ID)

    # Create another ride that will be an ideal match with only .5 degrees further
    ride_id = RideHelper.add_ride(user_id, origin, dest_lon+0.003,  dest_lat+0.003, departure_timestamp+10*60)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with only .3 degrees distance from ride to match"
    print ride

    # Create another ride that leaves from a different origin
    origin = """{
            "origin_1":"lga",
            "origin_2":"Terminal B"
        }"""
    ride_id = RideHelper.add_ride(user_id, origin, dest_lon, dest_lat, departure_timestamp)
    # Check to see that the ride info was stored
    ride = RideHelper.get_ride(ride_id)
    print "Ride with different origin, same max distance"
    print ride
    
    return ride_to_match_id

def get_matches(ride_to_match_id):
    # Get matches
    print ride_to_match_id
    rides = RideHelper.get_matches(ride_to_match_id)
    pri

# Test file

from lib.UserHelper import UserHelper
from lib.RideHelper import RideHelper
import time
import datetime
from model.Ride import Ride
from model.User import User

# Create a new users
first_name = "Helen"
last_name = "Sadowski"
phone = "7804552741"
image_url = "asdf.jpg"

# Store the user
user_id = UserHelper.add_user(first_name, last_name, phone, image_url)
user_id_to_match = user_id

# Get the user info
print UserHelper.get_user_by_phone("7804552741")

# Create a ride with this user, that will be used at the ride to match
dt = datetime.datetime.now()
departure_timestamp = time.mktime(dt.timetuple())
dest_lat = 40.65 
dest_lon = 73.78
origin = """ {
    "origin_1":"jfk",
    "origin_2":"Terminal A"
    } """
ride_id = RideHelper.add_ride(user_id, origin, dest_lat, dest_lon, departure_timestamp)
ride_to_match = ride_id

# Check to see that the ride info was stored
ride = RideHelper.get_ride(ride_id)
print "ride to match"
print ride

# Check for a ride that does not exist
ride_id = "10291032491203"
ride = RideHelper.get_ride(ride_id)
print "should return an error, no ride exists"
print ride

# Switch users
user = UserHelper.get_user_by_phone("7804552742")
user_id = user.get("user_id")
print "current user:"
print user

# Create another ride that will leave in 2 hrs
ride_id = RideHelper.add_ride(user_id, origin, dest_lat, dest_lon, departure_timestamp+(60*2*60))
# Check to see that the ride info was stored
ride = RideHelper.get_ride(ride_id)
print "Ride that will leave 2 hrs later"
print ride

# Create another ride that will go to a far away destination
ride_id = RideHelper.add_ride(user_id, origin, dest_lat=dest_lon, dest_lon=dest_lat, departure_timestamp))
# Check to see that the ride info was stored
ride = RideHelper.get_ride(ride_id)
print "Ride with far away destination"
print ride

# Create another ride that will be an ideal match, only .5 degrees further
ride_id = RideHelper.add_ride(user_id, origin, dest_lat+0.5, dest_lon+0.5, departure_timestamp))
# Check to see that the ride info was stored
ride = RideHelper.get_ride(ride_id)
print "Ride with only .5 degrees distance from ride to match"
print ride

# Get another user
user_id = UserHelper.get_user_by_phone("6469152002")

# Create another ride that will be an ideal match with only .5 degrees further
ride_id = RideHelper.add_ride(user_id, origin, dest_lat+0.3, dest_lon+0.3, departure_timestamp+10*60))
# Check to see that the ride info was stored
ride = RideHelper.get_ride(ride_id)
print "Ride with only .3 degrees distance from ride to match"
print ride

# Create another ride that leaves from a different origin
origin = """{
        "origin_1":"lga"
        "origin_2":"Terminal B"
    }"""
ride_id = RideHelper.add_ride(user_id, origin, dest_lat, dest_lon, departure_timestamp))
# Check to see that the ride info was stored
ride = RideHelper.get_ride(ride_id)
print "Ride with different origin"
print ride

# Get matches
rides = RideHelper.get_matches(ride_to_match)
print rides

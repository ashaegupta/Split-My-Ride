## Stores and retrieves rides

## Columns
# rideID
# userID
# To
# From
# Time
# Match (0 = no match
#        rideID2 = match
#        -1 = expired...24 hrs past time)


####### SHOULD I STORE THE user's info in here as well, like their images, name, etc? 
####### or should i just create a user object with that info on the app side that pulls from models/users and links to this based
####### on userID?


## Functions
def storeRide(userID, To, From, Time):
    generate a rideID
    store userID, To, From, Time

def getRidebyFrom(str departure):
    return a dictionary of rides that are leaving from departure and are NOT matched and are NOT expired
    
def getRidebyUser(str userID):
    return a dicitionary of rides that are from userID that are NOT matched and are NOT expired
    
def getBestMatches(str departure, str destination):
    return a dicitionary of rides that are leaving from departure and going to destination that are NOT matched and are NOT expired
    
def storeMatch(str rideID1, str rideID2):
    rideID1.match = rideID2
    rideID2.match = rideID1 (but store in the database)
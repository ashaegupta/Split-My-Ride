import datetime
import math
import time

def datetime_to_timestamp(datetime_ob):
    return time.mktime(datetime_ob.timetuple())

def datetime_from_timestamp(timestamp):
    return datetime.datetime.fromtimestamp(timestamp)
    
def distance_between_two_points(loc1, loc2):
    lon1 = loc1[0]
    lat1 = loc1[1]
    lon2 = loc2[0]
    lat2 = loc2[1]
    #
    # http://www.geesblog.com/2009/01/calculating-distance-between-latitude-longitude-pairs-in-python/
    # The following formulas are adapted from the Aviation Formulary
    # http://williams.best.vwh.net/avform.htm
    #
    nauticalMilePerLat = 60.00721
    nauticalMilePerLongitude = 60.10793
    rad = math.pi / 180.0
    kmPerNauticalMile = 1.85200
    yDistance = (lat2 - lat1) * nauticalMilePerLat
    xDistance = (math.cos(lat1 * rad) + math.cos(lat2 * rad)) * (lon2 - lon1) * (nauticalMilePerLongitude / 2)
    distance = math.sqrt( yDistance**2 + xDistance**2 )
    return distance * kmPerNauticalMile
    

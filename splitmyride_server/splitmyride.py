import re
import urlparse
import urllib
from urlparse import parse_qs, parse_qsl

import tornado.httpserver
import tornado.ioloop
import tornado.web

import settings

from model.User import User
from lib.UserHelper import UserHelper


## Sets up all the HTTP Get / Post requests using Tornado, listening on port 80
class UserHandler(tornado.web.RequestHandler):
    
    # Get user info
    def get(self):
        if re.match('^/splitmyride/user.*$', self.request.uri):
            self.write(self.get_user_by_phone)
    
    # Get user info from database        
    def get_user_by_phone(self):
        phone = self.get_argument('phone')
        return UserHelper.get_user_by_phone(phone)
       
    # Add a new user with first_name, last_name, phone and image_url
    def post(self):
        if re.match('^/splitmyride/user.*$', self.request.uri):
            self.write(self.add_user())

    # Add user to database
    def add_user(self):
        first_name = self.get_argument('first_name') 
        last_name = self.get_argument('last_name')
        image_url = self.get_argument('image_url') 
        phone = self.get_argument('phone')
        return UserHelper.add_user(first_name, last_name, image_url, phone)
        

class AddRideHandler(tornado.web.RequestHandler):

    # Add a new ride
    def post(self):
        if re.match('^/splitmyride/addRide.*$', self.request.uri):
            self.write(self.add_ride())

    # Add user to database
    def add_ride(self):
        user_id = self.get_argument('user_id') 
        origin = self.get_argument('origin')
        destination = self.get_argument('destination') 
        time = self.get_argument('time')
        return RideHelper.add_ride(user_id, origin, destination, time)

class GetMatches(tornado.web.RequestHandler):
    
    def get(self):
        if re.match('^/splitmyride/getMatches.*$', self.request.uri):
            self.write(self.get_matches())
            
    def get_matches(self):
        ride_id = self.get_argument('ride_id')
        user_id = self.get_argument('user_id')
        return RideHelper.get_matches(ride_id)
        




application = tornado.web.Application([
    (r"/splitmyride/user.*", UserHandler),
    (r"/splitmyride/addRide.*", AddRideHandler),
    (r"/splitmyride/getMatches.*", GetPotentialMatchesHandler),
    (r"/splitmyride/Match.*", RequestMatchHandler),
    (r"/splitmyride/requestMatchResponse.*", RequestMatchResponseHandler),
    (r"/splitmyride/terminalsInfo.*", TerminalsHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    
## COnvert string into a dictionary
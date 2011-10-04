# Main function

## Sets up all the HTTP Get / Post requests using Tornado, listening on port 80



### FUNCTIONS
# Store a ride
# Get all rides from a certain location
# Get the best match for a departure, destination pair
# Get all rides for a specific user
# Get terminals & airline lists
# Save user info
# Get user info


### Is this where I should put chron calls? Put them in the init method of this class?

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

class UserHandler(tornado.web.RequestHandler):
    
    # Get user info
    def get(self):
        if re.match('^/splitmyride/user.*$', self.request.uri):
            return self.get_user()
            
    def get_user(self):
        phone = self.get_argument('phone')
        UserHelper.get_user(phone)
        ## NEED TO CHANGE THIS BACK INTO JSON?
       
    # Add a new user with first_name, last_name, phone and image_url
    def post(self):
        if re.match('^/splitmyride/user.*$', self.request.uri):
            return self.add_user()

    # Add user to database
    def add_user(self):
        first_name = self.get_argument('first_name') 
        last_name = self.get_argument('last_name')
        image_url = self.get_argument('image_url') 
        phone = self.get_argument('phone')
        
        user_id = UserHelper.add_user(first_name, last_name, image_url, phone)
        status = "success"
        if not user_id:
            status = "failed"
        return self.redirect('/splitmyride/user?%s=1', status=status)  % status
        
        
        



application = tornado.web.Application([
    (r"/splitmyride/user.*", UserHandler),
    (r"/splitmyride/addRide.*", AddRideHandler),
    (r"/splitmyride/viewPotentialMatches.*", ViewPotentialMatchesHandler),
    (r"/splitmyride/requestMatch.*", RequestMatchHandler),
    (r"/splitmyride/requestMatchResponse.*", RequestMatchResponseHandler),
    (r"/splitmyride/terminalsInfo.*", TerminalsHandler),
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    

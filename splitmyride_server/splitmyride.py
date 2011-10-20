import re

import tornado.httpserver
import tornado.ioloop
import tornado.web

from lib.RideHelper import RideHelper
from lib.TerminalHelper import TerminalHelper
from lib.UserHelper import UserHelper

from lib import ApiResponse

class BaseHandler(tornado.web.RequestHandler):
    def require_params(self, required_params):
        missing_params = []
        for param in required_params:
            if param not in self.arguments:
                missing_params.append(param)
        if missing_params:
            error = ApiResponse.API_MISSING_PARAMS
            error['message'] += ' %s' % ', '.join(missing_params)
            self.finish(error)
            return False
        return True

## Sets up all the HTTP Get / Post requests using Tornado, listening on port 80
class UserHandler(BaseHandler):
    
    # Get user info
    def get(self):
        user = {}
        m = re.match('^/user/([\d].*)$', self.request.uri)
        if m:
            phone = m.group(1)
            user = UserHelper.get_user_by_phone(phone)
        self.write(user)
       
    # Add a new user with first_name, last_name, phone and image_url
    def post(self):
        required_params = ['first_name', 'last_name', 'image_url', 'phone']
        # returning becuase calling write() a few lines below will throw an error
        # since require_params already called write() or finish()
        if not self.require_params(required_params): return
        first_name = self.get_argument('first_name') 
        last_name = self.get_argument('last_name')
        image_url = self.get_argument('image_url') 
        phone = self.get_argument('phone')
        resp = UserHelper.add_user(first_name, last_name, image_url, phone)
        self.write(resp)
        
class RideHandler(BaseHandler):

    def post(self):
        required_params = ['user_id', 'origin', 'dest_lon', 'dest_lat', 'departure_time']
        if not self.require_params(required_params): return
        user_id = self.get_argument('user_id') 
        origin = self.get_argument('origin')
        dest_lon = self.get_argument('dest_lon') 
        dest_lat = self.get_argument('dest_lat')
        departure_time = self.get_argument('departure_time')
        resp = RideHelper.create_or_update_ride(user_id, origin, 
                                                dest_lon, dest_lat, 
                                                departure_time)
        self.write(resp)

class MatchHandler(BaseHandler):
    
    def get(self):
        matches = {}
        m = re.match('^/match/([0-9a-f]){32}$', self.request.uri)
        if m:
            ride_id = m.group(1)
            matches = RideHelper.get_matches(ride_id)
        self.write(matches)
    
    # Request, accept or decline a match
    def post(self):
        required_params = ['action', 'ride_id', 'match_ride_id']
        if not self.require_params(required_params): return
        action = self.get_argument('action')
        ride_id = self.get_argument('ride_id')
        match_ride_id = self.get_argument('match_ride_id')
        resp = RideHelper.do_action(action, ride_id, match_ride_id)
        self.write(resp)

class TerminalHandler(BaseHandler):

    def get(self):
        terminals = {}
        m = re.match('^/terminal/([a-zA-Z]){3}$', self.request.uri)
        if m:
            airport = m.group(1)
            terminals = TerminalHelper.get_terminals(airport)
        self.write(terminals)

application = tornado.web.Application([
    #(r"/", MainHandler),                 # get() - homepage - link to app
    (r"/user/.*", UserHandler),          # get() - get user data; post() - create a user
    (r"/ride/.*", RideHandler),          # post() - create or edit a ride
    (r"/match/.*", MatchHandler),        # get() - list of matches / match for a ride; post() - request/accept/decline a match
    (r"/terminal/.*", TerminalHandler),  # get() - get a list of terminals by airline
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    
## Convert string into a dictionary

# --- urls ---
# user/:phone
# - get() a user's data, e.g. http://splitmyri.de/user/6469152002
# user/add
# - post() to create a user, e.g. http://splitmyri.de/user/add with a POST body containing all the data to create the user

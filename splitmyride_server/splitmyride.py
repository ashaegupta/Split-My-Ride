import re

import tornado.httpserver
import tornado.ioloop
import tornado.web
import simplejson

from lib.RideHelper import RideHelper
from lib.TerminalHelper import TerminalHelper
from lib.UserHelper import UserHelper
from lib import ApiResponse

class BaseHandler(tornado.web.RequestHandler):
    def check_params(self, required_params):
        missing_params = []
        invalid_types = {}
        
        for param, param_type in required_params.iteritems():
            if param not in self.request.arguments.keys():
                missing_params.append(param)
            else:
                try:
                    if param_type == 'str':
                        eval(param_type)(self.get_argument(param))
                    elif param_type == 'int':
                        int(float(self.get_argument(param)))
                    elif param_type == 'float':
                        float(self.get_argument(param))
                except:
                    invalid_types[param]=param_type
        
        if missing_params or invalid_types:
            error = ApiResponse.API_MISSING_OR_INVALID_PARAMS
            if missing_params:
                error['message'] += ApiResponse.API_MISSING_PARAMS_MSG + ' %s. ' % ', '.join(missing_params)
            if invalid_types:
                error['message'] += (' %s cannot be typecasted to a(n) %s, respectively.' 
                                                    % (', '.join(invalid_types.keys()), 
                                                       ', '.join(invalid_types.values())))
            self.finish(error)
            return False
        return True

## Sets up all the HTTP Get / Post requests using Tornado, listening on port 80
class UserHandler(BaseHandler):
    
    # Get user info by their phone number
    def get(self):
        user = {}
        m = re.match('^/user/([\d].*)$', self.request.uri)
        if m:
            phone = m.group(1)
            user = UserHelper.get_user_by_phone(phone)
        self.write(user)
       
    # Add a new user with first_name, last_name, phone and image_url
    def post(self):
        required_params = {
            'first_name':'str',
            'last_name':'str',
            'image_url':'str',
            'phone':'str'
        }
        # returning becuase calling write() a few lines below will throw an error
        # since check_params already called write() or finish()
        if not self.check_params(required_params): return
        first_name = self.get_argument('first_name') 
        last_name = self.get_argument('last_name')
        image_url = self.get_argument('image_url') 
        phone = self.get_argument('phone')
        resp = UserHelper.add_user(first_name=first_name, last_name=last_name, image_url=image_url, phone=phone)
        self.write(resp)
        
class RideHandler(BaseHandler):

    # Post a new ride to the database with the following data
    #       user_id = string
    #       origin = string wrapped list with two elements, venue_id and place pick-up
    #       dest_lon = longitude of destination
    #       dest_lat = latitude of destination
    #       departure time = desired time of departure
    #       TODO: Clean up this method, change required_params to be a dictionary that also checks for type.
    def post(self):
        required_params = {
            'user_id':'str',
            'origin_venue':'str',
            'dest_lon':'float',
            'dest_lat':'float',
            'departure_time':'float'
        }
        if not self.check_params(required_params): return
        
        if 'ride_id' not in self.request.arguments or not self.get_argument('ride_id'): ride_id=None            
        else: ride_id=self.get_argument('ride_id')
        
        if 'origin_pickup' not in self.request.arguments or not self.get_argument('origin_pickup'): origin_pickup=None            
        else: origin_pickup=self.get_argument('origin_pickup')
        
        user_id = self.get_argument('user_id')
        origin_venue = self.get_argument('origin_venue')
        origin_pick_up = self.get_argument('origin_pickup')
        dest_lon = float(self.get_argument('dest_lon'))
        dest_lat = float(self.get_argument('dest_lat'))
        departure_time = float(self.get_argument('departure_time')
            
        resp = RideHelper.create_or_update_ride(user_id=user_id, ride_id=ride_id, origin_venue=origin_venue, 
                                                origin_pick_up=origin_pickup,
                                                dest_lon=dest_lon, dest_lat=dest_lat, 
                                                departure_time=departure_time)
        self.write(resp)

class MatchHandler(BaseHandler):
    
    # Get the matches for a given ride_id.
    #   If the ride_id is PREPENDING, returns a list of potential matches
    #   If the ride_id is PENDING, returns the requested match to be confirmed
    #   If the ride_id is MATCHED, returns the match
    def get(self):
        matches = {}
        m = re.match('^/match/([0-9a-f]{32})$', self.request.uri)
        if m:
            ride_id = m.group(1)
            matches = RideHelper.get_matches(ride_id)
            matches_js = simplejson.dumps(matches)
        self.write(matches_js)
    
    # Request, accept or decline a match
    def post(self):
        required_params = {
            'action':'str',
            'ride_id':'str',
            'match_ride_id':'str'
        }
        if not self.check_params(required_params): return
        action = self.get_argument('action')
        ride_id = self.get_argument('ride_id')
        match_ride_id = self.get_argument('match_ride_id')
        resp = RideHelper.do_action(action=action, ride_id=ride_id, match_ride_id=match_ride_id)
        self.write(resp)

class TerminalHandler(BaseHandler):

    def get(self):
        terminals = {}
        m = re.match('^/terminal/([a-zA-Z]{3})$', self.request.uri)
        if m:
            airport = m.group(1)
            terminals = TerminalHelper.get_terminals(airport)
        self.write(terminals)

class MainHandler(BaseHandler):
    def get(self):
        self.write("This is the homepage")

application = tornado.web.Application([
    (r"/", MainHandler),                 # get() - homepage - link to app
    (r"/user/.*", UserHandler),       # get() - get user data; post() - create a user
    (r"/ride/.*", RideHandler),          # post() - create or edit a ride
    (r"/match/.*", MatchHandler),        # get() - list of matches / match for a ride; post() - request/accept/decline a match
    (r"/terminal/.*", TerminalHandler),  # get() - get a list of terminals by airline
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.ioloop.IOLoop.instance().start()
    
# --- urls ---
# user/:phone
# - get() a user's data, e.g. http://splitmyri.de/user/5555555555
# user/
# - post() to create a user, e.g. http://splitmyri.de/user/ with a POST body containing all the data to create the user
# user  /:phone
# - get() a user's data, e.g. http://splitmyri.de/user/5555555555
# user/
# - post() to create a user, e.g. http://splitmyri.de/user/ with a POST body containing all the data to create the user


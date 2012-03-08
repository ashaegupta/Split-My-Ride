import re

import tornado.httpserver
import tornado.autoreload
import tornado.ioloop
import tornado.web
import simplejson

import search

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
class SearchHandler(BaseHandler):
    
    # Search for places
    def get(self):
        required_params = {
            'term':'str',
            'location':'str',
            'lat':'float',
            'lon':'float'
        }

        if not self.check_params(required_params): return
        term = self.get_argument('term') 
        location = self.get_argument('location')
        lat = self.get_argument('lat') 
        lon = self.get_argument('lon')    
        
        resp = search.do(term=term, location=location, lat=lat, lon=lon)
        self.write(resp)
        
        
class MainHandler(BaseHandler):
    def get(self):
        self.write("This is the homepage")

application = tornado.web.Application([
    (r"/", MainHandler),                 # get() - homepage - link to app
    (r"/search/.*", SearchHandler),       # get() - get user data; post() - create a user
])

if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(80)
    tornado.autoreload.start()
    tornado.ioloop.IOLoop.instance().start()
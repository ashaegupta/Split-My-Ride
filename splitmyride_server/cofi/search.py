import oauth2
import settings
import simplejson as json
import urllib
import urllib2
from place import Place
import place

YELP_WIFI_CAFE_SEARCH_TERM ='wifi+cafe'
YELP_ROOT_URL = 'http://api.yelp.com/v2/search?term='
YELP_BUSINESSES_TERM = "businesses"

def do(term="", location="", lat=None, lon=None):
    url = make_search_url(term, location, lat, lon)
    signed_url = get_signed_url(url)
    response = get_results(signed_url)
    return parse_results(response)

def make_search_url(term, location, lat, lon):
    if(term==""):
        term = YELP_WIFI_CAFE_SEARCH_TERM
    if(location == ""):
        return YELP_ROOT_URL + term + "&ll=" + str(lat) + "," + str(lon)
    else:
        return YELP_ROOT_URL + term + "&location=" + location

def get_signed_url(url):
    consumer = oauth2.Consumer(settings.YELP_CONSUMER_KEY, settings.YELP_CONSUMER_SECRET)
    oauth_request = oauth2.Request('GET', url, {})
    oauth_request.update({'oauth_nonce': oauth2.generate_nonce(),
                          'oauth_timestamp': oauth2.generate_timestamp(),
                          'oauth_token': settings.YELP_TOKEN,
                          'oauth_consumer_key': settings.YELP_CONSUMER_KEY})

    token = oauth2.Token(settings.YELP_TOKEN, settings.YELP_TOKEN_SECRET)
    oauth_request.sign_request(oauth2.SignatureMethod_HMAC_SHA1(), consumer, token)
    return oauth_request.to_url()

def get_results(signed_url):
    # Connect
      try:
        conn = urllib2.urlopen(signed_url, None)
        try:
          response = json.loads(conn.read())
        finally:
          conn.close()
      except urllib2.HTTPError, error:
        response = json.loads(error.read())
      return response
    
def parse_results(response):
    places = []
    for b in response[YELP_BUSINESSES_TERM]:
        p = place.new_from_json(b)
        places.append(p)
    return places

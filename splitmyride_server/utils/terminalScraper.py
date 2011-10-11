import urllib2
from BeautifulSoup import BeautifulSoup
from model.Terminal import Terminal

# this file name should be upper case
def scrape_and_store_terminals(klass):
    all_airports_info = {}
    all_airports_info = klass.scrape_all_airports_info()
    response = Terminal.store_terminal_info(all_airports_info)

def scrape_all_airports_info(klass):
    all_airports_info = {}
    for airport in klass.airports:
        airlines = klass._get_airlines_by_airport(airport)
        all_airports_info[airport] = airlines
    return all_airports_info

def _scrape_airlines_by_airport(klass, airport):
    airlines = {}
    airport_html = "http://www.panynj.gov/airports/" + airport + "-airlines.html"
    data = urllib2.urlopen(airport_html).read()
    if not data:
        return
    soup = BeautifulSoup(data)
    for row in soup('table')[0].tbody('tr'):
        tds = row('td')
        airline = tds[0].a.string
        arrival_terminal = tds[4].string
        airlines[airline] = arrival_terminal
    return airlines
import urllib2
from BeautifulSoup import BeautifulSoup

airports = ["jfk", "ewr", "lga"]

def getAllTerminals(klass):
    terminals = {}
    for airport in klass.airports:
        terms = klass._getTerminals(airport)    
        terminals[airport] = terms
    return terminals

def _getTerminals(klass, airport):
    terms = {}
    airport_html = "http://www.panynj.gov/airports/" + airport + "-airlines.html"
    data = urllib2.urlopen(airport_html).read()
    if not data:
        return
    soup = BeautifulSoup(data)
    for row in soup('table')[0].tbody('tr'):
        tds = row('td')
        airline = tds[0].a.string
        arrival_terminal = tds[4].string
        terms[airline] = arrival_terminal
    return terms
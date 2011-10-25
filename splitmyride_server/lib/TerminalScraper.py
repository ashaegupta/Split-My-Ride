import logging
import urllib2
from BeautifulSoup import BeautifulSoup
from model.Terminal import Terminal

def scrape_and_store_terminals():
    all_airports_info = scrape_all_airports_info()
    response = Terminal.store_terminal_info(all_airports_info)

def scrape_all_airports_info():
    all_airports_info = {}
    airports = ['jfk', 'ewr', 'lga']
    for airport in airports:
        airlines = _scrape_airlines_by_airport(airport)
        all_airports_info[airport] = airlines
    return all_airports_info

def _scrape_airlines_by_airport(airport):
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

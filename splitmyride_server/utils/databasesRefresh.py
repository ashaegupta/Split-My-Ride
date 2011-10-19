### Runs a cron to refresh databases
import sys
sys.path.append("../")

from utils import terminalScraper
from model.Ride import Ride

def do_scrape():
    terminalScraper.scrape_and_store_terminals()
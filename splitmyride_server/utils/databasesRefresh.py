### Runs a cron to refresh databases
from utils import terminalScraper
from model.Ride import Ride

terminalScraper.scrape_and_store_terminals()

import sys
sys.path.append("../")
import logging
import uuid
import MongoMixIn

class Terminal(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'terminal'
    MONGO_COLLECTION_NAME   = 'terminal_c'
    
    A_AIRPORT               = 'airport'                          
    A_AIRLINE               = 'airline'
    A_TERMINAL              = 'terminal'
    
    ### Do I need to do this?
    @classmethod
    def setup_mongo_indexes(klass):
        coll = klass.mdbc()
    
    @classmethod
    def store_terminal_info(klass, all_airports_info=None):      
        success = True
        if not all_airports_info: all_airports_info = {}
        
        for airport, airlines in all_airports_info.iteritems():
            for airline, terminal in airlines.iteritems():
                doc = {
                    klass.A_AIRPORT: airport,
                    klass.A_AIRLINE: airline,
                    klass.A_TERMINAL: terminal
                }
                try:
                    klass.mdbc().update(spec=doc, document={"$set": doc}, upsert=True, safe=True) ## Assuming this will just update whatever is there
                except Exception, e:
                    print "error: %s. locals: %s" % (e, locals())
                    success = False
        return success

    @classmethod
    def get_terminal_info_by_airport(klass, airport):
        airlines = {}
        spec = {klass.A_AIRPORT:airport}
        docs = klass.mdbc().find(spec)
        airlines = klass.list_from_cursor(docs)
        return airlines
      

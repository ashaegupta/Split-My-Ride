import sys
sys.path.append("../")
import logging
import uuid
import MongoMixIn
import splitmyride_settings

class Terminal(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'terminal'
    
    if splitmyride_settings.ON_TEST:
        MONGO_COLLECTION_NAME   = 'terminal_c_test'
    else:
        MONGO_COLLECTION_NAME   = 'terminal_c'
    
    A_AIRPORT               = 'airport'                          
    A_AIRLINE               = 'airline'
    A_TERMINAL              = 'terminal'
    
    @classmethod
    def setup_mongo_indexes(klass):
        coll = klass.mdbc()
    
    @classmethod
    def store_terminal_info(klass, all_airports_info=None):      
        if not all_airports_info: all_airports_info = {}
        
        for airport, airlines in all_airports_info.iteritems():
            for airline, terminal in airlines.iteritems():
                doc = {
                    klass.A_AIRPORT: airport,
                    klass.A_AIRLINE: airline,
                    klass.A_TERMINAL: terminal
                }
                try:
                    klass.mdbc().update(spec=doc, document={"$set": doc}, upsert=True, safe=True)
                except Exception, e:
                    print "error: %s. locals: %s" % (e, locals())
                    return False
        return True

    @classmethod
    def get_terminal_info_by_airport(klass, airport):
        spec = {klass.A_AIRPORT:airport}
        docs = klass.mdbc().find(spec)
        airlines = klass.dict_from_cursor(docs, key=klass.A_AIRLINE, remove_object_id=True)
        return airlines
      

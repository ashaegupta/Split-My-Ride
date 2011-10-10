import sys
sys.path.append("../")
import logging
import uuid
import MongoMixIn

class Terminal(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'terminal'
    MONGO_COLLECTION_NAME   = 'terminal_c'
    
    A_ROW_ID                = 'id'
    A_AIRPORT               = 'airport'                          
    A_AIRLINE               = 'airline'
    A_TERMINAL              = 'terminal'
    
    ### Do I need to do this?
    @classmethod
    def setup_mongo_indexes(klass):
        coll = klass.mdbc()
    
    @classmethod
    def store_terminal_info(klass, all_airports_info=None):      
        if not all_airports_info: all_airports_info = {}
        
        for airport, airlines in all_airports_info.iteritems():
            for airline, terminal in airlines.iteritems():
                row_id = airport+"&"+airline
                spec=row_id
                doc = {"A_ID":row_id 
                       "A_AIRPORT": airport,
                       "A_AIRLINE": airline,
                       "A_TERMINAL": terminal
                        }
        try:
            klass.mdbc().update(spec=spec, document={"$set": doc}, upsert=True, safe=True) ## Assuming this will just update whatever is there
        except Exception, e:
            return False
        return row_id

    @classmethod
    def get_terminal_info_by_airport(klass, airport):
        airlines = {}
        try:
            # Return all rows with A_AIRPORT = airport

        if airline:
                airlines{airlines}
        return airlines
      
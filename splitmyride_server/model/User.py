import sys
sys.path.append("../")
import logging
import uuid
import datetime
import MongoMixIn



class User(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'user'
    MONGO_COLLECTION_NAME   = 'user_c'
    
    A_ID                    = 'id'                          # why "A_"? convention?
    A_FIRST_NAME            = 'first_name'
    A_LAST_NAME             = 'last_name'
    A_IMAGE_URL             = 'image_url'
    A_PHONE                 = 'phone'

    ### Do I need to do this?
    @classmethod
    def setup_mongo_indexes(klass):
        coll = klass.mdbc()
    
    @classmethod
    def create_or_update_user(klass, doc=None):      
        if not doc: doc = {}

        user_id = doc.get(klass.A_ID)       # Need to randomly generate a user_id
        if not user_id:
            user_id = str(uuid.uuid4())
        spec = {klass.A_ID:user_id}

        first_name = doc.get(klass.A_FIRST_NAME)
        last_name = doc.get(klass.A_LAST_NAME)
        image_url = doc.get(klass.A_IMG_URL)
        phone = doc.get(klass.A_PHONE)
                
        try:
            klass.mdbc().update(spec=spec, document={"$set": doc}, upsert=True, safe=True)
            return user_id
        except Exception, e:
            logging.error("COULD NOT UPSERT document in model.User Exception: %s" % e.message)
        return None

    @classmethod
    def get_user(klass, phone):
        spec = {klass.A_PHONE:phone}
        try:
            cursor = klass.mdbc().find(spec).limit(limit)
            return klass.list_from_cursor(cursor)
        except Exception, e:
            logging.error("COULD NOT retreieve user in model.User Exception: %s" % e.message)
        return None
        

# Things to add
# - input formatting check (phone number is all numbers)
#        
    
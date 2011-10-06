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

        try:
            klass.mdbc().update(spec=spec, document={"$set": doc}, upsert=True, safe=True)
            return {"user_id":user_id, "status":1}
        except Exception, e:
            logging.error("COULD NOT UPSERT document in model.User Exception: %s" % e.message)
        
        return {"status":0}

    @classmethod
    def get_user_by_phone(klass, phone):
        user = {}
        
        spec = {klass.A_PHONE:phone}
        try:
            cursor = klass.mdbc().find(spec).limit(limit)
            user = klass.dict_from_cursor()
            user["status"] = 1
        except Exception, e:
            logging.error("COULD NOT RETREIVE user in model.User Exception: %s" % e.message)
            user["status"] = 0
        
        return user
    
    @classmethod
    def get_users(klass, users=[]):
        users_info = {}
        
        for user_id in users:
            user = {}
            spec = {klass.A_ID:user_id}
            try:
                cursor = klass.mdbc().find(spec).limit(limit)
                user = klass.dict_from_cursor(cursor)
                user["status"] = 1
            except Exception, e:
                logging.error("COULD NOT RETREIVE user in model.User Exception: %s" % e.message)
                user["status"] = 0
            
            users_info[user_id] = user
        
        return users_info

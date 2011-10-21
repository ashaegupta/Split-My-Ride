import sys
sys.path.append("../")
import logging
import uuid
import datetime
import MongoMixIn
import splitmyride_settings

class User(MongoMixIn.MongoMixIn):    
    MONGO_DB_NAME           = 'user'
    
    if splitmyride_settings.ON_TEST:
        MONGO_COLLECTION_NAME = 'user_c_test'
    else:
        MONGO_COLLECTION_NAME = 'user_c'
    
    A_USER_ID               = 'user_id'
    A_FIRST_NAME            = 'first_name'
    A_LAST_NAME             = 'last_name'
    A_IMAGE_URL             = 'image_url'
    A_PHONE                 = 'phone'

    ### Do I need to do this?
    @classmethod
    def setup_mongo_indexes(klass):
        from pymongo import ASCENDING
        coll = klass.mdbc()
        coll.ensure_index([(klass.A_PHONE, ASCENDING)], unique=True)
        coll.ensure_index([(klass.A_USER_ID, ASCENDING)], unique=True)
    
    @classmethod
    def create_or_update_user(klass, doc=None):      
        if not doc: doc = {}

        user_id = doc.get(klass.A_USER_ID)
        if not user_id:
            user_id = uuid.uuid4().hex
        spec = {klass.A_USER_ID:user_id}

        try:
            klass.mdbc().update(spec=spec, document={"$set": doc}, upsert=True, safe=True)
        except Exception, e:
            logging.error("COULD NOT UPSERT document in model.User Exception: %s" % e.message)
            return False
            
        return user_id

    @classmethod
    def get_user_by_phone(klass, phone):
        spec = {klass.A_PHONE:phone}
        return klass.mdbc().find_one_remove_object_id(spec, remove_object_id=True)
    
    @classmethod
    def get_users_by_user_ids(klass, user_ids): 
        users_info = {}
        
        query = {klass.A_USER_ID:{"$in":user_ids}}
        cursor = klass.mdbc().find(query)
        users_info = klass.dict_from_cursor(cursor, key=klass.A_USER_ID, remove_object_id=True)
        
        return users_info

    @classmethod
    def get_user_by_user_id(klass, user_id): 
        spec = {klass.A_USER_ID:user_id}
        return klass.mdbc().find_one_remove_object_id(spec, remove_object_id=True)

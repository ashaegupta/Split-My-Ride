import simplejson

from model.User import User


class UserHelper(object):
    
    @classmethod
    def add_user(klass, first_name, last_name, image_url, phone):
        doc = {
            User.A_FIRST_NAME:first_name,
            User.A_LAST_NAME:last_name,
            User.A_IMAGE_URL:image_url,
            User.A_PHONE:phone
        }
        return simplejson.dumps(User.create_or_update_user(doc))
        
    @classmethod
    def get_user_by_phone(klass, phone):
        return simplejson.dumps(User.get_user_by_phone(phone))
    
    # Change this to be for a list of users
    @classmethod
        def get_users_by_id(klass, users=[]):
            return simplejson.dumps(User.get_users(users))
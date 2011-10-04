
from model.User import User

class UserHelper(object):
    
    @classmethod
    def add_user(klass, first_name, last_name, image_url, phone):
        doc = {
            User.A_FIRST_NAME:text,
            User.A_LAST_NAME:text,
            User.A_IMAGE_URL:text,
            User.A_PHONE:text
        }
        return User.create_or_update_user(doc)
        
    @classmethod
    def get_user(klass, phone):
        return User.get_user(phone)
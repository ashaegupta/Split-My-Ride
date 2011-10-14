from model.User import User
from lib import ApiResponse

class UserHelper(object):
    
    @classmethod
    def add_user(klass, first_name, last_name, phone, image_url):
        doc = {
            User.A_FIRST_NAME:first_name,
            User.A_LAST_NAME:last_name,
            User.A_IMAGE_URL:image_url,
            User.A_PHONE:phone
        }
        user_id = User.create_or_update_user(doc)
        
        if not user_id:
            return ApiResponse.USER_COULD_NOT_CREATE
        else:
            return {User.A_USER_ID: user_id}
        
    @classmethod
    def get_user_by_phone(klass, phone):
        user = User.get_user_by_phone(phone)
        if not user:
            return ApiResponse.USER_NOT_FOUND
        else:
            del user[User.A_OBJECT_ID]
            return user
        
    
    @classmethod
    def get_users_by_id(klass, user_ids):
        print "^"*100
        print user_ids
        print "^"*100
        users = User.get_users_by_user_ids(user_ids)
        print "*"*100
        print users
        print "*"*100
        if not users:
            return ApiResponse.USER_NOT_FOUND
        else:
            for uid, user in users.iteritems():
                try:
                    del users[uid][User.A_OBJECT_ID]
                except:
                    print "problem with user_id", user_id
            return users

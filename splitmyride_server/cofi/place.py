class Place():
    id = ""
    name = ""
    image_url = ""
    url = ""
    mobile_url = ""
    phone = ""
    diplay_phone = ""
    review_count = None
    rating = None
    rating_img_url = ""
    rating_img_url_small = ""
    location = {}
    location_coordinate = {}
    location_coordinate_latitude = None
    location_coordinate_longitude = None
    location_address = []
    location_display_address = []
    location_city = ""
    outlets = None #boolean
    food = None #boolean

# TODO Add all items
def new_from_json(json):
    place = Place()
    place.id = json["id"]
    place.name = json["name"]
    place.image_url = json["image_url"]
    place.location = json["location"]
    place.location_coordinate = place.location["coordinate"]
    place.location_coordinate_latitude = place.location_coordinate["latitude"]
    place.location_coordinate_longitude = place.location_coordinate["longitude"]
    place.review_count = json["review_count"]
    place.rating = json["rating"]
    place.rating_img_url_small = json["rating_img_url_small"]
    if json.has_key("phone"):
        place.phone = json["phone"]
    place.mobile_url = json["mobile_url"]
    return place

#TODO Add all items
def print_all(place):
    print place.id 
    print place.name
    print place.image_url
    print place.location
    print place.review_count
    print place.rating
    print place.rating_img_url_small
    print place.phone
    print place.mobile_url
    print place.location_coordinate_latitude
    print place.location_coordinate_longitude
    
    
    
'''
class Place():
    str_attrs = [
        "id",
        "name",
        "image_url",
        "url",
        "mobile_url",
        "phone",
        "display_phone",
        "rating_img_url",
        "rating_img_url_small",
        "location_city"
        ]
        
    num_attrs = [
        "location_coordinate_latitude",
        "location_coordinate_latitude",
        "review_count",
        "rating",
        "outlets",
        "food",
        ]
    
    dict_attrs = [
        "location",
        "location_coordinate",
        "location_address",
        "location_display_address"
        ]

    for s in str_attrs:
        setattr(self, s, "")
        
    for n in num_attrs:
        setattr(self, n, None)

    for n in num_attrs:
        setattr(self, n, None)

'''   
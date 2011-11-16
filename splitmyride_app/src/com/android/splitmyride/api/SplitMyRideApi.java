package com.android.splitmyride.api;

import java.util.ArrayList;
import java.util.List;

import org.apache.http.NameValuePair;
import org.apache.http.message.BasicNameValuePair;
import org.json.JSONException;
import org.json.JSONObject;

import com.android.splitmyride.classes.Ride;
import com.android.splitmyride.classes.User;
import com.android.splitmyride.data.AppPreferences;

public class SplitMyRideApi {

	public static final String ROOT = "http://splitmyri.de/";
	public static final String ERROR = "error";
	public static final String MESSAGE = "message";
	
	// Save a user object to the server
	public static String saveUser(User user) {
        List<NameValuePair> data = new ArrayList<NameValuePair>(4);   
        data.add(new BasicNameValuePair(AppPreferences.FIRST_NAME, user.firstName));
        data.add(new BasicNameValuePair(AppPreferences.LAST_NAME, user.lastName));
        data.add(new BasicNameValuePair(AppPreferences.PHONE, user.phone));
        data.add(new BasicNameValuePair(AppPreferences.IMAGE_URL, "testimage")); //TODO send actual image
        
        JSONObject json = ApiUtils.doHttpPost(ROOT + "user/", data);
        
        return returnOneString(json, AppPreferences.USER_ID);
	}
	

	// Save a ride to the server
	public static String saveRide(Ride ride) {
		List<NameValuePair> data = new ArrayList<NameValuePair>(7);
		data.add(new BasicNameValuePair(AppPreferences.RIDE_ID, ride.userId));
		data.add(new BasicNameValuePair(AppPreferences.RIDE_ID, ride.rideId));
		data.add(new BasicNameValuePair(AppPreferences.RIDE_ORIGIN_VENUE, ride.originVenue));
		data.add(new BasicNameValuePair(AppPreferences.RIDE_ORIGIN_PICKUP, ride.originPickup));
		data.add(new BasicNameValuePair(AppPreferences.RIDE_DEST_LON, ride.destLon.toString()));
		data.add(new BasicNameValuePair(AppPreferences.RIDE_DEST_LAT, ride.destLat.toString()));
		data.add(new BasicNameValuePair(AppPreferences.RIDE_DEPT_TIME_LONG, ride.deptTimeLong.toString()));
		
		JSONObject json = ApiUtils.doHttpPost(ROOT + "ride/", data);
        
        return returnOneString(json, AppPreferences.RIDE_ID);

	}
	
	// Method to return one string from a given JSON and check to see if an error exists
	public static String returnOneString(JSONObject json, String s) {
	    String response = "";
	       
        if (json.has(ERROR) && json.has(MESSAGE)) {
    	    try {
		  	response = json.getString(MESSAGE);
		  } catch (JSONException e) {
		  	e.printStackTrace();
		  }
        } else {
    	    try {
		  	response = json.getString(s);
		  } catch (JSONException e) {
		  	e.printStackTrace();
		  }
        }
        return response;
	}   
	
}

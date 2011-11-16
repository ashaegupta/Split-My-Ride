package com.android.splitmyride.data;

import java.util.Calendar;

import android.content.Context;
import android.content.SharedPreferences;
import android.util.Log;

import com.android.splitmyride.classes.Ride;
import com.android.splitmyride.classes.User;
import com.android.splitmyride.utils.TimeUtils;

/** All methods used to store, retrieve or clear user data stored persistently in SharedPreferences **/

public class AppPreferences {

	public static final boolean DEBUG = false;
	public static final boolean COMPLETE_TEST = true;
	public static final boolean PARTIAL_TEST = true;
	public static final String PREFS_NAME = "SplitMyRide";
	
	// Set names of all variables used in AppPreferences
	public static final String USER_ID = "user_id";
	public static final String FIRST_NAME = "first_name";
	public static final String LAST_NAME = "last_name";
	public static final String PHONE = "phone";
	public static final String IMAGE_URL = "image_url";
	public static final String STATUS = "status";  // Represents current stage in the ride matching process
	
	public static final String RIDE_ID = "ride_id";
	public static final String RIDE_ORIGIN_VENUE = "origin_venue";
	public static final String RIDE_ORIGIN_PICKUP = "origin_pickup";
	public static final String RIDE_DEST_NAME = "dest_address";
	public static final String RIDE_DEST_LON = "dest_lon";
	public static final String RIDE_DEST_LAT = "dest_lat";
	public static final String RIDE_DEPT_TIME_LONG = "dept_time_long";
	
	public static final String MATCH_RIDE_ID = "match_ride_id";
	public static final String MATCH_ORIGIN_VENUE = "match_origin_venue";
	public static final String MATCH_ORIGIN_PICKUP = "match_origin_pickup";
	public static final String MATCH_DEST_NAME = "match_dest_address";
	public static final String MATCH_DEPT_TIME_LONG = "match_dept_time_long";
	
	
	/*************************** Store user, ride, match data ***************************/
	
	// Store user info 
	public static void storeUser(Context ctxt, User user) {
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putString(USER_ID, user.id);
	    editor.putString(FIRST_NAME, user.firstName);
	    editor.putString(LAST_NAME, user.lastName);
	    editor.putString(PHONE, user.phone);
	    editor.putString(IMAGE_URL, user.image);
	    editor.commit();
	}
	// Store ride info
	public static void storeRide(Context ctxt, Ride ride) {
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putString(USER_ID, ride.userId);
	    editor.putString(RIDE_ID, ride.rideId);
	    editor.putString(RIDE_ORIGIN_VENUE, ride.originVenue);
	    editor.putString(RIDE_ORIGIN_PICKUP, ride.originPickup);
	    editor.putFloat(RIDE_DEST_LON, ride.destLon);
	    editor.putFloat(RIDE_DEST_LAT, ride.destLat);
	    editor.putLong(RIDE_DEPT_TIME_LONG, ride.deptTimeLong);
	    editor.putInt(STATUS, 1);
	    editor.commit();
	}
	// Store match info
	public static void storeMatch(Context ctxt, Ride matchRide) {
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putString(MATCH_RIDE_ID, matchRide.rideId);
	    editor.putString(MATCH_ORIGIN_VENUE, matchRide.originVenue);
	    editor.putString(MATCH_ORIGIN_PICKUP, matchRide.originPickup);
	    editor.putLong(MATCH_DEPT_TIME_LONG, matchRide.deptTimeLong);
	    editor.commit();
	}
	
	/*************************** Clear user, ride and match data ***************************/	
	
	// Clear all data
	public static void clearAll(Context ctxt){
		clearUser(ctxt);
		clearRide(ctxt);
		clearMatch(ctxt);
	}
	
	
	// Clear user info
	public static void clearUser(Context ctxt) {
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putString(USER_ID, "");
	    editor.putString(FIRST_NAME, "");
	    editor.putString(LAST_NAME, "");
	    editor.putString(PHONE, "");
	    editor.putString(IMAGE_URL, "");
	    editor.putInt(STATUS, 0);
	    editor.commit();
	}
	
	// Clear ride data
	public static void clearRide(Context ctxt) {
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putString(RIDE_ID, "");
	    editor.putString(RIDE_ORIGIN_VENUE, "");
	    editor.putString(RIDE_ORIGIN_PICKUP, "");
	    editor.putString(RIDE_DEST_NAME, "");
	    editor.putLong(RIDE_DEPT_TIME_LONG, 0);
	    editor.commit();
	}
	
	// Clear match data
	public static void clearMatch(Context ctxt) {
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putString(MATCH_RIDE_ID, "");
	    editor.putString(MATCH_ORIGIN_VENUE, "");
	    editor.putString(MATCH_ORIGIN_PICKUP, "");
	    editor.putString(MATCH_DEST_NAME, "");
	    editor.putLong(MATCH_DEPT_TIME_LONG, 0);
	    editor.commit();
	}
	
	
	/************************ Sets value for a given key in SharedPreferences ***************************/
	
	// Set a value of type string in SharedPreferences
	public static void setString(Context ctxt, String key, String value){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putString(key, value);
	    editor.commit();
	}
	// Set value of type integer in SharedPreferences
	public static void setInt(Context ctxt, String key, Integer value){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putInt(key, value);
	    editor.commit();
	}
	// Set a value of type long in SharedPreferences
	public static void setLong(Context ctxt, String key, Long value){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putLong(key, value);
	    editor.commit();
	}
	
	// Set a value of type Float in SharedPreferences
	public static void setFloat(Context ctxt, String key, Float value){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
	    SharedPreferences.Editor editor = settings.edit();
	    editor.putFloat(key, value);
	    editor.commit();
	}
	
	
	/********************* Gets value for a given key in SharedPreferences *********************/
	
	// Get a value of type integer from SharedPreferences
	public static Integer getInt(Context ctxt, String key){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
		return settings.getInt(key, 0);
	}
	
	// Get a value of type string in SharedPreferences
	public static String getString(Context ctxt, String key){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
		return settings.getString(key, "");
	}
	
	// Get a value of type long in SharedPreferences
	public static Long getLong(Context ctxt, String key){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
		return settings.getLong(key, 0);
	}
	
	// Get a value of type float in SharedPreferences
	public static Float getFloat(Context ctxt, String key){
		SharedPreferences settings = ctxt.getSharedPreferences(PREFS_NAME, 0);
		return settings.getFloat(key, 0);
	}
	
	
	/**************************** Check existence of a given key ****************************/
	
	// Check if a non-null value exists for a given key
	public static Boolean checkExistence(Context ctxt, String key) {
		String id = getString(ctxt, key);
		if (id == null || id == "") {
			return false;
		} else {
			return true;
		}
	}
	
	/**************************** Log all elements ****************************/
	
	// Check if a non-null value exists for a given key
	public static void logAll(Context ctxt) {
		String APP_NAME = "SplitMyRide";
		Log.v(APP_NAME, "userId " + getString(ctxt, USER_ID));
		Log.v(APP_NAME, "first " + getString(ctxt, FIRST_NAME));
		Log.v(APP_NAME, "lastname " + getString(ctxt, LAST_NAME));
		Log.v(APP_NAME, "phone " + getString(ctxt, PHONE));
		Log.v(APP_NAME, "rideId " + getString(ctxt, RIDE_ID));
		
		Log.v(APP_NAME, "lat " + getFloat(ctxt, RIDE_DEST_LAT));
		Log.v(APP_NAME, "lon " + getFloat(ctxt, RIDE_DEST_LON));
		Log.v(APP_NAME, "venue " + getString(ctxt, RIDE_ORIGIN_VENUE));
		Log.v(APP_NAME, "pickup " + getString(ctxt, RIDE_ORIGIN_PICKUP));
		
		Log.v(APP_NAME, "depttimelong " + getLong(ctxt, RIDE_DEPT_TIME_LONG));
		int hour = TimeUtils.epochTimeToCalendar(getLong(ctxt, RIDE_DEPT_TIME_LONG), Calendar.HOUR_OF_DAY);
		int min = TimeUtils.epochTimeToCalendar(getLong(ctxt, RIDE_DEPT_TIME_LONG), Calendar.MINUTE);
		Log.v(APP_NAME, "time " + hour + ":" + min);
	}	
}
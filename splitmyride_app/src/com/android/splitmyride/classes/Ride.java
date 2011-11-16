package com.android.splitmyride.classes;

import com.android.splitmyride.api.SplitMyRideApi;
import com.android.splitmyride.data.AppPreferences;

import android.content.Context;
import android.content.SharedPreferences;

public class Ride {
	
	public String userId;
	public String rideId;
	public String originVenue;
	public String originPickup;
	public Float destLon;
	public Float destLat;
	public Long deptTimeLong;
	public String deptTimeStr;
	public Integer status;	 //TODO May be able to delete this if not using it
	public String matchRideID;
	

	// Method to create a ride from NameValue pairs in AppPreferences
	public static Ride createRidefromAppPreferences(Context ctxt) {
		Ride ride = new Ride();
		ride.userId = AppPreferences.getString(ctxt, AppPreferences.USER_ID);
		ride.rideId = AppPreferences.getString(ctxt, AppPreferences.RIDE_ID);
		ride.originPickup = AppPreferences.getString(ctxt, AppPreferences.RIDE_ORIGIN_PICKUP);
		ride.originVenue = AppPreferences.getString(ctxt, AppPreferences.RIDE_ORIGIN_VENUE);
		ride.deptTimeLong = AppPreferences.getLong(ctxt, AppPreferences.RIDE_DEPT_TIME_LONG);
		ride.destLon = AppPreferences.getFloat(ctxt, AppPreferences.RIDE_DEST_LON);
		ride.destLat = AppPreferences.getFloat(ctxt, AppPreferences.RIDE_DEST_LAT);
		return ride;
	}
	
	// Method to create a ride from json object
	
	// Store ride info in AppPreferences and on Server if available
	public static void storeRide(Context ctxt, Ride ride, Boolean saveToServer) {
		Boolean userExists = AppPreferences.checkExistence(ctxt, AppPreferences.USER_ID);
		if (saveToServer && userExists) {
			String id = SplitMyRideApi.saveRide(ride);
			ride.rideId = id;
			// TODO add error handling
		}
		AppPreferences.storeRide(ctxt, ride);
	}


}

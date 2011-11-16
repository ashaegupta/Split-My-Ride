package com.android.splitmyride.classes;

import android.content.Context;

import com.android.splitmyride.api.SplitMyRideApi;
import com.android.splitmyride.data.AppPreferences;

public class User {
	
	public String id;
	public String phone;
	public String firstName;
	public String lastName;
	public String fullName;
	public String image;
	public Ride Ride;
	public Integer status;

	/** Method to create a createUser(NameValuePair)
	 *  store that in AppPreferences
	 *  http-post
	 *  Return user object
	 */
	
	/** Method to create a userFromJson object
	 * 
	 */
	
	//Save user to AppPreferences and to the server
	public static void storeUser(Context ctxt, User user, Boolean saveToServer) {
		if (saveToServer) {
			String userId = SplitMyRideApi.saveUser(user);
			user.id = userId;
			//TODO add check for error
		}
		AppPreferences.storeUser(ctxt, user);
	}
	
	
	// Method to add a ride to this user
	
	// Create fullname
	// If no Ride

}

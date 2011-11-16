package com.android.splitmyride;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

import com.android.splitmyride.data.AppPreferences;

// Abstract Activity that all SplitMyRide Activities inherit from
public class AbstractSplitMyRideActivity extends Activity {
	
	public String APP_NAME = "SplitMyRide";
	
	// Redirect to a different activity depending on where the user is in the ride-matching process
	public void launchRedirect() {
	    
		Integer status = AppPreferences.getInt(this, AppPreferences.STATUS);
		
		Log.v(this.APP_NAME, "In LaunchRide");
		Log.v(this.APP_NAME, "status: " + status.toString());
		
		if (status == 1){
			Intent i =  new Intent(this, RideListActivity.class);
			startActivity(i);
			finish();
		} else if (status == 2) {
			Intent i =  new Intent(this, MatchedActivity.class);
			startActivity(i);
			finish();
		} else if (status == 3) {
			Intent i =  new Intent(this, PayActivity.class);
			startActivity(i);
			finish();
		}

	}
}

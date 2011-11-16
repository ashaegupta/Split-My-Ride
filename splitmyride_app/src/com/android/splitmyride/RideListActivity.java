package com.android.splitmyride;

import com.android.splitmyride.data.AppPreferences;

import android.os.Bundle;
import android.util.Log;

public class RideListActivity extends AbstractSplitMyRideActivity {
	
	public static String ACTIVITY_NAME = "RideListActivity";
	
	/** Called when the activity is opened. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.v(this.APP_NAME, "In " + ACTIVITY_NAME);
        setContentView(R.layout.main);
        
        AppPreferences.logAll(this);
    }
    
	public void onResume(Bundle savedInstanceState) {
		launchRedirect();
	}

}

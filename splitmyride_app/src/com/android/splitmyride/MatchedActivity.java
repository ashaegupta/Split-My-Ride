package com.android.splitmyride;

import android.os.Bundle;
import android.util.Log;

public class MatchedActivity extends AbstractSplitMyRideActivity {
	
	public static String ACTIVITY_NAME = "MatchedActivity";
	
	/** Called when the activity is opened. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.v(this.APP_NAME, "In " + ACTIVITY_NAME);
        setContentView(R.layout.main); 
    }
    
	public void onResume(Bundle savedInstanceState) {
		launchRedirect();
	}

}

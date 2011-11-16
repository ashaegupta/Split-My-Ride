package com.android.splitmyride;

import android.app.Application;
import android.util.Log;

import com.android.splitmyride.data.AppPreferences;

public class AbstractApplication extends Application {
	
	@Override
    public void onCreate() {
        super.onCreate();
        
        Log.v("SplitMyRide", "in AbstractApplication");
        
        if (AppPreferences.COMPLETE_TEST){
        	AppPreferences.clearAll(this);
        }
    }

}

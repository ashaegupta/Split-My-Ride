package com.android.splitmyride;

import java.util.Calendar;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.TimePicker;

import com.android.splitmyride.classes.Ride;
import com.android.splitmyride.data.AppPreferences;
import com.android.splitmyride.utils.TimeUtils;

// Activity to create or edit a ride 
// Activity is called in two scenarios:
//   1. when the user does not have a valid ride on file
// 		I.e., when the app is launched for the first time or
// 		when the user's ride has expired or a match is complete
//   2. when the user wants to edit an existing ride



public class RideActivity extends AbstractSplitMyRideActivity {
   
	public static String ACTIVITY_NAME = "RideActivity";
	
	private Button mSaveButton;
	private EditText mTerminalEditText;
	private TimePicker mDeptTimePicker;
	
	// Called when the activity is first started
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        
        // For testing purposes clear app preferences
        if (AppPreferences.COMPLETE_TEST){
        	AppPreferences.clearAll(this);
        }
        
        launchRedirect();
        setContentView(R.layout.ride);
        setWidgets();
	    prefillFieldsIfNecessary();
	    
	    mSaveButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				saveRide();
				startNextActivity();
			}
        });
        	
    }
    
    
    /***************************Layout Helper Methods **********************************************/
   
    // Method to link all the widgets to the appropriate views
    private void setWidgets() {
    	mTerminalEditText = (EditText) findViewById(R.id.editTerminal);
        mSaveButton = (Button) findViewById(R.id.buttonSave);
        mDeptTimePicker = (TimePicker) findViewById(R.id.timePicker1);
    }
    
    // Prefill data fields with existing data if it exists
    private void prefillFieldsIfNecessary(){
    	  if(AppPreferences.checkExistence(RideActivity.this, AppPreferences.RIDE_ID)) {
      		Ride ride = Ride.createRidefromAppPreferences(this);
          	setInputFields(ride);
  	    }
    }
    
    // Prefill data
    private void setInputFields(Ride ride) {
    	mTerminalEditText.setText(ride.originPickup);
      	mDeptTimePicker.setCurrentHour(TimeUtils.epochTimeToCalendar(ride.deptTimeLong, Calendar.HOUR_OF_DAY));
      	mDeptTimePicker.setCurrentMinute(TimeUtils.epochTimeToCalendar(ride.deptTimeLong, Calendar.MINUTE));
    	//TODO ADD OTHER DATA TO PREFILL HERE
    }
    
    
    
    /*********************************Saving Data Helper Methods ***********************************/
    
    // Save the ride in AppPreferences and on the server if a user exists
    private void saveRide(){
    	Ride ride = rideFromUserInputs();
    	Ride.storeRide(this, ride, true);
    }
    
    // Method to create a ride from all user inputs
    private Ride rideFromUserInputs() {
    	Ride ride = new Ride();
    	ride.originVenue = "jfk"; //TODO GET THIS FROM LOCATION
    	ride.originPickup = mTerminalEditText.getText().toString();
    	ride.destLon = (float) 73.21; //TODO
    	ride.destLat = (float) 49.21; //TODO
    	ride.deptTimeLong = (long) TimeUtils.timePickerToEpochTime(mDeptTimePicker);
    	ride.rideId = AppPreferences.getString(this, AppPreferences.RIDE_ID); //If exists already, get previous to edit
    	ride.userId = AppPreferences.getString(this, AppPreferences.USER_ID); //If exists already, get previous to edit
    	return ride;
    }
    
    
    /*********************************Activity Flow Methods ***************************************/
    
    // Go to RideListActivity, unless this user is new, then go to UserActivity to create a new user
    private void startNextActivity() {
    	Intent i = new Intent(RideActivity.this, RideListActivity.class);
    	if(!(AppPreferences.checkExistence(this, AppPreferences.USER_ID))) {
    		i = new Intent(RideActivity.this, UserActivity.class);
    	}
    	startActivity(i);
    	finish();
    }
    
    // On resume, redirect to the relevant screen for the user
    public void onResume(Bundle savedInstanceState) {
	    launchRedirect();
	}
}
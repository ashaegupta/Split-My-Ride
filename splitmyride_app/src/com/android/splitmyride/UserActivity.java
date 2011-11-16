package com.android.splitmyride;

import android.content.Intent;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

import com.android.splitmyride.classes.User;
import com.android.splitmyride.data.AppPreferences;

// Method to create or edit a user's profile information
public class UserActivity extends AbstractSplitMyRideActivity{
	
	public static String ACTIVITY_NAME = "UserActivity";
	
	EditText mFirstNameEditText;
	EditText mLastNameEditText;
	EditText mPhoneEditText;
	Button mSaveButton;
	
	/** Called when the activity is opened. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.user);
        
        Log.v(this.APP_NAME, "In " + ACTIVITY_NAME);
        
        setWidgets();
        prefillFieldsIfNecessary();
        
        mSaveButton.setOnClickListener(new View.OnClickListener() {
			@Override
			public void onClick(View v) {
				saveUser();
				Intent i = new Intent(new Intent(UserActivity.this, RideListActivity.class));
				startActivity(i);
				finish();
			}
        });
    }
    
    /***************************Layout Helper Methods **********************************************/
    
    // Method to link all the widgets to the appropriate views
    private void setWidgets() {
    	mFirstNameEditText = (EditText) findViewById(R.id.firstnameEdtitext);
    	mLastNameEditText = (EditText) findViewById(R.id.lastnameEditText);
    	mPhoneEditText = (EditText) findViewById(R.id.phoneEditText);
    	mSaveButton = (Button) findViewById(R.id.buttonSave);
    }
    
    // Prefill data fields with existing data if it exists
    private void prefillFieldsIfNecessary(){
    	  if(AppPreferences.checkExistence(UserActivity.this, AppPreferences.USER_ID)) {
    		  mFirstNameEditText.setText(AppPreferences.getString(this, AppPreferences.FIRST_NAME));
    		  mLastNameEditText.setText(AppPreferences.getString(this, AppPreferences.LAST_NAME));
    		  mPhoneEditText.setText(AppPreferences.getString(this, AppPreferences.PHONE));
    		  //TODO ADD IMAGE URL
  	    }
    }
    
    /*********************************Saving Data Helper Methods ***********************************/
    
    // Save user in AppPreferences and on the server
    private void saveUser(){
    	User user = createUserFromInputs(); 
    	User.storeUser(this, user, true);
    }
    
    // Create a new user object from current UI inputs
    private User createUserFromInputs() {
    	User user = new User();
    	user.firstName = mFirstNameEditText.getText().toString();
    	user.lastName = mLastNameEditText.getText().toString();
    	user.phone = mPhoneEditText.getText().toString();
    	user.id = AppPreferences.getString(this, AppPreferences.USER_ID);
    	//TODO ADD IMAGE URL
    	return user;
    	
    }
    	
    	
    	//IF INTENT COMES FROM RIDE CREATION, then Also store a ride on the server
    	//Ride ride = createRideFromAppPreferences();
    	//storeRide(this, ride, true);

}

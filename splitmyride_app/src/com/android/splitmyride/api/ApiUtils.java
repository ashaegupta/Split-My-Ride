package com.android.splitmyride.api;

import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.util.List;

import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.DefaultHttpClient;
import org.apache.http.util.EntityUtils;
import org.json.JSONException;
import org.json.JSONObject;

import com.android.splitmyride.data.AppPreferences;

public class ApiUtils {
    protected static final String TAG = "ApiUtils";
    protected static final boolean DEBUG = AppPreferences.DEBUG;
    
    // Does an HttpPost and returns a JSONObject
    public static JSONObject doHttpPost(String url, List<NameValuePair> data){
    	HttpClient httpclient = new DefaultHttpClient();   
    	HttpPost httppost = new HttpPost(url); 
    	JSONObject json = new JSONObject();
	    
    	try {
            httppost.setEntity(new UrlEncodedFormEntity(data));
            try {
                HttpResponse response = httpclient.execute(httppost);
                String responseBody = EntityUtils.toString(response.getEntity());
                
                try {
                	json = new JSONObject(responseBody);
                } catch (JSONException e) {
                	e.printStackTrace();
                }
                
            } catch (ClientProtocolException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        } catch (UnsupportedEncodingException e) {
            e.printStackTrace();
        }
	    return json;
	}
    
    
    
    
    
}
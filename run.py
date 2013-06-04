from httplib2 import Http
import json, os, sched, time, datetime

# You foursquare oAUTH Token
oauth_token = "XXXXXXXXXXXX"

# A list of all SSID's with there Foursquare ID
knownSSIDs = {"VikingCo": "4cf665801801a1439e58e9d4", "Boomhut": "4d4577261b62b1f7a979fde2"}

# Refresh interval in seconds
refreshInterval = 300;

#################################### Stay away below here... ####################################

# Some var's... Ignore this sh*t...
lastSSID = ""
scheduler = sched.scheduler(time.time, time.sleep)

# The magic function
def checkSSID(sc): 
    global lastSSID
    
    # The current time
    currenttime = datetime.datetime.now().strftime("%H:%M:%S")

    # Your current SSID (Yes, only works on a Mac, Sorry..)
    currentSSID = os.popen("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I | awk '/ SSID/ {print substr($0, index($0, $2))}'").read().strip()

    # Check if you SSID is changed
    if currentSSID == lastSSID:
        print "%s - SSID Not changed: %s" % (currenttime, currentSSID)
    else:
        print "%s - New SSID Found: %s" % (currenttime, currentSSID)
        
        # Check if we known the SSID
        if currentSSID in knownSSIDs:

            # Fetch venueID from the known SSID list
            venueID = knownSSIDs.get(currentSSID)

            print "%s - Checking you in to this known Foursquare location: %s" % (currenttime, venueID)
            
            # Do a Checkin call to Foursquare
            url = "https://api.foursquare.com/v2/checkins/add?oauth_token="+oauth_token+"&venueId="+venueID+"&v=20130522"
            response, content = Http().request(url, "POST")
            content = json.loads(content)
            
            # Check if everythin was OK...
            if content['meta']['code'] == 200:
                print datetime.datetime.now().strftime("%H:%M:%S"), "- Checked in!"
                
                # Print checkin scores!
                for score in content['response']['checkin']['score']['scores']:
                    print "%s - %s :: Earned %d points." % (currenttime, score['message'], score['points'])
            else:
                # Oeps, error!
                print "%s - ERROR: Not Checked in.!" % (currenttime)

    # Update our lastSSID to our new SSID
    lastSSID = currentSSID    

    # Set interval to check again our SSID in x-minutes!
    sc.enter(refreshInterval, 1, checkSSID, (sc,))


# Runs script!
checkSSID(scheduler)

# Tel timer to start now!
scheduler.run()







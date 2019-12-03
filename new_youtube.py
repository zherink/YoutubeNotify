import urllib.request, json
import time
import os
import smtplib, ssl
import re

def look_for_new_video():
    api_key = os.getenv('GOOGLE_API_KEY')
    channel_id = 'UCaN1rig0bL7SUod2WN0P8XA'
    base_video_url = 'https://www.youtube.com/watch?v='
    base_search_url = 'https://www.googleapis.com/youtube/v3/search?'

    url = base_search_url + 'key={}&channelId={}&part=snippet,id&order=date&maxResults=1&type=video'.format(api_key, channel_id)
    try:
        inp = urllib.request.urlopen(url)
    except:
        print('API access forbidden')
        return
    resp = json.load(inp)

    vidID = resp['items'][0]['id']['videoId']

    new_video = False
    with open('videoid.json', 'r') as json_file:
        data = json.load(json_file)
        if data['videoId'] != vidID:
            try:
                msg = 'There is a new video from {}{}'.format(base_video_url, vidID).replace('https://', '')
                print(msg)
                send_message(msg)
            except:
                print('could not send message to Zach')
            new_video = True
        
        if new_video:
            with open('videoid.json', 'w') as json_file:
                data = {'videoId' : vidID}
                json.dump(data, json_file)

def send_message(msg):
    port = 465
    email_password = os.getenv('ETEXT_PASS')
    email_sender = os.getenv('ETEXT_EMAIL')
    context = ssl.create_default_context()
    server = smtplib.SMTP_SSL('smtp.gmail.com', port, context=context)
    try:
        server.login(email_sender, email_password)
    except:
        print('could not sign in to email')
    server.sendmail(email_sender, os.getenv('ETEXT_ZACH'), msg)

if not os.path.isfile('videoid.json'):
    f = open('videoid.json', 'w')
    data = {'videoId' : ''}
    json.dump(data,f)
    f.close()
try: 
    while True:
        look_for_new_video()
        time.sleep(300)
except KeyboardInterrupt:
    print('stopping')

# msg = 'There is a new video from https://www.youtube.com/watch?v=PkyFic4Et6M'.replace('https://', '')
# send_message(msg)

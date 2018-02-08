# This code is taken from https://github.com/mattmakai/fullstackpython.com/blob/gh-pages/source/content/posts/160604-build-first-slack-bot-python.markdown
# It is covered by MIT license

import os
import time
import urllib
import json
from slackclient import SlackClient
import nltk

# starterbot's ID
BOT_ID = 'none'

# instantiate Slack & Twilio clients
slack_client = SlackClient('BotToken')

# openweathermap api Token
OWMapitoken = 'WeatherToken'

# constants
#AT_BOT = "<@" + BOT_ID + ">"
#EXAMPLE_COMMAND = "do"


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    #response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
    #           "* command with numbers, delimited by spaces."
    #if command.startswith(EXAMPLE_COMMAND):
    #    response = "Sure...write some more code then I can do that!"
    #slack_client.api_call("chat.postMessage", channel=channel,
    #                      text=response, as_user=True)
	
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=command, as_user=True)

def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    #TODO: Uncommment the line below to see raw messages
    #print "Raw message looks like " + ' '.join(str(e) for e in slack_rtm_output)
    correctID(slack_rtm_output)
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
	   # import pdb; pdb.set_trace()
            if output and 'text' in output and 'bot_id' not in output:
            #if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                cityname = output['text'].strip().lower()
				
	
                link = "http://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=" + OWMapitoken
                databuffer = urllib.urlopen(link)           
                data = json.loads(databuffer.read())
                if data['cod'] != 200 and len(cityname) < 11:
                    cityname = is_city(cityname)
                    link = "http://api.openweathermap.org/data/2.5/weather?q=" + cityname + "&appid=" + OWMapitoken
                    databuffer = urllib.urlopen(link)           
                    data = json.loads(databuffer.read())
                if data["cod"] == 200:
                    dataname = data["name"]
                    for item in data["weather"]:
                    	weather = item.get("main")
                    temp = data["main"]['temp']
                    temp = str(temp - 273.15)
                    if cityname == dataname.lower():
                	    return cityname + " is now " + temp + " Celsius and "+ weather, output['channel']
                return output['text'].strip().lower(), output['channel']
    
                #return output['text'].split(AT_BOT)[1].strip().lower(), \
                #       output['channel']
    return None, None

	

def correctID(slack_rtm_output):
	print "Incoming Message: " + ' '.join(str(e) for e in slack_rtm_output)
	for out in slack_rtm_output:
		if out and 'text' in out and len(out) > 0:
			print "OUTPUT NAME: " + ' '.join(out['text'])


def similarity(x, y):
	count = 0
	for i, ch in enumerate(x):
		try:
			if (ch == y[i]) or (ch == y[i+1]) or (ch == y[i-1]):
				count += 1
		except IndexError:
			continue
	return count
	
def is_city(city):
	count = 2
	new_city = city
	with open('cities_json.txt', 'r') as f:
		data = json.load(f)
		
	for i in data:
				
		if abs(len(city) - len(i['name'])) < 2:
			similar = similarity(city, i['name'])
			
			if similar > len(i['name'])/2:
				print(similar)
				temp = nltk.edit_distance(city, i['name'].lower())
				print(i['name'])
				if count > temp:
					count = temp
					new_city = i['name'].lower()
					return new_city
				if temp < 2:
					break
			
	return new_city

	
if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())
            if command and channel:
            	print "Command = ", command, "channel = ", channel
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
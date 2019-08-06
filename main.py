from gtts import gTTS
from io import BytesIO
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import requests
import time
import unidecode
import json
import yaml

# Author:       Andrei Biswas
# GitHub:       codeabiswas
# Email:        petitendian@gmail.com

# Created on:   Sunday, August 4, 2019
# Modified on:  Monday, August 5, 2019

"""
    This method fetches your settings from the configuration file
"""
def get_user_data():

    # Load all the data into the config variable and return it in a list format
    with open("config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)

    # Check if the user has filled out the appropriate data
    if config['name'] == 'your-name-here':
        print("Please add your name to the config.yml file.")
        return []
    if config['username'] == 'your-Reddit-username-here':
        print("Please add your Reddit username to the config.yml file.")
        return []
    if config['password'] == 'your-Reddit-password-here':
        print("Please add your Reddit password to the config.yml file.")
        return []

    return [config['name'], config['username'], config['password'], config['urls'], 
            config['headline_count'], config['useless_messages'], config['speech_lang']]

"""
    This method fetches data from Reddit given a list including all the necessary information for Reddit access
"""
def fetch_data(configData):

    # Set up the username and password
    user_pass_dict = {'user': configData[1],
                      'passwd': configData[2],
                      'api_type': 'json' }

    someSession = requests.Session()
    # A User-Agent needs to be updated otherwise the API does not respond
    someSession.headers.update({'User-Agent': 'daily_headlines: codeabiswas'})
    someSession.post('https://www.reddit.com/api/login', data=user_pass_dict)

    # Sleep for a bit so API is not overloaded
    time.sleep(0.5)

    # Set the greet statement with user's given name
    greetStatement = "Hello " + configData[0]

    # Append to the return string
    returnString = greetStatement

    # Get the list of all the subreddit URLs
    urls = configData[3]
    
    # For each URL in the URL list
    for url in urls:
        
        urlPath = url.split('/')
        # Get the name of the subreddit
        titleSplit = "...\n\nToday's {} headlines are...\n\n".format(urlPath[4])
        
        # Append the above string to the return string 
        returnString += titleSplit

        # Set the URL to fetch information in JSON format
        url = url + "/.json?limit={}".format(str(configData[4]))

        # Get, store, and decode the data in JSON format
        html = someSession.get(url)
        data = json.loads(html.content.decode('utf-8'))

        # List for storing all the headlines
        headlines = []

        # Locally store the messages that we do not want to read
        uselessMessages = configData[5]
        
        # A counter to number the news headlines
        listingNum = 1

        # Go through each listing
        for listing in data['data']['children']:
            
            # Given the headline is not a useless message
            if listing['data']['title'] not in uselessMessages:
                
                # Replace & character with "and"
                try:    
                    listing['data']['title'] = str.replace(listing['data']['title'], "&amp;", "and")
                except ValueError:
                    pass

                # Format the string accordingly and append it to the headlines list
                titleString = str(listingNum) + ". " + unidecode.unidecode(listing['data']['title'])
                headlines.append(titleString)
                
                # Increment the counter
                listingNum += 1
        
        # Create the final return string
        returnString += '...\n\n'.join(headlines)

    return returnString

"""
    This method defines what this program mainly does
"""
def main():
    
    # Get the list containing all the information
    configData = get_user_data()

    # If an error has occured (indicated by empty list), just exit the program
    if len(configData) == 0:
        return

    # Get all the headlines
    someText = fetch_data(configData)
    
    print(someText)

    # Get the text to speech
    tts = gTTS(someText, lang=configData[6], slow=False)

    pygame.mixer.init()
    # This init() is needed otherwise the sound is not heard
    pygame.init()
    
    # Use a memory stream
    with BytesIO() as someFile:
        tts.write_to_fp(someFile)
        someFile.seek(0)
        pygame.mixer.music.load(someFile)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.event.set_allowed(pygame.USEREVENT)
        pygame.mixer.music.play()
        # The above method is an asynchronous one. Therefore, this wait() is required so that the speaking is completed and the BytesIO() file will be closed.
        pygame.event.wait()

if __name__ == "__main__":
    # Run the main program
    main()
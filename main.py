from gtts import gTTS
from io import BytesIO
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
# Modified on:  Sunday, August 4, 2019

def get_user_credentials():

    with open("config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)

    return [config['username'], config['password']]


def get_headlines():

    userCredentials = get_user_credentials()

    user_pass_dict = {'user': userCredentials[0],
                      'passwd': userCredentials[1],
                      'api_type': 'json' }

    sess = requests.Session()
    sess.headers.update({'User-Agent': 'daily_headlines: codeabiswas'})
    sess.post('https://www.reddit.com/api/login', data=user_pass_dict)

    time.sleep(1)

    allTitles = ""

    introStatements = ["Good morning Andrei! Today's world news includes...\n\n", "...\n\nToday's technology news includes...\n\n", "...\n\nToday's music news includes...\n\n"]
    urls = ['https://reddit.com/r/worldnews/.json?limit=3', 'https://www.reddit.com/r/technology/.json?limit=3', 'https://www.reddit.com/r/MusicNews/.json?limit=3']
    
    i = 0

    for url in urls:
        allTitles += introStatements[i]
        i += 1

        html = sess.get(url)
        data = json.loads(html.content.decode('utf-8'))

        titles = []
    
        notUsefulMessageOne = "Any form of threatening, harassing, or violence / physical harm towards anyone will result in a ban"
        notUsefulMessageTwo = "Got a tech question or want to discuss tech? Weekly /r/Technology Tech Support / General Discussion Thread"
        
        listingNum = 1
        for listing in data['data']['children']:
            
            if listing['data']['title'] != notUsefulMessageOne and listing['data']['title'] != notUsefulMessageTwo: 
                titleString = str(listingNum) + ". " + unidecode.unidecode(listing['data']['title'])
                titles.append(titleString)
                listingNum += 1
        
        allTitles += '...\n\n'.join(titles)

    return allTitles

def main():
    
    someText = ""
    someText = get_headlines()
    
    print(someText)

    tts = gTTS(someText, lang='en', slow=False)

    pygame.mixer.init()
    # This init() is needed otherwise the sound is not played
    pygame.init()
    
    # Use a memory stream
    with BytesIO() as f:
        tts.write_to_fp(f)
        f.seek(0)
        pygame.mixer.music.load(f)
        pygame.mixer.music.set_endevent(pygame.USEREVENT)
        pygame.event.set_allowed(pygame.USEREVENT)
        pygame.mixer.music.play()
        # The above method is an asynchronous one. Therefore, this wait() is required so that the speaking is completed and the BytesIO() file will be closed.
        pygame.event.wait()
    
if __name__ == "__main__":
        
    main()
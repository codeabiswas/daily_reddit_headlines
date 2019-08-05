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
# Modified on:  Monday, August 5, 2019

def get_user_data():

    with open("config.yml", 'r') as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.SafeLoader)

    return [config['name'], config['username'], config['password'], config['urls'], config['headline_count'], config['useless_messages']]


def fetch_data():

    configData = get_user_data()

    user_pass_dict = {'user': configData[1],
                      'passwd': configData[2],
                      'api_type': 'json' }

    someSession = requests.Session()
    someSession.headers.update({'User-Agent': 'daily_headlines: codeabiswas'})
    someSession.post('https://www.reddit.com/api/login', data=user_pass_dict)

    time.sleep(0.5)

    allTitles = ""

    greetStatement = "Hello " + configData[0]
    allTitles = greetStatement
    urls = configData[3]
    
    for url in urls:
        urlPath = url.split('/')
        titleSplit = "...\n\nToday's {} headlines are...\n\n".format(urlPath[4])
        allTitles += titleSplit

        url = url + "/.json?limit={}".format(str(configData[4]))

        html = someSession.get(url)
        data = json.loads(html.content.decode('utf-8'))

        titles = []
    
        uselessMessages = configData[5]
        
        listingNum = 1
        for listing in data['data']['children']:
            
            if listing['data']['title'] not in uselessMessages:

                try:    
                    listing['data']['title'] = str.replace(listing['data']['title'], "&amp;", "and")

                except ValueError:
                    pass

                titleString = str(listingNum) + ". " + unidecode.unidecode(listing['data']['title'])
                titles.append(titleString)
                listingNum += 1
        
        allTitles += '...\n\n'.join(titles)

    return allTitles

def main():
    
    someText = fetch_data()
    
    print(someText)

    tts = gTTS(someText, lang='en', slow=False)

    pygame.mixer.init()
    # This init() is needed otherwise the sound is not heard
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
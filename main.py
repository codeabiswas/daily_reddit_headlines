from gtts import gTTS
from io import BytesIO
import pygame

def main(someText):
    
    tts = gTTS(someText, lang='en')

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
    
    someText = "Good Morning Andrei!"
    
    main(someText)
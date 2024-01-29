import pytchat
from random import randint
import pyttsx3
import elevenlabs
import os
"""to find this id check the YT stream and take the code at the end of the watch id 

EXAMPLE: https://www.youtube.com/watch?v=48p4yG9WWug

Take 48p4yG9WWug and input it into the console while the script is running"""

# *Test-key-here* test api key
api_key = input('Please enter your elevenlabs API Key: ')
vid_id = input('\nPlease enter the video id for the yt stream: ')


elevenlabs.set_api_key(api_key)
chat = pytchat.create(video_id=vid_id)

while chat.is_alive():

    for c in chat.get().sync_items():
        print(f"[{c.author.name}]- {c.message}")
        chance = randint(1, 10)
        print(chance)

        if chance == 10:
            cryptonic_voice = randint(1, 10)
            print(cryptonic_voice)

            if cryptonic_voice == 10:
                engine = elevenlabs.generate(
                    text=c.message,
                    voice='41yC8yXdJjA78m7VlJjD'
                )
                elevenlabs.save(engine, 'cryptonic_voice.mp3')
                os.system('start cryptonic_voice.mp3')

            else:
                engine = pyttsx3.init()
                engine.setProperty('volume', 1.2)
                engine.say(c.message)
                engine.runAndWait()

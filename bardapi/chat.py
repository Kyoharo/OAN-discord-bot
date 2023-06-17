import requests
from bardapi import Bard
from bardapi.constants import SEPARATOR_LINE, SESSION_HEADERS
import os 
from time import sleep

 
class ChatBard:

    def __init__(self):
        self.bard = None
        self.sessions = {}


    def initialize_bard(self, language=None):
        token = "WwjZpQ6HoOzq6-Xrk8M0TNN1Bmsb6QO3xvuzSWTG7h0BqCeQ-Ol742SJFPIIqRYpNGRHyA."

        if language is None:
            self.language = os.getenv("_BARD_API_LANG", default="english")
        timeout = int(os.getenv("_BARD_API_TIMEOUT", default=30))

        session = requests.Session()
        session.headers = SESSION_HEADERS
        session.cookies.set("__Secure-1PSID", token)

        self.bard = Bard(
            token=token, session=session, timeout=timeout, language=language
        )

    def start(self, user_id,question,language=None,reset=None):
        if language != None and reset != None:
            try :
                del self.sessions[user_id]  # Delete user ID from sessions
                print(f" {user_id} New chat opened successfully")
            except Exception:
                print(f" {user_id} New chat opened successfully")


        if user_id not in self.sessions:
            self.initialize_bard(language)
            self.sessions[user_id] = self.bard
            print("Created new session")
        else:
            self.bard = self.sessions[user_id]
            print("Using existing session")

        user_input = question.lower()
        
        response = self.bard.get_answer(user_input)

        if response["images"]:
            images_text = '  \n  • '.join([f'[Click Here]({image})' for image in response['images']])
            value = f"{response['content']}\n  • {images_text}"
            return value
        else:
            return response['content']

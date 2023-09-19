import requests
from bardapi import Bard
from bardapi.constants import SEPARATOR_LINE, SESSION_HEADERS
import os 
from time import sleep
from dotenv import load_dotenv
load_dotenv()
import smtplib



class ChatBard:

    def __init__(self):
        self.bard = None
        self.sessions = {}
        self.current_token_index = 0
        self.content_list = []


    def send_email(self,body):
        sender = "abdoataa38@gmail.com"         # sender email
        receiver = "abdoataa39@gmail.com","abdoataa38@gmail.com"       #receiver emails
        password = "xvggwyltaajqkbwk"           #sender app password
        subject = "OAN TOkENS"      # the subject
        #header                                             #in the message conten the subject and body
        message = f"""subject: {subject}\n\n    
{body}
        """

        server = smtplib.SMTP("smtp.gmail.com", 587)       # server protocol
        server.ehlo()                                      # to start connecting with the server
        server.starttls()                                   # start encreption
        server.login(sender, password)                      #login
        server.sendmail(sender,receiver, message)           #send the email
        server.quit()                                       #quit


    def initialize_bard(self, language=None):
        
        self.tokens =[
            os.getenv('BARD_TOKEN1'),
            os.getenv('BARD_TOKEN2'),
            os.getenv('BARD_TOKEN3'),
            os.getenv('BARD_TOKEN4'),
            os.getenv('BARD_TOKEN5'),
            os.getenv('BARD_TOKEN6'),
            os.getenv('BARD_TOKEN7'),
            os.getenv('BARD_TOKEN8')
        ]
        self.token = self.tokens[self.current_token_index]
        if language is None:
            self.language = os.getenv("_BARD_API_LANG", default="english")
        timeout = int(os.getenv("_BARD_API_TIMEOUT", default=30))

        session = requests.Session()
        session.headers = SESSION_HEADERS
        session.cookies.set("__Secure-1PSID", self.token)
        self.bard = Bard(
            token=self.token, session=session, timeout=timeout, language=language
        )
                    

    def start(self, user_id, question=None, language=None, reset=None, image=None):
        self.content_list = []
        start_input = {
            "USER_ID": user_id,
            "QUESTION": question,
            "LANGUAGE": language,
            "RESET": reset,
            "IMAGE": image
        }
        
        
        if language is not None and reset is not None:
            try:
                del self.sessions[user_id]  # Delete user ID from sessions
                print(f"{user_id} New chat opened successfully")
            except Exception:
                print(f"{user_id} New chat opened successfully")

        try:
            if user_id not in self.sessions:
                self.initialize_bard(language)
                self.sessions[user_id] = self.bard
                print("Created new session")
            else:
                self.bard = self.sessions[user_id]
                print("Using existing session")

            if image is not None:
                if question is None:
                    user_input = "What is in the image?"
                else:
                    user_input = question.lower()
                image = open(image, 'rb').read()
                response = self.bard.ask_about_image(user_input, image)
            else:
                user_input = question.lower()
                response = self.bard.get_answer(user_input)

            self.content_list.append(response['content'])

            if response['images']:
                for image in response['images']:
                    self.content_list.append(image)
        except Exception as e:
            print(f"Issue {e} with ((( {self.current_token_index}  ))):\n < {self.token}>")
            if self.current_token_index > len(self.tokens):
                self.send_email( body = "All tokens has been used please reload.\n\nBR\nOAN ")
                print(f"{self.token} : {self.current_token_index}")
                del self.sessions[user_id]

            elif self.current_token_index > len(self.tokens) /2:
                self.send_email( body = "Alert!!\n tokens more then 3.\n\nBR\nOAN ")
                print(f"{self.token} : {self.current_token_index}")
                self.current_token_index = self.current_token_index + 1
                self.token = self.tokens[self.current_token_index]
                del self.sessions[user_id]
                self.start(
                    start_input["USER_ID"],
                    start_input["QUESTION"],
                    start_input["LANGUAGE"],
                    start_input["RESET"],
                    start_input["IMAGE"]
                )

            else:
                self.current_token_index = self.current_token_index + 1
                if self.current_token_index > 8:
                    self.current_token_index = 0
                self.token = self.tokens[self.current_token_index]
                print(f"- New tocken = {self.current_token_index}  {self.token} ")
                del self.sessions[user_id]
                self.start(
                    start_input["USER_ID"],
                    start_input["QUESTION"],
                    start_input["LANGUAGE"],
                    start_input["RESET"],
                    start_input["IMAGE"]
                )
        return self.content_list

        



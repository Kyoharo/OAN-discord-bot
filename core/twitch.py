

import requests
from dotenv import load_dotenv
import os
import re

class TwitchStreamChecker:
    def __init__(self):
        load_dotenv()
        self.client_id = os.getenv('CLIENT_ID_TWITCH')
        self.client_secret = os.getenv('CLIENT_SECRET_TWITCH')
        self.access_token = self._get_access_token()

    def _get_access_token(self):
        body = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            "grant_type": 'client_credentials'
        }
        response = requests.post('https://id.twitch.tv/oauth2/token', body)
        keys = response.json()
        return keys['access_token']
    
    def is_user_exist(self, streamer_name):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        user_data = requests.get('https://api.twitch.tv/helix/users?login=' + streamer_name, headers=headers).json()
        user_info = user_data.get('data', None)
        
        if user_info:
            user_info = user_info[0]
            return {
                'id': user_info['id'],
                'login': user_info['login'],
                'display_name': user_info['display_name'],
                'profile_image_url': user_info['profile_image_url'],
            }
        else:
            return None

    def is_streamer_live(self, streamer_name):
        headers = {
            'Client-ID': self.client_id,
            'Authorization': 'Bearer ' + self.access_token
        }
        
        user_info = self.is_user_exist(streamer_name)
        
        stream = requests.get('https://api.twitch.tv/helix/streams?user_login=' + streamer_name, headers=headers)
        stream_data = stream.json()
        
        if len(stream_data['data']) == 1:
            stream_info = stream_data['data'][0]
            thumbnail_url = stream_info['thumbnail_url']
            
            return {
                'is_live': True,
                'stream_title': stream_info['title'],
                'game_name': stream_info['game_name'],
                'viewer_count': stream_info['viewer_count'],
                'thumbnail_url': thumbnail_url,
                'started_at': stream_info['started_at'],
                'profile_image_url': user_info['profile_image_url'],
            }
        else:
            return {
                'is_live': False
            }

def get_name_from_url(url):
    """Gets the name from the given URL."""
    if url.startswith("http"):
        match = re.search(r"https?://www\.twitch\.tv/(.*)", url)
        if match:
            return match.group(1)
    else:
        return url
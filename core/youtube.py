import json
import requests
from tqdm import tqdm
from googleapiclient.discovery import build
import re
import requests
import re
import random


API_KEY = ["AIzaSyBBCwJsZ1AGeEE8HPRTCaMuxIMCcNAN6hk",
           "AIzaSyAV2QNO5vc8-oXvTpi-lMNIvdy0wxlk5mw"]



def get_live_stream_id(channel_url):
    channel_url = "https://www.youtube.com/c/" + channel_url
    response = requests.get(channel_url)
    if response.status_code == 200:
        content = response.text
        match = re.search(r'"videoId":"(.*?)"', content)
        
        if match:
            return match.group(1)
        else:
            return None
    else:
        return None
    


def get_latest_ids(channel):
    try:
        channel = "https://www.youtube.com/@" + channel
        html = requests.get(channel+"/videos").text
        latest_video_id = re.search('(?<="videoId":").*?(?=")', html).group()
        html = requests.get(channel+"/shorts").text
        latest_shorts_id = re.search('(?<="videoId":").*?(?=")', html).group()
        last_ids = [latest_video_id, latest_shorts_id]
        return last_ids
    except Exception as e: 
        print(e)
        return []


def get_channel_ids(url):
    if not url.startswith("https"):
        if not url.startswith("@"):
            url = "https://www.youtube.com/@" + url
        else:
            url = "https://www.youtube.com/" + url
    response = requests.get(url)
    if response.status_code == 200:
        page_content = response.text
        pattern = r'"channelId":"(.*?)"'
        matches = re.findall(pattern, page_content)
        
        # If there are multiple matches, choose the last one
        if matches:
            channel_id = matches[-1]
            return channel_id
        else:
            print("No channel ID found")
            return None
    else:
        print("Failed to fetch the webpage")
        return None
    

def get_channel_name(url_or_name):
    if url_or_name.startswith("https"):
        # Extract channel name from the URL
        match = re.search(r'https://www\.youtube\.com/@?(\w+)', url_or_name)
        if match:
            return match.group(1)
    elif url_or_name.startswith("@"):
        # Remove "@" symbol and return the name
        return url_or_name[1:]
    return url_or_name

    
class YTstats:

    def __init__(self, api_key, channel_id):
        self.api_key = api_key
        self.channel_id = channel_id
        self.channel_statistics = None
        self.video_data = None

    def extract_all(self):
        self.get_channel_statistics()
        self.get_channel_video_data()



    def get_channel_statistics(self):
        """Extract the channel statistics, high-quality profile image URL, and username"""
        print('Getting channel statistics...')
        
        # Construct the URL to retrieve channel statistics and branding settings
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics,snippet&id={self.channel_id}&key={self.api_key}'
        pbar = tqdm(total=1)
        
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        
        try:
            # Extract statistics
            statistics = data['items'][0]['statistics']
            
            # Extract high-quality channel profile image URL
            profile_image_url_high = data['items'][0]['snippet']['thumbnails']['high']['url']
            
            # Extract channel username
            username = data['items'][0]['snippet']['title']
        except KeyError:
            print('Could not get channel statistics')
            statistics = {}
            profile_image_url_high = None
            username = None
        
        # Create a dictionary to store statistics, profile image URL, and username
        channel_data = {
            'statistics': statistics,
            'profile_image_url_high': profile_image_url_high,
            'username': username
        }
        
        pbar.update(1)
        pbar.close()
        
        return channel_data



    def is_channel_live(self):
        """Check if the channel is currently live and get live stream details"""
        print('Checking if channel is live...')
        
        # Construct the URL to search for live broadcasts by the channel
        url = f'https://www.googleapis.com/youtube/v3/search?part=id,snippet&type=video&eventType=live&channelId={self.channel_id}&key={self.api_key}'
        
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        
        if 'items' in data and len(data['items']) > 0:
            # Extract live stream details
            live_stream_info = data['items'][0]['snippet']
            
            title = live_stream_info['title']
            description = live_stream_info['description']
            published_at = live_stream_info['publishedAt']
            thumbnail_url = live_stream_info['thumbnails']['high']['url']
            
            live_stream_id = data['items'][0]['id']['videoId']
            
            return live_stream_id, {
                'title': title,
                'description': description,
                'publishedAt': published_at,
                'thumbnails_high': thumbnail_url
            }
        else:
            return None, None
        
    def get_channel_video_data(self):
        "Extract all video information of the channel"
        print('get video data...')
        channel_videos = self._get_channel_id(limit=3)
        return channel_videos
    

    def _get_channel_id(self, limit=None, check_all_pages=True):
        url = f"https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=snippet,id&order=date"
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        print(url)
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        
        video_ids = []
        item_data = data['items']
        
        for item in item_data:
            if item['id']['kind'] == 'youtube#video':
                video_ids.append(item['id']['videoId'])
        
        return video_ids
    

    def _get_video_data(self, video_id):
        url = f"https://www.googleapis.com/youtube/v3/videos?key={self.api_key}&id={video_id}&part=snippet"
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        
        if 'items' in data and len(data['items']) > 0:
            video_item = data['items'][0]
            snippet = video_item['snippet']
            
            published_at = snippet['publishedAt']
            title = snippet['title']
            description = snippet['description']
            thumbnails_high = snippet['thumbnails']['high']['url']
            
            video_data = {
                'publishedAt': published_at,
                'title': title,
                'description': description,
                'thumbnails_high': thumbnails_high
            }
            return video_data
        else:
            return None


# CHANNEL_URL = "https://www.youtube.com/c/SpongeBobOfficial"
# test = get_live_stream_id(CHANNEL_URL)
# print(test)
# channel_id = get_channel_ids("https://www.youtube.com/@SpongeBobOfficial")

# youtube = YTstats(random.choice(API_KEY), channel_id)

# print(youtube.is_channel_live())
# # channel_data = youtube.get_channel_statistics()
# print('Channel Statistics:', channel_data['statistics'])
# print('Channel Profile Image URL:', channel_data['profile_image_url_high'])
# print('View Count:', channel_data['statistics']['viewCount'])
# print('Subscriber Count:', channel_data['statistics']['subscriberCount'])

# print('USERNAME:', channel_data['username'])

# # #getting html of the /videos page



import yt_dlp 
import requests 
from PIL import Image
from io import BytesIO 
from yt_dlp import DownloadError
import sys
import os

main_path = os.path.realpath(os.path.dirname(__file__))
main_path = os.path.dirname(main_path)
path_audio = os.path.join(main_path,"Songs", "%(title)s.%(ext)s")
path_video = os.path.join(main_path,"Videos", "%(title)s.%(ext)s")
base_path = getattr(sys, '_MEIPASS', main_path)

ffmpeg_path = os.path.join(base_path, "ffmpeg", "ffmpeg.exe")


audio = {
            "format": "mp3/bestaudio/best",
            "compat_opts": ["no-youtube-unavailable-videos"], # Skips the unavailable videos
            "noplaylist": True, # If a URL from a song in a playlist is used, skips the playlist
            "outtmpl":path_audio, # The desired path to save the video
            "ffmpeg_location": ffmpeg_path,
            "postprocessors": [
                {  
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                }
                            ],
            "name":"Songs"
                }
video = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best", 
    "compat_opts": ["no-youtube-unavailable-videos"],
    "noplaylist": True,
    "outtmpl": path_video,
    "ffmpeg_location": ffmpeg_path,
    "name":"Videos"
}
array=[]
array.append(audio)
array.append(video)

class ytb:
    option = array[0] # Default value audio
    def __init__(self, info):
        self.title = info["title"]
        self.url = info["webpage_url"]
        if "entries" in info:
            self.type = "Playlist"
            self.thumbnail = None
        else:
            self.type = "Video"
            self.thumbnail = info["thumbnail"]

    @classmethod
    def extract_audio(cls, url):
        with yt_dlp.YoutubeDL(cls.option) as ytdl:
            try:
                info = ytdl.extract_info(url, download = False)
                if info.get("is_live"):
                    return f"Can't download Livestream."
                return cls(info)
            except Exception as e:
                if "URL" in str(e) or "HTTP" in str(e):
                    return f"Not a valid URL"
                else:
                    return e
    @classmethod
    def change_option(cls, ptr):
        cls.option = array[ptr]

    # Function to load an image from a URL 
    def get_thumbnail(self): 
        try: 
            response = requests.get(self.thumbnail) 
            response.raise_for_status()  # Check for HTTP errors 
            image = Image.open(BytesIO(response.content)) 
            return image 
        except Exception as e: 
            print(f"Error loading image: {e}") 
            return None 

    def download(self):
        path = os.path.realpath(os.path.dirname("YTBTOMP3")) +"\\"+ytb.option["name"]
        self.folder_exists(path)
        with yt_dlp.YoutubeDL(self.option) as ytdl:
            ytdl.download([self.url])

    def folder_exists(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
            print(f"Base directory '{path}' was created.")
        else:
            print(f"Base directory '{path}' already exists.")

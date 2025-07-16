import yt_dlp
import os
import re
from pathlib import Path

class YoutubeHandler:
    def __init__(self):
        self.destination_folder = ""
        self.url = ""

    def set_destination(self, folder_path):
        self.destination_folder = folder_path

    def set_url(self, url):
        self.url = url

    def format_duration(self, seconds):
        if seconds is None:
            return "N/A"
        else:
            minutes = seconds // 60
            seconds = seconds % 60
            return f"{minutes}:{seconds:02d}"
    
    def format_date(self, date):
        if date is None:
            return "N/A"
        else:
            return date.strftime("%d-%m-%Y")

    def fix_filename(self, filename):
        # remove all non-alphanumeric characters
        filename = re.sub(r'[<>:"/\\|?*]', '', filename)
        filename = filename.replace('  ', ' ').strip()
        return filename
    
    def get_info(self):

        if not self.url:
            return None

        ydl_opts = {'quiet': True, 'no_warnings': True}

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(self.url, download=False)

                if info_dict is None:
                    return None

                thumbnail_url = None
                if 'thumbnails' in info_dict and info_dict['thumbnails']:
                    thumbnail_url = info_dict['thumbnails'][-1]['url']

                upload_date = None
                if 'upload_date' in info_dict and info_dict['upload_date']:
                    date_str = info_dict['upload_date']
                    if len(info_dict['upload_date']) == 8:
                        upload_date = f"{date_str[6:8]}-{date_str[4:6]}-{date_str[0:4]}"
        
                return {
                    'title': info_dict.get('title', 'Título não disponível'),
                    'uploader': info_dict.get('uploader', 'N/A'),
                    'upload_date': upload_date,
                    'duration': self.format_duration(info_dict.get('duration')),
                    'duration_seconds': info_dict.get('duration', 0),
                    'thumbnail': thumbnail_url,
                }
                
        except Exception as e:
            print(f"Erro ao obter informações do vídeo: {e}")
            return None
        
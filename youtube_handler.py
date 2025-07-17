import yt_dlp
import os
import re
from pathlib import Path


class YoutubeHandler:
    def __init__(self):
        self.url = None
        self.destination_folder = None

    def set_url(self, url):
        self.url = url

    def set_destination(self, path):
        self.destination_folder = path

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
        # Remove all non-alphanumeric characters
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
        
    def download(self, progress_callback=None):
        if not self.url or not self.destination_folder:
            return False, "URL ou pasta de destino não definidos"
        os.makedirs(self.destination_folder, exist_ok=True)
        def progress_hook(d):
            if progress_callback and d['status'] == 'downloading':
                try:
                    if 'total_bytes' in d:
                        percent = (d['downloaded_bytes'] / d['total_bytes']) * 100
                    elif 'total_bytes_estimate' in d:
                        percent = (d['downloaded_bytes'] / d['total_bytes_estimate']) * 100
                    else:
                        percent = 0
                    progress_callback(percent)
                except:
                    pass
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.destination_folder, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'postprocessor_args': [
                '-ar', '44100',
                '-ac', '2',
            ],
            'progress_hooks': [progress_hook] if progress_callback else [],
            'quiet': True,
            'no_warnings': True,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([self.url])
                return True, "Download concluído com sucesso"
        except Exception as e:
            error_msg = str(e)
            if "ffmpeg" in error_msg.lower():
                return False, "FFmpeg não encontrado. Instale o FFmpeg para converter para MP3"
            elif "private" in error_msg.lower() or "unavailable" in error_msg.lower():
                return False, "Vídeo privado ou não disponível"
            elif "copyright" in error_msg.lower():
                return False, "Vídeo bloqueado por direitos autorais"
            else:
                return False, f"Erro no download: {error_msg}"
            
    def download_all(self, urls, progress_callback=None):
        if not urls or not self.destination_folder:
            return False, "URLs ou pasta de destino não definidos"
        total_videos = len(urls)
        success_count = 0
        failed_count = []
        for i, video_info in enumerate(urls):
            try:
                self.set_url(video_info['url'])
                if progress_callback:
                    overall_progress = ( i / total_videos) * 100
                    progress_callback(overall_progress, video_info['title'], i + 1, total_videos)
                success, message = self.download()
                if success:
                    success_count += 1
                else:
                    failed_count.append({
                        'title': video_info['title'],
                        'message': message
                    })                 
            except Exception as e:
                failed_count.append({
                    'title': video_info.get('title', 'Título não disponível'),
                    'message': str(e)
                })
            if progress_callback:
                progress_callback(100, 'Download concluído', success_count, total_videos)
            return success_count, failed_count
        
    @staticmethod
    def extract_video_id(url):
        patterns = [
            r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([a-zA-Z0-9_-]{11})',
            r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})'
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    @staticmethod
    def is_valid_url(url):
        return YoutubeHandler.extract_video_id(url) is not None
        
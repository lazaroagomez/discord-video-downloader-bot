import os
import yt_dlp
from pathlib import Path
import asyncio

class VideoDownloader:
    """
    A class to handle video downloads from various social media platforms
    with size restrictions and automatic compression if needed.
    """
    
    def __init__(self):
        self.download_path = os.getenv('DOWNLOAD_PATH')
        self.max_file_size_bytes = 8 * 1024 * 1024  # 8 MB
        self.ydl_opts = {
            'format': 'mp4[filesize<=8M]/best[ext=mp4][filesize<=8M]/best[filesize<=8M]/best',
            'outtmpl': os.path.join(self.download_path, '%(id)s.%(ext)s'),
            'quiet': True,
            'no_warnings': True,
            'extractor_args': {
                'facebook': {
                    'format': 'dash_sd_src',  # Try SD format for Facebook
                }
            }
        }

    async def download_with_info(self, url):
        """
        Downloads a video and returns its path along with metadata.
        Handles compression if the file is too large.
        
        Args:
            url (str): The URL of the video to download
            
        Returns:
            dict: Contains 'path' to the video file and 'info' metadata,
                 or None if download fails
        """
        try:
            platform = self._detect_platform(url)
            if platform == 'facebook':
                self.ydl_opts['format'] = 'worst[ext=mp4]/worst'

            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                video_path = ydl.prepare_filename(info)

                if os.path.exists(video_path) and os.path.getsize(video_path) > self.max_file_size_bytes:
                    compressed_path = await self._compress_video(video_path)
                    if compressed_path:
                        os.remove(video_path)
                        return {'path': compressed_path, 'info': info}
                    else:
                        os.remove(video_path)
                        self.ydl_opts['format'] = 'worst[ext=mp4]/worst'
                        with yt_dlp.YoutubeDL(self.ydl_opts) as ydl_worst:
                            info = ydl_worst.extract_info(url, download=True)
                            video_path = ydl_worst.prepare_filename(info)
                            if os.path.exists(video_path) and os.path.getsize(video_path) <= self.max_file_size_bytes:
                                return {'path': video_path, 'info': info}
                            os.remove(video_path)
                            return None

                return {'path': video_path, 'info': info} if os.path.exists(video_path) else None

        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return None

    def _detect_platform(self, url):
        """
        Detects the social media platform from the URL
        
        Args:
            url (str): The URL to analyze
            
        Returns:
            str: Platform name or 'unknown'
        """
        if 'facebook.com' in url or 'fb.watch' in url:
            return 'facebook'
        elif 'tiktok.com' in url:
            return 'tiktok'
        elif 'instagram.com' in url:
            return 'instagram'
        elif 'youtube.com' in url:
            return 'youtube'
        return 'unknown'

    async def _compress_video(self, video_path):
        """
        Compresses a video file to meet size restrictions using ffmpeg
        
        Args:
            video_path (str): Path to the video file to compress
            
        Returns:
            str: Path to the compressed video, or None if compression fails
        """
        output_path = f"{os.path.splitext(video_path)[0]}_compressed.mp4"
        try:
            process = await asyncio.create_subprocess_exec(
                'ffmpeg', '-i', video_path,
                '-c:v', 'libx264',
                '-preset', 'veryfast',
                '-crf', '32',           # Higher compression
                '-vf', 'scale=480:-2',  # Reduce to 480p
                '-c:a', 'aac',
                '-b:a', '96k',
                '-movflags', '+faststart',
                output_path,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()

            if process.returncode != 0:
                raise Exception(stderr.decode())

            if os.path.getsize(output_path) <= self.max_file_size_bytes:
                return output_path

            os.remove(output_path)
            return None

        except Exception as e:
            print(f"Error compressing video: {str(e)}")
            if os.path.exists(output_path):
                os.remove(output_path)
            return None
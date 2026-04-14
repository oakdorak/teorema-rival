
import yt_dlp

ydl_opts = {
    'format': 'bestaudio/best',
    'quiet': True,
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info("https://www.youtube.com/watch?v=QeFIp0iWPUg", download=False)
    print(info['url'])

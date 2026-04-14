from youtube_transcript_api import YouTubeTranscriptApi
import json

urls = [
    "https://www.youtube.com/watch?v=uWeexVsEbHo",
    "https://www.youtube.com/watch?v=S18DCJbNgCk",
    "https://www.youtube.com/watch?v=4EVHlFHqNEA",
    "https://www.youtube.com/watch?v=596fOfnYkKQ"
]

all_transcripts = {}
for url in urls:
    video_id = url.split('v=')[-1].split('&')[0]
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=['es'])
        all_transcripts[video_id] = " ".join([t['text'] for t in transcript])
    except Exception as e:
        print(f"Error {video_id}: {e}")

print("---RESULT---")
print(json.dumps(all_transcripts))

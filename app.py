from flask import Flask, render_template, request, jsonify
import requests
from pytube import YouTube

app = Flask(__name__)

INVIDIOUS_API_URL = "https://invidious.snopyta.org/api/v1/search"

@app.route('/')
def home():
    return render_template('index.html', search_results=None)

# TODO: pagination or infinite scroll
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')

    if search_query:
        '''
        q: String
        page: Int32
        sort_by: "relevance", "rating", "upload_date", "view_count"
        date: "hour", "today", "week", "month", "year"
        duration: "short", "long", "medium"
        type: "video", "playlist", "channel", "movie", "show", "all", (default: all)
        features: "hd", "subtitles", "creative_commons", "3d", "live", "purchased", "4k", "360", "location", "hdr", "vr180" (comma separated: e.g. "&features=hd,subtitles,3d,live")
        region: ISO 3166 country code (default: "US")
        '''
        params = {
            'q': search_query,
            'type': "video"
        }
        try:
            response = requests.get(INVIDIOUS_API_URL, params=params)
            response.raise_for_status()
            results = response.json()
        except requests.exceptions.RequestException as e:
            return jsonify(error=str(e)), 500

        return render_template('index.html', search_results=results, search_query=search_query)
    else:
        return render_template('index.html', search_results=None)

@app.route('/play/<video_id>')
def play(video_id):
    video_url = get_youtube_video_url(video_id)
    video_title = get_youtube_video_title(video_id)
    return render_template('video_player.html', video_url=video_url, video_title=video_title)

def get_youtube_video_url(video_id):
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    video_stream = yt.streams.filter(file_extension='mp4', res='720p').first()
    return video_stream.url if video_stream else None

def get_youtube_video_title(video_id):
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    return yt.title

if __name__ == '__main__':
    app.run(debug=True)

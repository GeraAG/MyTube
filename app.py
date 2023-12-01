from flask import Flask, render_template, request, jsonify
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta
from pytube import YouTube, Channel

app = Flask(__name__)

#TODO: chaeck if invideous insctance is not working and use working one
#invidious_instance = "https://invidious.nerdvpn.de"
invidious_instance = "https://invidious.io.lol"
#invidious_instance = "https://redirect.invidious.io"
INVIDIOUS_API_URL = "https://invidious.snopyta.org/api/v1/search"
INVIDIOUS_WATCH_API_URL = invidious_instance + "/api/v1/videos/"
INVIDIOUS_COMMENTS_API_URL = invidious_instance + "/api/v1/comments/"


@app.route('/')
def home():
    return render_template('index.html', search_results=None)

# TODO: pagination or infinite scroll
@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('search_query')
    page = request.args.get('page', 1, type=int)

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
            'page': page,
            'type': "all"
        }
        try:
            response = requests.get(INVIDIOUS_API_URL, params=params)
            response.raise_for_status()
            results = response.json()
        except requests.exceptions.RequestException as e:
            return jsonify(error=str(e)), 500

        currentTime = datetime.today()

        for result in results:
            if result['type'] == "video":
                result['viewCount'] = shorten_views(result['viewCount'])
                #result['published'] =
                publishedTime = datetime.fromtimestamp(result['published'])
                diff = relativedelta(currentTime, publishedTime)
                if diff.years > 1:
                    result['published'] = str(diff.years) + " years ago"
                elif diff.years == 1:
                    result['published'] = "1 year ago"
                elif diff.months > 1:
                    result['published'] = str(diff.months) + " months ago"
                elif diff.months == 1:
                    result['published'] = "1 month ago"
                elif diff.days > 1:
                    result['published'] = str(diff.days) + " days ago"
                elif diff.days == 1:
                    result['published'] = "1 day ago"
                elif diff.hours > 1:
                    result['published'] = str(diff.hours) + " hours ago"
                elif diff.hours == 1:
                    result['published'] = "1 hour ago"
                elif diff.minutes > 1:
                    result['published'] = str(diff.minutes) + " minutes ago"
                else:
                    print(publishedTime)
                    result['published'] = ""



        # Render the results as HTML for the initial request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return paginated results as JSON for AJAX requests
            return jsonify(html=render_template('result.html', search_results=results))
        else:
            # Return the entire HTML page for the initial request
            return render_template('index.html', search_results=results, search_query=search_query)

    else:
        # Return only the form when there's no search query
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # For AJAX requests, return an empty response
            return jsonify(html="")
        else:
            # For initial requests, return the form and no results
            return render_template('index.html', search_results=None)

@app.route('/watch/<video_id>')
def watch(video_id):
    yt = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    #channel = Channel(yt.channel_url)

    video_stream = yt.streams.filter(file_extension='mp4', res='720p').first()
    if video_stream:
        video_url = video_stream.url
    else:
        video_url = ""

    '''
    video_details = {
        'author': yt.author,
        'channel_id': yt.channel_id,
        'channel_url': yt.channel_url,
        'channel_name': channel.channel_name,
        'description': yt.description,
        'keywords': yt.keywords,
        'publish_date': yt.publish_date,
        'rating': yt.rating,
        'thumbnail_url': yt.thumbnail_url,
        'title': yt.title,
        'views': yt.views
    }
    '''

    api_url = INVIDIOUS_WATCH_API_URL + video_id
    try:
        responseVideo = requests.get(api_url)
        responseVideo.raise_for_status()
        resultsVideo = responseVideo.json()
        description = resultsVideo['description'].replace('\n', '<br>')
    except requests.exceptions.RequestException as e:
        print('error')
        return jsonify(error=str(e)), 500

    comments_api_utl = INVIDIOUS_COMMENTS_API_URL + video_id
    try:
        responseComments = requests.get(comments_api_utl)
        responseComments.raise_for_status()
        resultsComments = responseComments.json()
        for com in resultsComments['comments']:
            com['content'] = com['content'].replace('\n', '<br>')
            print(com['content'].replace('\n', '<br>'))
    except requests.exceptions.RequestException as e:
        print('error')
        return jsonify(error=str(e)), 500

    return render_template('watch.html', video_url=video_url, details=resultsVideo, description=description, commentsData=resultsComments)

def shorten_views(num_views):
    if num_views < 1000:
        return str(num_views)
    elif num_views < 1e6:
        return f'{num_views/1e3:.1f}K'
    elif num_views < 1e9:
        return f'{num_views/1e6:.1f}M'
    else:
        return f'{num_views/1e9:.1f}B'

if __name__ == '__main__':
    app.run(debug=True)

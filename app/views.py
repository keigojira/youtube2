from django.shortcuts import render
from django.conf import settings
import google.oauth.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

API_KEY = settings.YOUTUBE_API_KEY
DISCOVERY_URL = 'https://www.googleapis.com/discovery/v1/apis'
API_SERVICE = build('youtube', 'v3', developerKey=API_KEY, discoveryServiceUrl=DISCOVERY_URL)

def index(request):
    try:
        request = API_SERVICE.search().list(q='Django tutorial', maxResults=5, type='video', videoEmbeddable=True)
        response = request.execute()

        videos = []
        for search_result in response.get('items', []):
            video_id = search_result['id']
            video = API_SERVICE.videos().get(id=video_id).execute()
            videos.append(video)
    except HttpError as e:
        print('The API request failed with error %s' % e)

    return render(request, 'index.html', {'videos': videos})

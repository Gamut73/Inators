import os
from dotenv import load_dotenv
import googleapiclient.discovery

load_dotenv('local.env')

api_service_name = "youtube"
api_version = "v3"

DEVELOPER_KEY = os.getenv("GOOGLE_API_KEY")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY)


def get_first_youtube_search_video_result_id(query, max_results=1):
    request = youtube.search().list(
        part="snippet",
        maxResults=max_results,
        q=query,
        type="video"
    )
    response = request.execute()
    return response['items'][0]['id']['videoId'] if response['items'] else None


if __name__ == "__main__":
    print(get_first_youtube_search_video_result_id("The bird people in china trailer"))

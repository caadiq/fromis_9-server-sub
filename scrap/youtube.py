from pydantic import BaseModel
from pytubefix import YouTube


class Videos(BaseModel):
    videoId: str


async def get_details(videos):
    details = []

    for video in videos:
        detail = scraping(video.videoId)
        details.append(detail)

    return details


def scraping(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(url)

    length = yt.length
    views = yt.views

    if length is None:
        length = 0
    if views is None:
        views = 0

    return {"videoId": video_id, "length": length, "views": views}

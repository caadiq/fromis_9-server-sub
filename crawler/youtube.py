from pydantic import BaseModel
from pytube import YouTube


class Videos(BaseModel):
    videoId: str


async def get_details(videos):
    details = []

    for video in videos:
        detail = crawling(video.videoId)
        details.append(detail)

    return details


def crawling(video_id):
    url = f"https://www.youtube.com/watch?v={video_id}"
    yt = YouTube(url)

    length = yt.length
    views = yt.views

    return {"videoId": video_id, "length": length, "views": views}
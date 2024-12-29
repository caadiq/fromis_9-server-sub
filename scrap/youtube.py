from pydantic import BaseModel
from pytubefix import YouTube
import asyncio


class Videos(BaseModel):
    videoId: str


async def get_details(videos):
    tasks = []
    for video in videos:
        task = asyncio.create_task(scraping(video.videoId))
        tasks.append(task)

    details = await asyncio.gather(*tasks, return_exceptions=True)
    return [detail for detail in details if detail is not None]


async def scraping(video_id):
    try:
        def get_youtube_info():
            url = f"https://www.youtube.com/watch?v={video_id}"
            yt = YouTube(url)
            return yt.length, yt.views

        length, views = await asyncio.to_thread(get_youtube_info)

        length = length if length is not None else 0
        views = views if views is not None else 0

        return {"videoId": video_id, "length": length, "views": views}

    except Exception as e:
        return None
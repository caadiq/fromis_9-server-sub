from typing import List

from fastapi import FastAPI, HTTPException

from scrap.dcinside import get_posts
from scrap.weverse_notice import get_notices
from scrap.weverse_shop import get_albums
from scrap.youtube import Videos, get_details

app = FastAPI()


@app.post("/youtube")
async def youtube_details(videos: List[Videos]):
    try:
        return await get_details(videos)
    except Exception as e:
        print(f"Error occurred while getting details: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/weverse/shop")
async def weverse_shop():
    try:
        return await get_albums()
    except Exception as e:
        print(f"Error occurred while getting details: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/weverse/notice")
async def weverse_notice():
    try:
        return await get_notices()
    except Exception as e:
        print(f"Error occurred while getting details: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/dcinside")
async def dcinside():
    try:
        return await get_posts()
    except Exception as e:
        print(f"Error occurred while getting details: {e}")
        raise HTTPException(status_code=400, detail=str(e))

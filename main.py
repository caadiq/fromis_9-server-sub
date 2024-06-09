from typing import List

from fastapi import FastAPI, HTTPException

from scrap.dcinside import get_posts
from scrap.weverseshop import get_items
from scrap.youtube import Videos, get_details

app = FastAPI()


@app.post("/youtube")
async def youtube_details(videos: List[Videos]):
    try:
        return await get_details(videos)
    except Exception as e:
        print(f"Error occurred while getting details: {e}")
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/weverseshop")
async def weverse_shop():
    try:
        return await get_items()
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

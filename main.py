from typing import List

from fastapi import FastAPI, HTTPException

from crawler.youtube import Videos, get_details

app = FastAPI()


@app.post("/youtube")
async def youtube_details(videos: List[Videos]):
    try:
        return await get_details(videos)
    except Exception as e:
        print(f"Error occurred while getting details: {e}")
        raise HTTPException(status_code=400, detail=str(e))
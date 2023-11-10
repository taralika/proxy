from fastapi import FastAPI, HTTPException, Request
import httpx

app = FastAPI()

@app.get("/")
async def read_item(url: str, request: Request):
    if not url.startswith('http://') and not url.startswith('https://'):
        raise HTTPException(status_code=400, detail="Invalid URL provided.")

    headers = {
        'User-Agent': 'Kaka Bua kaka@bua.com'
    }

    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            resp.raise_for_status()  # Raises an HTTPError if the status is 4xx, 5xx
            return resp.json()
        except httpx.HTTPError as e:
            content = e.response.content if e.response else "HTTP error occurred"
            raise HTTPException(status_code=400, detail=content)
        except httpx.RequestError as e:
            raise HTTPException(status_code=500, detail="An error occurred while requesting.")

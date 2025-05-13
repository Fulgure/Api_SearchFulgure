from fastapi import FastAPI
from pydantic import BaseModel
from search import Search
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

s = Search()
app = FastAPI()

@app.get("/v1/search")
async def search(q: str):
    return s.search(q)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7000)
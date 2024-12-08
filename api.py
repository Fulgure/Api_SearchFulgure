from fastapi import FastAPI
from pydantic import BaseModel
from search import Search
from fastapi.middleware.cors import CORSMiddleware

s = Search()
app = FastAPI()

@app.get("/search/v1/{query}")
async def search(query: str):
    return s.search(query)
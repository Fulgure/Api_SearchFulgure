from fastapi import FastAPI
from pydantic import BaseModel
from search import Search
from fastapi.middleware.cors import CORSMiddleware
import unicorn

s = Search()
app = FastAPI()

@app.get("/search/v1/{query}")
async def search(query: str):
    return s.search(query)

if __name__ == "__main__":
    unicorn.run(app, host="0.0.0.0", port=8000)
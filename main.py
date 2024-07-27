from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app = FastAPI()

class PostStructure(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None



@app.get("/")
def root():
    return {"Hello":"This is the welcome page!"}

@app.post("/createposts")
def create_post(post: PostStructure):
    print(post.model_dump())
    return {"new_post": post}


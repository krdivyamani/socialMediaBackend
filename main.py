from fastapi import FastAPI
from fastapi.params import Body

app = FastAPI()


@app.get("/")
def root():
    return {"Hello":"This is the welcome page!"}

@app.post("/createposts")
def create_post(payload: dict = Body(...)):
    return {"new_post": f"title: {payload['title']}, content: {payload['content']}"}
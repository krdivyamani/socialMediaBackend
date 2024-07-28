from fastapi import FastAPI, HTTPException, status, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='xxxxx',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB connected")
        break
    except Exception as error:
        print("Connecting to DB failed")
        time.sleep(2)

app = FastAPI()

class PostStructure(BaseModel):
    title: str
    content: str
    published: bool = True

        
@app.get("/")
def root():
    return {"Hello":"This is the welcome page!"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT *  FROM posts """)
    posts = cursor.fetchall()
    return {"message":posts}

@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM posts WHERE id = (%s) """, (str(id),))
    post = cursor.fetchone()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with ID: {id} doesn't exist.")
    
    return {"post_detail": post}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: PostStructure):
    print(post.model_dump())
    cursor.execute("""INSERT INTO posts(title, content, published) VALUES(%s, %s, %s) 
                   RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = (%s) RETURNING *""", (str(id), ))
    deleted_post = cursor.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with ID: {id} doesn't exist")
    conn.commit()
    return Response(status_code=status.HTTP_404_NOT_FOUND)

@app.put("/posts/{id}")
def update_post(id: int, post: PostStructure):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = (%s) 
                   RETURNING * """, (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"The post with ID: {id} doesn't exist")
    conn.commit()
    return {"data": updated_post}
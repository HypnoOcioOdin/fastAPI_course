from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import uvicorn


app = FastAPI()


@app.get('/blog')
def index(limit: int, published: bool = False, sort: Optional[str] = None):
    # only get 10 published blogs
    if published:
        return {"data":f"{limit} blogs from db "}
    else:
        return {"data":f"all blogs from db "}

@app.get('/blog/unpublished')
def unpublished():
    return {"data":"all unpublished data"}

@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {"data":id}

@app.get('/blog/{id}/comments')
def comments(id: int, limit: int = 10):
    # fetch comments of blog with id = id
    return {"data": f"limited output on {limit}"}



@app.post('/blog')
def create_blog(blog: Blog):
    return {"data":f"Blog is created with title {blog.title}"}


# if __name__ == "__main__":
#     uvicorn.run(app,host="127.0.0.1",port = 9000)

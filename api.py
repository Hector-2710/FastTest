from fastapi import FastAPI, status
from uuid import UUID

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def get_hello():
    return {"Hello": "World"}

@app.get("/post/{id}", status_code=status.HTTP_200_OK)
def get_post_by_id(id: int):
    return {"id": id}

@app.get("/post", status_code=status.HTTP_200_OK)
def get_post(id: UUID):
    return {"id": id}

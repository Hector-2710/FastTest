from fastapi import FastAPI, status
from uuid import UUID

app = FastAPI()

list_users = []

@app.get("/", status_code=status.HTTP_200_OK)
def get_hello():
    return {"Hello": "World"}

@app.get("/post/{id}", status_code=status.HTTP_200_OK)
def get_post_by_id(id: UUID):
    return {"id": id}

@app.get("/post", status_code=status.HTTP_200_OK)
def get_post(id: UUID):
    return {"id": id}

@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_user(user: dict):
    list_users.append(user)
    return user

@app.put("/user/{username}", status_code=status.HTTP_200_OK)
def update_user(username: str, data: dict):
    for user in list_users:
        if user["username"] == username:
            user.update(data)
            return user
    return {"error": "User not found"}

@app.patch("/user/{username}", status_code=status.HTTP_200_OK)
def patch_user(username: str, data: dict):
    for user in list_users:
        if user["username"] == username:
            user.update(data)
            return user
    return {"error": "User not found"}

@app.delete("/user/{username}", status_code=status.HTTP_200_OK)
def delete_user(username: str):
    global list_users
    list_users = [u for u in list_users if u["username"] != username]
    return {"message": f"User {username} deleted"}

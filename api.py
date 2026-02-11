from fastapi import FastAPI,status, HTTPException

app = FastAPI()

@app.get("/", status_code=status.HTTP_200_OK)
def get_hello():
    return {"Hello": "World"}


@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_user(user: dict):
        if "name" not in user:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Name is required")
        return {"user": user}

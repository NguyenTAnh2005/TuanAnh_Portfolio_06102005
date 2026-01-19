from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import auth


app = FastAPI()

@app.get("/")
def read_root():
    return {"Message" : "Welcome Backend của dự án Portfolio"}

app.include_router(auth.router)






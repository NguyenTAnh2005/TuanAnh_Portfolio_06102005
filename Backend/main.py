from fastapi import FastAPI, Depends, HTTPException, status
app = FastAPI()


@app.get("/")
def read_root():
    return {"Message" : "Welcome Backend của dự án Portfolio"}


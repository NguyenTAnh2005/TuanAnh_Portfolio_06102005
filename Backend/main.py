from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import auth, myinfo, role, user, project


app = FastAPI()

@app.get("/")
def read_root():
    return {"Message" : "Welcome Backend của dự án Portfolio"}

app.include_router(auth.router)
app.include_router(myinfo.router)
app.include_router(role.router)
app.include_router(user.router)
app.include_router(project.router)






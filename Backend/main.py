from fastapi import FastAPI, Depends, HTTPException, status
from app.routers import auth, myinfo, role, user, project, system
from app.routers import category_blog, blog, timeline, system_config
from app.routers import category_achievement as ca, achievement as ach

# CORS 
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings


app = FastAPI()
#=============================== CODE CROS
origins = [
    settings.FRONTEND_URL,
]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)
#==========================================

@app.get("/")
def read_root():
    return {"Message" : "Welcome Backend của dự án Portfolio"}

app.include_router(auth.router)
app.include_router(myinfo.router)
app.include_router(role.router)
app.include_router(user.router)
app.include_router(project.router)
app.include_router(category_blog.router)
app.include_router(blog.router)
app.include_router(timeline.router)
app.include_router(ca.router)
app.include_router(ach.router)
app.include_router(system_config.router)

app.include_router(system.router)







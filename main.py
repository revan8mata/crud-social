from fastapi import  FastAPI
from fastapi.middleware.cors import CORSMiddleware


from routers import post, user
import models
import auth
import vote
from database import engine

# models.base.metadata.create_all(bind=engine)
app = FastAPI()


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.ROUTER)
app.include_router(user.ROUTER)
app.include_router(post.ROUTER)
app.include_router(vote.ROUTER)
# app.include_router(coments.ROUTER)
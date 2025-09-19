from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user,auth,vote
import uvicorn
import os
# models.Base.metadata.create_all(bind=engine)            since we are using alembic this line is not required
app= FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return{"message":"Welcome Shobana "}


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Render sets this
    uvicorn.run(app, host="0.0.0.0", port=port)



    
    
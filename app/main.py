from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import post,user,auth,vote
import uvicorn
import os
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine,text
from .config import settings
# models.Base.metadata.create_all(bind=engine)            since we are using alembic this line is not required
from fastapi import FastAPI,HTTPException,status,Response,Depends,APIRouter
from app import models,schemas,utils
from sqlalchemy.orm import Session
from app.database import get_db

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

DATABASE_URL = f"mysql+pymysql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}?ssl_ca={os.path.join(os.getcwd(), 'ca.pem')}"

engine = create_engine(DATABASE_URL)

# Test DB connection endpoint
@app.get("/test-db")
def test_db():
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * from usersTable;"))
            return {"db_time": str(result.fetchone()),"username":settings.database_username}
    except Exception as e:
        return {"error": str(e)}


@app.get("/run-migrations")
def run_migrations():
    try:
        alembic_cfg = Config(os.path.join(os.getcwd(), "alembic.ini"))
        command.upgrade(alembic_cfg, "head")
        return {"message": "✅ Migrations completed successfully!"}
    except Exception as e:
        return {"error": str(e)}

@app.get("/insert")
def insert():
    try:
        with engine.connect() as conn:
            query = text("INSERT INTO usersTable (email, password) VALUES ('shobana@gmail.com', 'pass@123')")
            conn.execute(query)
            conn.commit()
    except Exception as e:
        return {"error": str(e)}


@app.get("/{id}",response_model=schemas.UserCreateResponse)
def get_user(id:int,db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"the request with id: {id} was not found")
    print(user)
    return user

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Render sets this
    uvicorn.run(app, host="0.0.0.0", port=port)



    
    
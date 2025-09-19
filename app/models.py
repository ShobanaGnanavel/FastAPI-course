from sqlalchemy import Column,Integer,String,Boolean,DateTime,func,text,TIMESTAMP,ForeignKey
from sqlalchemy.sql.expression import null
from .database import Base
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "postTable"

    id = Column(Integer,primary_key=True,nullable=False,index=True)
    title = Column(String(255),nullable=False)
    content = Column(String(255),nullable=False)
    published = Column(Boolean,server_default=text('1'))
    createat = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    owner_id = Column(Integer,ForeignKey("usersTable.id",ondelete="CASCADE"),nullable=False)

    owner = relationship("usersTable") #have to call the python class

class Users(Base):
    __tablename__="usersTable"

    id = Column(Integer,primary_key=True,nullable=False,index=True)
    email = Column(String(50),nullable=False,unique=True)
    password = Column(String(255),nullable=False,unique=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))
    phone_number = Column(String(255))

class Vote(Base):
    __tablename__="votesTable"
    
    user_id = Column(Integer,ForeignKey("usersTable.id"),primary_key=True,nullable=False)
    post_id = Column(Integer,ForeignKey("postTable.id"),primary_key=True,nullable=False)

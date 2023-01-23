from sqlalchemy import Column, create_engine, create_engine,String,Date
from sqlalchemy.orm import declarative_base

engine=create_engine("sqlite:///pages", echo=False)
Base=declarative_base()


class Pages(Base):
    __tablename__="pages"
    url=Column(String,primary_key=True)
    document=Column(String)
    date=Column(Date)
def init():
    Base.metadata.drop_all(engine)# Delete sqlite db if already exit
    Base.metadata.create_all(engine)

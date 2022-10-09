from datetime import datetime
from typing import List, Optional
import pandas as pd
from sqlmodel import Field
from sqlmodel import SQLModel
from sqlmodel import Session
from sqlmodel import Relationship
from sqlmodel import create_engine 

from sdv import load_demo


class Users(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True) 
    country: str  
    gender: Optional[str] = None  
    age: Optional[int] = None

    sessions: List["Sessions"] = Relationship(back_populates="user")

class Sessions(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True) 
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")  
    device: Optional[str] = None  
    os: Optional[int] = None
    minute : Optional[int] = None

    user: Optional[Users] = Relationship(back_populates="sessions")
    transactions: List["Transactions"] = Relationship(back_populates="session")


class Transactions(SQLModel, table=True):

    id: Optional[int] = Field(default=None, primary_key=True) 
    session_id: Optional[int] = Field(default=None, foreign_key="sessions.id")
    timestamp: Optional[datetime] = None
    amount: Optional[float] = None
    cancelled: Optional[bool] = False

    session: Optional[Sessions] = Relationship(back_populates="transactions")

sqlite_file_name = "database.db" 

sqlite_url = f"sqlite:///{sqlite_file_name}" 
engine = create_engine(sqlite_url, echo=True) 


def create_db_and_tables():

    SQLModel.metadata.create_all(engine)


def df_to_sqlmodel(df: pd.DataFrame, table: SQLModel) -> List[SQLModel]:
    objs = [table(**row) for row in df.to_dict('records')]
    return objs


def populate():
    _, tables = load_demo(metadata=True)

    map_table_class = {
        'users' : Users,
        'sessions' : Sessions,
        'transactions' : Transactions
        }

    with Session(engine) as session:
        for table in tables:
            db_entries = df_to_sqlmodel(tables[table], map_table_class[table])
            for db_entry in db_entries:
                session.add(db_entry)
                session.commit()


if __name__ == "__main__":
    create_db_and_tables()
    populate()

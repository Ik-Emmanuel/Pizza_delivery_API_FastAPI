from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base,sessionmaker
import json

with open('credentials.json', 'r') as file:
    conn_str = json.load(file)

engine=create_engine(conn_str['db_connection'], echo=True)
Base=declarative_base()
Session=sessionmaker()
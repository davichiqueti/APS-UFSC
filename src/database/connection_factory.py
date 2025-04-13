from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()
db_engine = create_engine(os.environ["DATABASE_CONN_STRING"])
db_connection = db_engine.connect()

from pymongo import MongoClient
from redis import Redis
from sqlalchemy import create_engine

from app.config import settings


mysql_engine = create_engine(
    settings.mysql_url,
    pool_pre_ping=True,
    pool_recycle=3600,
    future=True
)

mongo_client = MongoClient(
    settings.mongodb_url,
    serverSelectionTimeoutMS=5000
)

mongo_database = mongo_client[settings.mongodb_database]

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5
)
from fastapi import FastAPI, HTTPException
from sqlalchemy import text

from app.database import (
    mongo_database,
    mysql_engine,
    redis_client
)
from app.routers import content, events, orders, trending, users, admin

app = FastAPI(
    title="Event Ticketing Service API",
    version="0.1.0",
    description=(
        "COMP 642 course project using MySQL, "
        "MongoDB, Redis, and FastAPI."
    )
)

app.include_router(events.router)
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(content.router)
app.include_router(trending.router)
app.include_router(admin.router)

@app.get("/", tags=["System"])
def root():
    return {
        "application": "Event Ticketing Service API",
        "documentation": "/docs",
        "healthCheck": "/health"
    }


@app.get("/health", tags=["System"])
def health_check():
    service_status = {
        "api": "healthy",
        "mysql": "unknown",
        "mongodb": "unknown",
        "redis": "unknown"
    }

    try:
        with mysql_engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        service_status["mysql"] = "healthy"

    except Exception:
        service_status["mysql"] = "unhealthy"

    try:
        mongo_database.command("ping")
        service_status["mongodb"] = "healthy"

    except Exception:
        service_status["mongodb"] = "unhealthy"

    try:
        redis_client.ping()
        service_status["redis"] = "healthy"

    except Exception:
        service_status["redis"] = "unhealthy"

    if "unhealthy" in service_status.values():
        raise HTTPException(
            status_code=503,
            detail=service_status
        )

    return service_status
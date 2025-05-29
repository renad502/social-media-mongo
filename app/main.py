from fastapi import FastAPI
from app.api.routes import auth_routes, user_routes, follow_routes
from app.db.database import connect_to_mongo, close_mongo_connection

app = FastAPI(title="Social Media API")

# Event handlers
@app.on_event("startup")
async def startup_db():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db():
    await close_mongo_connection()

# Routers
app.include_router(auth_routes.auth_router, prefix="/auth")
app.include_router(user_routes.router, prefix="/users")
app.include_router(follow_routes.router, prefix="/follows")

from app.api.routes import post_routes
app.include_router(post_routes.router)

from app.api.routes import comments_routes
app.include_router(comments_routes.router, prefix="/api")

from app.api.routes import like_routes
app.include_router(like_routes.router, prefix="/likes")

from app.api.routes import dm_routes
app.include_router(dm_routes.router)

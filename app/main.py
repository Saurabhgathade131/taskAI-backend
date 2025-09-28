from fastapi import FastAPI
from app.core.logging_ import init_logging
from app.db.mongo import mongo
from app.api.routes import auth as auth_router
from app.api.routes import tasks as tasks_router
from app.core.config import settings

# Initialize logging
init_logging()

# Create FastAPI app
app = FastAPI(title="AI Todo - Backend (scaffold)")

# Include routers
app.include_router(auth_router.router)
app.include_router(tasks_router.router)


@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB when app starts"""
    await mongo.connect()


@app.on_event("shutdown")
async def shutdown_event():
    """Disconnect from MongoDB when app shuts down"""
    await mongo.close()


# Root health check
@app.get("/")
async def root():
    return {"msg": "ok"}

@app.get("/health")
async def health_check():
    return {"message":"I am healthy"}
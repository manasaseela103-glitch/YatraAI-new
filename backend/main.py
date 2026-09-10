from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from config import settings
import database
from routes import trips, discovery, budget, safety, business, admin, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: initialize database connection and data
    await database.init_db()
    yield
    # Shutdown logic if needed
    await database.close_db()


app = FastAPI(
    title="YatraAI API",
    description="Smart tourism platform API for itinerary generation, adaptive replanning, discovery, safety, and local business empowerment.",
    version="1.0.0",
    lifespan=lifespan
)

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"status": "error", "message": str(exc), "path": request.url.path}
    )

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "message": "YatraAI API is running",
        "status": "success"
    }


# Health check endpoint
@app.get("/api/health")
async def health_check():
    db_status = await database.get_db_status()
    return {
        "status": "healthy",
        "service": "YatraAI Backend",
        "database": db_status
    }


# Include Routers with /api prefix
app.include_router(trips.router, prefix="/api")
app.include_router(discovery.router, prefix="/api")
app.include_router(budget.router, prefix="/api")
app.include_router(safety.router, prefix="/api")
app.include_router(business.router, prefix="/api")
app.include_router(admin.router, prefix="/api")
app.include_router(users.router, prefix="/api")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

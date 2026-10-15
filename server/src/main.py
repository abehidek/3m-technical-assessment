from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.shared.config import settings
from src.auth.presentation.routes.auth_routes import router as auth_router
from src.ticket.presentation.routes.ticket_routes import router as ticket_router

app = FastAPI(
    title="3m-technical-assessment",
    description="3m-technical-assessment",
    version="0.0.1",
)

# Configure CORS - Must be BEFORE including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        settings.frontend_url,
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],
)

# Register routers AFTER middleware
app.include_router(auth_router)
app.include_router(ticket_router)


@app.get("/")
async def root():
    return {
        "message": "3m-technical-assessment",
        "version": "0.0.1",
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}

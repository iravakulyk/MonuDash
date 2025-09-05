from typing import List, AsyncGenerator

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from monudash.models.monument import Monument
from monudash.database import get_session
from monudash.constants import STATIC_DIR, DEFAULT_HOST, DEFAULT_PORT

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")


@app.get("/")
async def get_root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/monuments")
async def get_monuments(session: AsyncSession = Depends(get_session)) -> List[Monument]:
    """Get all monuments from the database."""

    statement = select(Monument)
    result = await session.execute(statement)
    monuments = result.scalars().all()
    return list(monuments)


@app.get("/api/monuments/{monument_id}")
async def get_monument(monument_id: str, session: AsyncSession = Depends(get_session)) -> Monument:
    """Get a specific monument by ID from the database."""

    statement = select(Monument).where(Monument.id == monument_id)
    result = await session.execute(statement)
    monument = result.scalar_one_or_none()
    if monument is None:
        raise HTTPException(status_code=404, detail="Monument not found")
    return monument


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("monudash.main:app", host=DEFAULT_HOST, port=DEFAULT_PORT, reload=True)
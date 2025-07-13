from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pathlib import Path
from models.monument import Monument
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get paths from environment variables or use defaults
STATIC_DIR = os.getenv('STATIC_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"))
RESOURCES_DIR = os.getenv('RESOURCES_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "resources"))

# Serve static files (frontend)
app.mount("/static", StaticFiles(directory=STATIC_DIR, html=True), name="static")

@app.get("/")
async def get_root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/api/monuments")
async def get_monuments() -> list[Monument]:
    # Use the environment variable for resources path
    csv_path = os.path.join(RESOURCES_DIR, 'monuments_with_coordinates.csv')

    # Read the CSV file with coordinates
    df = pd.read_csv(csv_path)

    # Convert DataFrame to list of Monument objects
    monuments = [
        Monument(
            id=str(row['FID']),
            denkmalnummer=str(row['denkmalnummer']),
            denkmalart=str(row['denkmalart']),
            lage=str(row['lage']),
            link=str(row['link']),
            lat=row['lat'] if pd.notna(row['lat']) else None,
            lng=row['lng'] if pd.notna(row['lng']) else None,
        )
        for _, row in df.iterrows()
    ]
    
    return monuments

@app.get("/api/monuments/{monument_id}")
async def get_monument(monument_id: str) -> Monument:
    csv_path = os.path.join(RESOURCES_DIR, 'monuments_with_coordinates.csv')
    df = pd.read_csv(csv_path)
    row = df[df['FID'].astype(str) == monument_id]
    if row.empty:
        raise HTTPException(status_code=404, detail="Monument not found")
    row = row.iloc[0]
    return Monument(
        id=str(row['FID']),
        denkmalnummer=str(row['denkmalnummer']),
        denkmalart=str(row['denkmalart']),
        lage=str(row['lage']),
        link=str(row['link']),
        lat=row['lat'] if pd.notna(row['lat']) else None,
        lng=row['lng'] if pd.notna(row['lng']) else None,
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
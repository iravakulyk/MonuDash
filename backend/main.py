from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import httpx
from bs4 import BeautifulSoup
from pydantic import BaseModel
from pyproj import Transformer

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create transformer for UTM zone 32N (EPSG:32632) to WGS84 (EPSG:4326)
transformer = Transformer.from_crs("EPSG:32632", "EPSG:4326")

class Monument(BaseModel):
    id: str
    denkmalnummer: str
    denkmalart: str
    lage: str
    link: str
    lat: float | None = None
    lng: float | None = None

@app.get("/api/monuments")
async def get_monuments() -> list[Monument]:
    try:
        # Read the CSV file
        df = pd.read_csv('resources/denkmal_prodenkmal_csv.csv')
        
        # Initialize list to store monuments with coordinates
        monuments = []
        
        # Create async client for making requests
        async with httpx.AsyncClient() as client:
            for _, row in df.iterrows():
                monument = Monument(
                    id=row['FID'],
                    denkmalnummer=row['denkmalnummer'],
                    denkmalart=row['denkmalart'],
                    lage=row['lage'],
                    link=row['link'],
                )
                
                # Fetch the detail page
                try:
                    response = await client.get(row['link'])
                    if response.status_code == 200:
                        # Parse coordinates from the response
                        soup = BeautifulSoup(response.text, 'html.parser')
                        
                        # Find the table row containing coordinates
                        coord_row = soup.find('th', text='Koordinaten')
                        if coord_row and coord_row.find_next_sibling('td'):
                            coord_text = coord_row.find_next_sibling('td').text.strip()
                            try:
                                # Extract easting and northing from the coordinate text
                                easting, northing = map(float, coord_text.split())
                                
                                # Transform from UTM to lat/lng
                                lat, lng = transformer.transform(northing, easting)
                                monument.lat = lat
                                monument.lng = lng
                            except Exception as e:
                                print(f"Error parsing coordinates '{coord_text}': {str(e)}")
                
                except Exception as e:
                    print(f"Error fetching details for {row['link']}: {str(e)}")
                
                monuments.append(monument)
        
        return monuments
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 
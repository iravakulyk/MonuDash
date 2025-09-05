"""
This script fetches the coordinates for the monuments in Aachen by parsing the website for each monument.
It saves the coordinates to a new CSV file.
"""

import pandas as pd
import httpx
from bs4 import BeautifulSoup
from pathlib import Path
import pyproj

def extract_coordinates_from_text(text):
    """Try to extract coordinates from text content"""
    # Remove any non-essential whitespace
    text = ' '.join(text.split())
    
    # Split text into words and look for number pairs
    words = text.split()
    numbers = []
    for word in words:
        try:
            num = float(word.replace(',', '.'))
            numbers.append(num)
        except ValueError:
            continue
    
    if len(numbers) >= 2:
        return numbers[0], numbers[1]
    return None, None

def find_header_row(soup, header_text):
    """Find a table row containing the given header text"""
    # Try different ways to find the header
    for th in soup.find_all('th'):
        # Check if this header contains our text
        if header_text in th.get_text(strip=True):
            # Get the parent tr element
            tr = th.find_parent('tr')
            if tr:
                return tr
    return None

def parse_monument_entry(row, client):
    """Parse a single monument entry, fetch page, extract coordinates, and return lat/lng or None."""
    try:
        response = client.get(row['link'])
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        coord_row = find_header_row(soup, "Koordinaten")
        if coord_row:
            td = coord_row.find('td')
            if td:
                coord_text = td.get_text(strip=True)
                easting, northing = extract_coordinates_from_text(coord_text)
                if easting is not None and northing is not None:
                    try:
                        transformer = pyproj.Transformer.from_crs("EPSG:32632", "EPSG:4326", always_xy=True)
                        lng, lat = transformer.transform(easting, northing)
                        return lat, lng
                    except Exception:
                        pass
    except Exception:
        pass
    return None, None


def fetch_coordinates(input_filepath, output_name="monuments_with_coordinates.csv"):
    output_file = input_filepath.parent / output_name

    # Read the original CSV file
    df = pd.read_csv(input_filepath)

    # Add new columns for coordinates
    df['lat'] = None
    df['lng'] = None

    found_count = 0

    # Create client for making requests
    with httpx.Client() as client:
        for index, row in list(df.iterrows()):
            print(f"\nProcessing monument {index + 1}/{len(df)}")
            lat, lng = parse_monument_entry(row, client)
            df.at[index, 'lat'] = lat
            df.at[index, 'lng'] = lng
            if lat is not None and lng is not None:
                found_count += 1
                print(f"Successfully added coordinates for monument {index + 1}")

    # Save the updated dataframe to a new CSV file
    df.to_csv(output_file, index=False)
    print(f"\nProcess completed. Data saved to {output_file}")
    print(f"Found coordinates for {found_count} out of {len(df)} entries.")

if __name__ == "__main__":
        # Get the absolute path to the resources directory
    base_dir = Path(__file__).resolve().parent.parent.parent
    input_csv = base_dir / 'resources' / 'denkmal_prodenkmal_csv.csv'
    fetch_coordinates(input_csv) 
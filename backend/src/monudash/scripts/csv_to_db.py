from monudash.constants import MONUMENTS_CSV
import pandas as pd
from datetime import datetime
import asyncio

from monudash.database import init_db, get_session
from monudash.models.monument import Monument

def parse_date(date_str: str) -> datetime | None:
    """Parse date string to date object."""
    if not date_str or pd.isna(date_str):
        return None
    try:
        return datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return None

async def migrate_csv_to_db(csv_path: str) -> None:
    """Migrate data from CSV to SQLite database."""
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)
    
    print("Initializing database...")
    await init_db()
    
    print("Starting migration...")
    async for session in get_session():
        for _, row in df.iterrows():
            monument = Monument(
                id=row['FID'],
                official_id=row['denkmalnummer'],
                type=row['denkmalart'],
                address=row['lage'],
                url=row['link'],
                lat=float(row['lat']) if pd.notna(row['lat']) else None,
                lng=float(row['lng']) if pd.notna(row['lng']) else None,
                entry_date=parse_date(row['eintragungsdatum']),
                deletion_date=parse_date(row['geloescht'])
            )
            session.add(monument)
        
        print("Committing changes to database...")
        await session.commit()
    
    print("Migration completed successfully!")

if __name__ == "__main__":
    csv_path = MONUMENTS_CSV
    asyncio.run(migrate_csv_to_db(csv_path)) 
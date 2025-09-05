from sqlmodel import SQLModel, Field
from datetime import datetime
from pydantic import BaseModel

class AachenDenkmal(BaseModel):
    FID: str
    denkmalnummer: str | None = None
    denkmalart: str
    lage: str | None = None
    eintragungsdatum: datetime | None = None
    geloescht: datetime | None = None
    link: str

class MonumentBase(SQLModel):
    lat: float | None = None
    lng: float | None = None
    address: str | None = None
    url: str | None = None

    official_id: str | None = None
    type: str

    entry_date: datetime | None = None
    deletion_date: datetime | None = None

class Monument(MonumentBase, table=True):
    id: str | None = Field(default=None, primary_key=True)
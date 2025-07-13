from pydantic import BaseModel

class Monument(BaseModel):
    id: str
    denkmalnummer: str
    denkmalart: str
    lage: str
    link: str
    lat: float | None = None
    lng: float | None = None
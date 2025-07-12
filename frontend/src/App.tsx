import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { useEffect, useState } from 'react'
import 'leaflet/dist/leaflet.css'
import './utils/leaflet-icons'
import './App.css'

interface Monument {
  id: string;
  denkmalnummer: string;
  denkmalart: string;
  lage: string;
  link: string;
  lat: number | null;
  lng: number | null;
}

function App() {
  const [monuments, setMonuments] = useState<Monument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchMonuments = async () => {
      try {
        const response = await fetch('http://localhost:8000/api/monuments');
        if (!response.ok) {
          throw new Error('Failed to fetch monuments');
        }
        const data = await response.json();
        setMonuments(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
      } finally {
        setLoading(false);
      }
    };

    fetchMonuments();
  }, []);

  if (loading) {
    return <div>Loading monuments...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <div style={{ height: '100vh', width: '100vw', margin: 0, padding: 0, overflow: 'hidden' }}>
      <MapContainer 
        center={[50.7753, 6.0839]} // Aachen coordinates
        zoom={13} 
        style={{ height: '100%', width: '100%' }}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        {monuments.map(monument => {
          if (monument.lat && monument.lng) {
            return (
              <Marker 
                key={monument.id} 
                position={[monument.lat, monument.lng]}
              >
                <Popup>
                  <div>
                    <h3>{monument.denkmalnummer}</h3>
                    <p>{monument.denkmalart}</p>
                    <p>{monument.lage}</p>
                    <a href={monument.link} target="_blank" rel="noopener noreferrer">
                      More details
                    </a>
                  </div>
                </Popup>
              </Marker>
            );
          }
          return null;
        })}
      </MapContainer>
    </div>
  );
}

export default App;

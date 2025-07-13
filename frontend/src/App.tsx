import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet'
import { useEffect, useState } from 'react'
import 'leaflet/dist/leaflet.css'
import './utils/leaflet-icons'
import './App.css'
import { useMap } from 'react-leaflet';
import { useRef } from 'react';

interface Monument {
  id: string;
  denkmalnummer: string;
  denkmalart: string;
  lage: string;
  link: string;
  lat: number | null;
  lng: number | null;
}

function MonumentMarker({ monument, onClick }: { monument: Monument, onClick: (monument: Monument) => void }) {
  const popupRef = useRef(null);
  const map = useMap();

  return (
    <Marker
      position={[monument.lat!, monument.lng!]}
      eventHandlers={{
        click: () => onClick(monument),
        mouseover: () => {
          if (popupRef.current) {
            // @ts-ignore
            popupRef.current.openOn(map);
          }
        },
        mouseout: () => {
          if (popupRef.current) {
            // @ts-ignore
            popupRef.current._close();
          }
        },
      }}
    >
      <Popup ref={popupRef}>
        <div>
          <h3>{monument.lage}</h3>
        </div>
      </Popup>
    </Marker>
  );
}

function MonumentDetailsPanel({ monument, onClose }: { monument: Monument, onClose: () => void }) {
  return (
    <div style={{ flex: 1, background: '#fff', borderLeft: '1px solid #ccc', padding: '2rem', overflowY: 'auto', height: '100%', minWidth: 300 }}>
      <button style={{ float: 'right', fontSize: '1.2rem' }} onClick={onClose}>&times;</button>
      <h2>{monument.lage}</h2>
      <p><strong>Art:</strong> {monument.denkmalart}</p>
      <p><strong>Denkmalnummer:</strong> {monument.denkmalnummer}</p>
      <a href={monument.link} target="_blank" rel="noopener noreferrer">
        More details
      </a>
    </div>
  );
}

function App() {
  const [monuments, setMonuments] = useState<Monument[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedMonument, setSelectedMonument] = useState<Monument | null>(null);

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
    <div style={{ display: 'flex', height: '100vh', width: '100vw', margin: 0, padding: 0, overflow: 'hidden' }}>
      <div style={{ flex: 2, transition: 'flex 0.3s', height: '100%' }}>
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
              return <MonumentMarker key={monument.id} monument={monument} onClick={setSelectedMonument} />;
            }
            return null;
          })}
        </MapContainer>
      </div>
      {selectedMonument && (
        <MonumentDetailsPanel monument={selectedMonument} onClose={() => setSelectedMonument(null)} />
      )}
    </div>
  );
}

export default App;

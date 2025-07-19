import { useLoader, Canvas } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Suspense, Component } from 'react';
import type { ErrorInfo } from 'react';
import { GLTFLoader } from 'three/examples/jsm/Addons.js';

interface ModelViewerProps {
    modelPath: string;
    scale?: number;
}


function Model({ modelPath, scale = 1 }: ModelViewerProps) {
    // useLoader will automatically handle loading and caching
    const gltf = useLoader(GLTFLoader, modelPath);

    return (
        <primitive
            object={gltf.scene}
            scale={scale}
            position={[0, 0, 0]}
        />
    );
}

function LoadingFallback() {
    return (
        <mesh>
            <boxGeometry args={[1, 1, 1]} />
            <meshStandardMaterial color="gray" />
        </mesh>
    );
}

export default function ModelViewer({ modelPath, scale = 1 }: ModelViewerProps) {
    return (
        <div style={{ width: '100%', height: '100%', position: 'relative' }}>
            <ErrorBoundary>
                <Canvas
                    camera={{ position: [0, 0, 5], fov: 45 }}
                    style={{ background: '#f0f0f0' }}
                >
                    {/* Ambient light for overall illumination */}
                    <ambientLight intensity={0.5} />

                    {/* Front lights */}
                    <directionalLight position={[5, 5, 5]} intensity={0.5} /> {/* Front Right */}
                    <directionalLight position={[-5, 5, 5]} intensity={0.5} /> {/* Front Left */}

                    {/* Back lights */}
                    <directionalLight position={[5, 5, -5]} intensity={0.5} /> {/* Back Right */}
                    <directionalLight position={[-5, 5, -5]} intensity={0.5} /> {/* Back Left */}

                    <Suspense fallback={<LoadingFallback />}>
                        <Model modelPath={modelPath} scale={scale} />
                    </Suspense>
                    <OrbitControls />
                </Canvas>
            </ErrorBoundary>
        </div>
    );
}


// Error boundary component
class ErrorBoundary extends Component<{ children: React.ReactNode }, { hasError: boolean; error: string | null }> {
    constructor(props: { children: React.ReactNode }) {
        super(props);
        this.state = { hasError: false, error: null };
    }

    static getDerivedStateFromError(error: Error) {
        return { hasError: true, error: error.message };
    }

    componentDidCatch(error: Error, errorInfo: ErrorInfo) {
        console.error('Model loading error:', error);
        console.error('Error info:', errorInfo);
    }

    render() {
        if (this.state.hasError) {
            return (
                <div style={{
                    position: 'absolute',
                    top: '50%',
                    left: '50%',
                    transform: 'translate(-50%, -50%)',
                    background: 'rgba(255, 0, 0, 0.1)',
                    padding: '1rem',
                    borderRadius: '4px',
                    color: 'red'
                }}>
                    Error loading model: {this.state.error}
                </div>
            );
        }

        return this.props.children;
    }
}
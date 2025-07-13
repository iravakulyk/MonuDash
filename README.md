# MonuDash - Historical Monuments Explorer

An open-source university project developed at RWTH Aachen University for visualizing and exploring historical monuments through interactive maps and 3D models.

## About

MonuDash is an academic project that combines open data from the City of Aachen with student-created 3D models to create an accessible platform for exploring architectural heritage. The project emphasizes open-source technologies and open data to promote transparency and collaboration in cultural heritage documentation.

## Features

- Interactive open-source map displaying historical monuments
- Integration with open data from Aachen GeoServer
- 3D model viewer featuring models created by RWTH Aachen University students
- Responsive and modern user interface
- Automated data enrichment pipeline

## Project Structure

```
MonuDash/
├── backend/           # FastAPI backend server
│   ├── main.py       # Main application entry point
│   └── scripts/      # Data enrichment scripts
├── frontend/         # React frontend application
└── resources/        # Data resources and 3D models
    ├── denkmal_prodenkmal_csv.csv  # Raw monument data
    └── StudentWorks/               # 3D models created by RWTH students
```

## Data Sources

- Primary data source: [Aachen GeoPortal](https://geoportal.aachen.de/) (Open Data)
- Monument details: Aachen GeoServer API (Open Data)
- 3D Models: Created by students of RWTH Aachen University as part of their coursework

## Open Source Technology Stack

### Backend
- FastAPI: Modern, open-source Python web framework
- Python scripts for data enrichment
- Data processing and GeoJSON handling using open-source libraries
- SQLite for local development, PostgreSQL for production

### Frontend
- React: Open-source JavaScript library for user interfaces
- Three.js: Open-source 3D graphics library
- Leaflet: Open-source JavaScript library for interactive maps
- OpenStreetMap as the base map provider

## 3D Models

The 3D models in this project were created by students of RWTH Aachen University. Each model represents a historical monument in Aachen and was carefully crafted as part of their academic work. The models are available in open formats including .blend (Blender) and .glb (GL Binary).

### Attribution

All 3D models are credited to their respective student creators from RWTH Aachen University. Each model in the StudentWorks directory includes:
- Student attribution
- Creation date
- Source files (.blend)
- Optimized web format (.glb)
- Reference images
- Documentation

### Usage Rights

These 3D models are released under an open-source license (specify license) with attribution requirements:
1. The original student creator
2. RWTH Aachen University
3. The MonuDash project

## Getting Started

### Prerequisites
- Node.js and npm for frontend development
- Python 3.12 for backend development
- uv for Python dependency management (install with: `curl -LsSf https://astral.sh/uv/install.sh | bash`)
- Git LFS (Large File Storage) for handling 3D models and large assets

Note: This repository uses Git LFS to manage large files like 3D models (.blend, .glb) and images. Make sure to install Git LFS before cloning the repository to properly download all assets.

### Git LFS Setup
```bash
git lfs install
```

## Academic Context

This project is developed as part of the academic curriculum at RWTH Aachen University. It serves as both a practical implementation of open-source development practices and a contribution to the digital documentation of cultural heritage.

### Educational Goals
- Practical experience with open-source development
- Working with real-world open data
- Contributing to cultural heritage documentation
- Collaborative software development in an academic context

## Contributing

This is an open-source university project and contributions are welcome! 

## License

This project is released under [specify open-source license] to ensure it remains freely available for academic and public use.

## Acknowledgments

- RWTH Aachen University for project supervision and support
- City of Aachen for providing open access to monument data
- RWTH Aachen University students for creating the 3D models
- Open-source community for providing the tools and libraries used in this project

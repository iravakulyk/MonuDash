.PHONY: frontend backend install

# Start the frontend development server
frontend:
	cd frontend && npm run dev

# Start the backend server
backend:
	cd backend && uv run python -m monudash.main

# Install dependencies
install:
	cd frontend && npm install
	cd backend && uv sync
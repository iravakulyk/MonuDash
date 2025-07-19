.PHONY: frontend backend all

# Start both frontend and backend
all: frontend backend

# Start the frontend development server
frontend:
	cd frontend && npm run dev

# Start the backend server
backend:
	cd backend && uv run python main.py

# Install dependencies
install:
	cd frontend && npm install
	cd backend && pip install -e .

.DEFAULT_GOAL := all

# Frontend build stage
FROM node:latest AS frontend-build

WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm install
COPY frontend .
RUN npm run build

# Backend stage
FROM python:latest AS backend-build

# Set the working directory
WORKDIR /app

# Install system dependencies (if needed)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy pyproject.toml and lock file first for dependency install
COPY backend/pyproject.toml backend/uv.lock ./

# Install dependencies using uv
ENV UV_LINK_MODE=copy
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync

# Copy the rest of the backend code
COPY backend/ .

# Copy frontend build output to /app/static
COPY --from=frontend-build /frontend/dist /app/static
COPY resources/monuments.db /app/resources/

# Set backend environment variables
ENV STATIC_DIR=/app/static \
    RESOURCES_DIR=/app/resources

# Expose port (adjust if your app uses a different port)
EXPOSE 8000

# Default command to run the backend with uvicorn (ASGI app in main.py)
CMD ["uv", "run", "uvicorn", "monudash.main:app", "--host", "0.0.0.0", "--port", "8000"] 
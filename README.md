<div align="center">

# Music-Service API

<p>
  RESTful backend for managing audio content using <strong>FastAPI</strong>.<br>
  Part of the <strong>Music-Center</strong> course project.
</p>

<p>
  <a href="#about-project">
    <img src="https://img.shields.io/badge/status-active-brightgreen.svg" alt="Status">
  </a>
  <a href="#tech-stack">
    <img src="https://img.shields.io/badge/FastAPI-0.110+-green.svg" alt="FastAPI">
  </a>
  <a href="#license">
    <img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="License">
  </a>
  <a href="#installation">
    <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python">
  </a>
</p>

---

</div>

## Contents

- [About Project](#about-project)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
  - [Installation](#installation)
  - [Docker Setup](#docker-setup)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Server](#usage)
  - [API Documentation](#api-documentation)
- [Development](#development)
  - [Project Structure](#project-structure)
  - [Database Schema](#database-schema)
  - [Features](#features)
- [License](#license)

## 📖 About Project

**Music-Service** is a REST API server implemented using the FastAPI framework, designed for programmatic management of a catalog of musical compositions and performers. The service provides functionality for uploading, storing, and streaming audio files, as well as for organizing, filtering, and searching musical content.

This repository contains the backend implementation of the **Music-Center** course project and serves as the backend component for interacting with the music library via an HTTP interface.

## Tech Stack

| Layer        | Technology                                                                           |
| ------------ | ------------------------------------------------------------------------------------ |
| Language     | ![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white) |
| Framework    | ![FastAPI](https://img.shields.io/badge/FastAPI-%3E=0.110-green?logo=fastapi)        |
| Web Server   | ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-blueviolet)                     |
| ORM / Models | SQLAlchemy, Pydantic                                                                 |
| Database     | MySQL                                                                                |
| Media        | Local file storage (audio)                                                           |

See `requirements.txt` for a complete list of dependencies.

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/gloomforge/Music-Server.git
cd Music-Server
```

2. Create a virtual environment:

```bash
python -m venv .venv
python3 -m venv .venv # on Unix/maxOS
```

3. Activate the virtual environment:

- macOS/Linux:

```bash
source .venv/bin/activate
```

- Windows (PowerShell):

```bash
.venv\Scripts\Aptivate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Configure environment variables:

```bash
cp .env.example .env
# Edit .env with your settings (e.g., DATABASE_URL)
```

### Docker Setup

1. Make sure you have Docker and Docker Compose installed on your system

2. Build and run the containers:

```bash
# Build and start all services in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

The docker-compose.yml includes:

- FastAPI application service (auto-reload enabled for development)
- MySQL 8.0 database service
- Volumes for persistent MySQL data storage
- Hot-reload configuration for local development

Default configuration:

Services:

- Backend API: http://localhost:4200 (with hot-reload)
- MySQL: localhost:3306

Environment variables:

- MySQL Database: music_catalog
- MySQL User: gloomforge
- MySQL Password: gloomforge

Volume mounts:

- MySQL data: persistent volume for database files
- Application code: mounted for live development

### Configuration

The application can be configured using environment variables or `.env` file:

```env
# Database Configuration
DATABASE_URL=mysql+aiomysql://gloomforge:gloomforge@localhost:3306/music_catalog
```

## Usage

1. Start the server:

```bash
# Local development
uvicorn main:app --reload

# Production
uvicorn main:app --host 0.0.0.0 --port 4200
```

2. Access the API documentation:

- Swagger UI: http://localhost:4200/docs
- ReDoc: http://localhost:4200/redoc

## Development Structure

```
Music-Server/
├── app/                    # Application initialization
│   ├── config.py          # Configuration management
│   ├── events.py          # Startup/shutdown events
│   └── routes.py          # Route registration
├── src/                    # Source code
│   ├── albums/            # Albums module
│   ├── artists/           # Artists module
│   ├── auth/              # Authentication module
│   ├── db/                # Database configuration
│   ├── genres/            # Genres module
│   ├── media_files/       # File handling module
│   └── tracks/            # Tracks module
├── docker-compose.yml     # Docker compose configuration
├── Dockerfile             # Docker build instructions
├── main.py               # Application entry point
└── requirements.txt      # Python dependencies
```

### API Documentation

Comprehensive API documentation is available through:

- Interactive Swagger UI at `/docs`
- ReDoc documentation at `/redoc`

### Features

- User authentication and authorization
- CRUD operations for tracks, artists, albums, and genres
- File upload and streaming for audio files
- Search and filtering capabilities
- Docker support for easy deployment

### Database Schema

The service uses MySQL with the following main entities:

- Users
- Artists
- Albums
- Tracks
- Genres
- Media Files

## License

This project is licensed under the MIT License. See LICENSE for details.

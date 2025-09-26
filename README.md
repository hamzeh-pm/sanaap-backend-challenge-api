# SANAAP Backend Challenge API

A Django REST Framework API with role-based access control (RBAC), secure document management, and authentication system built for the SANAAP technical interview challenge.

## Features

- **Role-Based Access Control (RBAC)** - Admin, Editor, and Viewer roles with granular permissions
- **JWT Authentication** - Secure token-based authentication with refresh tokens
- **Document Management** - Secure file upload, storage, and access control
- **RESTful API** - CRUD operations with filtering, searching, and pagination
- **API Documentation** - Interactive Swagger/OpenAPI documentation
- **Docker Support** - Containerized development and deployment
- **Testing** - Unit tests with pytest
- **Security Features** - Protected file serving, permission-based access
- **Secure File Storage** - MinIO S3-compatible storage with private bucket access

## Table of Contents

- [Quick Start](#quick-start)
- [Development Setup (Test Environment)](#development-setup)
- [Environment Configuration](#environment-configuration)
- [Authentication & Authorization](#authentication--authorization)
- [Testing](#testing)
- [API Endpoints](#api-endpoints)
- [Production](#production)

## Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### 1. Clone Repository
```bash
git clone https://github.com/hamzeh-pm/sanaap-backend-challenge-api.git
cd sanaap-backend-challenge-api
```

### 2. Start with docker
```bash
# Build and start all services
docker compose -f docker-compose.local.yml up --build

# Or run in background
docker compose -f docker-compose.local.yml up --build -d
```

### 3. Create Super User
```bash
# Method 1: Using management command
docker compose -f docker-compose.local.yml exec django python manage.py create_superuser \
  --username admin \
  --email admin@example.com \
  --password securepassword

# Method 2: Environment variables (see Environment Configuration)
```

### 4. Create Initial Admin User
user django admin site to create first Admin user (user with role admin)

### 4. Access the API

- API Base URL: http://localhost:8001/api/
- API Documentation: http://localhost:8001/api/docs/
- Admin Panel: http://localhost:8001/admin/

## Development Setup (Test Environment)

### Option 1: Docker Development
```bash
# Start development environment
docker compose -f docker-compose.local.yml up --build

# View logs
docker compose -f docker-compose.local.yml logs -f django

# Execute commands in container
docker compose -f docker-compose.local.yml exec django python manage.py shell

# Stop services
docker compose -f docker-compose.local.yml down
```

#### Services:
- Django application (Port 8001)
- PostgreSQL database (Port 5433)
- Redis cache (Port 6380)
- MinIO storage (Port 9000, Console: 9001)
- Celery worker

### Option 2: Local Development
**Prerequisites:** Python 3.13+, PostgreSQL, Redis
```bash
# Install dependencies
uv sync

# Set environment
export USE_DOCKER=False

# Run migrations
python manage.py migrate

# Create superuser
python manage.py create_superuser --username [username] --password [password] --email [email(optional)]

# Start development server
python manage.py runserver
```

#### Local Access:
- API: http://localhost:8000/api/
- Documentation: http://localhost:8000/api/docs/
- MinIO Console: http://localhost:9001

## Environment Configuration
### environment file Structure
```bash
.envs/
├── .docker/          # Docker development
│   ├── .django.env
|   ├── .postgres.env
│   └── .minio.env
|
└── .local/           # Local development  
    ├── .django.env
    ├── .postgres.env
    └── .minio.env
```
### Docker Environment (.django.env)
```bash
# Django
USE_DOCKER=True
DJANGO_SECRET_KEY=secure_secret_key

# Superuser Configuration
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@sanaap.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password

# Redis
REDIS_URL=redis://redis:6379/0
```

### Docker Environment (.postgres.env)
```bash
# PostgreSQL Configuration
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=sanaap_db
POSTGRES_USER=sanaap_user
POSTGRES_PASSWORD=your_db_password
DATABASE_URL=postgres://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}
```

### MinIO Environment (.minio.env)
```bash
# MinIO Server Configuration
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=miniopassword

# Django S3 Configuration
MINIO_ACCESS_KEY_ID=minioadmin
MINIO_SECRET_ACCESS_KEY=miniopassword
MINIO_STORAGE_BUCKET_NAME=django-media
MINIO_S3_ENDPOINT_URL=http://minio:9000
```

### Local Environment (.django.env + .postgres.env + .minio.env)
```bash
# Django Settings
USE_DOCKER=False
DJANGO_SECRET_KEY=secure_secret_key

# Database (connects to Docker PostgreSQL)
DATABASE_URL=postgres://sanaap_user:your_db_password@127.0.0.1:5432/sanaap_db

# Redis (connects to Docker Redis)
REDIS_URL=redis://127.0.0.1:6380/0

# Superuser Configuration
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@sanaap.com
DJANGO_SUPERUSER_PASSWORD=your_secure_password

# Django S3 Configuration
MINIO_ACCESS_KEY_ID=minioadmin
MINIO_SECRET_ACCESS_KEY=miniopassword
MINIO_STORAGE_BUCKET_NAME=django-media
MINIO_S3_ENDPOINT_URL=http://127.0.0.1:9000
```

## Authentication & Authorization
### User Roles

| Role | Permissions |
| :--- | :--- |
| Admin | Full CRUD on All Resources |
| Editor | Create Update View documents |
| Viewer | View Documents |

### Authentication Flow
#### 1. Obtain Token
```bash
POST /api/token/
{
  "username": "admin",
  "password": "securepassword"
}
```

#### 2. Use Token
```bash
Authorization: Bearer <access_token>
```

#### 3. Refresh Token
```bash
POST /api/token/refresh/
{
  "refresh": "<refresh_token>"
}
```

## Testing
### Run Tests
```bash
# With Docker
docker compose -f docker-compose.local.yml exec django pytest

# Locally
pytest

# With coverage
pytest --cov=sanaap_backend_challenge_api

# Specific test file
pytest sanaap_backend_challenge_api/documents/tests/
```

### Test Structure
```bash
tests/
├── conftest.py                    # Test fixtures
├── accounts/
│   ├── test_permissions.py
│   ├── test_role_views.py
│   └── test_user_views.py
└── documents/
    ├── test_document_service.py
    ├── test_document_views.py
    └── test_secure_file_access.py
```

## API Endpoints
### Authentication
```bash
POST   /api/token/                 # Obtain JWT token
POST   /api/token/refresh/         # Refresh JWT token
```

### User Management
```bash
GET    /api/accounts/roles/        # List available roles (Admin only)
GET    /api/accounts/users/        # List users (Admin only)
GET    /api/accounts/users/{id}/   # Get user details (Admin only)
POST   /api/accounts/users/        # Create user (Admin only)
PATCH  /api/accounts/users/{id}/   # Update user (Admin only)
DELETE /api/accounts/users/{id}/   # Delete user (Admin only)
```

### Document Management
```bash
GET    /api/documents/             # List documents (Admin/Editor/Viewer)
POST   /api/documents/             # Upload document (Admin/Editor)
GET    /api/documents/{id}/        # Get document details (Admin/Editor/Viewer)
PATCH  /api/documents/{id}/        # Update document (Admin/Editor)
DELETE /api/documents/{id}/        # Delete document (Admin Only)
GET    /api/documents/files/{id}/  # Download file (Admin/Editor/Viewer)
```

# Production
> !note: the production need file is not setup due to nature of the project
- docker-compose.production.yml
- .envs/.production/.django
- .envs/.production/.postgres
- docker/production/Dockerfile
- docker/production/entrypoint
- docker/production/start
- docker/production/start-celeryworker
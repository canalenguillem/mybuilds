# Docker & Deployment Specifications

## Docker Architecture

### Container Services

#### 1. Frontend Service (Vite + React)
**Image**: `submittal-automation-system/frontend:latest`

**Build Context**: `./frontend`

**Exposed Port**: 3000 (Vite dev) or 80 (nginx production)

**Volumes**:
- `./frontend/src:/app/src` (development - hot reload)
- `./frontend/public:/app/public`

**Environment Variables**:
- `VITE_API_URL=http://backend:8000/api`
- `VITE_APP_NAME=Submittal Automation System`
- `NODE_ENV=development|production`

**Dependencies**: None (standalone)

---

#### 2. Backend Service (FastAPI + Uvicorn)
**Image**: `submittal-automation-system/backend:latest`

**Build Context**: `./backend`

**Exposed Port**: 8000

**Volumes**:
- `./backend/app:/app/app` (development)
- `./volumes/documents:/app/data/documents` (uploaded files)
- `./volumes/generated_pdfs:/app/data/generated_pdfs` (generated submittals)
- `./volumes/backups:/app/data/backups` (database backups)

**Environment Variables**:
- `DATABASE_URL=mysql+pymysql://user:password@mariadb:3306/submittal_db`
- `MONGODB_URL=mongodb://mongodb:27017/submittal_db`
- `REDIS_URL=redis://redis:6379/0`
- `CELERY_BROKER_URL=redis://redis:6379/1`
- `OPENAI_API_KEY=<your-key>`
- `AWS_ACCESS_KEY_ID=<optional>`
- `AWS_SECRET_ACCESS_KEY=<optional>`
- `JWT_SECRET_KEY=<strong-random-key>`
- `ENVIRONMENT=development|production`

**Healthcheck**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1
```

**Dependencies**: mariadb, mongodb, redis

---

#### 3. MariaDB Service
**Image**: `mariadb:11.3-noble`

**Exposed Port**: 3306

**Volumes**:
- `./volumes/mariadb:/var/lib/mysql` (data persistence)
- `./backend/app/database/migrations/init.sql:/docker-entrypoint-initdb.d/01-init.sql` (initialization)

**Environment Variables**:
- `MARIADB_ROOT_PASSWORD=<strong-password>`
- `MARIADB_DATABASE=submittal_db`
- `MARIADB_USER=submittal_user`
- `MARIADB_PASSWORD=<strong-password>`
- `MARIADB_ALLOW_EMPTY_ROOT_PASSWORD=0`

**Healthcheck**:
```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD mariadb-admin -u submittal_user -p<password> ping || exit 1
```

**Dependencies**: None

---

#### 4. MongoDB Service
**Image**: `mongo:7.0`

**Exposed Port**: 27017

**Volumes**:
- `./volumes/mongodb:/data/db` (data persistence)
- `./volumes/mongodb/config:/data/configdb` (config)

**Environment Variables**:
- `MONGO_INITDB_ROOT_USERNAME=admin`
- `MONGO_INITDB_ROOT_PASSWORD=<strong-password>`
- `MONGO_INITDB_DATABASE=submittal_db`

**Healthcheck**:
```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --start-period=30s --retries=3 \
  CMD mongosh --eval 'db.adminCommand("ping")' || exit 1
```

**Dependencies**: None

---

#### 5. Redis Service
**Image**: `redis:7-alpine`

**Exposed Port**: 6379

**Volumes**:
- `./volumes/redis:/data` (persistence with AOF)

**Command**:
```
redis-server --appendonly yes --requirepass <strong-password>
```

**Healthcheck**:
```dockerfile
HEALTHCHECK --interval=10s --timeout=5s --start-period=20s --retries=3 \
  CMD redis-cli --no-auth-warning ping || exit 1
```

**Dependencies**: None

---

#### 6. Celery Worker Service
**Image**: `submittal-automation-system/backend:latest` (same as backend)

**Command**: `celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4`

**Volumes**:
- `./backend/app:/app/app` (development)
- `./volumes/generated_pdfs:/app/data/generated_pdfs`
- `./volumes/backups:/app/data/backups`

**Environment Variables**:
- Same as backend service
- `CELERY_WORKER_ID=worker-1`

**Healthcheck**: None (workers don't expose HTTP)

**Dependencies**: mariadb, mongodb, redis, backend

---

#### 7. Nginx Reverse Proxy
**Image**: `nginx:alpine`

**Build Context**: `./nginx`

**Exposed Ports**: 
- 80 (HTTP)
- 443 (HTTPS)

**Volumes**:
- `./nginx/nginx.conf:/etc/nginx/nginx.conf:ro`
- `./nginx/conf.d:/etc/nginx/conf.d:ro`
- `./nginx/ssl:/etc/nginx/ssl:ro` (SSL certificates)

**Environment Variables**: None (static config)

**Healthcheck**:
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/health || exit 1
```

**Dependencies**: backend, frontend

---

#### 8. Optional: n8n Service
**Image**: `n8nio/n8n:latest`

**Exposed Port**: 5678

**Volumes**:
- `./volumes/n8n:/home/node/.n8n`

**Environment Variables**:
- `N8N_HOST=n8n`
- `N8N_PORT=5678`
- `N8N_PROTOCOL=http`
- `WEBHOOK_URL=http://n8n:5678`
- `DATABASE_TYPE=postgres`
- `DATABASE_URL=postgres://user:pass@postgres:5432/n8n`

**Dependencies**: postgres (optional, for n8n metadata storage)

---

## Docker Compose Configuration

### Development Setup (docker-compose.yml)

```yaml
version: '3.9'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: development
    ports:
      - "3000:3000"
    volumes:
      - ./frontend/src:/app/src
      - ./frontend/public:/app/public
      - /app/node_modules
    environment:
      - VITE_API_URL=http://localhost:8000/api
      - NODE_ENV=development
    networks:
      - submittal-network
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    ports:
      - "8000:8000"
    volumes:
      - ./backend/app:/app/app
      - ./volumes/documents:/app/data/documents
      - ./volumes/generated_pdfs:/app/data/generated_pdfs
    environment:
      - DATABASE_URL=mysql+pymysql://submittal_user:password@mariadb:3306/submittal_db
      - MONGODB_URL=mongodb://admin:password@mongodb:27017/submittal_db?authSource=admin
      - REDIS_URL=redis://:password@redis:6379/0
      - CELERY_BROKER_URL=redis://:password@redis:6379/1
      - JWT_SECRET_KEY=dev-secret-key-change-in-production
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ENVIRONMENT=development
      - LOG_LEVEL=DEBUG
    depends_on:
      mariadb:
        condition: service_healthy
      mongodb:
        condition: service_healthy
      redis:
        condition: service_healthy
    networks:
      - submittal-network
    restart: unless-stopped

  mariadb:
    image: mariadb:11.3-noble
    ports:
      - "3306:3306"
    volumes:
      - ./volumes/mariadb:/var/lib/mysql
    environment:
      - MARIADB_ROOT_PASSWORD=rootpassword
      - MARIADB_DATABASE=submittal_db
      - MARIADB_USER=submittal_user
      - MARIADB_PASSWORD=password
    healthcheck:
      test: ["CMD", "mariadb-admin", "-u", "submittal_user", "-ppassword", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - submittal-network
    restart: unless-stopped

  mongodb:
    image: mongo:7.0
    ports:
      - "27017:27017"
    volumes:
      - ./volumes/mongodb:/data/db
      - ./volumes/mongodb/config:/data/configdb
    environment:
      - MONGO_INITDB_ROOT_USERNAME=admin
      - MONGO_INITDB_ROOT_PASSWORD=password
      - MONGO_INITDB_DATABASE=submittal_db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - submittal-network
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - ./volumes/redis:/data
    command: redis-server --appendonly yes --requirepass password
    healthcheck:
      test: ["CMD", "redis-cli", "--no-auth-warning", "ping"]
      interval: 10s
      timeout: 5s
      retries: 3
    networks:
      - submittal-network
    restart: unless-stopped

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
      target: development
    command: celery -A app.tasks.celery_app worker --loglevel=info --concurrency=4
    volumes:
      - ./backend/app:/app/app
      - ./volumes/generated_pdfs:/app/data/generated_pdfs
    environment:
      - DATABASE_URL=mysql+pymysql://submittal_user:password@mariadb:3306/submittal_db
      - MONGODB_URL=mongodb://admin:password@mongodb:27017/submittal_db?authSource=admin
      - REDIS_URL=redis://:password@redis:6379/0
      - CELERY_BROKER_URL=redis://:password@redis:6379/1
      - ENVIRONMENT=development
    depends_on:
      - mariadb
      - mongodb
      - redis
      - backend
    networks:
      - submittal-network
    restart: unless-stopped

networks:
  submittal-network:
    driver: bridge
```

### Production Setup (docker-compose.prod.yml)

Key differences:
- Nginx reverse proxy in front
- No hot-reload
- Optimized builds
- Resource limits
- No exposed database ports (only internal)
- Environment-based configuration
- Health checks configured
- Logging configuration
- Auto-restart policies

---

## Dockerfile Best Practices

### Backend Dockerfile (Multi-stage)

```dockerfile
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Development
FROM python:3.11-slim as development

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Stage 3: Production
FROM python:3.11-slim as production

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

COPY . .

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app

USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD curl -f http://localhost:8000/api/v1/health || exit 1

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Frontend Dockerfile (Multi-stage)

```dockerfile
# Stage 1: Builder
FROM node:20-alpine as builder

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

RUN npm run build

# Stage 2: Development
FROM node:20-alpine as development

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 3000

CMD ["npm", "run", "dev"]

# Stage 3: Production
FROM nginx:alpine as production

COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 80

HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
  CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
```

---

## Environment Configuration

### .env.example (Root Directory)

```bash
# Application
APP_NAME=Submittal Automation System
APP_ENVIRONMENT=development
DEBUG=true

# Database - MariaDB
MARIADB_ROOT_PASSWORD=rootpassword
MARIADB_DATABASE=submittal_db
MARIADB_USER=submittal_user
MARIADB_PASSWORD=securepassword
MARIADB_PORT=3306

# Database - MongoDB
MONGODB_ADMIN_USER=admin
MONGODB_ADMIN_PASSWORD=securepassword
MONGODB_DATABASE=submittal_db
MONGODB_PORT=27017

# Cache - Redis
REDIS_PASSWORD=securepassword
REDIS_PORT=6379

# Backend
BACKEND_PORT=8000
DATABASE_URL=mysql+pymysql://submittal_user:securepassword@mariadb:3306/submittal_db
MONGODB_URL=mongodb://admin:securepassword@mongodb:27017/submittal_db?authSource=admin
REDIS_URL=redis://:securepassword@redis:6379/0
CELERY_BROKER_URL=redis://:securepassword@redis:6379/1

# JWT
JWT_SECRET_KEY=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# AI/LLM Integration
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4
OPENAI_TIMEOUT=60

# AWS (Optional)
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_REGION=us-east-1
S3_BUCKET_NAME=

# Email (Optional)
SMTP_SERVER=
SMTP_PORT=587
SMTP_USERNAME=
SMTP_PASSWORD=
SMTP_FROM_EMAIL=

# Frontend
VITE_API_URL=http://localhost:8000/api
VITE_APP_NAME=Submittal Automation System
VITE_LOG_LEVEL=debug

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Security
CORS_ORIGINS=http://localhost:3000,http://localhost
ALLOWED_HOSTS=localhost,127.0.0.1

# File Storage
FILE_STORAGE_TYPE=local # local, s3, minio
FILE_MAX_SIZE_MB=50
ALLOWED_FILE_TYPES=pdf,docx,xlsx,pptx,txt,png,jpg

# n8n (Optional)
N8N_HOST=http://n8n:5678
N8N_API_KEY=
```

---

## Deployment Instructions

### Local Development

1. **Clone repository**
   ```bash
   git clone <repo-url>
   cd submittal-automation-system
   ```

2. **Create environment file**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

3. **Build and start services**
   ```bash
   docker-compose up -d
   ```

4. **Initialize database**
   ```bash
   docker-compose exec backend python scripts/init_db.py
   docker-compose exec backend python scripts/seed_data.py
   ```

5. **Access application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs
   - MongoDB Express: http://localhost:8081 (if included)

### Production Deployment

1. **Prepare environment**
   ```bash
   cp .env.example .env.production
   # Edit with production values
   export COMPOSE_FILE=docker-compose.prod.yml
   ```

2. **Build images**
   ```bash
   docker-compose build --no-cache
   ```

3. **Deploy**
   ```bash
   docker-compose up -d
   ```

4. **Run migrations**
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

5. **Configure SSL/TLS**
   - Place certificates in `./nginx/ssl/`
   - Update nginx configuration

6. **Setup monitoring** (optional)
   - Configure log aggregation
   - Setup health monitoring
   - Configure alerts

---

## Health Checks

All critical services have healthchecks configured:

```bash
# Check service health
docker-compose ps

# Manual health check
curl http://localhost:8000/api/v1/health
curl http://localhost:3000/health
```

---

## Backup & Recovery

### Backup

```bash
./scripts/backup.sh
```

Creates backups of:
- MariaDB database
- MongoDB database
- Uploaded documents
- Generated PDFs

### Recovery

```bash
./scripts/restore.sh <backup-date>
```

---

## Scaling Considerations

### Horizontal Scaling
- Multiple Celery workers: `docker-compose up -d --scale celery_worker=3`
- Load balancer for backend instances
- Database replication (MariaDB primary-replica)

### Resource Limits (Production)
```yaml
services:
  backend:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```


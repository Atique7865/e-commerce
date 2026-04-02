# TalentHeart Limited — Web Application

> Production-ready Django digital-agency platform with Docker, Nginx, Redis, PostgreSQL, and Kubernetes support.

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Django](https://img.shields.io/badge/Django-4.2-green)](https://djangoproject.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://postgresql.org)
[![Redis](https://img.shields.io/badge/Redis-7-red)](https://redis.io)
[![Docker](https://img.shields.io/badge/Docker-ready-blue)](https://docker.com)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-manifests-blue)](https://kubernetes.io)

---

## Table of Contents

1. [Features](#features)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Local Development](#local-development)
5. [Docker Setup](#docker-setup)
6. [Dockerize Without Docker Compose](#dockerize-without-docker-compose)
7. [Kubernetes Deployment](#kubernetes-deployment)
8. [Environment Variables](#environment-variables)
9. [Admin Panel](#admin-panel)

---

## Features

| Feature | Details |
|---------|---------|
| 🔐 Authentication | Sign-up, login, logout, extended user profiles |
| 📊 Dashboard | Client overview with order stats |
| 🛠 Services | Digital Marketing, Web Development, DevOps catalogue |
| 🛒 Orders | Full booking system (pending → in progress → completed) |
| 📧 Contact Form | Saves to DB + email notification via SMTP |
| ⚡ Redis | Cache backend + session storage |
| 🐘 PostgreSQL | Production-grade relational database |
| 🌐 Nginx | Static file serving + reverse proxy |
| ☸️ Kubernetes | Full manifests with HPA, Ingress, TLS, resource limits |
| 🐳 Docker | Multi-stage build, dev & prod Compose files |

---

## Architecture

```
Internet
   │
   ▼
┌─────────────────────────────────────────────────┐
│  Nginx (port 80/443)                            │
│   ├── /static/*  → staticfiles volume (direct) │
│   ├── /media/*   → media volume    (direct)    │
│   └── /*         → Gunicorn :8000  (proxy)     │
└─────────────────────────────────────────────────┘
                        │
                        ▼
             ┌──────────────────┐
             │  Django/Gunicorn │
             │  (web container) │
             └──────────────────┘
               │              │
               ▼              ▼
    ┌──────────────┐  ┌──────────────┐
    │  PostgreSQL  │  │    Redis     │
    │  (database)  │  │  (cache +    │
    │              │  │   sessions)  │
    └──────────────┘  └──────────────┘
```

---

## Project Structure

```
talentheart-app/
├── Dockerfile                 # Multi-stage production image
├── docker-compose.yml         # Dev stack (web + db + redis + nginx)
├── docker-compose.prod.yml    # Production overrides
├── .dockerignore
├── .env.example               # Environment variable template
├── manage.py
├── requirements.txt
│
├── talentheart/               # Django project config
│   ├── settings.py            # All settings (env-driven)
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── accounts/                  # Auth + user profiles
├── services/                  # Service catalogue + seeder command
├── orders/                    # Order/booking system
├── contact/                   # Contact form + email
├── dashboard/                 # Client dashboard
│
├── templates/                 # Bootstrap 5 HTML templates
├── static/                    # CSS + JS source
├── media/                     # User uploads (runtime)
│
├── nginx/
│   ├── nginx.conf             # Global Nginx config
│   └── conf.d/
│       ├── talentheart.conf   # Virtual host (proxy + static serving)
│       └── proxy_params.conf  # Shared proxy headers
│
├── docker/
│   └── entrypoint.sh          # Container startup script
│
└── k8s/                       # Kubernetes manifests
    ├── namespace.yaml
    ├── configmap.yaml
    ├── secret.yaml
    ├── ingress.yaml
    ├── postgres/
    │   ├── statefulset.yaml
    │   ├── service.yaml
    │   └── pvc.yaml
    ├── redis/
    │   ├── deployment.yaml
    │   └── service.yaml
    ├── web/
    │   ├── deployment.yaml
    │   ├── service.yaml
    │   ├── hpa.yaml
    │   └── pvcs.yaml
    └── nginx/
        ├── deployment.yaml
        ├── service.yaml
        └── configmap.yaml
```

---

## Local Development

### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

### Setup

```bash
# 1. Clone the repository
git clone https://github.com/your-org/talentheart.git
cd talentheart

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
cp .env.example .env
# Edit .env — set DB credentials, SECRET_KEY, email settings
```

```bash
# 5. Create the PostgreSQL database
psql -U postgres -c "CREATE DATABASE talentheart_db;"
psql -U postgres -c "CREATE USER talentheart WITH PASSWORD 'your_password';"
psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE talentheart_db TO talentheart;"

# 6. Apply migrations
python manage.py migrate

# 7. Seed the three core services
python manage.py seed_services

# 8. Create an admin account
python manage.py createsuperuser

# 9. Start the dev server
python manage.py runserver
```

Open → http://127.0.0.1:8000  
Admin → http://127.0.0.1:8000/admin/

---

## Docker Setup

### Prerequisites
- Docker ≥ 24
- Docker Compose ≥ 2.20

### Development — full stack in one command

```bash
# Copy and configure environment
cp .env.example .env

# Build and start all services (web, db, redis, nginx)
docker compose up --build

# Open the app
open http://localhost
```

The first start will automatically:
1. Wait for PostgreSQL and Redis to be healthy
2. Run `python manage.py migrate`
3. Run `python manage.py seed_services`
4. Collect static files
5. Start Gunicorn

### Useful Docker commands

```bash
# Follow app logs only
docker compose logs -f web

# Run a management command inside the container
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py shell

# Open a PostgreSQL shell
docker compose exec db psql -U talentheart -d talentheart_db

# Open a Redis shell
docker compose exec redis redis-cli

# Rebuild after code changes
docker compose up --build web

# Stop and remove containers (keep volumes)
docker compose down

# Stop and remove everything INCLUDING database volumes
docker compose down -v
```

### Production deployment with Docker Compose

```bash
# Set all required environment variables (no defaults in prod)
export SECRET_KEY="your-50-char-production-secret"
export DEBUG="False"
export ALLOWED_HOSTS="talentheart.com,www.talentheart.com"
export DB_PASSWORD="strong-db-password"
export EMAIL_HOST_USER="your@gmail.com"
export EMAIL_HOST_PASSWORD="your-app-password"

# Launch with production overrides (2 web replicas, no source bind-mount)
docker compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Check running services
docker compose ps
```

### Build and push image to a registry

```bash
# Build production image
docker build -t your-registry/talentheart:latest .

# Push to registry
docker push your-registry/talentheart:latest
```

---

## Dockerize Without Docker Compose

Run every service manually using plain `docker` commands — no Compose required.

### Prerequisites
- Docker ≥ 24
- A `.env` file configured from `.env.example`

### Step 1 — Create a shared network

```bash
docker network create talentheart-net
```

### Step 2 — Start PostgreSQL

```bash
docker run -d \
  --name talentheart-db \
  --network talentheart-net \
  -e POSTGRES_DB=talentheart_db \
  -e POSTGRES_USER=talentheart \
  -e POSTGRES_PASSWORD=your_db_password \
  -v talentheart-pg-data:/var/lib/postgresql/data \
  postgres:15-alpine
```

### Step 3 — Start Redis

```bash
docker run -d \
  --name talentheart-redis \
  --network talentheart-net \
  redis:7-alpine \
  redis-server --maxmemory 256mb --maxmemory-policy allkeys-lru
```

### Step 4 — Build the application image

```bash
docker build -t talentheart-web:latest .
```

### Step 5 — Run the Django / Gunicorn container

```bash
docker run -d \
  --name talentheart-web \
  --network talentheart-net \
  -e SECRET_KEY="your-secret-key" \
  -e DEBUG="False" \
  -e ALLOWED_HOSTS="localhost,127.0.0.1" \
  -e DB_NAME="talentheart_db" \
  -e DB_USER="talentheart" \
  -e DB_PASSWORD="your_db_password" \
  -e DB_HOST="talentheart-db" \
  -e DB_PORT="5432" \
  -e REDIS_URL="redis://talentheart-redis:6379/0" \
  -v talentheart-static:/app/staticfiles \
  -v talentheart-media:/app/media \
  talentheart-web:latest
```

### Step 6 — Start Nginx

```bash
docker run -d \
  --name talentheart-nginx \
  --network talentheart-net \
  -p 80:80 \
  -v talentheart-static:/app/staticfiles:ro \
  -v talentheart-media:/app/media:ro \
  -v "$(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro" \
  -v "$(pwd)/nginx/conf.d:/etc/nginx/conf.d:ro" \
  nginx:1.25-alpine
```

> **Windows PowerShell:** replace `$(pwd)` with `${PWD}`.

### Step 7 — Verify everything is running

```bash
docker ps
# All four containers (db, redis, web, nginx) should show "Up"

# Check web logs
docker logs -f talentheart-web

# Create a superuser
docker exec -it talentheart-web python manage.py createsuperuser
```

Open → http://localhost  
Admin → http://localhost/admin/

### Teardown

```bash
docker stop talentheart-nginx talentheart-web talentheart-redis talentheart-db
docker rm   talentheart-nginx talentheart-web talentheart-redis talentheart-db
docker network rm talentheart-net
# Remove volumes only when you want to wipe all data
docker volume rm talentheart-pg-data talentheart-static talentheart-media
```

---

## Kubernetes Deployment

### Prerequisites
- `kubectl` ≥ 1.28
- A running cluster (EKS / GKE / AKS / k3s / minikube)
- [metrics-server](https://github.com/kubernetes-sigs/metrics-server) (for HPA)
- [nginx-ingress-controller](https://kubernetes.github.io/ingress-nginx/)
- [cert-manager](https://cert-manager.io/) (for automatic TLS)
- An RWX-capable StorageClass (e.g., AWS EFS, GCP Filestore, NFS) for shared volumes

### 0. Build and push the image to Docker Hub

All Kubernetes manifests reference the image `atique123/talentheart`. Build, tag, and push it before deploying.

```bash
# Log in to Docker Hub
docker login

# Build the production image
docker build -t atique123/talentheart:latest .

# (Optional) tag a versioned release
docker tag atique123/talentheart:latest atique123/talentheart:v1.0.0

# Push both tags
docker push atique123/talentheart:latest
docker push atique123/talentheart:v1.0.0
```

> For CI/CD pipelines (GitHub Actions, GitLab CI, etc.), store your Docker Hub credentials as repository secrets (`DOCKERHUB_USERNAME` / `DOCKERHUB_TOKEN`) and run the same commands in the workflow.

### 1. Update the image name

Edit `k8s/web/deployment.yaml` and replace the placeholder with your Docker Hub image:
```yaml
image: atique123/talentheart:latest
```
Pin a specific version tag in production instead of `latest`:
```yaml
image: atique123/talentheart:v1.0.0
```

### 2. Set real secrets

```bash
# Encode your values
echo -n 'my-production-secret-key' | base64
echo -n 'strong-db-password'       | base64
echo -n 'email@gmail.com'          | base64
echo -n 'gmail-app-password'       | base64
```

Edit `k8s/secret.yaml` with the base64-encoded values, then apply.

> ⚠️ **Never commit real secrets.** Use [Sealed Secrets](https://github.com/bitnami-labs/sealed-secrets),
> [HashiCorp Vault](https://www.vaultproject.io/), or your cloud provider's secret manager in production.

### 3. Update the domain

Edit `k8s/ingress.yaml` and replace `talentheart.com` with your domain.  
Update `k8s/configmap.yaml` → `ALLOWED_HOSTS` to match.

### 4. Choose a StorageClass

Edit `k8s/web/pvcs.yaml` and set `storageClassName` to an RWX class in your cluster:

| Cloud | StorageClass |
|-------|-------------|
| AWS EKS | `efs-sc` (requires EFS CSI driver) |
| GKE | `standard-rwx` or Filestore CSI |
| AKS | `azurefile` |
| On-prem | NFS provisioner |

### 5. Deploy everything

```bash
# Apply in dependency order
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secret.yaml

# Storage
kubectl apply -f k8s/postgres/pvc.yaml
kubectl apply -f k8s/web/pvcs.yaml

# Database
kubectl apply -f k8s/postgres/statefulset.yaml
kubectl apply -f k8s/postgres/service.yaml

# Cache
kubectl apply -f k8s/redis/deployment.yaml
kubectl apply -f k8s/redis/service.yaml

# Application
kubectl apply -f k8s/web/deployment.yaml
kubectl apply -f k8s/web/service.yaml
kubectl apply -f k8s/web/hpa.yaml

# Nginx proxy
kubectl apply -f k8s/nginx/configmap.yaml
kubectl apply -f k8s/nginx/deployment.yaml
kubectl apply -f k8s/nginx/service.yaml

# Ingress (TLS)
kubectl apply -f k8s/ingress.yaml
```

Or apply everything at once:
```bash
kubectl apply -R -f k8s/
```

### 6. Verify deployment

```bash
# Check all pods are Running
kubectl get pods -n talentheart

# Check services
kubectl get svc -n talentheart

# Check ingress and note the external IP
kubectl get ingress -n talentheart

# Follow web pod logs
kubectl logs -f deployment/talentheart-web -n talentheart

# Create the Django superuser inside a pod
kubectl exec -it deployment/talentheart-web -n talentheart \
  -- python manage.py createsuperuser

# Watch HPA scale the web deployment
kubectl get hpa -n talentheart -w
```

### Kubernetes Architecture

```
                    ┌──────────────────────────────┐
                    │       Ingress (TLS)           │
                    │  talentheart.com → nginx svc  │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │   nginx Deployment (×2)       │
                    │   ConfigMap-driven config     │
                    │   Reads staticfiles PVC       │
                    └──────────────┬───────────────┘
                                   │
                    ┌──────────────▼───────────────┐
                    │  talentheart-web (×2–10)     │
                    │  HPA: CPU>70% → scale out    │
                    │  RollingUpdate strategy       │
                    └────────┬────────────┬────────┘
                             │            │
              ┌──────────────▼──┐  ┌─────▼─────────────┐
              │  PostgreSQL 15  │  │    Redis 7          │
              │  StatefulSet ×1 │  │  Deployment ×1     │
              │  PVC: 10Gi      │  │  allkeys-lru 256MB │
              └─────────────────┘  └────────────────────┘
```

---

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ | — | Django secret key (50+ random chars) |
| `DEBUG` | ✅ | `False` | Set `True` for development only |
| `ALLOWED_HOSTS` | ✅ | `localhost` | Comma-separated list of valid hostnames |
| `DB_NAME` | ✅ | `talentheart_db` | PostgreSQL database name |
| `DB_USER` | ✅ | `postgres` | PostgreSQL username |
| `DB_PASSWORD` | ✅ | — | PostgreSQL password |
| `DB_HOST` | ✅ | `localhost` | PostgreSQL host |
| `DB_PORT` | | `5432` | PostgreSQL port |
| `REDIS_URL` | ✅ | `redis://localhost:6379/0` | Redis connection URL |
| `EMAIL_HOST` | | `smtp.gmail.com` | SMTP server |
| `EMAIL_PORT` | | `587` | SMTP port |
| `EMAIL_HOST_USER` | | — | SMTP username |
| `EMAIL_HOST_PASSWORD` | | — | SMTP password / app password |
| `DEFAULT_FROM_EMAIL` | | `noreply@talentheart.com` | Sender address |
| `CONTACT_EMAIL` | | `info@talentheart.com` | Contact form recipient |

---

## Admin Panel

Access at `/admin/` — manage:

- **Users** — view/edit all registered users and their profiles
- **Services** — add/edit/deactivate services and their features
- **Orders** — update order status, add internal notes, filter by status
- **Contact Messages** — read submissions, mark as read

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Language | Python 3.11 |
| Framework | Django 4.2 |
| Database | PostgreSQL 15 |
| Cache / Sessions | Redis 7 + django-redis |
| Web Server | Gunicorn + Nginx |
| Static Files | WhiteNoise (dev) / Nginx volume (prod) |
| Container | Docker (multi-stage) |
| Orchestration | Kubernetes with HPA + Ingress |
| UI | Bootstrap 5 + Bootstrap Icons |

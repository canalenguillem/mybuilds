# myBuilds — Technical Submittal Automation System

Web platform that lets building-materials suppliers generate compliant,
consultant-ready technical submittal packages automatically.

**Stack:** FastAPI · React 18 + Vite · MariaDB · MongoDB · Redis · Celery · Docker

---

## Quick start (development)

```bash
cp .env.example .env          # adjust secrets if you like
docker compose up -d --build  # build & start the stack
docker compose exec backend python scripts/seed_data.py   # roles + admin user
```

Then open:

| Service        | URL                              |
| -------------- | -------------------------------- |
| Frontend       | http://localhost:3100            |
| Backend API    | http://localhost:8100/api/v1     |
| API docs       | http://localhost:8100/docs       |
| Health check   | http://localhost:8100/api/v1/health |

> Host ports are remapped (see `.env`) to avoid clashing with other services
> on this machine. Containers still use standard ports internally.

**Default admin login** (from `.env`): `admin@mybuilds.com` / `Admin123!`

---

## What is implemented (foundation)

- ✅ Docker orchestration: MariaDB, MongoDB, Redis, FastAPI backend, Celery worker, Vite frontend
- ✅ All SQLAlchemy ORM models (users, roles/permissions, products, documents,
  templates, submittals, compliance, audit) per `docs/DATABASE_SCHEMA.md`
- ✅ JWT authentication — register / login / refresh / logout / me, with RBAC roles
- ✅ Bcrypt password hashing, refresh-token sessions, standard error envelope
- ✅ React app with design tokens from `docs/DESIGN_IMPLEMENTATION_GUIDE.md`,
  login → dashboard flow with protected routing and silent token refresh

## Next phases (see `docs/IMPLEMENTATION_ROADMAP.md`)

- Document & product CRUD + upload, template builder, submittal generation (Celery + PDF),
  AI compliance statements, analytics dashboard, remaining MVP screens.

---

## Project layout

```
backend/   FastAPI app (app/api, app/services, app/database, app/tasks, scripts)
frontend/  Vite + React (src/pages, src/components, src/services, src/context)
docs/      Specifications and the high-fidelity HTML prototype
volumes/   Runtime data (DBs, uploads, generated PDFs) — git-ignored
```

See `docs/PROJECT_STRUCTURE.md` for the full intended structure.

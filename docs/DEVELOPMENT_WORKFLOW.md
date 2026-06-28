# Development Workflow & Technology Stack

## Technology Stack

### Backend
| Technology | Version | Purpose | Justification |
|-----------|---------|---------|--------------|
| Python | 3.11+ | Core language | Strong ML/AI libraries, async support, type hints |
| FastAPI | 0.104+ | Web framework | High performance, auto-generated docs, async/await, validation |
| Uvicorn | 0.24+ | ASGI server | Production-ready, high performance, WebSocket support |
| SQLAlchemy | 2.0+ | ORM | Type-safe, relationship management, migration support |
| Pydantic | 2.0+ | Data validation | Type hints, validation, JSON schema generation |
| PyJWT | 2.8+ | Authentication | JWT token generation/validation, standard approach |
| PyPDF2 | 4.0+ | PDF manipulation | PDF merging, manipulation, mature library |
| ReportLab | 4.0+ | PDF generation | Professional PDF creation, TOC generation |
| python-docx | 0.8+ | Word docs | Future support for DOCX templates |
| python-pptx | 0.6+ | PowerPoint | Future support for PPTX templates |
| pymongo | 4.6+ | MongoDB driver | MongoDB connectivity, async support |
| redis | 5.0+ | Redis client | Redis interaction, async support |
| celery | 5.3+ | Task queue | Distributed async tasks, scheduling |
| pytest | 7.4+ | Testing | Unit/integration testing, fixtures, mocking |
| python-multipart | 0.0.6+ | File uploads | Multipart form handling for file uploads |
| requests | 2.31+ | HTTP client | External API calls, LLM integration |
| pytesseract | 0.3+ | OCR | Document text extraction |
| python-dotenv | 1.0+ | Env management | Environment variable loading |
| alembic | 1.13+ | Migrations | Database schema versioning |
| cryptography | 41+ | Encryption | Secure data handling |

### Frontend
| Technology | Version | Purpose | Justification |
|-----------|---------|---------|--------------|
| React | 18+ | UI library | Component reusability, large ecosystem, developer experience |
| Vite | 5.0+ | Build tool | Lightning-fast builds, HMR, modern tooling |
| JavaScript/ES2023+ | Latest | Language | Flexible, widely understood |
| Axios | 1.6+ | HTTP client | Promise-based, interceptors, error handling |
| React Router | 6.20+ | Routing | Client-side routing, nested routes, hooks |
| Context API | Built-in | State management | No external dependency for simple state |
| CSS3 | Latest | Styling | CSS variables, flexbox, grid, modern features |
| React Hook Form | 7.48+ | Forms | Lightweight, performant form handling |
| Zustand/Jotai | Optional | State management | Lightweight alternative to Redux if needed |
| Recharts | 2.10+ | Charts/Graphs | React-friendly charting library |
| React Beautiful DND | 13.1+ | Drag-drop | Smooth drag-drop for section reordering |
| Framer Motion | 10.16+ | Animations | Smooth animations and transitions (optional) |
| date-fns | 2.30+ | Date handling | Lightweight date utility library |
| lodash | 4.17+ | Utilities | Common utility functions |
| clsx | 2.0+ | CSS classes | Dynamic class name management |
| vitest | Latest | Testing | Fast unit testing for Vite projects |
| msw | 2.0+ | API mocking | Mock API for testing |

### Database
| Technology | Version | Purpose | Justification |
|-----------|---------|---------|--------------|
| MariaDB | 11.3+ | Relational DB | Open-source MySQL compatible, ACID compliance, proven stability |
| MongoDB | 7.0+ | Document DB | Flexible schema, document storage, aggregation pipeline |
| Redis | 7.0+ | Cache/Queue | Sub-millisecond performance, simple operations, message queue |

### Infrastructure
| Technology | Version | Purpose | Justification |
|-----------|---------|---------|--------------|
| Docker | 24+ | Containerization | Environment consistency, deployment simplicity |
| Docker Compose | 2.20+ | Orchestration | Local multi-container setup, development simplicity |
| Nginx | Alpine | Reverse proxy | Lightweight, high performance, static file serving |
| Git | Latest | Version control | Standard, distributed, branching model |

### External Services
| Service | Purpose | Justification |
|---------|---------|--------------|
| OpenAI API | LLM/Compliance | GPT-4 for requirement extraction, advanced NLP |
| Claude API | Alternative LLM | More cost-effective, good for document analysis |
| AWS S3 / MinIO | File storage | Scalable, cost-effective (S3) or on-premise (MinIO) |
| SMTP | Email delivery | Simple, universal email transport |

### Optional/Future
| Technology | Purpose |
|-----------|---------|
| n8n | Workflow automation, advanced integrations |
| Celery Beat | Task scheduling, cron jobs |
| Elasticsearch | Full-text search (beyond basic DB search) |
| LogStash/ELK | Log aggregation and analysis |
| Prometheus/Grafana | Monitoring and metrics |
| GitHub Actions | CI/CD pipeline |
| Stripe/Payment Gateway | Future monetization |

---

## Development Workflow

### 1. Initial Setup

```bash
# Clone repository
git clone <repo-url>
cd submittal-automation-system

# Install Git hooks (optional pre-commit checks)
pip install pre-commit
pre-commit install

# Copy environment file
cp .env.example .env
# Edit .env with local settings

# Start Docker containers
docker-compose up -d

# Create databases and tables
docker-compose exec backend python scripts/init_db.py

# Seed with test data (optional)
docker-compose exec backend python scripts/seed_data.py

# Frontend dependencies are installed in container
```

### 2. Development Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f celery_worker

# Stop services
docker-compose down

# Stop and remove volumes (fresh start)
docker-compose down -v

# Rebuild after dependency changes
docker-compose down
docker-compose build
docker-compose up -d
```

### 3. Code Changes During Development

#### Backend
- Code changes auto-reload via Uvicorn reload flag
- Database schema changes → create migration file with Alembic
- New dependencies → add to requirements.txt, rebuild container

#### Frontend
- Code changes hot-reload via Vite HMR
- New components → create in `src/components/`
- New pages → create in `src/pages/`
- New dependencies → add to package.json, npm install in container

### 4. Database Migrations

```bash
# Create new migration
docker-compose exec backend alembic revision --autogenerate -m "Add new column"

# Review migration file in backend/app/database/migrations/versions/

# Apply migrations
docker-compose exec backend alembic upgrade head

# Rollback one migration
docker-compose exec backend alembic downgrade -1
```

### 5. API Testing During Development

```bash
# Access interactive API docs
curl http://localhost:8000/docs

# Or use REST client
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Or use tools like Postman, Insomnia, REST Client (VS Code)
```

### 6. Frontend Development

```bash
# Access Vite dev server
# http://localhost:3000

# Development features:
# - Hot Module Replacement (HMR)
# - Fast refresh
# - Source map debugging
```

---

## Git Workflow

### Branch Strategy
```
main (production-ready code)
  ├── staging (pre-production)
  └── develop (integration branch)
        ├── feature/document-upload
        ├── feature/template-builder
        ├── feature/compliance-ai
        ├── bugfix/submission-number
        └── chore/dependency-update
```

### Commit Message Format
```
<type>(<scope>): <subject>

<body>

<footer>

Types: feat, fix, docs, style, refactor, perf, test, chore
Scopes: backend, frontend, database, docker, docs
```

Example:
```
feat(backend): implement PDF generation service

Implement async PDF generation using PyPDF2 and ReportLab.
Add support for:
- Document merging
- TOC generation
- Page numbering
- Header/footer insertion

Closes #123
```

### Pull Request Process
1. Create feature branch from `develop`
2. Make commits with clear messages
3. Create PR with detailed description
4. Code review by team members
5. Run automated tests
6. Merge after approval
7. Delete feature branch

---

## Testing Strategy

### Backend Testing
```bash
# Run all tests
docker-compose exec backend pytest

# Run specific test file
docker-compose exec backend pytest app/tests/test_auth.py

# Run with coverage
docker-compose exec backend pytest --cov=app

# Run specific test
docker-compose exec backend pytest app/tests/test_auth.py::test_login
```

**Test Structure**:
- Unit tests: Service logic, utilities
- Integration tests: API endpoints, database
- Fixture-based: Reusable test data

### Frontend Testing
```bash
# Run all tests
cd frontend
npm test

# Run specific test file
npm test -- DocumentUpload.test.jsx

# Run with coverage
npm test -- --coverage
```

### Testing Best Practices
- **Backend**: 80%+ code coverage
- **Frontend**: Test components, hooks, services
- **E2E**: Critical user flows (optional for MVP)
- **Load Testing**: Performance validation

---

## Debugging

### Backend Debugging

**VS Code Python Extension**:
```json
{
  "name": "FastAPI",
  "type": "python",
  "request": "attach",
  "connect": {
    "host": "localhost",
    "port": 5678
  }
}
```

Or use `pdb` for interactive debugging:
```python
import pdb; pdb.set_trace()
```

### Frontend Debugging

**Browser DevTools**:
- React Developer Tools extension
- Redux DevTools (if using Redux)
- Network tab for API calls
- Console for errors

**VS Code**:
```json
{
  "type": "chrome",
  "request": "launch",
  "name": "Launch Chrome",
  "url": "http://localhost:3000",
  "webRoot": "${workspaceFolder}/frontend/src"
}
```

### Database Debugging

```bash
# Access MariaDB CLI
docker-compose exec mariadb mariadb -u submittal_user -p submittal_db

# Access MongoDB CLI
docker-compose exec mongodb mongosh

# Redis CLI
docker-compose exec redis redis-cli -a password
```

---

## Performance Optimization Checklist

### Backend
- [ ] Database query optimization (indexes, N+1 queries)
- [ ] Async/await for I/O operations
- [ ] Caching frequently accessed data
- [ ] Pagination for list endpoints
- [ ] Response compression (gzip)
- [ ] Connection pooling
- [ ] Monitoring slow queries

### Frontend
- [ ] Code splitting by route
- [ ] Lazy loading components
- [ ] Image optimization
- [ ] CSS/JS minification (production)
- [ ] Bundle analysis
- [ ] Remove unused dependencies
- [ ] Optimize re-renders (React.memo, useMemo)

### Infrastructure
- [ ] CDN for static assets
- [ ] Load balancing
- [ ] Database replication
- [ ] Redis caching
- [ ] Horizontal scaling
- [ ] Health checks
- [ ] Monitoring & alerting

---

## Common Development Tasks

### Adding New Feature

1. **Create feature branch**
   ```bash
   git checkout -b feature/new-feature
   ```

2. **Backend**: Create API endpoint
   - Add route in `api/v1/`
   - Add service method
   - Add database model if needed
   - Add tests

3. **Frontend**: Create UI component
   - Create component in `src/components/`
   - Create service method if needed
   - Add tests
   - Connect to API

4. **Database**: Update schema
   - Create migration if needed
   - Update ORM models

5. **Test**: Verify functionality
   - Run unit tests
   - Test manually
   - Check for regressions

6. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat(scope): description"
   git push origin feature/new-feature
   ```

### Debugging API Issue

1. Check backend logs: `docker-compose logs -f backend`
2. Review API response in browser DevTools
3. Test with curl: `curl http://localhost:8000/api/v1/endpoint`
4. Check database state: `docker-compose exec mariadb mariadb ...`
5. Add print/log statements for debugging
6. Use Python debugger for complex logic

### Performance Issue

1. **Backend**: Check slow query log, use profiling
2. **Frontend**: Use React DevTools, check bundle size
3. **Database**: Check query execution plans, add indexes
4. **Network**: Check API response times, optimize payloads
5. **Infrastructure**: Monitor CPU, memory, disk usage

---

## Code Quality Standards

### Python (Backend)
- **Style**: PEP 8 (via Black formatter)
- **Linting**: Flake8, Pylint
- **Type Checking**: mypy (optional but recommended)
- **Testing**: pytest with 80%+ coverage
- **Documentation**: Docstrings for functions/classes

### JavaScript/React (Frontend)
- **Style**: Prettier for formatting
- **Linting**: ESLint with recommended rules
- **Testing**: Vitest for unit tests
- **Documentation**: JSDoc for functions
- **Component Structure**: Single Responsibility Principle

### Commit Standards
- Clear, descriptive messages
- Reference issue numbers
- Conventional Commits format

### Code Review
- Peer review before merge
- Check for security issues
- Verify test coverage
- Ensure documentation

---

## Deployment Checklist

### Pre-Deployment
- [ ] All tests passing
- [ ] Code reviewed and approved
- [ ] Security scan completed
- [ ] Database migrations tested
- [ ] Environment variables configured
- [ ] Secrets stored safely (not in code)
- [ ] Logs configured appropriately
- [ ] Monitoring/alerts configured

### Deployment
- [ ] Build images: `docker-compose build`
- [ ] Run migrations: `alembic upgrade head`
- [ ] Start services: `docker-compose up -d`
- [ ] Verify health checks
- [ ] Monitor logs for errors
- [ ] Test critical workflows

### Post-Deployment
- [ ] Monitor error rates
- [ ] Check performance metrics
- [ ] Verify all features working
- [ ] Monitor resource usage
- [ ] Update deployment documentation
- [ ] Communicate changes to team

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port already in use | Change port in docker-compose.yml or kill process |
| Database connection failed | Verify credentials in .env, check DB container is running |
| Frontend not loading | Check Vite dev server logs, verify VITE_API_URL |
| Slow PDF generation | Check document sizes, optimize PDF merge logic |
| High memory usage | Check for memory leaks, optimize queries, scale workers |
| API timeout | Increase timeout settings, optimize long-running operations |
| Redis connection refused | Verify Redis password, check container is running |


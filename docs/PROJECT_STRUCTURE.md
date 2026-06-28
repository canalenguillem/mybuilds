# Project Structure & Organization

## Directory Layout

```
submittal-automation-system/
├── docker-compose.yml                 # Docker orchestration (dev & prod configs)
├── .dockerignore
├── .gitignore
├── .env.example                       # Environment variables template
├── README.md
├── ARCHITECTURE.md
├── DATABASE_SCHEMA.md
├── API_SPECIFICATIONS.md
│
├── backend/                           # FastAPI Backend (Python)
│   ├── Dockerfile
│   ├── requirements.txt                # Python dependencies
│   ├── .env.example
│   ├── main.py                         # Application entry point
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py                   # Configuration management
│   │   ├── dependencies.py             # Dependency injection
│   │   ├── exceptions.py               # Custom exceptions
│   │   ├── middleware.py               # Request/response middleware
│   │   │
│   │   ├── api/                        # API route handlers
│   │   │   ├── __init__.py
│   │   │   ├── v1/
│   │   │   │   ├── __init__.py
│   │   │   │   ├── auth.py             # Authentication routes
│   │   │   │   ├── documents.py        # Document management routes
│   │   │   │   ├── products.py         # Product management routes
│   │   │   │   ├── templates.py        # Template management routes
│   │   │   │   ├── submittals.py       # Submittal generation routes
│   │   │   │   ├── compliance.py       # Compliance analysis routes
│   │   │   │   ├── analytics.py        # Analytics/reporting routes
│   │   │   │   └── health.py           # Health check routes
│   │   │   └── router.py               # Route aggregator
│   │   │
│   │   ├── services/                   # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py         # Authentication logic
│   │   │   ├── document_service.py     # Document management logic
│   │   │   ├── product_service.py      # Product logic
│   │   │   ├── template_service.py     # Template logic
│   │   │   ├── submittal_service.py    # PDF generation logic
│   │   │   ├── compliance_service.py   # AI compliance logic
│   │   │   ├── analytics_service.py    # Analytics logic
│   │   │   ├── storage_service.py      # File storage abstraction
│   │   │   ├── pdf_service.py          # PDF manipulation
│   │   │   ├── ocr_service.py          # Document OCR/parsing
│   │   │   ├── ai_service.py           # LLM integration
│   │   │   └── audit_service.py        # Audit logging
│   │   │
│   │   ├── models/                     # Pydantic request/response models
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── documents.py
│   │   │   ├── products.py
│   │   │   ├── templates.py
│   │   │   ├── submittals.py
│   │   │   ├── compliance.py
│   │   │   ├── common.py               # Shared models (pagination, etc.)
│   │   │   └── responses.py            # Standard response formats
│   │   │
│   │   ├── database/                   # Database layer
│   │   │   ├── __init__.py
│   │   │   ├── session.py              # Session management
│   │   │   ├── models.py               # SQLAlchemy ORM models
│   │   │   │   ├── users.py
│   │   │   │   ├── documents.py
│   │   │   │   ├── products.py
│   │   │   │   ├── templates.py
│   │   │   │   ├── submittals.py
│   │   │   │   ├── compliance.py
│   │   │   │   └── common.py
│   │   │   ├── repositories/           # Data access patterns
│   │   │   │   ├── __init__.py
│   │   │   │   ├── base_repository.py  # Base CRUD repo
│   │   │   │   ├── user_repository.py
│   │   │   │   ├── document_repository.py
│   │   │   │   ├── template_repository.py
│   │   │   │   ├── submittal_repository.py
│   │   │   │   └── compliance_repository.py
│   │   │   └── migrations/             # Alembic migrations
│   │   │       ├── env.py
│   │   │       ├── script.py.mako
│   │   │       └── versions/
│   │   │           ├── 001_initial_schema.py
│   │   │           └── ...
│   │   │
│   │   ├── tasks/                      # Celery async tasks
│   │   │   ├── __init__.py
│   │   │   ├── celery_app.py           # Celery configuration
│   │   │   ├── pdf_generation.py       # PDF generation tasks
│   │   │   ├── compliance_analysis.py  # AI analysis tasks
│   │   │   ├── email_delivery.py       # Email tasks
│   │   │   └── document_processing.py  # Document processing tasks
│   │   │
│   │   ├── utils/                      # Utility functions
│   │   │   ├── __init__.py
│   │   │   ├── security.py             # Security utilities
│   │   │   ├── pdf_utils.py            # PDF helpers
│   │   │   ├── validators.py           # Input validation
│   │   │   ├── decorators.py           # Custom decorators
│   │   │   ├── logger.py               # Logging configuration
│   │   │   └── constants.py            # App constants
│   │   │
│   │   ├── external/                   # External integrations
│   │   │   ├── __init__.py
│   │   │   ├── openai_client.py        # OpenAI/Claude API client
│   │   │   ├── aws_s3_client.py        # AWS S3 integration
│   │   │   ├── minio_client.py         # MinIO integration
│   │   │   ├── email_client.py         # Email service
│   │   │   └── n8n_client.py           # n8n workflow integration
│   │   │
│   │   └── tests/                      # Unit & integration tests
│   │       ├── __init__.py
│   │       ├── conftest.py             # Pytest configuration
│   │       ├── test_auth.py
│   │       ├── test_documents.py
│   │       ├── test_templates.py
│   │       ├── test_submittals.py
│   │       ├── test_compliance.py
│   │       └── fixtures/               # Test data
│   │
│   └── scripts/                        # Utility scripts
│       ├── init_db.py                  # Database initialization
│       ├── seed_data.py                # Seed test data
│       └── backup.sh                   # Backup script
│
├── frontend/                           # Vite + React Frontend
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── package.json                    # Node dependencies
│   ├── vite.config.js                  # Vite configuration
│   ├── .env.example
│   ├── index.html
│   │
│   ├── public/                         # Static assets
│   │   ├── images/
│   │   ├── icons/
│   │   └── fonts/
│   │
│   ├── src/
│   │   ├── main.jsx                    # React entry point
│   │   ├── App.jsx                     # Root component
│   │   ├── index.css                   # Global styles
│   │   │
│   │   ├── components/                 # Reusable components
│   │   │   ├── common/                 # Common UI components
│   │   │   │   ├── Header.jsx
│   │   │   │   ├── Sidebar.jsx
│   │   │   │   ├── Navbar.jsx
│   │   │   │   ├── Footer.jsx
│   │   │   │   ├── Button.jsx
│   │   │   │   ├── Modal.jsx
│   │   │   │   ├── Spinner.jsx
│   │   │   │   ├── Toast.jsx
│   │   │   │   ├── Pagination.jsx
│   │   │   │   └── Loading.jsx
│   │   │   │
│   │   │   ├── auth/                   # Authentication components
│   │   │   │   ├── LoginForm.jsx
│   │   │   │   ├── RegisterForm.jsx
│   │   │   │   └── ProtectedRoute.jsx
│   │   │   │
│   │   │   ├── documents/              # Document management components
│   │   │   │   ├── DocumentUpload.jsx
│   │   │   │   ├── DocumentList.jsx
│   │   │   │   ├── DocumentPreview.jsx
│   │   │   │   ├── DocumentVersions.jsx
│   │   │   │   └── DocumentSearch.jsx
│   │   │   │
│   │   │   ├── templates/              # Template builder components
│   │   │   │   ├── TemplateBuilder.jsx
│   │   │   │   ├── SectionDragDrop.jsx
│   │   │   │   ├── TemplateEditor.jsx
│   │   │   │   ├── SectionSelector.jsx
│   │   │   │   └── BrandingConfig.jsx
│   │   │   │
│   │   │   ├── submittals/             # Submittal generation components
│   │   │   │   ├── SubmittalWizard.jsx
│   │   │   │   ├── GenerationProgress.jsx
│   │   │   │   ├── SubmittalList.jsx
│   │   │   │   ├── SubmittalPreview.jsx
│   │   │   │   └── SubmittalDownload.jsx
│   │   │   │
│   │   │   ├── compliance/             # Compliance review components
│   │   │   │   ├── ComplianceDashboard.jsx
│   │   │   │   ├── StatementReview.jsx
│   │   │   │   ├── ComplianceStatus.jsx
│   │   │   │   └── GapAnalysis.jsx
│   │   │   │
│   │   │   └── analytics/              # Analytics components
│   │   │       ├── Dashboard.jsx
│   │   │       ├── MetricsCard.jsx
│   │   │       ├── Chart.jsx
│   │   │       └── ReportGenerator.jsx
│   │   │
│   │   ├── pages/                      # Page components (views)
│   │   │   ├── Dashboard.jsx
│   │   │   ├── LoginPage.jsx
│   │   │   ├── Documents/
│   │   │   │   ├── DocumentsPage.jsx
│   │   │   │   └── UploadPage.jsx
│   │   │   ├── Templates/
│   │   │   │   ├── TemplatesPage.jsx
│   │   │   │   └── BuilderPage.jsx
│   │   │   ├── Submittals/
│   │   │   │   ├── SubmittalsPage.jsx
│   │   │   │   └── GeneratorPage.jsx
│   │   │   ├── Compliance/
│   │   │   │   └── CompliancePage.jsx
│   │   │   ├── Analytics/
│   │   │   │   └── AnalyticsPage.jsx
│   │   │   ├── Admin/
│   │   │   │   ├── UserManagement.jsx
│   │   │   │   └── Settings.jsx
│   │   │   └── NotFound.jsx
│   │   │
│   │   ├── services/                   # API service layer
│   │   │   ├── api.js                  # Axios/fetch configuration
│   │   │   ├── authService.js
│   │   │   ├── documentService.js
│   │   │   ├── templateService.js
│   │   │   ├── submittalService.js
│   │   │   ├── complianceService.js
│   │   │   └── analyticsService.js
│   │   │
│   │   ├── hooks/                      # Custom React hooks
│   │   │   ├── useAuth.js
│   │   │   ├── useApi.js
│   │   │   ├── useForm.js
│   │   │   ├── usePagination.js
│   │   │   └── useLocalStorage.js
│   │   │
│   │   ├── context/                    # Context API
│   │   │   ├── AuthContext.jsx
│   │   │   ├── ThemeContext.jsx
│   │   │   └── NotificationContext.jsx
│   │   │
│   │   ├── store/                      # State management (if using Redux)
│   │   │   ├── store.js
│   │   │   ├── slices/
│   │   │   │   ├── authSlice.js
│   │   │   │   ├── documentSlice.js
│   │   │   │   └── ...
│   │   │   └── middleware/
│   │   │
│   │   ├── styles/                     # CSS/SCSS files
│   │   │   ├── variables.css           # CSS variables
│   │   │   ├── globals.css
│   │   │   ├── components.css
│   │   │   └── utils.css
│   │   │
│   │   ├── utils/                      # Utility functions
│   │   │   ├── helpers.js
│   │   │   ├── validators.js
│   │   │   ├── formatters.js
│   │   │   ├── constants.js
│   │   │   └── errorHandler.js
│   │   │
│   │   └── config.js                   # Frontend configuration
│   │
│   ├── tests/                          # Frontend tests
│   │   ├── unit/
│   │   ├── integration/
│   │   └── __mocks__/
│   │
│   └── build/                          # Built files (after npm run build)
│
├── docs/                               # Documentation
│   ├── API.md
│   ├── DEPLOYMENT.md
│   ├── CONTRIBUTING.md
│   ├── DEVELOPMENT.md
│   ├── USER_GUIDE.md
│   └── ARCHITECTURE.md
│
├── nginx/                              # Nginx reverse proxy
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── conf.d/
│   │   ├── api.conf                    # Backend routing
│   │   └── frontend.conf               # Frontend routing
│   └── ssl/
│       ├── cert.pem
│       └── key.pem
│
├── volumes/                            # Data persistence
│   ├── mariadb/                        # MariaDB data
│   ├── mongodb/                        # MongoDB data
│   ├── redis/                          # Redis persistence
│   ├── documents/                      # Uploaded documents storage
│   ├── generated_pdfs/                 # Generated submittals storage
│   └── backups/                        # Database backups
│
├── scripts/                            # Utility scripts
│   ├── backup.sh
│   ├── restore.sh
│   ├── health_check.sh
│   ├── migrate.sh
│   └── seed_data.sh
│
└── .github/                            # GitHub workflows/CI-CD
    ├── workflows/
    │   ├── test.yml                    # Run tests on PR
    │   ├── build.yml                   # Build Docker images
    │   ├── deploy.yml                  # Deploy to production
    │   └── lint.yml                    # Code quality checks
    └── ISSUE_TEMPLATE/
```

---

## File Naming Conventions

### Backend (Python)
- **Modules**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions/Methods**: `snake_case`
- **Constants**: `CONSTANT_CASE`

### Frontend (JavaScript/React)
- **Components**: `PascalCase.jsx`
- **Services**: `camelCase.js`
- **Utilities**: `camelCase.js`
- **CSS/SCSS**: `kebab-case.css`
- **Constants**: `CONSTANT_CASE`

### Database
- **Tables**: `snake_case` (singular or plural consistently)
- **Columns**: `snake_case`
- **Indexes**: `idx_column_name` or `unique_column_names`
- **Foreign Keys**: `fk_table_column`

---

## Key Files Explained

### Backend Entry Points
- **main.py**: FastAPI app initialization, middleware setup, route registration
- **config.py**: Environment-based configuration, settings management
- **dependencies.py**: Dependency injection, database sessions, current user resolution

### Frontend Entry Points
- **main.jsx**: React app root, provider setup, initial rendering
- **App.jsx**: Root component with routing, layout structure
- **index.css**: Global styles, CSS variables, base styles

### Configuration Files
- **.env.example**: Template for environment variables (copy to .env for local development)
- **docker-compose.yml**: Multi-container orchestration for dev/prod
- **Dockerfile**: Container image building instructions

---

## Development vs Production Structure

### Development
- Hot-reload enabled (frontend with Vite, backend with Uvicorn reload)
- Mock data and seeders
- Verbose logging
- Local file storage
- Single docker-compose.yml with all services

### Production
- Optimized builds (minified frontend, compiled backend)
- Nginx reverse proxy
- Cloud storage (S3/MinIO)
- Minimal logging
- Separate docker-compose configurations
- Health checks and restart policies
- Database backups automated
- SSL/TLS certificates

---

## Important Notes

1. **Volume Mounts**: 
   - Database data persists in `volumes/` directory
   - Generated PDFs stored in `volumes/generated_pdfs/`
   - Document uploads in `volumes/documents/`

2. **Environment Variables**:
   - Copy `.env.example` to `.env` for local development
   - Different `.env.production` for production deployment

3. **Database Migrations**:
   - Stored in `backend/app/database/migrations/`
   - Run automatically on startup or manually with scripts

4. **Testing**:
   - Backend tests in `backend/app/tests/`
   - Frontend tests in `frontend/tests/`
   - Run with `pytest` (backend) and `npm test` (frontend)


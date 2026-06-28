# System Architecture & Technical Design

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        Frontend (Vite + React)                   │
│  ├─ Document Management UI                                       │
│  ├─ Template Builder (Drag-Drop)                                 │
│  ├─ Submittal Generator                                          │
│  ├─ Compliance Review Dashboard                                  │
│  └─ Analytics & Reporting                                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │ (HTTP/WebSocket)
┌──────────────────────▼──────────────────────────────────────────┐
│                    FastAPI Backend (Python)                      │
│  ├─ Authentication & Authorization                               │
│  ├─ Document Management Service                                  │
│  ├─ Template Management Service                                  │
│  ├─ PDF Generation Service                                       │
│  ├─ AI Compliance Analysis Service                               │
│  ├─ User & Role Management                                       │
│  └─ Audit Logging Service                                        │
└──────┬──────────────┬──────────────┬──────────────┬──────────────┘
       │              │              │              │
   ┌───▼─┐    ┌──────▼─────┐  ┌────▼───┐  ┌─────▼────┐
   │MySQL│    │  MongoDB   │  │ Redis  │  │ OpenAI  │
   │/    │    │  (Document │  │(Cache) │  │/Claude  │
   │Maria│    │  Metadata) │  │        │  │API      │
   │DB   │    │            │  │        │  │         │
   └─────┘    └────────────┘  └────────┘  └─────────┘
```

---

## Architecture Layers

### Presentation Layer (Frontend)
**Technology**: Vite + React + JavaScript

**Components**:
- Document Management Dashboard
- Template Builder Interface
- Submittal Generation Wizard
- Compliance Review Interface
- User Management Interface
- Analytics Dashboard
- Document Viewer/Preview

**Key Features**:
- Responsive design (Desktop-first)
- Real-time form validation
- Drag-and-drop functionality
- File upload with progress
- PDF preview
- Role-based UI rendering

---

### API Layer (Backend)
**Technology**: FastAPI (Python 3.10+)

**Core Services**:

#### 1. Authentication Service
- JWT token generation/validation
- User session management
- Role-based access control (RBAC)
- Optional LDAP/AD integration

#### 2. Document Management Service
- Document upload/storage
- Document indexing and search
- Version control
- Metadata management
- File storage abstraction (local/S3)

#### 3. Template Management Service
- CRUD operations for templates
- Template versioning
- Section management
- Conditional logic engine
- Template cloning/copying

#### 4. PDF Generation Service
- PDF merge and assembly
- TOC generation
- Page numbering
- Header/footer insertion
- Branding application
- Performance optimization (async processing)

#### 5. AI Compliance Service
- Document parsing/OCR
- Requirement extraction
- Specification analysis
- Compliance statement generation
- Confidence scoring
- Audit trail creation

#### 6. Reporting & Analytics Service
- Metrics calculation
- Dashboard data aggregation
- Report generation
- Export functionality

#### 7. Audit Service
- Action logging
- Change tracking
- Compliance trail
- Export capabilities

---

### Data Layer

#### Primary Database (MariaDB)
**Purpose**: Transactional data, structured information

**Tables**:
- users
- roles
- permissions
- templates
- template_sections
- products
- documents
- submittals
- submissions_audit
- compliance_statements
- compliance_reviews
- user_sessions
- system_settings

#### Document Database (MongoDB)
**Purpose**: Document metadata, flexible schema

**Collections**:
- document_metadata
- compliance_requirements
- extraction_results
- ai_analysis_cache
- template_configurations
- submittal_archives

#### Cache Layer (Redis)
**Purpose**: Performance optimization, session management

**Use Cases**:
- Session tokens
- Template cache
- Document metadata cache
- Rate limiting
- Queue for async tasks
- Real-time notifications

---

## Service Communication

### Synchronous Communication
- REST APIs for CRUD operations
- WebSocket for real-time updates
- File uploads/downloads

### Asynchronous Communication
- Task queue for PDF generation (Celery + Redis)
- Email delivery queue
- Document processing queue
- Compliance analysis queue

---

## Data Flow Diagrams

### Document Upload Flow
```
User → Frontend Upload UI → FastAPI Document Endpoint 
→ Validate & Store File → Index in MongoDB 
→ Extract Metadata → Cache in Redis 
→ Return Response to Frontend
```

### Submittal Generation Flow
```
User selects Product + Consultant + Template
→ Frontend calls Submittal API
→ Fetch template from Cache/DB
→ Load product documents
→ Merge PDFs (queue async task)
→ Generate TOC/numbering
→ Apply branding
→ Return download link
```

### Compliance Analysis Flow
```
User uploads Consultant Requirements PDF
→ FastAPI receives document
→ Extract text via OCR/parsing
→ Send to AI API for requirement extraction
→ Compare against product datasheets
→ Generate compliance statements
→ Store results in MongoDB
→ Return to reviewer dashboard
```

---

## Security Architecture

### Authentication
- JWT tokens with expiration (15min access, 7day refresh)
- Secure password hashing (bcrypt)
- Optional 2FA support

### Authorization
- Role-based access control (RBAC)
- Resource-level permissions
- API endpoint protection
- Audit logging of all actions

### Data Protection
- Encryption at rest (database-level)
- TLS/HTTPS for data in transit
- Sensitive data masking in logs
- Secure file storage
- Regular backup strategy

### API Security
- Rate limiting
- CORS configuration
- Input validation and sanitization
- SQL injection prevention (ORM usage)
- CSRF protection
- Secure headers

---

## External Integrations

### AI/LLM Integration
- **Primary**: OpenAI GPT-4 API or Claude API
- **Purpose**: Requirement extraction, compliance analysis
- **Implementation**: Async calls with retry logic
- **Fallback**: Manual review required

### File Storage Options
- Local file system (development)
- AWS S3 (production recommended)
- MinIO (on-premise alternative)

### Email Service
- SMTP for email delivery
- Queue-based processing
- Template-based notifications

### Optional: Workflow Automation
- n8n integration for advanced workflows
- Document triggers
- Automated approval chains
- Integration with external systems

---

## Performance Considerations

### Optimization Strategies
- Redis caching for frequently accessed data
- Async task processing for long-running operations
- Database indexing strategy
- API response compression
- Frontend lazy loading and code splitting
- CDN for static assets

### Scalability Plan
- Stateless API design
- Load balancing ready
- Horizontal scaling via Docker
- Database replication strategy
- Document storage on shared volume
- Queue system for background tasks

---

## Deployment Architecture

### Docker Containers
1. **Frontend** (Vite dev server or nginx)
2. **Backend** (FastAPI with Uvicorn)
3. **MariaDB** (Relational database)
4. **MongoDB** (Document database)
5. **Redis** (Cache and queue)
6. **Celery Worker** (Async tasks)
7. **Nginx** (Reverse proxy)

### Docker Compose Orchestration
- Development environment with hot-reload
- Production-ready configurations
- Volume management for data persistence
- Network isolation
- Environment variable configuration

---

## Development Workflow

### Local Development
- Docker Compose for full stack
- Hot-reload for frontend and backend
- Database migrations automated
- Seed data for testing

### Code Organization
- Modular service architecture
- Clear separation of concerns
- Reusable components (frontend)
- Utility/helper functions
- Configuration management

### Version Control
- Feature branches
- Pull request workflow
- Semantic versioning
- Git hooks for quality checks

---

## Monitoring & Logging

### Application Monitoring
- API performance metrics
- Error tracking and reporting
- User activity monitoring
- System health checks
- Database query performance

### Logging Strategy
- Structured logging (JSON format)
- Centralized log aggregation (optional)
- Different log levels
- Audit trail separate from application logs
- Log retention policy

---

## Technology Justification

| Component | Technology | Reason |
|-----------|-----------|--------|
| Backend | FastAPI | High performance, async support, auto docs, type hints |
| Frontend | React + Vite | Modern UX, component reusability, fast builds |
| Primary DB | MariaDB | ACID compliance, transactional data, proven reliability |
| Document DB | MongoDB | Flexible schemas, document metadata, quick iteration |
| Cache | Redis | Sub-millisecond performance, session management, queuing |
| PDF Library | PyPDF2/ReportLab | Python ecosystem, PDF manipulation, cost-effective |
| AI/LLM | OpenAI/Claude | Advanced NLP, requirement extraction, statement generation |
| Task Queue | Celery | Distributed task processing, long-running operations |
| Containerization | Docker | Environment consistency, deployment simplicity |


# API Specifications & Endpoints

## Authentication Endpoints

### POST /api/v1/auth/register
Register new user

**Request:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "password": "securepassword",
  "full_name": "Full Name",
  "company": "Company Name"
}
```

**Response (201):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "username",
  "full_name": "Full Name",
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### POST /api/v1/auth/login
Authenticate user and get tokens

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "refresh_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 900,
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "roles": ["operator"],
    "permissions": ["create_submittal", "upload_document"]
  }
}
```

---

### POST /api/v1/auth/refresh
Refresh access token using refresh token

**Request:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200):**
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "expires_in": 900
}
```

---

### POST /api/v1/auth/logout
Logout user and revoke tokens

**Request:**
```json
{
  "refresh_token": "eyJhbGc..."
}
```

**Response (200):**
```json
{
  "message": "Successfully logged out"
}
```

---

## Document Management Endpoints

### POST /api/v1/documents/upload
Upload document for a product

**Request:** (multipart/form-data)
```
- file: <binary PDF file>
- product_id: 1
- document_type: datasheets
- title: "Product Datasheet v2.1"
```

**Response (201):**
```json
{
  "id": 123,
  "product_id": 1,
  "document_type": "datasheets",
  "title": "Product Datasheet v2.1",
  "version": 1,
  "file_size": 2048576,
  "pages": 24,
  "storage_location": "s3",
  "created_at": "2024-01-15T10:30:00Z",
  "created_by": {
    "id": 1,
    "username": "admin"
  }
}
```

---

### GET /api/v1/documents
List all documents with filters

**Query Parameters:**
```
?product_id=1
&document_type=datasheets
&page=1
&page_size=20
&search=compliance
```

**Response (200):**
```json
{
  "total": 150,
  "page": 1,
  "page_size": 20,
  "documents": [
    {
      "id": 123,
      "product_id": 1,
      "document_type": "datasheets",
      "title": "Product Datasheet v2.1",
      "version": 1,
      "file_size": 2048576,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### GET /api/v1/documents/{document_id}
Get document metadata

**Response (200):**
```json
{
  "id": 123,
  "product_id": 1,
  "document_type": "datasheets",
  "title": "Product Datasheet v2.1",
  "version": 1,
  "file_size": 2048576,
  "pages": 24,
  "checksum": "abc123...",
  "extracted_text": "Product details...",
  "storage_location": "s3",
  "created_at": "2024-01-15T10:30:00Z",
  "versions": [
    {
      "version": 1,
      "file_size": 2048576,
      "changed_by": "admin",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### DELETE /api/v1/documents/{document_id}
Delete document and create archive

**Response (200):**
```json
{
  "message": "Document deleted successfully",
  "document_id": 123,
  "deleted_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/v1/documents/{document_id}/versions
Get document version history

**Response (200):**
```json
{
  "document_id": 123,
  "current_version": 2,
  "versions": [
    {
      "version": 2,
      "file_size": 2100000,
      "changed_by": "admin",
      "change_reason": "Updated compliance section",
      "created_at": "2024-01-20T14:00:00Z"
    },
    {
      "version": 1,
      "file_size": 2048576,
      "changed_by": "admin",
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

## Product Management Endpoints

### POST /api/v1/products
Create new product

**Request:**
```json
{
  "name": "Product XYZ",
  "description": "Product description",
  "category": "HVAC",
  "sku": "PRD-XYZ-001",
  "vendor_id": 1
}
```

**Response (201):**
```json
{
  "id": 1,
  "name": "Product XYZ",
  "description": "Product description",
  "category": "HVAC",
  "sku": "PRD-XYZ-001",
  "vendor_id": 1,
  "is_active": true,
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/v1/products
List all products

**Query Parameters:**
```
?category=HVAC
&is_active=true
&page=1
&page_size=20
```

**Response (200):**
```json
{
  "total": 50,
  "page": 1,
  "page_size": 20,
  "products": [
    {
      "id": 1,
      "name": "Product XYZ",
      "category": "HVAC",
      "sku": "PRD-XYZ-001",
      "document_count": 5,
      "templates_count": 2
    }
  ]
}
```

---

### GET /api/v1/products/{product_id}/documents
Get all documents for a product

**Response (200):**
```json
{
  "product_id": 1,
  "product_name": "Product XYZ",
  "documents": {
    "datasheets": [
      {
        "id": 123,
        "title": "Datasheet v2.1",
        "version": 1,
        "file_size": 2048576
      }
    ],
    "certificates": [
      {
        "id": 124,
        "title": "ISO 9001 Certificate",
        "version": 1
      }
    ],
    "manuals": []
  }
}
```

---

## Template Management Endpoints

### POST /api/v1/templates
Create new submittal template

**Request:**
```json
{
  "name": "HVAC System Submittal",
  "description": "Standard submittal for HVAC products",
  "product_id": 1,
  "consultant_id": "CONS-001",
  "template_type": "product_generic",
  "branding_config": {
    "company_logo_url": "/images/logo.png",
    "primary_color": "#0066cc",
    "font_family": "Arial"
  },
  "sections": [
    {
      "section_name": "Company Profile",
      "section_order": 1,
      "section_type": "static_document",
      "document_ids": [125, 126],
      "is_mandatory": true
    },
    {
      "section_name": "Product Datasheet",
      "section_order": 2,
      "section_type": "static_document",
      "document_ids": [123],
      "is_mandatory": true
    },
    {
      "section_name": "Compliance Statement",
      "section_order": 3,
      "section_type": "dynamic_compliance",
      "is_mandatory": true
    }
  ]
}
```

**Response (201):**
```json
{
  "id": 10,
  "name": "HVAC System Submittal",
  "product_id": 1,
  "version": 1,
  "is_active": true,
  "section_count": 3,
  "created_by": {
    "id": 1,
    "username": "admin"
  },
  "created_at": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/v1/templates
List all templates

**Query Parameters:**
```
?product_id=1
&consultant_id=CONS-001
&is_active=true
&page=1
&page_size=20
```

**Response (200):**
```json
{
  "total": 25,
  "page": 1,
  "page_size": 20,
  "templates": [
    {
      "id": 10,
      "name": "HVAC System Submittal",
      "product_id": 1,
      "consultant_id": "CONS-001",
      "version": 1,
      "section_count": 3,
      "is_active": true,
      "last_updated": "2024-01-15T10:30:00Z"
    }
  ]
}
```

---

### GET /api/v1/templates/{template_id}
Get template with sections

**Response (200):**
```json
{
  "id": 10,
  "name": "HVAC System Submittal",
  "product_id": 1,
  "version": 1,
  "branding_config": {
    "company_logo_url": "/images/logo.png",
    "primary_color": "#0066cc"
  },
  "sections": [
    {
      "id": 100,
      "section_name": "Company Profile",
      "section_order": 1,
      "section_type": "static_document",
      "document_ids": [125, 126],
      "is_mandatory": true,
      "documents": [
        {
          "id": 125,
          "title": "Company Overview",
          "file_size": 1048576
        }
      ]
    }
  ]
}
```

---

### PUT /api/v1/templates/{template_id}
Update template

**Request:** (Same structure as POST)

**Response (200):**
```json
{
  "id": 10,
  "name": "HVAC System Submittal",
  "version": 2,
  "updated_at": "2024-01-20T14:00:00Z"
}
```

---

### POST /api/v1/templates/{template_id}/sections/reorder
Reorder template sections (drag-drop)

**Request:**
```json
{
  "sections": [
    {
      "section_id": 100,
      "new_order": 3
    },
    {
      "section_id": 101,
      "new_order": 1
    },
    {
      "section_id": 102,
      "new_order": 2
    }
  ]
}
```

**Response (200):**
```json
{
  "message": "Sections reordered successfully",
  "template_id": 10,
  "sections": [
    {
      "section_id": 101,
      "section_name": "Company Profile",
      "new_order": 1
    }
  ]
}
```

---

## Submittal Generation Endpoints

### POST /api/v1/submittals/generate
Generate submittal from template

**Request:**
```json
{
  "template_id": 10,
  "product_id": 1,
  "consultant_id": "CONS-001",
  "project_name": "Downtown Office Complex",
  "project_code": "DOC-2024-001",
  "consultant_requirements_doc_id": 200,
  "metadata": {
    "custom_field_1": "value1",
    "custom_field_2": "value2"
  },
  "generate_compliance_statements": true,
  "ai_model": "gpt-4"
}
```

**Response (202 - Accepted - Async):**
```json
{
  "task_id": "task-abc123def456",
  "message": "Submittal generation started",
  "estimated_time_seconds": 45,
  "status_url": "/api/v1/submittals/tasks/task-abc123def456"
}
```

---

### GET /api/v1/submittals/tasks/{task_id}
Check submittal generation status

**Response (200):**
```json
{
  "task_id": "task-abc123def456",
  "status": "processing", // pending, processing, completed, failed
  "progress": 65,
  "submittal_id": null,
  "message": "Generating PDF...",
  "estimated_completion_time": "2024-01-15T10:45:00Z"
}
```

**Response (200) - Completed:**
```json
{
  "task_id": "task-abc123def456",
  "status": "completed",
  "progress": 100,
  "submittal_id": 500,
  "message": "Submittal generated successfully",
  "file_url": "/api/v1/submittals/500/download",
  "page_count": 128,
  "file_size": 5242880,
  "generation_time_ms": 42000
}
```

---

### GET /api/v1/submittals
List all submittals

**Query Parameters:**
```
?product_id=1
&consultant_id=CONS-001
&status=completed
&created_after=2024-01-01
&created_before=2024-01-31
&page=1
&page_size=20
```

**Response (200):**
```json
{
  "total": 120,
  "page": 1,
  "page_size": 20,
  "submittals": [
    {
      "id": 500,
      "submission_number": "SUB-2024-001",
      "product_id": 1,
      "template_id": 10,
      "consultant_id": "CONS-001",
      "project_name": "Downtown Office Complex",
      "status": "completed",
      "page_count": 128,
      "file_size": 5242880,
      "created_by": "operator1",
      "created_at": "2024-01-15T10:00:00Z",
      "generated_at": "2024-01-15T10:45:00Z"
    }
  ]
}
```

---

### GET /api/v1/submittals/{submittal_id}
Get submittal details

**Response (200):**
```json
{
  "id": 500,
  "submission_number": "SUB-2024-001",
  "product_id": 1,
  "template_id": 10,
  "consultant_id": "CONS-001",
  "project_name": "Downtown Office Complex",
  "project_code": "DOC-2024-001",
  "status": "completed",
  "page_count": 128,
  "file_size": 5242880,
  "total_sections": 3,
  "metadata": {
    "custom_field_1": "value1"
  },
  "generated_at": "2024-01-15T10:45:00Z",
  "created_by": {
    "id": 2,
    "username": "operator1"
  },
  "compliance_statements": [
    {
      "id": 600,
      "requirement": "ISO 9001 compliance",
      "statement": "Product XYZ is manufactured...",
      "confidence_score": 0.95,
      "review_status": "approved"
    }
  ],
  "audit_trail": [
    {
      "action": "created",
      "actor": "operator1",
      "timestamp": "2024-01-15T10:00:00Z"
    },
    {
      "action": "generated",
      "actor": "system",
      "timestamp": "2024-01-15T10:45:00Z"
    }
  ]
}
```

---

### GET /api/v1/submittals/{submittal_id}/download
Download generated PDF

**Response (200):**
- Content-Type: application/pdf
- Content-Disposition: attachment; filename="SUB-2024-001.pdf"
- Binary PDF content

---

### DELETE /api/v1/submittals/{submittal_id}
Delete submittal (archive)

**Response (200):**
```json
{
  "message": "Submittal archived successfully",
  "submittal_id": 500,
  "archived_at": "2024-01-15T10:30:00Z"
}
```

---

## AI Compliance Analysis Endpoints

### POST /api/v1/compliance/analyze
Analyze consultant requirements document

**Request:**
```json
{
  "consultant_requirements_doc_id": 200,
  "product_ids": [1, 2, 3],
  "ai_model": "gpt-4",
  "analysis_type": "full" // full, requirements_only, gaps_only
}
```

**Response (202 - Async):**
```json
{
  "task_id": "compliance-task-abc123",
  "message": "Compliance analysis started",
  "estimated_time_seconds": 120,
  "status_url": "/api/v1/compliance/tasks/compliance-task-abc123"
}
```

---

### GET /api/v1/compliance/tasks/{task_id}
Check compliance analysis status

**Response (200):**
```json
{
  "task_id": "compliance-task-abc123",
  "status": "completed",
  "progress": 100,
  "results": {
    "extracted_requirements": [
      {
        "requirement_id": 1,
        "requirement_text": "Product must comply with ISO 9001",
        "requirement_category": "quality_management",
        "confidence": 0.98
      }
    ],
    "compliance_statements": [
      {
        "requirement_id": 1,
        "product_id": 1,
        "statement": "Product XYZ is certified to ISO 9001:2015...",
        "confidence_score": 0.95,
        "source_documents": [123, 124]
      }
    ],
    "gaps": [
      {
        "requirement": "CE marking",
        "product_id": 2,
        "reason": "No CE certification found in documents",
        "risk_level": "high"
      }
    ]
  },
  "processing_time_ms": 95000,
  "tokens_used": 15000,
  "cost": 0.45
}
```

---

### GET /api/v1/compliance/requirements/{requirement_id}
Get extracted requirement details

**Response (200):**
```json
{
  "id": 1,
  "source_document_id": 200,
  "source_document_name": "Consultant Technical Specifications v2.1",
  "requirement_text": "Product must comply with ISO 9001",
  "requirement_category": "quality_management",
  "extracted_keywords": ["ISO 9001", "quality", "management"],
  "ai_extraction_confidence": 0.98,
  "extracted_at": "2024-01-15T10:30:00Z"
}
```

---

### POST /api/v1/compliance/statements/{statement_id}/review
Review and approve/reject AI-generated compliance statement

**Request:**
```json
{
  "review_status": "approved", // approved, rejected, needs_revision
  "review_notes": "Approved. Statement accurately reflects product compliance.",
  "revised_statement": null // Optional: If needs revision, provide corrected text
}
```

**Response (200):**
```json
{
  "id": 600,
  "review_status": "approved",
  "reviewed_by": {
    "id": 3,
    "username": "reviewer1"
  },
  "reviewed_at": "2024-01-15T11:00:00Z",
  "review_notes": "Approved. Statement accurately reflects product compliance."
}
```

---

### GET /api/v1/compliance/statements
List compliance statements

**Query Parameters:**
```
?submittal_id=500
&review_status=pending_review
&confidence_score_min=0.85
&page=1
&page_size=20
```

**Response (200):**
```json
{
  "total": 45,
  "page": 1,
  "page_size": 20,
  "statements": [
    {
      "id": 600,
      "submittal_id": 500,
      "requirement": "ISO 9001 Compliance",
      "statement": "Product XYZ is certified...",
      "confidence_score": 0.95,
      "is_ai_generated": true,
      "review_status": "pending_review",
      "created_at": "2024-01-15T10:45:00Z"
    }
  ]
}
```

---

## Analytics & Reporting Endpoints

### GET /api/v1/analytics/dashboard
Get dashboard metrics

**Response (200):**
```json
{
  "period": "2024-01-01 to 2024-01-31",
  "metrics": {
    "total_submittals_generated": 145,
    "total_documents_processed": 320,
    "total_pages_generated": 18500,
    "average_generation_time_seconds": 42,
    "compliance_statements_generated": 450,
    "compliance_accuracy_rate": 0.94,
    "avg_confidence_score": 0.91
  },
  "trends": {
    "daily_submittals": [
      { "date": "2024-01-01", "count": 5 },
      { "date": "2024-01-02", "count": 7 }
    ]
  },
  "top_products": [
    { "product_id": 1, "product_name": "Product XYZ", "submittals_count": 45 },
    { "product_id": 2, "product_name": "Product ABC", "submittals_count": 32 }
  ]
}
```

---

### GET /api/v1/analytics/export
Export analytics report

**Query Parameters:**
```
?format=pdf&date_from=2024-01-01&date_to=2024-01-31
```

**Response (200):**
- Content-Type: application/pdf
- Binary PDF report

---

## Webhook Support (Optional)

### POST /api/v1/webhooks
Register webhook for events

**Request:**
```json
{
  "event_type": "submittal.generated", // submittal.generated, compliance.reviewed, document.uploaded
  "url": "https://external-system.com/webhooks/submittal",
  "auth_token": "webhook-secret-token"
}
```

---

## Error Responses

### Standard Error Response (4xx/5xx)
```json
{
  "error": {
    "code": "INVALID_INPUT",
    "message": "Product ID is required",
    "details": {
      "field": "product_id",
      "reason": "Required field missing"
    },
    "timestamp": "2024-01-15T10:30:00Z",
    "request_id": "req-abc123def456"
  }
}
```

### Common Error Codes
- `INVALID_INPUT` - 400
- `UNAUTHORIZED` - 401
- `FORBIDDEN` - 403
- `NOT_FOUND` - 404
- `CONFLICT` - 409
- `RATE_LIMITED` - 429
- `INTERNAL_ERROR` - 500
- `SERVICE_UNAVAILABLE` - 503

---

## Rate Limiting

- **Anonymous users**: 10 requests/minute
- **Authenticated users**: 100 requests/minute
- **Premium users**: Unlimited

Headers returned:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1705336200
```

---

## Pagination

All list endpoints support:
- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)
- `sort_by`: Sort field (default: created_at)
- `sort_order`: asc or desc (default: desc)


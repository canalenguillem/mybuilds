# Database Schema & Data Models

## MariaDB Schema (Transactional Data)

### Users & Authentication

```sql
-- Users table
CREATE TABLE users (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(100) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  full_name VARCHAR(255),
  company VARCHAR(255),
  is_active BOOLEAN DEFAULT true,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_email (email),
  INDEX idx_username (username)
);

-- Roles table
CREATE TABLE roles (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User roles mapping (many-to-many)
CREATE TABLE user_roles (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  role_id INT NOT NULL,
  assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  assigned_by BIGINT,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  FOREIGN KEY (role_id) REFERENCES roles(id),
  FOREIGN KEY (assigned_by) REFERENCES users(id),
  UNIQUE KEY unique_user_role (user_id, role_id),
  INDEX idx_user_id (user_id)
);

-- Permissions table
CREATE TABLE permissions (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(100) UNIQUE NOT NULL,
  description TEXT,
  resource VARCHAR(100),
  action VARCHAR(50)
);

-- Role permissions mapping (many-to-many)
CREATE TABLE role_permissions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  role_id INT NOT NULL,
  permission_id INT NOT NULL,
  FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE CASCADE,
  FOREIGN KEY (permission_id) REFERENCES permissions(id) ON DELETE CASCADE,
  UNIQUE KEY unique_role_permission (role_id, permission_id)
);

-- User sessions
CREATE TABLE user_sessions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT NOT NULL,
  token_hash VARCHAR(255) UNIQUE NOT NULL,
  ip_address VARCHAR(45),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expires_at TIMESTAMP NOT NULL,
  revoked_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  INDEX idx_user_id (user_id),
  INDEX idx_token_hash (token_hash),
  INDEX idx_expires_at (expires_at)
);
```

### Products & Documents

```sql
-- Products table
CREATE TABLE products (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  category VARCHAR(100),
  sku VARCHAR(100) UNIQUE,
  vendor_id BIGINT,
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_name (name),
  INDEX idx_category (category)
);

-- Document types enum
-- datasheets, certificates, manuals, catalogues, vendor_lists, compliance_docs, etc.

-- Documents table
CREATE TABLE documents (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  product_id BIGINT NOT NULL,
  document_type VARCHAR(50) NOT NULL,
  title VARCHAR(255) NOT NULL,
  description TEXT,
  file_path VARCHAR(500) NOT NULL,
  file_size BIGINT,
  file_extension VARCHAR(10),
  storage_location VARCHAR(50), -- 'local', 's3', 'minio'
  original_filename VARCHAR(255),
  version INT DEFAULT 1,
  is_current_version BOOLEAN DEFAULT true,
  checksum VARCHAR(64), -- SHA-256 for integrity
  pages INT,
  extracted_text LONGTEXT, -- Full text for search
  created_by BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
  FOREIGN KEY (created_by) REFERENCES users(id),
  INDEX idx_product_id (product_id),
  INDEX idx_document_type (document_type),
  INDEX idx_version (version),
  FULLTEXT INDEX ft_extracted_text (extracted_text)
);

-- Document versioning
CREATE TABLE document_versions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  document_id BIGINT NOT NULL,
  version INT NOT NULL,
  file_path VARCHAR(500),
  file_size BIGINT,
  changed_by BIGINT NOT NULL,
  change_reason TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE,
  FOREIGN KEY (changed_by) REFERENCES users(id),
  UNIQUE KEY unique_doc_version (document_id, version),
  INDEX idx_document_id (document_id)
);
```

### Templates

```sql
-- Submittal templates
CREATE TABLE templates (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  product_id BIGINT,
  consultant_id VARCHAR(100), -- Consultant/client code
  template_type VARCHAR(50), -- 'product_generic', 'consultant_specific', 'custom'
  version INT DEFAULT 1,
  is_current_version BOOLEAN DEFAULT true,
  is_active BOOLEAN DEFAULT true,
  branding_config JSON, -- Logo, colors, fonts
  header_footer_config JSON, -- Header/footer templates
  created_by BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL,
  FOREIGN KEY (created_by) REFERENCES users(id),
  INDEX idx_product_id (product_id),
  INDEX idx_consultant_id (consultant_id),
  INDEX idx_template_type (template_type)
);

-- Template sections
CREATE TABLE template_sections (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  template_id BIGINT NOT NULL,
  section_name VARCHAR(255) NOT NULL,
  section_order INT NOT NULL,
  section_type VARCHAR(50), -- 'static_document', 'dynamic_compliance', 'custom_html'
  description TEXT,
  document_ids JSON, -- Array of document IDs to include
  conditional_logic JSON, -- Conditions for inclusion
  is_mandatory BOOLEAN DEFAULT true,
  is_editable BOOLEAN DEFAULT false,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
  UNIQUE KEY unique_section_order (template_id, section_order),
  INDEX idx_template_id (template_id)
);

-- Template versions
CREATE TABLE template_versions (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  template_id BIGINT NOT NULL,
  version INT NOT NULL,
  version_data JSON, -- Full template structure
  created_by BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  change_description TEXT,
  FOREIGN KEY (template_id) REFERENCES templates(id) ON DELETE CASCADE,
  FOREIGN KEY (created_by) REFERENCES users(id),
  UNIQUE KEY unique_template_version (template_id, version)
);
```

### Submittals

```sql
-- Submittals
CREATE TABLE submittals (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  submission_number VARCHAR(100) UNIQUE NOT NULL,
  product_id BIGINT NOT NULL,
  template_id BIGINT NOT NULL,
  consultant_id VARCHAR(100),
  project_name VARCHAR(255),
  project_code VARCHAR(100),
  status VARCHAR(50), -- 'draft', 'generated', 'reviewed', 'approved', 'archived'
  generated_file_path VARCHAR(500),
  file_size BIGINT,
  page_count INT,
  total_sections INT,
  metadata JSON, -- Project-specific metadata
  created_by BIGINT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  generated_at TIMESTAMP,
  FOREIGN KEY (product_id) REFERENCES products(id),
  FOREIGN KEY (template_id) REFERENCES templates(id),
  FOREIGN KEY (created_by) REFERENCES users(id),
  INDEX idx_product_id (product_id),
  INDEX idx_template_id (template_id),
  INDEX idx_consultant_id (consultant_id),
  INDEX idx_status (status),
  INDEX idx_created_at (created_at)
);

-- Submittal audit trail
CREATE TABLE submittal_audit (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  submittal_id BIGINT NOT NULL,
  action VARCHAR(50), -- 'created', 'generated', 'reviewed', 'approved', 'downloaded', 'archived'
  actor_id BIGINT NOT NULL,
  action_details JSON,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (submittal_id) REFERENCES submittals(id) ON DELETE CASCADE,
  FOREIGN KEY (actor_id) REFERENCES users(id),
  INDEX idx_submittal_id (submittal_id),
  INDEX idx_action (action),
  INDEX idx_timestamp (timestamp)
);
```

### Compliance Analysis

```sql
-- Compliance statements
CREATE TABLE compliance_statements (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  submittal_id BIGINT,
  requirement_id BIGINT,
  statement TEXT NOT NULL,
  confidence_score DECIMAL(3,2), -- 0.00 to 1.00
  source_document_ids JSON, -- Which documents support this
  is_ai_generated BOOLEAN DEFAULT true,
  review_status VARCHAR(50), -- 'pending_review', 'reviewed', 'approved', 'rejected'
  reviewer_id BIGINT,
  review_notes TEXT,
  reviewed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  FOREIGN KEY (submittal_id) REFERENCES submittals(id) ON DELETE CASCADE,
  FOREIGN KEY (reviewer_id) REFERENCES users(id),
  INDEX idx_submittal_id (submittal_id),
  INDEX idx_review_status (review_status),
  INDEX idx_confidence_score (confidence_score)
);

-- Compliance requirements extracted from consultant docs
CREATE TABLE compliance_requirements (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  source_document_id BIGINT,
  source_document_name VARCHAR(255),
  requirement_text TEXT NOT NULL,
  requirement_category VARCHAR(100),
  extracted_keywords JSON,
  ai_extraction_confidence DECIMAL(3,2),
  extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (source_document_id) REFERENCES documents(id) ON DELETE SET NULL,
  INDEX idx_source_document_id (source_document_id),
  INDEX idx_requirement_category (requirement_category)
);

-- Compliance analysis history
CREATE TABLE compliance_analysis_history (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  submittal_id BIGINT,
  consultant_requirements_doc_id BIGINT,
  analysis_type VARCHAR(50), -- 'auto_generation', 'comparison', 'gap_analysis'
  analysis_result JSON,
  ai_model_used VARCHAR(100),
  processing_time_ms INT,
  tokens_used INT,
  cost DECIMAL(8,4),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (submittal_id) REFERENCES submittals(id) ON DELETE CASCADE,
  FOREIGN KEY (consultant_requirements_doc_id) REFERENCES documents(id),
  INDEX idx_submittal_id (submittal_id),
  INDEX idx_created_at (created_at)
);
```

### Analytics & Audit

```sql
-- System audit log
CREATE TABLE audit_log (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  user_id BIGINT,
  action VARCHAR(100) NOT NULL,
  resource_type VARCHAR(50),
  resource_id BIGINT,
  changes JSON, -- Before/after values
  ip_address VARCHAR(45),
  user_agent TEXT,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
  INDEX idx_user_id (user_id),
  INDEX idx_action (action),
  INDEX idx_timestamp (timestamp)
);

-- Metrics table
CREATE TABLE metrics (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  metric_name VARCHAR(100) NOT NULL,
  metric_value DECIMAL(12,2),
  metric_date DATE,
  additional_data JSON,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY unique_metric_date (metric_name, metric_date),
  INDEX idx_metric_date (metric_date)
);

-- System settings
CREATE TABLE system_settings (
  id INT PRIMARY KEY AUTO_INCREMENT,
  setting_key VARCHAR(100) UNIQUE NOT NULL,
  setting_value VARCHAR(500),
  value_type VARCHAR(20), -- 'string', 'int', 'boolean', 'json'
  description TEXT,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

---

## MongoDB Collections (Document & Flexible Data)

### Document Collections

```javascript
// Document metadata and enriched information
db.createCollection("document_metadata", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["_id", "document_id", "content_type"],
      properties: {
        _id: { bsonType: "objectId" },
        document_id: { bsonType: "long" }, // FK to MariaDB
        content_type: { bsonType: "string" },
        full_text: { bsonType: "string" }, // OCR/extracted text
        keywords: { bsonType: "array", items: { bsonType: "string" } },
        entities: { // Named entity extraction
          bsonType: "object",
          properties: {
            organizations: { bsonType: "array" },
            locations: { bsonType: "array" },
            standards: { bsonType: "array" },
            specifications: { bsonType: "array" }
          }
        },
        metadata: { bsonType: "object" },
        extraction_date: { bsonType: "date" },
        ai_summary: { bsonType: "string" },
        embedding: { bsonType: "array", items: { bsonType: "double" } }
      }
    }
  }
});

// Compliance requirements cache
db.createCollection("compliance_requirements_cache", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      properties: {
        _id: { bsonType: "objectId" },
        requirement_id: { bsonType: "long" },
        requirement_text: { bsonType: "string" },
        extracted_elements: { bsonType: "object" },
        related_standards: { bsonType: "array" },
        risk_level: { bsonType: "string" },
        last_updated: { bsonType: "date" }
      }
    }
  }
});

// AI analysis results cache
db.createCollection("ai_analysis_results", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      properties: {
        _id: { bsonType: "objectId" },
        analysis_id: { bsonType: "string" },
        submittal_id: { bsonType: "long" },
        analysis_type: { bsonType: "string" },
        extracted_requirements: { bsonType: "array" },
        compliance_statements: { bsonType: "array" },
        gaps_identified: { bsonType: "array" },
        recommendations: { bsonType: "array" },
        confidence_scores: { bsonType: "object" },
        processing_time_ms: { bsonType: "int" },
        ai_model: { bsonType: "string" },
        created_at: { bsonType: "date" }
      }
    }
  }
});

// Template configurations
db.createCollection("template_configurations", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      properties: {
        _id: { bsonType: "objectId" },
        template_id: { bsonType: "long" },
        branding: { bsonType: "object" },
        sections: { bsonType: "array" },
        conditionals: { bsonType: "array" },
        generated_tocs: { bsonType: "array" },
        version_history: { bsonType: "array" },
        last_modified: { bsonType: "date" }
      }
    }
  }
});

// Submittal archives
db.createCollection("submittal_archives", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      properties: {
        _id: { bsonType: "objectId" },
        submittal_id: { bsonType: "long" },
        archive_data: { bsonType: "object" },
        original_file_path: { bsonType: "string" },
        archived_date: { bsonType: "date" },
        archived_by: { bsonType: "long" }
      }
    }
  }
});

// Event log for real-time features
db.createCollection("event_log", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      properties: {
        _id: { bsonType: "objectId" },
        event_type: { bsonType: "string" },
        user_id: { bsonType: "long" },
        resource_id: { bsonType: "long" },
        event_data: { bsonType: "object" },
        timestamp: { bsonType: "date" }
      }
    }
  }
});

// Create indexes for common queries
db.document_metadata.createIndex({ "document_id": 1 });
db.document_metadata.createIndex({ "keywords": 1 });
db.ai_analysis_results.createIndex({ "submittal_id": 1 });
db.ai_analysis_results.createIndex({ "created_at": -1 });
db.template_configurations.createIndex({ "template_id": 1 });
db.submittal_archives.createIndex({ "submittal_id": 1 });
db.submittal_archives.createIndex({ "archived_date": -1 });
db.event_log.createIndex({ "timestamp": -1 });
db.event_log.createIndex({ "user_id": 1, "timestamp": -1 });
```

---

## Redis Key Naming Convention

```
# Session management
session:{user_id}:{session_id} -> session_data (TTL: 7 days)
refresh_token:{token_hash} -> user_id (TTL: 7 days)
access_token_blacklist:{token_hash} -> 1 (TTL: 15 minutes)

# Cache
template:{template_id}:v{version} -> template_json (TTL: 1 hour)
document:{document_id}:metadata -> metadata_json (TTL: 24 hours)
product:{product_id}:documents -> document_ids_json (TTL: 12 hours)

# Rate limiting
rate_limit:{user_id}:{endpoint} -> count (TTL: 1 hour)

# Queues
celery_queue:pdf_generation -> task_ids
celery_queue:ai_analysis -> task_ids
celery_queue:email_delivery -> task_ids

# Real-time updates
websocket:user:{user_id}:notifications -> notification_queue

# Statistics (for fast dashboard queries)
stats:daily:{date}:submittals_generated -> count
stats:daily:{date}:documents_processed -> count
stats:monthly:{year}:{month}:revenue -> amount
```

---

## Data Relationships Summary

```
users (1) ─── (n) user_roles ─── (n) roles ─── (n) role_permissions
    │
    ├─── (1) (n) documents
    ├─── (1) (n) submittals
    └─── (1) (n) templates

products (1) ─── (n) documents
    │
    ├─── (n) templates
    └─── (n) submittals

templates (1) ─── (n) template_sections
    │
    └─── (n) submittals

submittals (1) ─── (n) submittal_audit
    │
    ├─── (n) compliance_statements
    └─── (1) (n) compliance_analysis_history

documents (1) ─── (n) document_versions
    │
    └─── (1) (n) compliance_requirements
```


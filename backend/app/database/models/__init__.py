"""ORM models package.

Importing this package registers every model on the shared ``Base.metadata``
so that ``Base.metadata.create_all()`` and Alembic autogenerate see them all.
"""
from app.database.models.users import (
    Permission,
    Role,
    User,
    UserSession,
    role_permissions,
    user_roles,
)
from app.database.models.products import Product
from app.database.models.documents import Document, DocumentVersion
from app.database.models.templates import Template, TemplateSection, TemplateVersion
from app.database.models.submittals import Submittal, SubmittalAudit
from app.database.models.compliance import (
    ComplianceAnalysisHistory,
    ComplianceRequirement,
    ComplianceStatement,
)
from app.database.models.common import AuditLog, Metric, SystemSetting

__all__ = [
    "User",
    "Role",
    "Permission",
    "UserSession",
    "user_roles",
    "role_permissions",
    "Product",
    "Document",
    "DocumentVersion",
    "Template",
    "TemplateSection",
    "TemplateVersion",
    "Submittal",
    "SubmittalAudit",
    "ComplianceStatement",
    "ComplianceRequirement",
    "ComplianceAnalysisHistory",
    "AuditLog",
    "Metric",
    "SystemSetting",
]

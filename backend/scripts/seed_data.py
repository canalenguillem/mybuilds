"""Idempotent seed script: roles, permissions, and the initial admin user.

Run inside the backend container:
    docker compose exec backend python scripts/seed_data.py
"""
import os
import sys

# Ensure the app package (one level up, /app) is importable when this script is
# run directly as `python scripts/seed_data.py`.
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import select

from app.config import settings
from app.database.base import Base
from app.database.session import SessionLocal, engine
import app.database.models  # noqa: F401  (register all models)
from app.database.models.users import (
    ROLE_ADMIN,
    ROLE_OPERATOR,
    ROLE_REVIEWER,
    ROLE_VIEWER,
    Permission,
    Role,
    User,
)
from app.utils.security import hash_password

ROLE_DEFS = {
    ROLE_ADMIN: "Full system access: user, template and document management.",
    ROLE_OPERATOR: "Generate submittals and manage documents.",
    ROLE_REVIEWER: "Review AI-generated compliance statements.",
    ROLE_VIEWER: "View and download generated submittals.",
}

# (name, resource, action)
PERMISSION_DEFS = [
    ("manage_users", "users", "manage"),
    ("manage_templates", "templates", "manage"),
    ("upload_document", "documents", "create"),
    ("manage_documents", "documents", "manage"),
    ("create_submittal", "submittals", "create"),
    ("view_submittal", "submittals", "read"),
    ("review_compliance", "compliance", "review"),
    ("view_analytics", "analytics", "read"),
]

# Which permissions each role receives.
ROLE_PERMISSIONS = {
    ROLE_ADMIN: [p[0] for p in PERMISSION_DEFS],
    ROLE_OPERATOR: ["upload_document", "manage_documents", "create_submittal", "view_submittal", "view_analytics"],
    ROLE_REVIEWER: ["review_compliance", "view_submittal"],
    ROLE_VIEWER: ["view_submittal"],
}


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        # Permissions
        perms: dict[str, Permission] = {}
        for name, resource, action in PERMISSION_DEFS:
            perm = db.scalar(select(Permission).where(Permission.name == name))
            if not perm:
                perm = Permission(name=name, resource=resource, action=action)
                db.add(perm)
            perms[name] = perm
        db.flush()

        # Roles + role→permission mapping
        roles: dict[str, Role] = {}
        for name, description in ROLE_DEFS.items():
            role = db.scalar(select(Role).where(Role.name == name))
            if not role:
                role = Role(name=name, description=description)
                db.add(role)
            role.permissions = [perms[p] for p in ROLE_PERMISSIONS[name]]
            roles[name] = role
        db.flush()

        # Admin user
        admin = db.scalar(select(User).where(User.email == settings.seed_admin_email))
        if not admin:
            admin = User(
                email=settings.seed_admin_email,
                username=settings.seed_admin_username,
                password_hash=hash_password(settings.seed_admin_password),
                full_name="System Administrator",
                company="myBuilds",
            )
            admin.roles = [roles[ROLE_ADMIN]]
            db.add(admin)
            print(f"Created admin user: {settings.seed_admin_email}")
        else:
            print(f"Admin user already exists: {settings.seed_admin_email}")

        db.commit()
        print("Seed complete: %d roles, %d permissions." % (len(roles), len(perms)))
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    try:
        seed()
    except Exception as exc:  # pragma: no cover
        print(f"Seed failed: {exc}", file=sys.stderr)
        sys.exit(1)

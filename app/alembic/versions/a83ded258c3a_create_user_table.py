"""create_user_table

Revision ID: a83ded258c3a
Revises: 4d51e007db62
Create Date: 2024-08-26 12:58:59.304426

"""
from typing import Sequence, Union
from uuid import uuid4
from datetime import datetime, timezone
from alembic import op
import sqlalchemy as sa

from schemas.user import get_password_hash
from settings import ADMIN_DEFAULT_PASSWORD

# revision identifiers, used by Alembic.
revision: str = 'a83ded258c3a'
down_revision: Union[str, None] = '4d51e007db62'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    user_table = op.create_table(
        'users',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column("email", sa.String, unique=True, nullable=True, index=True),
        sa.Column("username", sa.String, unique=True, index=True),
        sa.Column("first_name", sa.String),
        sa.Column("last_name", sa.String),
        sa.Column("password", sa.String),
        sa.Column("is_active", sa.Boolean, default=True),
        sa.Column("is_admin", sa.Boolean, default=False),
        sa.Column("company_id", sa.UUID, nullable=True),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_index("idx_usr_fst_lst_name", "users", ["first_name", "last_name"])
    op.create_foreign_key(
        "fk_user_company",
        "users",
        "companies",
        ["company_id"],
        ["id"]
    )
    # Data seed for first user
    op.bulk_insert(user_table, [
        {
            "id": uuid4(),
            "email": "trido@gmail.com", 
            "username": "admin",
            "password": get_password_hash(ADMIN_DEFAULT_PASSWORD),
            "first_name": "Tri",
            "last_name": "Do",
            "is_active": True,
            "is_admin": True,
            "created_at": datetime.now(timezone.utc),
            "updated_at": datetime.now(timezone.utc)
        }
    ])


def downgrade() -> None:
    op.drop_constraint('fk_user_company', 'users', type_='foreignkey')
    op.drop_table('users')

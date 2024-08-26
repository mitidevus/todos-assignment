"""create_task_table

Revision ID: a33e351b977d
Revises: a83ded258c3a
Create Date: 2024-08-26 13:23:52.500750

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from schemas.task import TaskStatus, TaskPriority

# revision identifiers, used by Alembic.
revision: str = 'a33e351b977d'
down_revision: Union[str, None] = 'a83ded258c3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'tasks',
        sa.Column('id', sa.UUID, nullable=False, primary_key=True),
        sa.Column("summary", sa.String, nullable=False),
        sa.Column("description", sa.String, nullable=False),
        sa.Column("status", sa.Enum(TaskStatus), nullable=False, default=TaskStatus.TODO),
        sa.Column("priority", sa.Enum(TaskPriority), nullable=False, default=TaskPriority.LOW),
        sa.Column("user_id", sa.UUID, nullable=False),
        sa.Column('created_at', sa.DateTime),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_foreign_key(
        "fk_task_user",
        "tasks",
        "users",
        ["user_id"],
        ["id"]
    )
    

def downgrade() -> None:
    op.drop_constraint('fk_task_user', 'tasks', type_='foreignkey')
    op.drop_table('tasks')
    op.execute("DROP TYPE taskstatus;")
    op.execute("DROP TYPE taskpriority;")
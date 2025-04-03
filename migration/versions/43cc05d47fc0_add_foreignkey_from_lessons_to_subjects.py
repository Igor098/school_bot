"""Add ForeignKey from lessons to subjects

Revision ID: 43cc05d47fc0
Revises: 69971255bfca
Create Date: 2025-04-03 15:46:01.739558

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '43cc05d47fc0'
down_revision: Union[str, None] = '69971255bfca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    with op.batch_alter_table("lessons") as batch_op:
        batch_op.add_column(sa.Column("subject_id", sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_lessons_subjects", "subjects", ["subject_id"], ["id"])


def downgrade():
    with op.batch_alter_table("lessons") as batch_op:
        batch_op.drop_constraint("fk_lessons_subjects", type_="foreignkey")
        batch_op.drop_column("subject_id")

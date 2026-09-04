"""embedding metadata compatibility guard

Revision ID: 0002_embedding_metadata
Revises: 0001_initial
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_embedding_metadata"
down_revision = "0001_initial"
branch_labels = None
depends_on = None

def upgrade():
    op.add_column("materials", sa.Column("embedding_provider", sa.String(40), nullable=True))
    op.add_column("materials", sa.Column("embedding_model", sa.String(120), nullable=True))
    op.add_column("materials", sa.Column("embedding_dimensions", sa.Integer(), nullable=True))

def downgrade():
    op.drop_column("materials", "embedding_dimensions")
    op.drop_column("materials", "embedding_model")
    op.drop_column("materials", "embedding_provider")

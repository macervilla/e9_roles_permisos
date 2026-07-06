"""estructura inicial

Revision ID: 3314f422a11f
Revises:
Create Date: 2026-07-04
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = "3314f422a11f"
down_revision: Union[str, Sequence[str], None] = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "roles",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(50), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=True),
    )

    op.create_table(
        "cargos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=True),
    )

    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("usuario", sa.String(50), nullable=False),
        sa.Column("clave", sa.String(255), nullable=False),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("rol_id", sa.Integer(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["rol_id"], ["roles.id"]),
        sa.UniqueConstraint("usuario"),
    )

    op.create_table(
        "docentes",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("nombre", sa.String(100), nullable=False),
        sa.Column("cargo_id", sa.Integer(), nullable=False),
        sa.Column("activo", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["cargo_id"], ["cargos.id"]),
    )


def downgrade() -> None:
    op.drop_table("docentes")
    op.drop_table("usuarios")
    op.drop_table("cargos")
    op.drop_table("roles")

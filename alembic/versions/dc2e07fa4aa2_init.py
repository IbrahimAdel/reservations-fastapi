"""init

Revision ID: dc2e07fa4aa2
Revises: 
Create Date: 2023-07-22 12:10:33.344503

"""
import enum

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'dc2e07fa4aa2'
down_revision = None
branch_labels = None
depends_on = None


class Role(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"


def upgrade() -> None:
    op.create_table(
        "restaurants",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("name", sa.String(80), nullable=False, unique=True),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now(), onupdate=sa.func.now()),
    )

    op.create_table(
        "tables",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("number", sa.Integer, nullable=False, default=1),
        sa.Column("capacity", sa.Integer, default=4),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("restaurant_id", sa.Integer, sa.ForeignKey("restaurants.id", onupdate="cascade", ondelete="cascade"))
    )
    op.create_unique_constraint("restaurant_id_table_number_unique", "tables", ['number', 'restaurant_id'],
                                schema='public')
    op.execute("CREATE INDEX tables_restaurant_id_index on tables USING HASH(restaurant_id)")

    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("number", sa.String(4), default="0000"),
        sa.Column("email", sa.String(55), unique=True),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column("role", sa.Enum(Role), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("restaurant_id", sa.Integer, sa.ForeignKey("restaurants.id", onupdate="cascade", ondelete="cascade"))
    )
    op.create_unique_constraint("restaurant_table_uc1", "users", ['number', 'restaurant_id'], schema='public')
    op.execute("CREATE INDEX users_restaurant_id_index on users USING HASH(restaurant_id)")

    op.create_table(
        "reservations",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("start", sa.TIMESTAMP(timezone=False), nullable=False, index=True),
        sa.Column("end", sa.TIMESTAMP(timezone=False), nullable=False, index=True),
        sa.Column("capacity_needed", sa.Integer(), nullable=False),
        sa.Column("created_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now()),
        sa.Column("updated_at", sa.TIMESTAMP(timezone=False), server_default=sa.func.now(), onupdate=sa.func.now()),
        sa.Column("restaurant_id", sa.Integer, sa.ForeignKey("restaurants.id", onupdate="cascade", ondelete="cascade")),
        sa.Column("table_id", sa.Integer, sa.ForeignKey("tables.id", onupdate="cascade", ondelete="SET NULL"),
                  index=True)
    )
    op.execute("CREATE INDEX reservations_restaurant_id_index on reservations USING HASH(restaurant_id)")


def downgrade() -> None:
    op.drop_table("reservations")
    op.drop_table("tables")
    op.drop_table("users")
    op.drop_table("restaurants")
    op.execute("""DROP TYPE role""")

"""create gpt3 results table

Revision ID: 7924e4f14118
Revises:
Create Date: 2020-08-30 13:23:18.808434

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "7924e4f14118"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "gpt3_results",
        sa.Column("result_id", sa.Text(), nullable=False),
        sa.Column("experiment_name", sa.Text(), nullable=False),
        sa.Column("api_params", sa.JSON()),
        sa.Column("response_time", sa.Float()),
        sa.Column("output_response", sa.Text()),
        sa.Column("language", sa.Text()),
        sa.Column("nlp_task", sa.Text()),
        sa.Column("error_msg", sa.Text()),
        sa.Column(
            "created_at",
            sa.DateTime,
            nullable=False,
            server_default="(now() at time zone 'IST')",
        ),
        sa.Column(
            "updated_at",
            sa.DateTime,
            nullable=False,
            server_default="(now() at time zone 'IST')",
        ),
    )
    op.create_index("gpt3_results_result_id", "gpt3_results", ["result_id"], unique=True)


def downgrade():
    op.drop_index("gpt3_results_result_id")
    op.drop_table("gpt3_results")

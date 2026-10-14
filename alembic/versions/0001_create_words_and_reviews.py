"""Create words and reviews tables."""
from alembic import op
import sqlalchemy as sa

revision = "0001_words_reviews"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        "words",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("word", sa.String(length=200), nullable=False),
        sa.Column("definition", sa.Text(), nullable=False),
        sa.Column("language", sa.String(length=80), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
    )
    op.create_index("ix_words_id", "words", ["id"])
    op.create_index("ix_words_word", "words", ["word"])
    op.create_index("ix_words_language", "words", ["language"])
    op.create_table(
        "reviews",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("word_id", sa.Integer(), nullable=False),
        sa.Column("review_date", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("interval", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("easiness_factor", sa.Float(), nullable=False, server_default="2.5"),
        sa.Column("repetition", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("next_review", sa.DateTime(), nullable=False),
        sa.CheckConstraint("score BETWEEN 0 AND 5", name="ck_reviews_score_range"),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_reviews_id", "reviews", ["id"])
    op.create_index("ix_reviews_word_id", "reviews", ["word_id"])
    op.create_index("ix_reviews_next_review", "reviews", ["next_review"])

def downgrade():
    op.drop_index("ix_reviews_next_review", table_name="reviews")
    op.drop_index("ix_reviews_word_id", table_name="reviews")
    op.drop_index("ix_reviews_id", table_name="reviews")
    op.drop_table("reviews")
    op.drop_index("ix_words_language", table_name="words")
    op.drop_index("ix_words_word", table_name="words")
    op.drop_index("ix_words_id", table_name="words")
    op.drop_table("words")

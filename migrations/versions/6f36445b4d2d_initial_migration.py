"""Initial migration

Revision ID: 6f36445b4d2d
Revises: 
Create Date: 2024-06-30 19:27:54.790509

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f36445b4d2d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables
    op.create_table(
        'pizzas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('ingredients', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'restaurant_pizzas',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('price', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table(
        'restaurants',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('address', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    # Drop tables in reverse order
    op.drop_table('restaurants')
    op.drop_table('restaurant_pizzas')
    op.drop_table('pizzas')

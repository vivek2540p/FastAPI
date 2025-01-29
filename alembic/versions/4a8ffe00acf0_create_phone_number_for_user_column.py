"""create phone number for user column

Revision ID: 4a8ffe00acf0
Revises: 
Create Date: 2025-01-27 15:12:18.435210

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a8ffe00acf0'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# alembic upgrade 4a8ffe00acf0
def upgrade() -> None:
    op.add_column('users',sa.Column('phone_number',sa.String(),nullable=True))



# alembic downgrade -1
def downgrade() -> None:
    op.drop_column('users','phone_number')

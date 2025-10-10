import databases
import sqlalchemy
from datetime import datetime
from app.core.config import settings


# Database setup
database = databases.Database(settings.database_url)
metadata = sqlalchemy.MetaData()

# Define the JSON store table
json_store = sqlalchemy.Table(
    "json_store",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.String, primary_key=True),
    sqlalchemy.Column("data", sqlalchemy.Text, nullable=False),
    sqlalchemy.Column("created_at", sqlalchemy.DateTime, nullable=False, default=datetime.utcnow),
    sqlalchemy.Column("last_updated", sqlalchemy.DateTime, nullable=False, default=datetime.utcnow),
    sqlalchemy.Column("limit_counter", sqlalchemy.Integer, nullable=False, default=0),
    sqlalchemy.Column("max_updates", sqlalchemy.Integer, nullable=False, default=50),
)

# Create the SQLite engine and table if not exists
engine = sqlalchemy.create_engine(settings.database_url)
metadata.create_all(engine)


async def get_database() -> databases.Database:
    """Get database connection."""
    if not database.is_connected:
        await database.connect()
    return database

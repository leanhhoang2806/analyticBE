# models.py

from sqlalchemy import Column, String, DateTime, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# These data model generated through `sqlacodegen postgresql://postgres:password@localhost:5432/mydatabase` from command line

class S3File(Base):
    __tablename__ = 's3_files'

    id = Column(UUID(as_uuid=True), primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(255), nullable=False)
    created_at = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))
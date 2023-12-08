from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, text
import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://postgres:password@localhost:5432/mydatabase', echo=True)

# Define a base class for declarative models
Base = declarative_base()

class S3File(Base):
    __tablename__ = 's3_files'

    id = Column(UUID(as_uuid=True), primary_key=True)
    file_name = Column(String(255), nullable=False)
    file_url = Column(String(255), nullable=False)
    created_at = Column(DateTime(True), server_default=text("CURRENT_TIMESTAMP"))

# Create the table in the database
# Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Add new users to the database
user1 = S3File(id = uuid.uuid4(), file_name = "test.txt", file_url = "https://s3.amazonaws.com/bucket/test.txt")

session.add(user1)
session.commit()

# Query the users from the database
users = session.query(S3File).all()

# Display the results
for user in users:
    print(f"User {user}")

# Close the session
session.close()

# s3_files_manager.py

from sqlalchemy.orm import Session
from src.models.database_models import S3File  # Assuming you have a S3File model defined

import logging

logging.basicConfig(level=logging.INFO)
class S3FilesManager:
    def __init__(self, db: Session):
        self.db = db

    def create_s3_file(self, new_s3_file: S3File):
        self.db.add(new_s3_file)
        self.db.commit()
        self.db.refresh(new_s3_file)
        return new_s3_file

    def get_all_s3_files(self):
        return self.db.query(S3File).all()

    def get_s3_file_by_id(self, file_id: int):
        return self.db.query(S3File).filter(S3File.id == file_id).first()

    def update_s3_file(self, file_id: int, updated_data: dict):
        s3_file = self.get_s3_file_by_id(file_id)
        if s3_file:
            for key, value in updated_data.items():
                setattr(s3_file, key, value)
            self.db.commit()
            self.db.refresh(s3_file)
            return s3_file
        return None

    def delete_s3_file(self, file_id: int):
        s3_file = self.get_s3_file_by_id(file_id)
        if s3_file:
            self.db.delete(s3_file)
            self.db.commit()
            return True
        return False

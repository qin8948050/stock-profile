from abc import abstractmethod

from sqlalchemy.orm import Session
from typing import Generic, TypeVar, Type, Any, Union, List, Dict
from pydantic import BaseModel
from core.database import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)

# EAV (Entity-Attribute-Value) model type
EAVModelType = TypeVar("EAVModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], *, eav_model: Type[EAVModelType] = None, eav_fk_name: str = None):
        self.model = model
        # For repositories that use the EAV pattern
        self.eav_model = eav_model
        self.eav_fk_name = eav_fk_name

    def get(self, db: Session, id: int):
        return db.query(self.model).filter(self.model.id == id).first()

    def list(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.model).offset(skip).limit(limit).all()

    def count(self, db: Session) -> int:
        return db.query(self.model).count()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = obj_in.model_dump()
        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, id: int):
        obj = db.query(self.model).filter(self.model.id == id).first()
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def update(self):
        pass

    @abstractmethod
    def _upsert_single(self, db: Session, *, data: Dict[str, Any], **kwargs) -> ModelType:
        """
        Abstract method to upsert a single record from a dictionary.
        The implementation should handle the specific logic for a model
        but should NOT commit the transaction.
        """
        raise NotImplementedError

    def _save_eav_attributes(self, db: Session, *, core_obj: ModelType, data: Dict[str, Any], excluded_keys: set):
        """
        A generic helper method to save extra fields into an EAV table.
        This method should be called by `_upsert_single` in subclasses.
        """
        if not self.eav_model or not self.eav_fk_name:
            return  # This repository is not configured for EAV

        for key, value in data.items():
            if key not in excluded_keys:
                eav_data = {
                    "attribute_name": key,
                    self.eav_fk_name: core_obj.id
                }
                # Check for numeric vs. string values
                if isinstance(value, (int, float)) and not isinstance(value, bool):
                    eav_data["value_numeric"] = value
                else:
                    eav_data["value_string"] = str(value) if value is not None else None

                eav_obj = self.eav_model(**eav_data)
                db.add(eav_obj)

    def upsert_from_json(self, db: Session, *, data: Union[Dict[str, Any], List[Dict[str, Any]]], **kwargs) -> Union[ModelType, List[ModelType]]:
        """
        Upserts financial data from a JSON object or a list of JSON objects.
        This method orchestrates the upsert process and handles transactions.
        """
        if isinstance(data, list):
            results = [self._upsert_single(db, data=item, **kwargs) for item in data]
            db.commit()
            for res in results:
                db.refresh(res)
            return results
        elif isinstance(data, dict):
            result = self._upsert_single(db, data=data, **kwargs)
            db.commit()
            db.refresh(result)
            return result
        else:
            raise TypeError("Data must be a dictionary or a list of dictionaries")
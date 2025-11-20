from sqlalchemy.orm import Session, joinedload
from models.company import Company, IndustryProfile
from schemas.company import CompanyCreate, CompanyUpdate
from .base import BaseRepository
from typing import Any, Dict

class CompanyRepository(BaseRepository[Company]):
    def __init__(self):
        super().__init__(Company)

    def get(self, db: Session, id: int) -> Company:
        """
        Overrides the base get method to eager load the industry_profile relationship.
        """
        return db.query(self.model).options(joinedload(self.model.industry_profile)).filter(self.model.id == id).first()
    
    def create(self, db: Session, *, obj_in: CompanyCreate) -> Company:
        """
        Overrides the base create method to handle the nested industry_profile.
        """
        profile_data = obj_in.industry_profile.model_dump() if obj_in.industry_profile else {}
        company_data = obj_in.model_dump(exclude={'industry_profile'})

        db_obj = self.model(**company_data)

        if profile_data:
            db_obj.industry_profile = IndustryProfile(**profile_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(self, db: Session, *, db_obj: Company, obj_in: CompanyUpdate) -> Company:
        """
        Overrides the base update method to handle the nested industry_profile.
        """
        update_data = obj_in.model_dump(exclude_unset=True)
        
        # Update company fields
        for field, value in update_data.items():
            if field != 'industry_profile':
                setattr(db_obj, field, value)

        # Update industry profile
        if 'industry_profile' in update_data and update_data['industry_profile'] is not None:
            profile_update_data = update_data['industry_profile']
            if db_obj.industry_profile:
                for key, value in profile_update_data.items():
                    setattr(db_obj.industry_profile, key, value)
            else:
                db_obj.industry_profile = IndustryProfile(**profile_update_data)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_code(self, db, code: str):
        return db.query(self.model).filter(self.model.ticker == code).first()

def get_company_repo() -> CompanyRepository:
    return CompanyRepository()

from fastapi import HTTPException

from app.core.config import settings
from app.models.company_model import Company
from app.schemas.company_schemas import CompanyCreate, CompanyUpdate
from app.services.base_services import CRUDBase


class CRUDCompany(CRUDBase[Company, CompanyCreate, CompanyUpdate]):
    def count_company(self,data_search: str = None) -> int:
        if data_search:
            return self.engine.count(Company, Company.name.match(f".*{data_search}.*"))
        return self.engine.count(Company)

    def get_company(self, *, id: str) -> Company:
        company = super().get(id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company

    def get_company_by_name(self, *, name: str) -> Company:
        return self.engine.find_one(Company, Company.name == name)

    def get_company_by_domain(self, *, domain: str) -> Company:
        return self.engine.find_one(Company, Company.domain == domain)

    def get_companies(
            self, *, page: int = 0, page_break: bool = False, data_search: str = None
    ) -> list[Company]:
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        if data_search:
            cursor = self.engine.find(
                Company,
                Company.name.match(f".*{data_search}.*"),
                **offset,
                sort=Company.created.desc(),
            )
        else:
            cursor = self.engine.find(Company, **offset, sort=Company.created.desc())
        return list(cursor)

    def create_company(self, *, obj_in: CompanyCreate) -> Company:
        company = self.get_company_by_name(
            name=obj_in.name
        ) or self.get_company_by_domain(domain=obj_in.domain)
        if company:
            raise HTTPException(status_code=400, detail="Company already exists")
        return super().create(obj_in=obj_in)

    def update_company(self, *, id: str, obj_in: CompanyUpdate) -> Company:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        update_data = {
            k: v for k, v in update_data.items() if v is not None and v != ""
        }

        db_obj: Company = self.get_company(id=id)

        for field in list(update_data.keys()):  # Create a copy of keys
            value = update_data[field]
            # Dynamically access the model field
            model_field = getattr(Company, field, None)
            if model_field is not None:
                company = self.engine.find_one(Company, model_field == value)
                if company and company.id != db_obj.id:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Company with this {field} already exists",
                    )
                elif company and company.id == db_obj.id:
                    del update_data[field]

        # If nothing has changed, return the original db_obj without updating
        if not update_data:
            return db_obj

        return super().update(db_obj=db_obj, obj_in=update_data)

    def remove_company(self, *, id: str) -> None:
        return super().remove(id=id)


company_services = CRUDCompany(Company)

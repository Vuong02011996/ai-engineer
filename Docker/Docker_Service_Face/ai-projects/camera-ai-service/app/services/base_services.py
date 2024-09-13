from typing import Any, Dict, Generic, Optional, Type, TypeVar, Union
from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from odmantic import SyncEngine, ObjectId

from app.models.base_model import BaseModel as Base
from app.core.config import settings
from app.db.session import get_engine
from app.common.utils import datetime_now_sec

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**
        """
        self.model = model
        self.engine: SyncEngine = get_engine()

    def get(self, id: Any) -> Optional[ModelType]:
        try:
            id = ObjectId(id)
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid ID")
        return self.engine.find_one(self.model, self.model.id == id)

    def get_multi(self, *, page: int = 0, page_break: bool = False) -> list[ModelType]:
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        cursor = self.engine.find(self.model, **offset, sort=self.model.created.desc())
        return list(cursor)

    def create(self, *, obj_in: CreateSchemaType) -> ModelType:
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        return self.engine.save(db_obj)

    def clean_update_input(self, obj_in: Union[UpdateSchemaType, Dict[str, Any]]):
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        # Exclude empty fields
        update_data = {
            k: v for k, v in update_data.items() if v is not None and v != ""
        }
        return update_data

    def update(
            self, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        # Clean the input
        update_data = self.clean_update_input(obj_in)
        updated = False
        # Update time modified, if update_data is not empty
        for field in obj_data:
            if field in update_data:
                if obj_data[field] != update_data[field]:
                    updated = True
                    setattr(db_obj, field, update_data[field])
        try:
            if updated:
                db_obj.modified = datetime_now_sec()
        except Exception as e:
            pass
        # TODO: Check if this saves changes with the setattr calls
        self.engine.save(db_obj)
        return db_obj

    def remove(self, *, id: str) -> ModelType:
        db_obj = self.get(id=id)
        if not db_obj:
            raise HTTPException(status_code=404, detail="Not found")
        self.engine.delete(db_obj)

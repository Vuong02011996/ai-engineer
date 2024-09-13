from typing import Optional
from fastapi import HTTPException
from odmantic import ObjectId, query
import base64

from app.core.security import get_password_hash, verify_password
from app.core.config import settings
from app.services.base_services import CRUDBase
from app.models.user_model import User
from app.schemas.user_schemas import UserCreate, UserUpdate
from app.common.utils.minio_services import upload_services


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def upload_avatar(self, avatar: bytes, username: str) -> str:
        avatar_string = str(avatar)
        avatar_data = base64.b64decode(avatar_string.split(",")[1])
        try:
            avatar_url = upload_services.upload_file_form(
                name=username, contents=avatar_data, bucket="oryza-ai"
            )
        except Exception:
            print("Error uploading avatar")
            return ""
        return avatar_url

    def count_user(self, *, rq_user: User, data_search: str = None) -> int:
        search_query = (
            query.or_(
                User.username.match(f".*{data_search}.*"),
                User.email.match(f".*{data_search}.*"),
            )
            if data_search
            else None
        )
        if rq_user.is_superuser:
            base_query = {} if not data_search else search_query
        else:
            base_query = (
                query.and_(User.company == rq_user.company.id, search_query)
                if data_search
                else User.company == rq_user.company.id
            )
        return self.engine.count(User, base_query)

    def check_owner_or_admin(self, *, user: User, owner_id: str) -> None:
        # Check if the user is the owner or an admin
        if not (user.is_superuser or user.id == ObjectId(owner_id)):
            raise HTTPException(status_code=403, detail="Not enough permissions")

    def check_user_exist(
        self, username: Optional[str] = None, email: Optional[str] = None
    ):
        # Check user exist by username or email
        if username:
            user = self.engine.find_one(User, User.username == username)
            if user:
                raise HTTPException(status_code=400, detail="Username already used")
        if email:
            user = self.engine.find_one(User, User.email == email)
            if user:
                raise HTTPException(status_code=400, detail="Email already used")

    def get_by_username(self, *, username: str):
        return self.engine.find_one(User, User.username == username)

    def get_by_email(self, *, email: str):
        return self.engine.find_one(User, User.email == email)

    def get_user(self, *, user: User, id: str) -> User:
        find_user = super().get(id=id)
        if not find_user:
            raise HTTPException(status_code=404, detail="User not found")
        if not self.is_superuser(user) and user.id != find_user.id:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return find_user

    def get_by_id_raw(self, *, id: str) -> User:
        find_user = super().get(id=id)
        if not find_user:
            raise HTTPException(status_code=404, detail="User not found")
        return find_user

    def get_all(
        self,
        *,
        rq_user: User,
        page: int = 0,
        page_break: bool = False,
        data_search: str = None,
    ):
        offset = (
            {"skip": page * settings.MULTI_MAX, "limit": settings.MULTI_MAX}
            if page_break
            else {}
        )
        search_query = (
            query.or_(
                User.username.match(f".*{data_search}.*"),
                User.email.match(f".*{data_search}.*"),
            )
            if data_search
            else None
        )

        if rq_user.is_superuser:
            base_query = {} if not data_search else search_query
        else:
            base_query = (
                query.and_(User.company == rq_user.company.id, search_query)
                if data_search
                else User.company == rq_user.company.id
            )

        cursor = self.engine.find(
            self.model, base_query, **offset, sort=self.model.created.desc()
        )
        return cursor

    def create_user(self, *, obj_in: UserCreate, is_active) -> User:
        from app.services.company_services import company_services

        print("obj_in", obj_in)
        self.check_user_exist(obj_in.username, obj_in.email)
        user_in = obj_in.model_dump()
        # if user is super user, it is admin
        if user_in.get("is_superuser"):
            user_in["is_admin"] = True
        # Hash the password
        hashed_password = get_password_hash(obj_in.password)
        del user_in["password"]
        user_in["hashed_password"] = hashed_password
        # Check if company is valid
        if user_in.get("company_id"):
            company = company_services.get_company(id=user_in["company_id"])
            user_in["company"] = company
        user_in["is_active"] = is_active

        # Upload the avatar
        if obj_in.avatar:
            user_in["avatar"] = self.upload_avatar(obj_in.avatar, obj_in.username)

        # Create the user
        return super().create(obj_in=User(**user_in))

    def update_user(self, *, id: str, obj_in: UserUpdate) -> User:
        # Just take the data that is not None
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)
        update_data = {
            k: v for k, v in update_data.items() if v is not None and v != ""
        }
        # Get the user
        db_obj: User = self.get_by_id_raw(id=id)
        # Check if new username is used
        if update_data.get("username"):
            name_used_user: User = self.get_by_username(
                username=update_data["username"]
            )
            if name_used_user:
                if name_used_user.id != db_obj.id:
                    raise HTTPException(status_code=400, detail="Username already used")
                else:
                    del update_data["username"]
        # Check if password is being updated
        # If so, check if the current password is correct
        if update_data.get("current_password"):
            if not verify_password(
                plain_password=update_data["current_password"],
                hashed_password=db_obj.hashed_password,
            ):
                raise HTTPException(
                    status_code=400, detail="Wrong username or password"
                )
            # Update with the new password
            hashed_password = get_password_hash(update_data["new_password"])
            del update_data["current_password"]
            del update_data["new_password"]
            update_data["hashed_password"] = hashed_password
        # New email, invalidate email validation
        if update_data.get("email") and db_obj.email != update_data["email"]:
            update_data["email_validated"] = False
        # Upload the avatar
        if obj_in.avatar:
            update_data["avatar"] = self.upload_avatar(obj_in.avatar, db_obj.username)
        # If nothing has changed, return the original db_obj without updating
        if not update_data:
            return db_obj
        # Everything else updates as normal
        return super().update(db_obj=db_obj, obj_in=update_data)

    def update_user_by_admin(self, *, id: str, obj_in: UserUpdate) -> User:
        from app.services.company_services import company_services

        # Get the user
        db_obj: User = self.get_by_id_raw(id=id)
        update_data = obj_in.model_dump(exclude_unset=True)
        print("update_data", update_data)
        if obj_in.new_password:
            hashed_password = get_password_hash(obj_in.new_password)
            update_data["hashed_password"] = hashed_password
        if obj_in.avatar:
            update_data["avatar"] = self.upload_avatar(obj_in.avatar, db_obj.username)
        if obj_in.company:
            company = company_services.get_company(id=obj_in.company)
            update_data["company"] = company
        print("update_data", update_data)
        return super().update(db_obj=db_obj, obj_in=update_data)

    def remove_user(self, *, id: str):
        super().remove(id=id)

    def authenticate(self, *, email: str, password: str) -> Optional[User]:
        email = email.lower()
        user = self.get_by_email(email=email) or self.get_by_username(username=email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if not verify_password(
            plain_password=password, hashed_password=user.hashed_password
        ):
            return None
        return user

    #  def validate_email(self, db: AgnosticDatabase, *, db_obj: User) -> User:
    #     obj_in = UserUpdate(**UserInDB.model_validate(db_obj).model_dump())
    #     obj_in.email_validated = True
    #     return  self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    #  def activate_totp(self, db: AgnosticDatabase, *, db_obj: User, totp_in: NewTOTP) -> User:
    #     obj_in = UserUpdate(**UserInDB.model_validate(db_obj).model_dump())
    #     obj_in = obj_in.model_dump(exclude_unset=True)
    #     obj_in["totp_secret"] = totp_in.secret
    #     return  self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    #  def deactivate_totp(self, db: AgnosticDatabase, *, db_obj: User) -> User:
    #     obj_in = UserUpdate(**UserInDB.model_validate(db_obj).model_dump())
    #     obj_in = obj_in.model_dump(exclude_unset=True)
    #     obj_in["totp_secret"] = None
    #     obj_in["totp_counter"] = None
    #     return  self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    #  def update_totp_counter(
    #     self, db: AgnosticDatabase, *, db_obj: User, new_counter: int
    # ) -> User:
    #     obj_in = UserUpdate(**UserInDB.model_validate(db_obj).model_dump())
    #     obj_in = obj_in.model_dump(exclude_unset=True)
    #     obj_in["totp_counter"] = new_counter
    #     return  self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    #  def toggle_user_state(
    #     self, db: AgnosticDatabase, *, obj_in: Union[UserUpdate, Dict[str, Any]]
    # ) -> User:
    #     db_obj =  self.get_by_email(db, email=obj_in.email)
    #     if not db_obj:
    #         return None
    #     return  self.update(db=db, db_obj=db_obj, obj_in=obj_in)

    @staticmethod
    def has_password(user: User) -> bool:
        return user.hashed_password is not None

    @staticmethod
    def is_active(user: User) -> bool:
        if not user:
            return False
        return user.is_active

    @staticmethod
    def is_superuser(user: User) -> bool:
        if not user:
            return False
        return user.is_superuser

    @staticmethod
    def is_admin(user: User) -> bool:
        if not user:
            return False
        return user.is_admin

    @staticmethod
    def is_email_validated(user: User) -> bool:
        return user.email_validated


user_services = CRUDUser(User)

from fastapi import APIRouter, Depends
from app.schemas.base_schemas import Msg, Count
from app.models.user_model import User
from app.schemas.user_schemas import (
    UserOut,
    UserCreate,
    UserUpdate,
    UserRegister,
    UserUpdateMe,
    ListUserOut,
)

from app.services.user_services import user_services
from app.api import deps

router = APIRouter()


# CREATE USER
def create_user(request: UserCreate, is_active: bool = True) -> UserOut:
    user: User = user_services.create_user(obj_in=request, is_active=is_active)
    return user


@router.post("/register", response_model=UserOut, status_code=201)
def register(
    request: UserRegister,
) -> UserOut:
    """
    Create new user without the need to be logged in.
    """
    user = create_user(request, is_active=False)
    return user


@router.post(
    "/create",
    response_model=UserOut,
    status_code=201,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def create_user_by_admin(request: UserCreate) -> UserOut:
    """
    Create new user, only for superuser.
    """
    user = create_user(request)
    return user


# READ USER
@router.get("/get/me", response_model=UserOut, status_code=200)
def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> UserOut:
    """
    Get current user.
    """
    return current_user


@router.get(
    "/get_all",
    status_code=200,
    response_model=ListUserOut,
)
def get_users(
    page: int = 0,
    page_break: bool = False,
    current_user: User = Depends(deps.get_current_active_admin),
    data_search: str = None,
):
    """
    Get all users, paginated.
    """
    return {
        "data": user_services.get_all(
            rq_user=current_user,
            page=page,
            page_break=page_break,
            data_search=data_search,
        )
    }


@router.get(
    "/count",
    status_code=200,
    response_model=Count,
)
def count_users(
    current_user: User = Depends(deps.get_current_active_admin),
    data_search: str = None,
) -> Count:
    return {
        "count": user_services.count_user(rq_user=current_user, data_search=data_search)
    }


@router.get("/get_by_id/{user_id}", response_model=UserOut, status_code=200)
def read_user(
    user_id: str,
    current_user: User = Depends(deps.get_current_user),
) -> UserOut:
    """
    Get user by ID, only for the user themselves or an admin.
    """
    # Check permission
    return user_services.get_user(user=current_user, id=user_id)


# UPDATE USER
@router.put("/update/me", response_model=UserOut, status_code=200)
def update_user_me(
    request: UserUpdateMe,
    current_user: User = Depends(deps.get_current_user),
) -> UserOut:
    """
    Update current user.
    """
    return user_services.update_user(id=current_user.id, obj_in=request)


@router.put("/update_by_id/{user_id}", response_model=UserOut, status_code=200)
def update_user(
    user_id: str,
    request: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> UserOut:
    """
    Update a user by user ID, only for the user themselves or an admin.
    """
    # Check permission
    if current_user.is_admin:
        # requester = RoleEnum.admin
        # if current_user.is_superuser:
        #     requester = RoleEnum.superuser
        # print("requester", requester.name)
        return user_services.update_user_by_admin(id=user_id, obj_in=request)
    print("requester: normal user")
    return user_services.update_user(id=user_id, obj_in=request, requester=current_user)


# DELETE USER
@router.delete(
    "/delete_by_id/{user_id}",
    status_code=200,
    response_model=Msg,
    dependencies=[Depends(deps.get_current_active_admin)],
)
def delete_user(user_id: str) -> Msg:
    """
    Delete a user, only for superuser.
    """
    user_services.remove_user(id=user_id)
    return Msg(msg="User deleted")

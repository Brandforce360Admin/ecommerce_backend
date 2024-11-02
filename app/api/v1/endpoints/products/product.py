from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.user_application import UserApplication
from app.dependencies import get_user_application
from app.domain.models.users import UserRole
from app.domain.security.authenticate_authorise import AuthenticationAndAuthorisation
from app.domain.value_objects.ids.session_id import SessionId

router = APIRouter()


@router.delete("/add")
def add_product(user_id: UUID, session_id: SessionId = Depends(AuthenticationAndAuthorisation(UserRole.admin)),
                user_application: UserApplication = Depends(get_user_application)):
    pass


@router.get("/list", response_model=None)
def get_product_list():
    pass


@router.get("/{product_id}/details", response_model=None)
def get_product_item_details():
    pass


@router.put("/{product_id}/details", response_model=None)
def update_product_item_details():
    pass


@router.delete("/{product_id}/details", response_model=None)
def delete_product_item_details():
    pass

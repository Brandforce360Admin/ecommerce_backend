from uuid import UUID

from fastapi import APIRouter, Depends

from app.application.cart_application import CartApplication
from app.dependencies import get_cart_application
from app.domain.models.users import UserRole
from app.domain.security.authenticate_authorise import AuthenticationAndAuthorisation
from app.domain.value_objects.ids.product_id import ProductId
from app.domain.value_objects.ids.session_id import SessionId
from app.domain.value_objects.ids.user_id import UserId
from app.domain.value_objects.quantity import Quantity

router = APIRouter()


@router.post("/add", response_model=None)
def add_product_to_user_cart():
    pass


@router.get("/details", response_model=None)
def get_user_cart():
    pass


@router.delete("/empty", response_model=None)
def empty_user_cart():
    pass


@router.delete("/products/{product_id}/details", response_model=None)
def remove_product_from_user_cart():
    pass


@router.put("/products/{product_id}/details", response_model=None)
def update_product_for_user_cart():
    pass

from fastapi import APIRouter

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

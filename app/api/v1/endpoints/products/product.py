from fastapi import APIRouter

router = APIRouter()


@router.post("/add", response_model=None)
def add_product():
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

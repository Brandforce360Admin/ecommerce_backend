from app.domain.models.addresses import Address
from app.domain.value_objects.ids.user_id import UserId


class UserAddressApplication:
    def __init__(self):
        pass

    def add_user_address(self, user_id: UserId, address: Address):
        pass

    def get_user_addresses(self, user_id: UserId, ):
        pass

    def delete_user_address(self, user_id: UserId, address_id: Address):
        pass

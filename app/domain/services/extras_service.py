from typing import Dict

from app.domain.excptions.extras_exceptions import ExtraDoesNotExistsException, ExtraNotAvailableException
from app.domain.models.extras import Extra
from app.domain.value_objects.quantity import Quantity


class ExtrasService:
    def __init__(self, extras_repository):
        self.extras_repository = extras_repository

    def check_existence_and_return_extras_dict(self, extras: Dict[Extra, Quantity]) -> Dict[Extra, Quantity]:
        updated_extra_quantity_dictionary = {}
        if extras:
            for extra in extras:
                db_extra = self.extras_repository.get_extra(extra)
                if db_extra is None:
                    raise ExtraDoesNotExistsException(f"Extra with extra id {extra.extra_id} does not exists")
                else:
                    if db_extra.is_available:
                        updated_extra_quantity_dictionary[db_extra] = extras[extra]
                    else:
                        raise ExtraNotAvailableException(f"Product with product id {extra.extra_id} is not available")
            return updated_extra_quantity_dictionary

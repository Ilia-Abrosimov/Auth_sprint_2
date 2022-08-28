def not_found_error(model: str, item_id: str) -> str:
    return f'{model.capitalize()} with id = {item_id} not found'


INVALID_PAGINATION_PositiveInt_ERROR = 'ensure this value is greater than 0'

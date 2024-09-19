import functools

from flask import request


class ResourceValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def validate_resource(fields_to_check):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if request.method in ['POST', 'PUT']:
                request_data = request.get_json()
                empty_fields = [field for field in fields_to_check if not request_data or not request_data.get(field)]
                if empty_fields:
                    raise ResourceValidationError(f"Invalid resource, missing or empty fields: {', '.join(empty_fields)}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

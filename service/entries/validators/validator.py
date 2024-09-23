from fastapi import Request, HTTPException, Depends


class ResourceValidationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def validate_fields(fields_to_check: list):
    async def dependency(request: Request):
        data = await request.json()
        empty_fields = [field for field in fields_to_check if not data or not data.get(field)]
        if empty_fields:
            raise ResourceValidationError(f"Invalid resource, missing or empty fields: {', '.join(empty_fields)}")

    return dependency

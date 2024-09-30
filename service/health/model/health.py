from pydantic import BaseModel


class Health(BaseModel):
    status: str = 'OK'
    message: str = 'Service is up and running'

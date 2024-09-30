from typing import Optional

from pydantic import BaseModel, constr


class Entry(BaseModel):
    id: Optional[str] = None
    title: constr(min_length=1)

    @staticmethod
    def from_json(json_data):
        return Entry(**json_data)

    def to_json(self):
        return self.model_dump()

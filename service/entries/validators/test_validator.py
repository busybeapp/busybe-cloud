from typing import Dict, Any

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from hamcrest import assert_that, is_
from starlette.responses import JSONResponse

from service.entries.validators.validator import validate_fields, \
    ResourceValidationError

app = FastAPI()


@app.exception_handler(ResourceValidationError)
async def handle_validation_error(request, exc: ResourceValidationError):
    return JSONResponse(status_code=400, content={"error": exc.message})


@app.post('/api/me', response_model=dict, status_code=201,
          dependencies=[Depends(validate_fields(['first_name', 'surname']))])
async def create_entry(test_profile: Dict[str, Any]):
    return {"message": "Resource is valid"}


@pytest.fixture
def client():
    return TestClient(app)


@pytest.mark.asyncio
async def test_post_request_with_required(client):
    response = client.post('/api/me', json={"first_name": "kuku", "surname": "popo"})
    assert_that(response.status_code, is_(201))
    assert_that(response.json(), is_({"message": "Resource is valid"}))


@pytest.mark.asyncio
async def test_post_request_without_surname(client):
    response = client.post('/api/me', json={"first_name": "kuku"})
    assert_that(response.status_code, is_(400))
    print(response.json())
    assert_that(response.json(), is_({"error": "Invalid resource, missing or empty fields: surname"}))


@pytest.mark.asyncio
async def test_post_request_missing_required(client):
    response = client.post('/api/me', json={})
    assert_that(response.status_code, is_(400))
    assert_that(response.json(), is_({"error": "Invalid resource, missing or empty fields: first_name, surname"}))

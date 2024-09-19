import pytest
from flask import Flask, jsonify, request
from hamcrest import assert_that, is_

from service.entries.validators.validator import ResourceValidationError
from service.entries.validators.validator import validate_resource

app = Flask(__name__)


@app.errorhandler(ResourceValidationError)
def handle_validation_error(error):
    response = jsonify({"error": error.message})
    response.status_code = 400
    return response


@app.route('/api/me', methods=['POST', 'GET'])
@validate_resource(['first_name', 'surname'])
def entries():
    if request.method == 'POST':
        return jsonify({"message": "Resource is valid"}), 201
    elif request.method == 'GET':
        return jsonify([]), 200


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_post_request_with_required(client):
    response = client.post('/api/me', json={"first_name": "kuku", "surname": "popo"})
    assert_that(response.status_code, is_(201))
    assert_that(response.get_json(), is_({"message": "Resource is valid"}))


def test_post_request_without_surname(client):
    response = client.post('/api/me', json={"first_name": "kuku"})
    assert_that(response.status_code, is_(400))
    assert_that(response.get_json(), is_({"error": "Invalid resource, missing or empty fields: surname"}))


def test_post_request_missing_required(client):
    response = client.post('/api/me', json={})
    assert_that(response.status_code, is_(400))
    assert_that(response.get_json(), is_({"error": "Invalid resource, missing or empty fields: first_name, surname"}))


def test_get_entries(client):
    response = client.get('/api/me')
    assert_that(response.status_code, is_(200))
    assert_that(response.get_json(), is_([]))

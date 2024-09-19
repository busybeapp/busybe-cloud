import os

from dotenv import load_dotenv
from flask import Flask, request, jsonify

from service.entries.persistence.driver import EntriesDriver
from service.entries.validators.validator import validate_resource, ResourceValidationError
from service.health.health_response import HealthResponse

app = Flask(__name__)

load_dotenv()

persistence = EntriesDriver()


@app.route('/api/health', methods=['GET'])
def health():
    return HealthResponse().to_client(), 202


@app.errorhandler(ResourceValidationError)
def handle_validation_error(error):
    response = jsonify({"error": error.message})
    response.status_code = 400
    return response


@app.route('/api/entries', methods=['POST', 'GET'])
@validate_resource(['title'])
def entries():
    if request.method == 'POST':
        persisted_entry = persistence.add_entry(request.get_json())
        return persisted_entry.to_json(), 201
    elif request.method == 'GET':
        return jsonify(persistence.get_entries()), 202


if __name__ == '__main__':
    app.run(host=os.getenv("ENDPOINT", 'localhost'), port=os.getenv("PORT", 8080))

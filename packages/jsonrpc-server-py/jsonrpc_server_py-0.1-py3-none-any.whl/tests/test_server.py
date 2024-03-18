# tests/test_server.py
import pytest
import subprocess
import time
import requests
import json

SERVER_URL = "http://localhost:8000"

@pytest.fixture(scope="session", autouse=True)
def server():
    # Start the server fixture as a subprocess
    server_process = subprocess.Popen(["python", "server_fixture.py"])
    time.sleep(1)  # Adjust as necessary to allow the server time to start

    yield server_process

    # Terminate the server process when the tests are done
    server_process.terminate()
    server_process.wait()


def test_sum_method():
    response = requests.post(SERVER_URL, json={"jsonrpc": "2.0", "method": "sum", "params": [2, 3], "id": 1})
    assert response.status_code == 200
    assert json.loads(response.text)["result"] == 5


def test_hello_method():
    response = requests.post(SERVER_URL, json={"jsonrpc": "2.0", "method": "hello", "params": ["World"], "id": 2})
    assert response.status_code == 200
    assert json.loads(response.text)["result"] == "Hello, World!"


def test_ping_method():
    response = requests.post(SERVER_URL, json={"jsonrpc": "2.0", "method": "ping", "params": [], "id": 1})
    assert response.status_code == 200
    assert response.json()["result"] == "pong", "Expected response result to be 'pong'"


def post_json_rpc(method, params=None, id=None):
    """Helper function to send JSON-RPC requests and return the response."""
    payload = {"jsonrpc": "2.0", "method": method}
    if params is not None:
        payload["params"] = params
    if id is not None:
        payload["id"] = id
    headers = {'Content-Type': 'application/json'}
    return requests.post(SERVER_URL, json=payload, headers=headers)


def test_invalid_jsonrpc_version():
    response = requests.post(SERVER_URL, json={"jsonrpc": "1.0", "method": "ping", "id": 1})
    assert response.status_code == 400, "Server should respond with a 400 status code for invalid JSON-RPC version."
    assert "error" in response.json(), "Response should contain an error object."
    assert response.json()["error"]["code"] == -32600, "Server should respond with error code -32600 for invalid JSON-RPC version."


def test_method_not_found():
    response = post_json_rpc("nonexistent_method", id=1)
    assert response.status_code == 400
    assert response.json()["error"]["code"] == -32601, "Server should respond with error code -32601 for method not found."


def test_invalid_request_object():
    response = requests.post(SERVER_URL, data="This is not a valid JSON-RPC request", headers={'Content-Type': 'application/json'})
    assert response.status_code == 400
    assert response.json()["error"]["code"] == -32700, "Server should respond with error code -32700 for invalid JSON."


def test_notification_support():
    # This test assumes 'ping' method exists and is a valid notification
    response = requests.post(SERVER_URL, json={"jsonrpc": "2.0", "method": "ping"}, headers={'Content-Type': 'application/json'})
    
    assert response.status_code in [200, 204], "Expected no response or a 204 status code for notification"
    assert not response.content, "Expected empty response body for notification"


@pytest.mark.parametrize("params", [
    ([42, 23]),  # positional arguments
    ({"a": 42, "b": 23})  # named arguments
])
def test_parameter_structures(params):
    response = post_json_rpc("sum", params=params, id=1)
    assert response.status_code == 200
    assert response.json()["result"] == 65, "Server should correctly sum the parameters."


def test_batch_requests():
    batch_data = [
        {"jsonrpc": "2.0", "method": "sum", "params": [2, 3], "id": 1},
        {"jsonrpc": "2.0", "method": "hello", "params": ["World"], "id": 2},
        {"jsonrpc": "2.0", "method": "ping"},  # Notification
    ]

    response = requests.post(SERVER_URL, json=batch_data, headers={'Content-Type': 'application/json'})
    assert response.status_code == 200

    responses = json.loads(response.text)
    assert len(responses) == 2  # Only responses with IDs are included
    assert responses[0]["result"] == 5  # Use integer index 0
    assert responses[1]["result"] == "Hello, World!"  # Use integer index 1

def test_batch_request_with_malformed_json():
    batch_data = "[{\"jsonrpc\": \"2.0\", \"method\": \"sum\", \"params\": [1, 2], \"id\": 1},"  # Missing closing bracket

    response = requests.post(SERVER_URL, data=batch_data, headers={'Content-Type': 'application/json'})
    assert response.status_code == 400

    error_response = response.json()
    assert error_response["error"]["code"] == -32700  # Parse error


def test_batch_request_with_invalid_jsonrpc_version():
    batch_data = [
        {"jsonrpc": "2.0", "method": "sum", "params": [1, 2], "id": 1},
        {"jsonrpc": "1.0", "method": "hello", "params": ["World"], "id": 2}  # Invalid JSON-RPC version
    ]

    response = requests.post(SERVER_URL, json=batch_data)
    assert response.status_code == 200

    responses = response.json()
    assert len(responses) == 2  # Expect responses for both requests

    # Check that the second request has an error for invalid JSON-RPC version
    assert any(r.get("error") and r.get("error").get("code") == -32600 for r in responses)


def test_batch_request_with_non_existent_method():
    batch_data = [
        {"jsonrpc": "2.0", "method": "sum", "params": [1, 2], "id": 1},
        {"jsonrpc": "2.0", "method": "nonExistentMethod", "params": [], "id": 2}
    ]

    response = requests.post(SERVER_URL, json=batch_data)
    assert response.status_code == 200

    responses = response.json()
    assert len(responses) == 2  # Responses for both, including the error

    # Check for method not found error
    assert any(r.get("error") and r.get("error").get("code") == -32601 for r in responses)


def test_empty_batch_request():
    batch_data = []

    response = requests.post(SERVER_URL, json=batch_data)
    assert response.status_code == 200

    responses = response.json()
    assert len(responses) == 0  # No responses expected

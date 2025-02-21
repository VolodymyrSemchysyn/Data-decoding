from http import client

import pytest
from starlette.testclient import TestClient

from src.main import app

client = TestClient(app)


@pytest.fixture
def sample_file(tmp_path):
    """Creates a temporary file for testing."""
    file_path = tmp_path / "test_file.bin"
    with open(file_path, "wb") as f:
        f.write(b"MIR\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")
        f.write(b"PRR\x00\x00\x00\x01\x00")
    return str(file_path)


def test_upload_file(sample_file):
    """Tests successful file upload."""
    with open(sample_file, "rb") as f:
        response = client.post("/api/data/upload_file", files={"file": ("test_file.bin", f)})
    assert response.status_code == 200
    assert "decoded_data" in response.json()


def test_edit_file_success(sample_file):
    """Tests successful file update."""
    response = client.post("/api/data/edit", json={
        "filename": sample_file,
        "operator": "Operator1",
        "temperature": 25,
        "tests": [
            {
                "type": "PRR",
                "pass_fail": 1,
                "part_number": 3
            },
            {
                "type": "PTR",
                "test_name": "Test1",
                "test_value": 10.5,
                "low": 5.0,
                "high": 15.0,
                "pass_fail": 1
            }
        ]
    })
    assert response.status_code == 200
    assert response.json() == {"message": "File updated successfully"}


def test_edit_file_not_found():
    """Tests handling case when file is not found."""
    response = client.post("/api/data/edit", json={
        "filename": "non_existent_file.bin",
        "operator": "Operator1",
        "tests": []
    })
    assert response.status_code == 404
    assert response.json() == {"detail": "File not found"}


def test_read_file(sample_file):
    """Tests successful file reading."""
    response = client.get("/api/data/read", params={"filename": sample_file})
    assert response.status_code == 200
    assert "decoded_data" in response.json()


def test_download_file(sample_file):
    """Tests successful file download."""
    response = client.get("/api/data/download", params={"filename": sample_file})
    assert response.status_code == 200
    assert (
        response.headers["content-disposition"].startswith("attachment; filename=") or
        response.headers["content-disposition"].startswith("attachment; filename*=")
    )

import pytest
from app import create_app
from unittest.mock import patch


@pytest.fixture
def client():
    app = create_app()
    app.testing = True
    with app.test_client() as client:
        yield client


@patch('app.s3_utils.list_photos', return_value=['photo1.jpg', 'photo2.jpg'])
def test_home_page(mock_list_photos, client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'photo1.jpg' in response.data
    assert b'photo2.jpg' in response.data


@patch('app.s3_utils.upload_to_s3')
@patch('app.db.add_photo_record')
def test_upload(mock_add_photo_record, mock_upload_to_s3, client):
    data = {
        'file': (open('tests/test_photo.jpg', 'rb'), 'test_photo.jpg')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 302  # Redirect after successful upload
    mock_upload_to_s3.assert_called_once()
    mock_add_photo_record.assert_called_once_with('test_photo.jpg')
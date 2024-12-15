import pytest
from unittest.mock import patch, MagicMock
from app.s3_utils import upload_to_s3, list_photos
from app.db import add_photo_record


@pytest.fixture
def mock_s3_client():
    with patch('app.s3_utils.get_s3_client') as mock_client:
        yield mock_client.return_value


@pytest.fixture
def mock_db():
    with patch('app.db.get_db') as mock_client:
        yield mock_client.return_value


def test_upload_to_s3(mock_s3_client):
    file = MagicMock()
    file.filename = 'test_photo.jpg'

    upload_to_s3(file)

    mock_s3_client.upload_fileobj.assert_called_once_with(file, 'djans-photos-bucket', 'test_photo.jpg')


# def test_list_photos(mock_s3_client):
#     mock_s3_client.list_objects_v2.return_value = {
#         'Contents': [{'Key': 'photo1.jpg'}, {'Key': 'photo2.jpg'}]
#     }

#     photos = list_photos()

#     assert photos == ['photo1.jpg', 'photo2.jpg']

def test_list_photos(mock_s3_client):
    # Mock the list_objects_v2 response
    mock_s3_client.list_objects_v2.return_value = {
        'Contents': [{'Key': 'photo1.jpg'}, {'Key': 'photo2.jpg'}]
    }
    
    # Mock the generate_presigned_url method
    mock_s3_client.generate_presigned_url.side_effect = lambda operation_name, Params, ExpiresIn: \
        f"https://presigned-url/{Params['Key']}"

    photos = list_photos()

    expected_photos = [
        {'key': 'photo1.jpg', 'url': 'https://presigned-url/photo1.jpg'},
        {'key': 'photo2.jpg', 'url': 'https://presigned-url/photo2.jpg'}
    ]
    assert photos == expected_photos

                                            
def test_add_photo_record(mock_db):
    mock_cursor = MagicMock()
    mock_db.cursor.return_value = mock_cursor

    add_photo_record('test_photo.jpg')

    mock_cursor.execute.assert_called_once_with("INSERT INTO photos (photo_name) VALUES (%s)", ('test_photo.jpg',))
    mock_db.commit.assert_called_once()
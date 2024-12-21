import pytest
from app import create_app
import boto3
from moto import mock_aws
import pymysql

@pytest.fixture
def test_db():
    """Set up test database"""
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='mysecurepassword',
        charset='utf8mb4'
    )
    cursor = connection.cursor()
    
    # Create test database and table
    cursor.execute('DROP DATABASE IF EXISTS photoDB_test')
    cursor.execute('CREATE DATABASE photoDB_test')
    cursor.execute('USE photoDB_test')
    cursor.execute('''
        CREATE TABLE photos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    connection.commit()
    
    yield connection
    
    # Cleanup
    cursor.execute('DROP DATABASE IF EXISTS photoDB_test')
    connection.commit()
    connection.close()

@pytest.fixture
def client(s3_bucket, test_db):
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_upload(client, s3_bucket, test_db):
    # Create test photo file
    with open('tests/test_photo.jpg', 'w') as f:
        f.write('test photo data')
    
    # Prepare file upload
    with open('tests/test_photo.jpg', 'rb') as f:
        data = {
            'file': (f, 'test_photo.jpg')
        }
        response = client.post('/upload', data=data, content_type='multipart/form-data')
    
    assert response.status_code == 302  # Redirect after successful upload
    
    # Verify S3 upload
    objects = s3_bucket.list_objects_v2(Bucket='test-photos-bucket')
    assert any(obj['Key'] == 'test_photo.jpg' for obj in objects.get('Contents', []))
    
    # Verify database record
    cursor = test_db.cursor()
    cursor.execute('SELECT photo_name FROM photos WHERE photo_name = %s', ('test_photo.jpg',))
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == 'test_photo.jpg'
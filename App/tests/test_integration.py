import pytest
from app import create_app
from unittest.mock import patch
import boto3
from moto import mock_aws

@pytest.fixture(autouse=True)
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    import os
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'
    os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'

@pytest.fixture
def s3_bucket():
    """Create a test S3 bucket."""
    with mock_aws():
        s3 = boto3.client('s3')
        # Create the bucket without LocationConstraint for us-east-1
        s3.create_bucket(Bucket='test-photos-bucket')
        yield s3

@pytest.fixture
def client(s3_bucket):
    app = create_app(testing=True)
    with app.test_client() as client:
        yield client

def test_home_page(client, s3_bucket):
    # Upload a test file to S3
    s3_bucket.put_object(
        Bucket='test-photos-bucket',
        Key='photo1.jpg',
        Body=b'test data'
    )
    
    response = client.get('/')
    assert response.status_code == 200
    assert b'photo1.jpg' in response.data

def test_upload(client, s3_bucket):
    with open('tests/test_photo.jpg', 'w') as f:
        f.write('test photo data')
        
    data = {
        'file': (open('tests/test_photo.jpg', 'rb'), 'test_photo.jpg')
    }
    response = client.post('/upload', data=data, content_type='multipart/form-data')
    assert response.status_code == 302  # Redirect after successful upload
    
    # Verify the file was uploaded to S3
    objects = s3_bucket.list_objects_v2(Bucket='test-photos-bucket')
    assert any(obj['Key'] == 'test_photo.jpg' for obj in objects.get('Contents', []))
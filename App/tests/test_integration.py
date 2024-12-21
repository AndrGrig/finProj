import pytest
from test_config import setup_test_environment
from app import create_app
import boto3
import pymysql
from moto import mock_s3

@pytest.fixture(autouse=True)
def setup_env():
    setup_test_environment()
    # Set up mock S3
    with mock_s3():
        s3 = boto3.client('s3')
        s3.create_bucket(Bucket='test-photos-bucket')
        yield

@pytest.fixture
def test_db():
    # Set up test database
    conn = pymysql.connect(
        host='localhost',
        user='root',
        password='mysecurepassword'
    )
    cursor = conn.cursor()
    cursor.execute('CREATE DATABASE IF NOT EXISTS photoDB_test')
    cursor.execute('USE photoDB_test')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS photos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            photo_name VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    yield conn
    # Cleanup
    cursor.execute('DROP DATABASE photoDB_test')
    conn.close()
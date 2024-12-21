import os

def setup_test_environment():
    os.environ.update({
        'DATABASE_URL': 'mysql+pymysql://root:mysecurepassword@localhost/photoDB_test',
        'S3_BUCKET': 'test-photos-bucket',
        'FLASK_SECRET_KEY': 'test-secret-key'
    })
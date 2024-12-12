import boto3
import os

def get_s3_client():
    return boto3.client('s3')

def upload_to_s3(file):
    s3 = get_s3_client()
    bucket = os.getenv('S3_BUCKET', 'djans-photos-bucket')
    s3.upload_fileobj(file, bucket, file.filename)

def list_photos():
    s3 = get_s3_client()
    bucket = os.getenv('S3_BUCKET', 'djans-photos-bucket')
    response = s3.list_objects_v2(Bucket=bucket)
    return [item['Key'] for item in response.get('Contents', [])]
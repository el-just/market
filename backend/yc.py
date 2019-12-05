import uuid
import boto3
import os

def save_file(file_data):
    bucket = os.environ['MARKET_YC_BUCKET']
    key = '%s.%s'%(str(uuid.uuid4()), file_data.filename.split('.')[-1])

    session = boto3.session.Session()
    s3 = session.client(
        service_name='s3',
        endpoint_url='https://storage.yandexcloud.net',
        )

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=file_data.file,
        )

    return 'https://storage.yandexcloud.net/%s/%s'%(bucket, key)

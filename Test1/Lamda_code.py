import boto3
from datetime import datetime, timezone, timedelta

s3 = boto3.client("s3")

BUCKET_NAME = "YOUR_BUCKET_NAME"

# Testing
AGE_THRESHOLD = timedelta(minutes=2)

# Production
# AGE_THRESHOLD = timedelta(days=30)

def lambda_handler(event, context):
    now = datetime.now(timezone.utc)
    paginator = s3.get_paginator("list_objects_v2")
    deleted = []

    for page in paginator.paginate(Bucket=BUCKET_NAME):
        if "Contents" not in page:
            continue

        for obj in page["Contents"]:
            key = obj["Key"]
            last_modified = obj["LastModified"]

            if now - last_modified > AGE_THRESHOLD:
                s3.delete_object(Bucket=BUCKET_NAME, Key=key)
                print(f"Deleted: {key}")
                deleted.append(key)

    return {
        "statusCode": 200,
        "deleted": deleted
    }
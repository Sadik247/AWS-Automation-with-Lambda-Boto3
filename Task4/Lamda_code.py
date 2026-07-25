import boto3
from botocore.exceptions import ClientError

s3 = boto3.client("s3")
sns = boto3.client("sns")

SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:700800569732:S3PublicBucketAlerts"


def lambda_handler(event, context):

    buckets = s3.list_buckets()["Buckets"]

    public_buckets = []

    for bucket in buckets:

        bucket_name = bucket["Name"]

        reasons = []

        # -------------------------
        # Check Block Public Access
        # -------------------------
        try:
            response = s3.get_public_access_block(Bucket=bucket_name)

            config = response["PublicAccessBlockConfiguration"]

            if not all(config.values()):
                reasons.append("Block Public Access Disabled")

        except ClientError:
            reasons.append("Block Public Access Not Configured")

        # -------------------------
        # Check Bucket Policy
        # -------------------------
        try:
            policy = s3.get_bucket_policy_status(Bucket=bucket_name)

            if policy["PolicyStatus"]["IsPublic"]:
                reasons.append("Bucket Policy is Public")

        except ClientError:
            pass

        # -------------------------
        # Check Bucket ACL
        # -------------------------
        try:

            acl = s3.get_bucket_acl(Bucket=bucket_name)

            for grant in acl["Grants"]:

                grantee = grant.get("Grantee", {})

                uri = grantee.get("URI", "")

                if (
                    "AllUsers" in uri
                    or "AuthenticatedUsers" in uri
                ):
                    reasons.append("Bucket ACL is Public")
                    break

        except ClientError:
            pass

        # -------------------------
        # Publish Alert
        # -------------------------

        if reasons:

            message = f"""
Public S3 Bucket Found

Bucket Name:
{bucket_name}

Reason(s):
{', '.join(reasons)}
"""

            sns.publish(
                TopicArn=SNS_TOPIC_ARN,
                Subject="Public S3 Bucket Detected",
                Message=message,
            )

            print(f"Alert sent for {bucket_name}")

            public_buckets.append(bucket_name)

    return {
        "statusCode": 200,
        "body": public_buckets,
    }
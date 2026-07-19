# AWS Assignment 2: Automated EBS Snapshot Creation and Cleanup

## Objective

Automate Amazon EBS volume backups by creating snapshots, tagging them,
deleting snapshots older than a retention period, and scheduling the
process using Amazon EventBridge.

------------------------------------------------------------------------

## Architecture

``` text
Amazon EventBridge (Weekly)
        |
        v
AWS Lambda (Python 3.12)
        |
 +------+------+
 |             |
 v             v
Create      Describe
Snapshot    Snapshots
 |             |
 v             v
Add Tag    Check Age
               |
        Older than 30 days?
           |         |
          Yes        No
           |
           v
     Delete Snapshot
```

## Prerequisites

-   AWS Account
-   Existing EC2 instance or EBS Volume
-   IAM permissions for Lambda, EC2, IAM and EventBridge

## Step 1: Create or Identify an EBS Volume

1.  Open **EC2** in the AWS Console.
2.  Navigate to **Elastic Block Store → Volumes**.
3.  Copy the **Volume ID** (example: `vol-0abc123456789abcd`).

If you don't have a volume, launch a small EC2 instance and use its root
EBS volume.

## Step 2: Create an IAM Role

1.  Open **IAM → Roles → Create role**.
2.  Select **AWS Service**.
3.  Choose **Lambda**.
4.  Attach the managed policy `AWSLambdaBasicExecutionRole`.
5.  Name the role `LambdaEBSBackupRole`.
6.  Create the role.

## Step 3: Add an Inline Policy

Open the role and navigate to:

**Permissions → Add permissions → Create inline policy → JSON**

Paste:

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:CreateSnapshot",
        "ec2:DescribeSnapshots",
        "ec2:DeleteSnapshot",
        "ec2:CreateTags"
      ],
      "Resource": "*"
    }
  ]
}
```

Save it as **EBSSnapshotPolicy**.

## Step 4: Create the Lambda Function

-   Function Name: `EBSSnapshotCleanup`
-   Runtime: `Python 3.12`
-   Execution Role: `LambdaEBSBackupRole`

## Step 5: Lambda Code

Added in Lamda_code.py in Task2 folder

## Step 6: Create a Test Event

Create a test event named `backup-test` with:

``` json
{}
```

Run the Lambda manually.

## Step 7: Verify Snapshot Creation

Go to **EC2 → Snapshots** and verify:

-   New snapshot created
-   Tag `CreatedBy=Lambda-Backup` exists

## Step 8: Configure EventBridge

1.  Open **Amazon EventBridge**.
2.  Create a new scheduled rule.
3.  Schedule:

``` text
cron(0 2 ? * SUN *)
```

4.  Target: `EBSSnapshotCleanup` Lambda function.

## Step 9: Production Change

After testing, update:

``` python
RETENTION_DAYS = 30
```

Deploy again.

## Step 10: Verify

CloudWatch logs should show:

``` text
Created Snapshot: snap-xxxxxxxx
Deleted Snapshot: snap-yyyyyyyy
```

## Discussion Point

AWS Data Lifecycle Manager (DLM) is the preferred service for scheduled
EBS snapshot creation and retention because it is fully managed and
requires no code.

AWS Lambda is preferred when custom retention logic, cross-account or
cross-region copies, notifications, tagging rules, or integration with
other AWS services are required.

## Assignment Checklist

-   Created or identified an EBS volume
-   Created IAM role
-   Added EC2 snapshot permissions
-   Created Lambda function
-   Created and tagged snapshots
-   Deleted snapshots older than retention
-   Printed snapshot IDs
-   Scheduled with EventBridge
-   Tested manually
-   Verified in EC2 console
-   Added DLM discussion

# AWS Assignment: Automated S3 Bucket Cleanup (Objects Older Than 30 Days)

## Objective

Automate the deletion of stale objects from an Amazon S3 bucket using
AWS Lambda (Python 3.12+).

------------------------------------------------------------------------

# Architecture

``` text
        Upload Files
             |
             v
         Amazon S3 Bucket
             |
             v
      AWS Lambda (Python)
             |
     List Objects (Paginator)
             |
      Check LastModified
             |
      Older than Threshold?
         /             \
       Yes             No
        |               |
 Delete Object      Keep Object
```

------------------------------------------------------------------------

# Prerequisites

-   AWS Account
-   IAM permissions to create S3, IAM Roles and Lambda
-   Basic knowledge of AWS Console

------------------------------------------------------------------------

# Step 1: Create an S3 Bucket

1.  Open AWS Console.

2.  Search for **S3**.

3.  Click **Create bucket**.

4.  Enter a unique bucket name. Example:

        assignment-cleanup-sadik

5.  Select your preferred AWS Region.

6.  Leave default settings.

7.  Click **Create bucket**.

------------------------------------------------------------------------

# Step 2: Upload Test Files

1.  Open the bucket.
2.  Click **Upload**.
3.  Upload a file named `one.png,two.png,three.png`.
4.  Wait at least **3 minutes**.
5.  Upload another file named `new.png`.

> For testing, we'll use a 2-minute threshold instead of 30 days.

------------------------------------------------------------------------

# Step 3: Create an IAM Role

1.  Open **IAM**.

2.  Select **Roles** → **Create role**.

3.  Trusted entity:

    -   AWS Service
    -   Lambda

4.  Click **Next**.

5.  Attach the managed policy:

        AWSLambdaBasicExecutionRole

6.  Name the role:

        LambdaS3CleanupRole

7.  Create the role.

## Add Inline Policy

Open the role.

**Permissions** → **Add permissions** → **Create inline policy** →
**JSON**

Replace the contents with:

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME"
    },
    {
      "Effect": "Allow",
      "Action": "s3:DeleteObject",
      "Resource": "arn:aws:s3:::YOUR_BUCKET_NAME/*"
    }
  ]
}
```

Replace `YOUR_BUCKET_NAME` with your bucket name.

Name the policy:

    S3CleanupPolicy

------------------------------------------------------------------------

# Step 4: Create Lambda Function

1.  Open **AWS Lambda**.

2.  Click **Create function**.

3.  Choose **Author from scratch**.

4.  Function name:

        S3CleanupFunction

5.  Runtime:

        Python 3.12

6.  Execution role:

        Use an existing role

7.  Select:

        LambdaS3CleanupRole

8.  Click **Create function**.

------------------------------------------------------------------------

# Step 5: Lambda Code

Replace the default code with:

``` python
update the code with s3 bucket objet deletion with 2 minutes (for test) in real we have to update 30 days 
```

Click **Deploy**.

------------------------------------------------------------------------

# Step 6: Create a Test Event

1.  Click **Test**.

2.  Create a new event.

3.  Event name:

        cleanup-test

4.  Event JSON:

``` json
{}
```

Save.

------------------------------------------------------------------------

# Step 7: Run the Lambda Function

Click **Test**.

Expected response:

``` json
{
  "statusCode": 200,
  "deleted": [
    "one.png"
  ]
}
```

------------------------------------------------------------------------

# Step 8: Verify the Bucket

Open the S3 bucket.

Expected:

-   `old.png` deleted
-   `new.png` still exists

------------------------------------------------------------------------

# Step 9: Switch to Production

Change:

``` python
AGE_THRESHOLD = timedelta(minutes=2)
```

to:

``` python
AGE_THRESHOLD = timedelta(days=30)
```

Deploy again.

------------------------------------------------------------------------

# Step 10: Verify CloudWatch Logs

Open:

AWS Lambda → Monitor → View CloudWatch Logs

Expected log:

``` text
Deleted: old.png
```

------------------------------------------------------------------------

# Why Use a Paginator?

Amazon S3 returns a maximum of 1,000 objects per request.

Using:

``` python
paginator = s3.get_paginator("list_objects_v2")
```

ensures all objects are processed.

------------------------------------------------------------------------

# Timezone Handling

Always use:

``` python
datetime.now(timezone.utc)
```

This matches the timezone-aware `LastModified` values returned by S3.

------------------------------------------------------------------------

# Testing Scenario

  Time      Action
  --------- ----------------------------------
  3:00 PM   Upload old.png
  3:03 PM   Upload new.png
  3:04 PM   Run Lambda
  Result    old.png deleted, new.png remains

------------------------------------------------------------------------

# Discussion Point

**Why not use S3 Lifecycle Rules?**

S3 Lifecycle Rules are the preferred solution when objects need to be
deleted solely based on age because they are fully managed, require no
code, and have minimal operational overhead.

AWS Lambda should be used when deletion depends on custom business
logic, such as object prefixes, tags, metadata, integration with other
AWS services, sending notifications, or performing additional actions
before or after deletion.

------------------------------------------------------------------------

# Assignment Checklist

-   [x] Created an S3 bucket
-   [x] Uploaded test files
-   [x] Created an IAM role
-   [x] Added S3 permissions using an inline policy
-   [x] Created a Python 3.12 Lambda function
-   [x] Used an S3 paginator
-   [x] Compared LastModified with UTC time
-   [x] Deleted objects older than the threshold
-   [x] Printed deleted object names
-   [x] Tested successfully
-   [x] Updated threshold to 30 days
-   [x] Documented when Lambda is preferred over Lifecycle Rules

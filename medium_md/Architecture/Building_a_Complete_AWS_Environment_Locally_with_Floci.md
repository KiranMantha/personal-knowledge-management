---
title: "Building a Complete AWS Environment Locally with Floci"
url: https://medium.com/p/0c777918c48a
---

# Building a Complete AWS Environment Locally with Floci

[Original](https://medium.com/p/0c777918c48a)

# Building a Complete AWS Environment Locally with Floci

[![Harshal Jethwa](https://miro.medium.com/v2/resize:fill:64:64/1*dgKwLTM0CGfRIa4DR9_Gag.jpeg)](https://harshaljethwaa.medium.com/?source=post_page---byline--0c777918c48a---------------------------------------)

[Harshal Jethwa](https://harshaljethwaa.medium.com/?source=post_page---byline--0c777918c48a---------------------------------------)

6 min read

·

Jun 15, 2026

--

2

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D0c777918c48a&operation=register&redirect=https%3A%2F%2Faws.plainenglish.io%2Fbuilding-a-complete-aws-environment-locally-with-floci-0c777918c48a&source=---header_actions--0c777918c48a---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

Cloud engineers often want to learn AWS services, build event-driven architectures, test Terraform code, and practice CI/CD pipelines without spending money on cloud resources.

This is where LocalStack and Floci become extremely useful. They allow you to emulate cloud services locally and build real-world architectures directly on your laptop.

In this guide, we’ll build a complete event-driven AWS architecture consisting of:

```
S3 Bucket  
   |  
Lambda Function  
   |  
DynamoDB Table  
   |  
SNS Topic
```

The same concepts can later be deployed to a real AWS account without significant changes.

## Why Use Local Cloud Emulators?

Benefits include:

* No AWS costs
* Fast development cycles
* Offline development
* CI/CD testing
* Infrastructure as Code testing
* Safe experimentation
* Learning cloud services without risk

## Floci Setup

Floci with CLI:

```
# macOS using Homebrew  
brew install floci-io/floci/floci  
# macOS or Linux using curl  
curl -fsSL https://floci.io/install.sh | sh  
# Windows PowerShell  
iwr https://floci.io/install.ps1 | iex  
# Windows using Scoop  
scoop bucket add floci https://github.com/floci-io/scoop-floci  
scoop install floci  
# Start AWS emulator  
floci start  
# Export AWS environment variables  
eval $(floci env)
```

## Floci with Docker:-

```
# All 53 services on :4566  
docker run -d --name floci \  
  -p 4566:4566 \  
  -v /var/run/docker.sock:/var/run/docker.sock \  
  floci/floci:latest  
  
export AWS_ENDPOINT_URL=http://localhost:4566  
export AWS_ACCESS_KEY_ID=test  
export AWS_SECRET_ACCESS_KEY=test  
export AWS_DEFAULT_REGION=us-east-1
```

Create bucket:-

```
 aws --endpoint-url=http://localhost:4566 s3 mb s3://mybucket  
aws --endpoint-url=http://localhost:4566 s3 ls
```

Verify:

```
curl http://localhost:4566/_localstack/health
```

Press enter or click to view image in full size

![]()

## Create an S3 Bucket

Create bucket:

```
aws --endpoint-url=http://localhost:4566 s3 mb s3://devops-lab
```

Verify:

```
aws --endpoint-url=http://localhost:4566 s3 ls
```

Upload file:

```
echo "hello localstack" > test.txt  
aws --endpoint-url=http://localhost:4566 \  
s3 cp test.txt s3://devops-lab
```

List objects:

```
aws --endpoint-url=http://localhost:4566 \  
s3 ls s3://devops-lab
```

Press enter or click to view image in full size

![]()

## Create DynamoDB Table

Create table:

```
aws --endpoint-url=http://localhost:4566 dynamodb create-table \  
  --table-name UploadedFiles \  
  --attribute-definitions \  
      AttributeName=FileName,AttributeType=S \  
  --key-schema \  
      AttributeName=FileName,KeyType=HASH \  
  --billing-mode PAY_PER_REQUEST
```

Verify:

```
aws --endpoint-url=http://localhost:4566 \  
dynamodb list-tables
```

Insert data:

```
aws --endpoint-url=http://localhost:4566 dynamodb put-item \  
  --table-name UploadedFiles \  
  --item '{"FileName":{"S":"test.txt"}}'
```

Read data:

```
aws --endpoint-url=http://localhost:4566 dynamodb scan \  
  --table-name UploadedFiles
```

Press enter or click to view image in full size

![]()

## Create SQS Queue

Create queue:

```
aws --endpoint-url=http://localhost:4566 sqs create-queue \  
  --queue-name my-queue
```

List queues:

```
aws --endpoint-url=http://localhost:4566 sqs list-queues
```

Send message:

```
aws --endpoint-url=http://localhost:4566 sqs send-message \  
  --queue-url http://localhost:4566/000000000000/my-queue \  
  --message-body "Hello Queue"
```

Receive message:

```
aws --endpoint-url=http://localhost:4566 sqs receive-message \  
  --queue-url http://localhost:4566/000000000000/my-queue
```

Press enter or click to view image in full size

![]()

## Create SNS Topic

Create topic:

```
aws --endpoint-url=http://localhost:4566 sns create-topic \  
  --name FileAlerts
```

List topics:

```
aws --endpoint-url=http://localhost:4566 sns list-topics
```

Publish message:

```
aws --endpoint-url=http://localhost:4566 sns publish \  
  --topic-arn arn:aws:sns:us-east-1:000000000000:FileAlerts \  
  --message "File uploaded"
```

Press enter or click to view image in full size

![]()

## Create Lambda Function

Create project:

```
mkdir lambda  
cd lambda
```

Create:

```
# lambda_function.py  
def handler(event, context):  
    return {  
        "statusCode": 200,  
        "body": "Hello from LocalStack"  
    }
```

Package:

```
zip function.zip lambda_function.py
```

Create function:

```
aws --endpoint-url=http://localhost:4566 lambda create-function \  
  --function-name process-upload \  
  --runtime python3.11 \  
  --handler lambda_function.handler \  
  --zip-file fileb://function.zip \  
  --role arn:aws:iam::000000000000:role/lambda-role
```

Verify:

```
aws --endpoint-url=http://localhost:4566 lambda list-functions
```

Invoke function:

```
aws --endpoint-url=http://localhost:4566 lambda invoke \  
  --function-name process-upload \  
  --cli-binary-format raw-in-base64-out \  
  --payload '{}' \  
  output.json
```

## With Terraform:

Create:

```
provider "aws" {  
  region     = "us-east-1"  
  access_key = "test"  
  secret_key = "test"  
  
  skip_credentials_validation = true  
  skip_metadata_api_check     = true  
  skip_requesting_account_id  = true  
  
  s3_use_path_style = true  
  
  endpoints {  
    s3 = "http://localhost:4566"  
  }  
}  
  
resource "aws_s3_bucket" "demo" {  
  bucket = "terraform-demo"  
}
```

Deploy:

```
terraform init  
terraform apply
```

Verify:

```
aws --endpoint-url=http://localhost:4566 s3 ls
```

Press enter or click to view image in full size

![]()

## Building a Complete Event-Driven Architecture

A realistic architecture:

```
S3 Upload  
    |  
    v  
Lambda  
    |  
    v  
SQS Queue  
    |  
    v  
Lambda Consumer  
    |  
    v  
DynamoDB  
    |  
    v  
SNS Alert
```

This architecture teaches:

* Event-driven systems
* Serverless computing
* Messaging patterns
* NoSQL databases
* Monitoring workflows
* Cloud automation

## Using Floci

Floci extends local cloud development beyond AWS and supports multiple cloud providers.

## Step 1:- Start AWS emulator:

```
docker run --rm -p 4566:4566 floci/floci:latest
```

## Step 2: Create an S3 Bucket

Create bucket:

```
aws --endpoint-url=http://localhost:4566 s3 mb s3://devops-lab
```

Verify:

```
aws --endpoint-url=http://localhost:4566 s3 ls
```

Expected:

```
devops-lab
```

Upload a test file:

```
echo "hello localstack" > test.txt  
aws --endpoint-url=http://localhost:4566 \  
s3 cp test.txt s3://devops-lab
```

Verify:

```
aws --endpoint-url=http://localhost:4566 \  
s3 ls s3://devops-lab
```

## Step 3: Create DynamoDB Table

Create table:

```
aws --endpoint-url=http://localhost:4566 dynamodb create-table \  
  --table-name UploadedFiles \  
  --attribute-definitions \  
      AttributeName=FileName,AttributeType=S \  
  --key-schema \  
      AttributeName=FileName,KeyType=HASH \  
  --billing-mode PAY_PER_REQUEST
```

Verify:

```
aws --endpoint-url=http://localhost:4566 dynamodb list-tables
```

Expected:

```
{  
  "TableNames": [  
    "UploadedFiles"  
  ]  
}
```

Press enter or click to view image in full size

![]()

## Step 4: Create SNS Topic

Create topic:

```
aws --endpoint-url=http://localhost:4566 sns create-topic \  
  --name FileAlerts
```

Verify:

```
aws --endpoint-url=http://localhost:4566 sns list-topics
```

Save the Topic ARN.

Example:

```
arn:aws:sns:us-east-1:000000000000:FileAlerts
```

Press enter or click to view image in full size

![]()

## Step 5: Create Lambda Function

Create project directory:

```
mkdir lambda  
cd lambda
```

Create Lambda code:

```
import json  
import boto3  
  
ddb = boto3.resource(  
    "dynamodb",  
    endpoint_url="http://host.docker.internal:4566"  
)  
  
sns = boto3.client(  
    "sns",  
    endpoint_url="http://host.docker.internal:4566"  
)  
  
TABLE_NAME = "UploadedFiles"  
  
TOPIC_ARN = "arn:aws:sns:us-east-1:000000000000:FileAlerts"  
  
  
def handler(event, context):  
  
    print(event)  
  
    bucket = event["Records"][0]["s3"]["bucket"]["name"]  
  
    key = event["Records"][0]["s3"]["object"]["key"]  
  
    table = ddb.Table(TABLE_NAME)  
  
    table.put_item(  
        Item={  
            "FileName": key,  
            "Bucket": bucket  
        }  
    )  
  
    sns.publish(  
        TopicArn=TOPIC_ARN,  
        Message=f"File uploaded: {key}"  
    )  
  
    return {  
        "statusCode": 200  
    }Save as:
```

```
lambda_function.py
```

Package:

```
zip function.zip lambda_function.py
```

Create Lambda:

```
aws --endpoint-url=http://localhost:4566 lambda invoke `  
>>   --function-name process-upload `  
>>   --cli-binary-format raw-in-base64-out `  
>>   --payload file://event.json `  
>>   output.json
```

Verify:

```
aws --endpoint-url=http://localhost:4566 lambda list-functions
```

Press enter or click to view image in full size

![]()

## Step 6: Test Lambda

Create:

```
{  
  "Records": [  
    {  
      "s3": {  
        "bucket": {  
          "name": "devops-lab"  
        },  
        "object": {  
          "key": "test.txt"  
        }  
      }  
    }  
  ]  
}
```

Save as:

```
event.json
```

Invoke:

```
aws --endpoint-url=http://localhost:4566 lambda invoke `  
>>   --function-name process-upload `  
>>   --cli-binary-format raw-in-base64-out `  
>>   --payload file://event.json `  
>>   output.json
```

View result:

```
cat output.json
```

Press enter or click to view image in full size

![]()

## Step 7: Configure S3 Event Notifications

Create:

```
{  
  "LambdaFunctionConfigurations": [  
    {  
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:000000000000:function:process-upload",  
      "Events": ["s3:ObjectCreated:*"]  
    }  
  ]  
}
```

Save as:

```
notification.json
```

Apply:

```
aws --endpoint-url=http://localhost:4566 \  
s3api put-bucket-notification-configuration \  
--bucket devops-lab \  
--notification-configuration file://notification.json
```

Verify:

```
aws --endpoint-url=http://localhost:4566 \  
s3api get-bucket-notification-configuration \  
--bucket devops-lab
```

Press enter or click to view image in full size

![]()

## Step 8: Upload File and Trigger Workflow

Upload:

```
echo "Testing Event Driven Architecture" > file1.txt  
  
aws --endpoint-url=http://localhost:4566 \  
s3 cp file1.txt s3://devops-lab
```

This upload should trigger:

```
S3  
 |  
 v  
Lambda  
 |  
 +--> DynamoDB  
 |  
 +--> SNS
```

## Step 9: Verify Resources

Check bucket:

```
aws --endpoint-url=http://localhost:4566 \  
s3 ls s3://devops-lab
```

Check table:

```
aws --endpoint-url=http://localhost:4566 \  
dynamodb scan \  
--table-name UploadedFiles
```

Check SNS:

```
aws --endpoint-url=http://localhost:4566 \  
sns list-topics
```

Check Lambda:

```
aws --endpoint-url=http://localhost:4566 \  
lambda list-functions
```

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Floci enable cloud engineers to build and test sophisticated architectures without cloud costs. By combining S3, Lambda, SQS, DynamoDB, SNS, Terraform, and CI/CD tooling, you can gain hands-on experience with production-grade cloud patterns entirely from your laptop.

In this blog, we built a local AWS environment and implemented a serverless architecture using S3, Lambda, DynamoDB, and SNS.

In the next blog, we’ll build the same architecture using Azure services with Floci-AZ, followed by a Google Cloud implementation using Floci-GCP, allowing us to compare AWS, Azure, and GCP architectures side by side.

**Follow me :**

**Linkedin:** [**https://www.linkedin.com/in/harshaljethwa/**](https://www.linkedin.com/in/harshaljethwa/)

**GitHub:** [**https://github.com/HARSHALJETHWA19/**](https://github.com/HARSHALJETHWA19/)

**Twitter:** [**https://twitter.com/harshaljethwaa**](https://twitter.com/harshaljethwaa)

**Thank You!!!**
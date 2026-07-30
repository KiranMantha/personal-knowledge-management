---
title: publish docker image to ecr
topic: AWS
tags:
  - docker
  - ecr
source_type: hands-on
confidence: confirmed
created: '2026-07-29'
---
Reference link: https://www.youtube.com/watch?v=zs3tyVgiBQQ

Commands
------------
1. Build Docker Image
- `docker build -t test .`

2. Run container /w image
- `docker run -d --publish 8888:5000 test`

3. Login to ECR
- `aws ecr get-login-password --region <your-aws-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com`

4. Tag the version
- `docker tag test:latest <your-ecr-repo-uri>:<image-tag>`

5. Upload
- `docker push <your-ecr-repo-uri>:<image-tag>`

Policy Document
-----------
```json
//ECR
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "ecr:*",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor01",
            "Effect": "Allow",
            "Action": "ecr:GetAuthorizationToken",
            "Resource": "*"
        },
        {
            "Sid": "VisualEditor02",
            "Effect": "Allow",
            "Action": "ecr:InitiateLayerUpload",
            "Resource": "*"
        }
    ]
}
```

ECS
`arn:aws:iam::aws:policy/AmazonECS_FullAccess`

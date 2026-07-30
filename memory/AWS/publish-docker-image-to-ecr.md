---
type: Learning
title: publish docker image to ecr
topic: AWS
tags:
  - docker
  - ecr
status: stable
generated:
  by: 'human:kiran'
  at: '2026-07-30T07:06:37.379Z'
verified:
  - by: agent-kiran/seed-script
    at: '2026-07-30T07:06:37.379Z'
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

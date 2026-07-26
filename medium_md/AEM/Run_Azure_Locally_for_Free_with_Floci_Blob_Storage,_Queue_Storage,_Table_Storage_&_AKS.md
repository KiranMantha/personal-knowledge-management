---
title: "Run Azure Locally for Free with Floci: Blob Storage, Queue Storage, Table Storage & AKS"
url: https://medium.com/p/6b31abf05614
---

# Run Azure Locally for Free with Floci: Blob Storage, Queue Storage, Table Storage & AKS

[Original](https://medium.com/p/6b31abf05614)

# Run Azure Locally for Free with Floci: Blob Storage, Queue Storage, Table Storage & AKS

[![Harshal Jethwa](https://miro.medium.com/v2/resize:fill:64:64/1*dgKwLTM0CGfRIa4DR9_Gag.jpeg)](https://harshaljethwaa.medium.com/?source=post_page---byline--6b31abf05614---------------------------------------)

[Harshal Jethwa](https://harshaljethwaa.medium.com/?source=post_page---byline--6b31abf05614---------------------------------------)

6 min read

·

Jun 16, 2026

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D6b31abf05614&operation=register&redirect=https%3A%2F%2Faws.plainenglish.io%2Frun-azure-locally-for-free-with-floci-blob-storage-queue-storage-table-storage-aks-6b31abf05614&source=---header_actions--6b31abf05614---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

In my previous blog, I explored running **53 AWS services locally** using Floci without creating an AWS account or worrying about cloud bills.

This time, let’s do the same with **Microsoft Azure**.

In this guide you’ll learn how to:

* Run Azure services locally
* Create Blob Storage
* Create Queue Storage
* Create Table Storage
* Create an AKS Cluster
* Verify the Kubernetes Cluster
* Build a simple AKS Guestbook application

Everything runs **locally** using Floci.

## Prerequisites

* Docker Desktop
* Azure CLI
* Floci CLI

## Install Floci

```
iwr https://floci.io/install.ps1 | iex
```

Start Azure Emulator

```
floci az start
```

Verify

```
floci az status
```

Check logs

```
floci az logs
```

Press enter or click to view image in full size

![]()

Export Azure Storage connection string

```
floci az env
```

Copy the generated value into PowerShell

```
$env:AZURE_STORAGE_CONNECTION_STRING="YOUR_CONNECTION_STRING"
```

## Blob Storage

## Create Container

```
az storage container create `  
    --name images `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## List Containers

```
az storage container list `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

Press enter or click to view image in full size

![]()

## Upload Blob

```
echo "Hello Azure" > image.txt  
az storage blob upload `  
    --container-name images `  
    --name image.txt `  
    --file image.txt `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## List Blobs

```
az storage blob list `  
    --container-name images `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## Download Blob

```
az storage blob download `  
    --container-name images `  
    --name image.txt `  
    --file download.txt `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## Queue Storage

## Create Queue

```
az storage queue create `  
    --name processing `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## List Queues

```
az storage queue list `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

Press enter or click to view image in full size

![]()

## Send Message

```
az storage message put `  
    --queue-name processing `  
    --content "Processing image" `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

Press enter or click to view image in full size

![]()

## Peek Messages

```
az storage message peek `  
    --queue-name processing `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## Table Storage

## Create Table

```
az storage table create `  
    --name Images `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## List Tables

```
az storage table list `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

Press enter or click to view image in full size

![]()

## Insert Entity

```
az storage entity insert `  
    --table-name Images `  
    --entity PartitionKey=Images RowKey=1 File=image.txt Status=Uploaded `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

Press enter or click to view image in full size

![]()

## Query Table

```
az storage entity query `  
    --table-name Images `  
    --connection-string "$env:AZURE_STORAGE_CONNECTION_STRING"
```

## Creating an AKS Cluster

Unlike Azure, Floci currently provisions AKS through the Azure Resource Manager (ARM) REST API.

Create a file called **aks-create.ps1**

```
$body = @{  
    location = "eastus"  
    properties = @{  
        kubernetesVersion = "1.29"  
        dnsPrefix = "my-cluster-dns"  
        agentPoolProfiles = @(  
            @{  
                name = "nodepool1"  
                count = 1  
                vmSize = "Standard_DS2_v2"  
                osType = "Linux"  
                mode = "System"  
            }  
        )  
    }  
} | ConvertTo-Json -Depth 10  
Invoke-RestMethod `  
    -Method Put `  
    -Uri "http://localhost:4577/subscriptions/my-sub/resourceGroups/my-rg/providers/Microsoft.ContainerService/managedClusters/my-cluster?api-version=2024-04-01" `  
    -ContentType "application/json" `  
    -Body $body
```

Or

```
curl -s -X PUT \  
  "http://localhost:4577/subscriptions/my-sub/resourceGroups/my-rg/providers/Microsoft.ContainerService/managedClusters/my-cluster?api-version=2024-04-01" \  
  -H "Content-Type: application/json" \  
  -d '{  
    "location": "eastus",  
    "properties": {  
      "kubernetesVersion": "1.29",  
      "dnsPrefix": "my-cluster-dns",  
      "agentPoolProfiles": [  
        {  
          "name": "nodepool1",  
          "count": 1,  
          "vmSize": "Standard_DS2_v2",  
          "osType": "Linux",  
          "mode": "System"  
        }  
      ]  
    }  
  }'
```

Run

```
.\aks-create.ps1
```

Expected Response

```
id : /subscriptions/my-sub/resourceGroups/my-rg/providers/Microsoft.ContainerService/managedClusters/my-cluster  
provisioningState : Creating  
fqdn : floci-az-aks-xxxx:6443
```

## Verify AKS Cluster

Get Cluster Details

```
Invoke-RestMethod `  
"http://localhost:4577/subscriptions/my-sub/resourceGroups/my-rg/providers/Microsoft.ContainerService/managedClusters/my-cluster?api-version=2024-04-01"
```

Press enter or click to view image in full size

![]()

List AKS Clusters

```
Invoke-RestMethod `  
"http://localhost:4577/subscriptions/my-sub/providers/Microsoft.ContainerService/managedClusters?api-version=2024-04-01"
```

Verify k3s Container

```
docker ps --filter ancestor=rancher/k3s
```

Press enter or click to view image in full size

![]()

Verify Kubernetes API

```
curl.exe -k https://localhost:6443
```

Press enter or click to view image in full size

![]()

Expected

```
401 Unauthorized
```

This confirms the Kubernetes API server is running.

## Get Harshal Jethwa’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

Verify Node

```
docker exec floci-az-aks-abe17c02 kubectl get nodes
```

Press enter or click to view image in full size

![]()

Expected

```
NAME           STATUS   ROLES           AGE   VERSION  
eaee9db8f7a7   Ready    control-plane   v1.34.x+k3s
```

At this point we’ve successfully:

* Created an AKS resource locally
* Started a real k3s Kubernetes cluster
* Verified the control plane
* Verified the Kubernetes API

## Mini AKS Project — Guestbook Application

Now that the AKS cluster is ready, let’s build a simple Guestbook application.

Architecture

```
            User  
              │  
              ▼  
      Frontend (Flask)  
              │  
              ▼  
            Redis
```

This project demonstrates:

* Deployments
* Services
* Namespaces
* Scaling
* Rolling Updates
* Docker Images
* Kubernetes Networking

## Project Structure

```
aks-demo/  
├── app/  
│   ├── app.py  
│   ├── requirements.txt  
│   └── Dockerfile  
│  
├── k8s/  
│   ├── namespace.yaml  
│   ├── redis.yaml  
│   ├── app.yaml  
│   ├── service.yaml  
│   └── ingress.yaml  
│  
└── README.md
```

## app.py

```
from flask import Flask  
import redis  
app = Flask(__name__)  
r = redis.Redis(host="redis", port=6379)  
@app.route("/")  
def home():  
    count = r.incr("visits")  
    return f"Hello from AKS! Visitors: {count}"  
app.run(host="0.0.0.0", port=5000)
```

## requirements.txt

```
Flask  
redis  
gunicorn
```

## Dockerfile

```
FROM python:3.12-slim  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install -r requirements.txt  
COPY . .  
CMD ["gunicorn","-b","0.0.0.0:5000","app:app"]
```

## namespace.yaml

```
apiVersion: v1  
kind: Namespace  
metadata:  
  name: aks-demo
```

## redis.yaml

```
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: redis  
  namespace: aks-demo  
spec:  
  replicas: 1  
  selector:  
    matchLabels:  
      app: redis  
  template:  
    metadata:  
      labels:  
        app: redis  
    spec:  
      containers:  
      - name: redis  
        image: redis:7  
---  
apiVersion: v1  
kind: Service  
metadata:  
  name: redis  
  namespace: aks-demo  
spec:  
  selector:  
    app: redis  
  ports:  
  - port: 6379
```

## app.yaml

```
apiVersion: apps/v1  
kind: Deployment  
metadata:  
  name: flask-app  
  namespace: aks-demo  
spec:  
  replicas: 2  
  selector:  
    matchLabels:  
      app: flask  
  template:  
    metadata:  
      labels:  
        app: flask  
    spec:  
      containers:  
      - name: flask  
        image: aks-demo:latest  
        imagePullPolicy: Never  
        ports:  
        - containerPort: 5000
```

## service.yaml

```
apiVersion: v1  
kind: Service  
metadata:  
  name: flask-service  
  namespace: aks-demo  
spec:  
  type: NodePort  
  selector:  
    app: flask  
  ports:  
  - port: 80  
    targetPort: 5000
```

## Build the Docker Image

```
docker build -t aks-demo .  
docker tag aks-demo:latest <dockerhub-user>/aks-demo:latest  
docker push <dockerhub-user>/aks-demo:latest
```

## Deploy to AKS

Once you have extracted the kubeconfig from the Floci-managed k3s cluster (or Floci exposes it automatically in a future release), deploy the application using:

```
kubectl apply -f k8s/
```

## Verify

```
kubectl get all -n aks-demo
```

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

## Scale the Application

```
kubectl scale deployment flask-app \  
    --replicas=5 \  
    -n aks-demo
```

Press enter or click to view image in full size

![]()

## Perform a Rolling Update

```
kubectl set image deployment/flask-app \  
    flask=aks-demo:v2 \  
    -n aks-demo
```

## Roll Back

```
kubectl rollout undo deployment/flask-app \  
    -n aks-demo
```

## What We Learned

In this guide we successfully:

* Ran Azure locally using Floci
* Created Blob Storage
* Created Queue Storage
* Created Table Storage
* Provisioned an AKS resource using Azure ARM REST APIs
* Verified the underlying Kubernetes cluster
* Built a sample AKS Guestbook project structure
* Learned the Kubernetes resources required to deploy an application

**Follow me :**

**Linkedin:** [**https://www.linkedin.com/in/harshaljethwa/**](https://www.linkedin.com/in/harshaljethwa/)

**GitHub:** [**https://github.com/HARSHALJETHWA19/**](https://github.com/HARSHALJETHWA19/)

**Twitter:** [**https://twitter.com/harshaljethwaa**](https://twitter.com/harshaljethwaa)

**Thank You!!!**
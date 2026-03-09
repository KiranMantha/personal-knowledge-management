---
title: "Tekton: Build Simple Build Pipeline using Kubernetes Native CI/CD Tools"
url: https://medium.com/p/e7c5ce430ea1
---

# Tekton: Build Simple Build Pipeline using Kubernetes Native CI/CD Tools

[Original](https://medium.com/p/e7c5ce430ea1)

# Tekton: Build Simple Build Pipeline using Kubernetes Native CI/CD Tools

[![8grams](https://miro.medium.com/v2/resize:fill:64:64/1*e1sk8OEf_n-7CB9sBMJ2rg.png)](/?source=post_page---byline--e7c5ce430ea1---------------------------------------)

[8grams](/?source=post_page---byline--e7c5ce430ea1---------------------------------------)

5 min read

·

Nov 10, 2023

--

Listen

Share

More

Press enter or click to view image in full size

![]()

## Introduction

[**Tekton**](https://tekton.dev/?ref=8grams.tech) is an open-source project that provides Kubernetes-style resources for declaring CI/CD-style pipelines. It’s a flexible framework that can be integrated into existing Kubernetes environments, extending their functionality by incorporating robust CI/CD capabilities.

What sets [Tekton](https://tekton.dev/?ref=8grams.tech) apart is its highly modular and scalable design. Pipelines are defined as a collection of tasks, which are made up of steps — each running in its own container. This granular approach provides tremendous flexibility, making [Tekton](https://tekton.dev/?ref=8grams.tech) an attractive solution for diverse CI/CD use cases.

If you want to know more about Tekton, check this article from us below:

[## Tekton: The Open Source, Kubernetes-native CI/CD Tools

### Introduction

8grams.medium.com](/tekton-the-open-source-kubernetes-native-ci-cd-tools-55c49db53234?source=post_page-----e7c5ce430ea1---------------------------------------)

In this article, we’ll establish a basic build pipeline using Tekton. The pipeline will adhere to the following requirements:

* We’ll use GitHub as our code repository. For this example, the code is hosted at [https://github.com/8grams/caddy-example](https://github.com/8grams/caddy-example?ref=8grams.tech).
* An image will be built from the code on each push event, which includes commits and tag pushes.
* Pushes to the develop branch will trigger the creation of an image tagged as ‘latest’.
* Pushing a tag will lead to the creation of an image with the corresponding tag name.
* The container image will be pushed to Docker Hub at [https://hub.docker.com/8grams/caddy-example](https://hub.docker.com/8grams/caddy-example?ref=8grams.tech).
* Tekton will send notifications to Discord using Discord Webhooks, which can be substituted with Slack Webhooks if preferred.

Let’s get started!

## Preparation

We will need some preparations such as:

* Create a repository on GitHub. For this example, we’ll use [https://github.com/8grams/caddy-example](https://github.com/8grams/caddy-example?ref=8grams.tech). Push your code commits to this repository.
* Set up a webhook on GitHub. This webhook will trigger the Tekton pipeline. To create a webhook, navigate to your organization’s settings, then select ‘*Webhooks*’ Remember to fill in the ‘*Webhook Secret*’ for security purposes.
* Tekton requires a public endpoint to receive the webhook. It’s highly recommended to secure this with SSL. You can refer to these articles on how to set up Nginx Ingress and protect it with a free SSL Certificate from Let’s Encrypt:

[## How to get Free SSL Certificate for Kubernetes Cluster using Let’s Encrypt

### Introduction

8grams.medium.com](/how-to-get-free-ssl-certificate-for-kubernetes-cluster-using-lets-encrypt-c3d4e9b613fe?source=post_page-----e7c5ce430ea1---------------------------------------)

* Install Tekton CLI to help us install any Tekton Tasks from Tekton Hub, see: [https://tekton.dev/docs/cli/](https://tekton.dev/docs/cli/?ref=8grams.tech).

## Install Tekton

Check it out our Tekton basic configuration on [https://github.com/8grams/tekton-k8s-example](https://github.com/8grams/tekton-k8s-example?ref=8grams.tech)

Download Tekton Config

```
~$ git clone git@github.com:8grams/tekton-k8s-example.git
```

Prepare some Namespaces to place Tekton’s workload:

```
~$ kubectl create namespace tekton  
~$ kubectl create namespace tekton-pipelines  
~$ kubectl create namespace tekton-pipelines-resolvers  
~$ kubectl create namespace tekton-dashboard
```

Install some Tekton Tasks that we need to build Docker Image from GitHub: `git-clone`, `kaniko`, and `send-to-webhook-discord`.

```
~$ tkn hub install task kaniko --namespace=tekton  
~$ tkn hub install task git-clone  
~$ tkn hub install task send-to-webhook-discord --namespace=tekton  
~$ kubectl -n tekton apply -f https://api.hub.tekton.dev/v1/resource/tekton/task/curl/0.1/raw
```

To getting started with Kaniko, check this article below:

[## Kaniko: Kubernetes Native Daemonless Docker Image Builder

### Introduction

8grams.medium.com](/kaniko-kubernetes-native-daemonless-docker-image-builder-8eec88979f9e?source=post_page-----e7c5ce430ea1---------------------------------------)

### Installing Tekton Resources

Install Tekton Operators resources

```
~$ cd operator  
~$ kubectl apply -f interceptors.yaml  
~$ kubectl apply -f pipeline.yaml  
~$ kubectl apply -f trigger.yaml
```

Install RBAC Resources

```
~$ cd webhook/rbac  
~$ kubectl -n tekton apply -f admin-role.yaml  
~$ kubectl -n tekton apply -f clusterrolebinding.yaml  
~$ kubectl -n tekton apply -f webhook-role.yaml
```

Next, install GitHub Secrets so that Tekton can access our source code. Although we are using a public repository in this example, installing GitHub Secrets is essential for accessing private repositories.

```
~$ cd webhook/secrets  
~$ kubectl -n tekton apply -f github-secret.yaml
```

Optionally, you may also install a Registry Secret if you plan to use a private Container Registry.

```
~$ kubectl -n tekton apply -f registry-secret.yaml
```

### Handle Code Commit Push

To manage Commit Pushes, we first need an endpoint to act as a receiver for the webhook. To fulfill this requirement, we will install Nginx Ingress:

```
~$ cd webhook  
~$ kubectl -n tekton apply -f ingress.yaml
```

And then we can install Tekton Trigger and Pipeline

```
~$ cd webhook/events/push  
~$ kubectl -n tekton apply -f pipeline.yaml  
~$ kubectl -n tekton apply -f triggers.yaml
```

### Handle Tag Push

GitHub essentially treats a tag push similarly to a commit push. Therefore, the steps are the same: we will install Tekton Triggers and Pipelines to handle the webhooks.

```
~$ cd webhook/events/manual  
~$ kubectl -n tekton apply -f pipeline.yaml  
~$ kubectl -n tekton apply -f triggers.yaml
```

### Install Tekton Dashboard

The Tekton Dashboard makes it easy to monitor build progress, identify failed pipelines, and much more. It provides a user-friendly interface for various purposes.

```
~$ cd dashboard  
~$ kubectl -n tekton-dashboard apply -f deployment.yaml  
~$ kubectl -n tekton-dashboard apply -f ingress.yaml
```

You can check this dashboard on [https://tekton-dashboard.example.com](https://tekton-dashboard.example.com/?ref=8grams.tech) . You should see an interface like below

Press enter or click to view image in full size

![]()

### Check Installation

If all installations success, we should see deployments installed properly on our Kubernetes Cluster

```
~$ kubectl -n tekton get deployment  
NAME                      READY   UP-TO-DATE   AVAILABLE   AGE  
el-8grams-listener-tag   1/1     1            1           10m  
el-8grams-listener       1/1     1            1           10m  
  
  
~$ kubectl -n tekton-pipelines get deployment  
NAME                                READY   UP-TO-DATE   AVAILABLE   AGE  
tekton-triggers-core-interceptors   1/1     1            1           15m  
tekton-triggers-controller          1/1     1            1           15m  
tekton-pipelines-webhook            1/1     1            1           15m  
tekton-triggers-webhook             1/1     1            1           15m  
tekton-pipelines-controller         1/1     1            1           15m  
  
  
~$ kubectl -n tekton-pipelines-resolvers get deployment  
NAME                                READY   UP-TO-DATE   AVAILABLE   AGE  
tekton-pipelines-remote-resolvers   1/1     1            1           15m  
  
  
~$ kubectl -n tekton-dashboard get deployment  
NAME               READY   UP-TO-DATE   AVAILABLE   AGE  
tekton-dashboard   1/1     1            1           16m
```

## Testing

All set! You can now push a commit to the code repository and then open the Tekton Dashboard. When you navigate to the ‘Pipelines’ menu, you’ll see a Tekton Pipeline actively building a Docker Image for you! Wait until it completes the build process, at which point it will send a notification to Discord.

Congratulations ~ you now have an open-source, reliable, and scalable build pipeline platform installed on your Kubernetes cluster.
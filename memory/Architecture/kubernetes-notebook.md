---
title: Kubernetes notebook
topic: Architecture
tags:
  - kubernetes
source_type: hands-on
confidence: confirmed
created: '2026-07-29'
---
Original Article: https://kodekloud.com/blog/kubernetes-objects/

# What Are Objects Used for in Kubernetes? 11 Types Explained
Kubernetes is a container orchestration tool, used to deploy & manage containerized applications in an automated way.

One of the key concepts in Kubernetes is the "desired state," which refers to the configurations of the applications that you want to deploy and run. Essentially, it's the way you want your applications to be set up and how you want them to behave in a Kubernetes environment. This includes things like how many instances of applications should be running, how those instances should be networked together, what resources they should have access to, and so on.

So, how do you define the desired state? By using objects.

What Are Kubernetes Objects?
----------------------------

**Objects are sort of like blueprints. They provide detailed instructions to Kubernetes on how the applications must be set up and managed**.

For example, a [Deployment](https://kodekloud.com/blog/kubernetes-deployments/) object might specify that you want three replicas (copies) of some application running at all times, while a Service object might define how you want to expose your application to the internet. Kubernetes then takes these instructions and automatically configures and manages the application accordingly, ensuring that it always matches the desired state.

In this blog post, we're going to take a closer look at 11 different types of Kubernetes objects and what they're used for. Let’s get started!


11 Types of Objects in Kubernetes
---------------------------------

There are many different types of Kubernetes objects. However, the ones that you'll most often use are as follows:

### 1\. Pods

Pods are the fundamental building blocks of the Kubernetes system. They are **used to deploy, scale, and manage containerized applications in a cluster**.

A Pod can host a single container or a group of containers that need to "sit closer together". By grouping two or more containers in a single Pod, they will be able to communicate much faster and share data more easily. It's important to note that, when a Pod contains multiple containers, all of the containers always run on a single worker node. They never span across multiple worker nodes.

One important characteristic of [Pods](https://kodekloud.com/blog/pods-in-kubernetes/) is that they are **ephemeral in nature**. This means that they are not guaranteed to have a long-term lifespan. They can be created, destroyed, and recreated at any time if required.

### 2\. Deployment

In Kubernetes, a Deployment object is used to manage the lifecycle of one or more identical Pods. A Deployment **allows you to declaratively manage the desired state of your application**, such as the number of replicas, the image to use for the Pods, and the resources required. Declaratively managing the state means specifying the desired end state of an application, rather than describing the steps to reach that state. Kubernetes figures out the steps on its own. So it will know what it has to do to launch the Deployment, according to the specifications provided by the user.

When you create a Deployment, you provide a Pod template, which defines the configuration of the Pods that the Deployment will manage. The Deployment then creates Pods that match this template, using a ReplicaSet. A ReplicaSet is responsible for creating and scaling Pods, and for ensuring that Pods that fail are replaced. When you update a Deployment, it will update the ReplicaSet, which in turn updates the Pods.

It's important to note that Deployment objects are **used to manage stateless applications**. Stateless applications are those that do not maintain any persistent data or state. This means that if a container running the application crashes or is terminated, it can be easily replaced. There's no need to preserve any data before deleting the old container and replacing it with a new one. Examples of stateless applications include web servers and load balancers.

### 3\. ReplicaSets

In Kubernetes, **Deployments don’t manage Pods directly**. That’s the job of the ReplicaSet object. When you create a Deployment in Kubernetes, a ReplicaSet is created automatically. **The ReplicaSet** **ensures that the desired number of replicas (copies) are running at all times by creating or deleting Pods as needed**.

To accomplish this, Kubernetes uses a concept called reconciliation loops. A reconciliation loop is a process that compares the desired state of a system with its current state and takes actions to bring the current state in line with the desired state.

Let's say you have specified that you want 3 replicas of a web server Pod to be running in your [Kubernetes cluster](https://kodekloud.com/blog/kubernetes-terms/). The reconciliation loop is constantly monitoring the current state of the cluster and comparing it to the desired state of 3 replicas. If it finds that there are only 2 replicas currently running, it will create a new replica to bring the current state in line with the desired state.

### 4\. StatefulSet

A StatefulSet is a Kubernetes object that is **used to manage stateful applications**. The word "state" means any stored data that the application or component needs to do its work. This state is typically stored in a persistent storage backend, such as a disk, or a database. And the state is maintained even if the underlying Pods/containers are recreated. The most common example of a stateful component in applications is a database such as MySQL or MongoDB.

The StatefulSet **ensures that each Pod is uniquely identified by a number, starting at zero**. This allows for a consistent naming scheme for each Pod and its associated resources, such as persistent storage (for example, when Volumes are used).

When a Pod in a StatefulSet must be replaced, for example, due to node failure, the new Pod is assigned the same numeric identifier as the previous Pod. This ensures that the new Pod has the same unique identity and is attached to the same persistent storage (Volume) that the previous Pod was using.

This **allows for the preservation of state and data across Pod replacements**. This is important for applications that do work that periodically adds, removes, or changes some data. They basically need to remember "what has happened in the past" (previous state). For example, a Pod can add a new entry to a database, maybe the email address of a new user. If the Pod has to be recreated, you don't want to lose the email address that was previously added.

### 5\. DaemonSets

A DaemonSet **ensures that a copy of a Pod is running across all, or a subset of nodes in a Kubernetes cluster**.

DaemonSets are **useful for running system-level services**, such as logging or monitoring agents, that need to run on every node in a cluster. Logging agents are used to collect log data from all the nodes in a cluster and send it to a centralized logging system for storage and analysis. Monitoring agents are used to collect metrics and performance data from all the nodes in a cluster, and send it to a monitoring system for analysis and alerting.

Like ReplicaSets, **DaemonSets are managed by a reconciliation loop**. A reconciliation loop is a mechanism that continuously checks and compares the desired state of a resource with the current state. The loop runs periodically and ensures that the DaemonSet is always in the desired state, automatically creating or deleting Pods as necessary.

### 6\. PersistentVolume

PersistentVolume **represents a piece of storage that you can attach to your Pod(s).**

The reason it's called "persistent" is because it's not tied to the life cycle of your Pod. In other words, even if your Pod gets deleted, the PersistentVolume will survive.

And there are a lot of different types of storage that you can attach using a PersistentVolume, like local disks, network storage, and cloud storage.

There are a few different use cases for PersistentVolumes in Kubernetes. **One common use case is for databases**. If you're running a database inside a Pod, you'll likely want to store the database files on a separate piece of storage that can persist even if the Pod gets deleted. And PersistentVolume can do that.

### 7\. Service

A [Kubernetes Service](https://kodekloud.com/blog/kubernetes-services/) is **a way to access a group of Pods that provide the same functionality**. It creates a single, consistent point of entry for clients to access the service, regardless of the location of the Pods.

For example, imagine you have a Kubernetes cluster with multiple Pods running a web application. Each Pod has its own IP address, but this can change at any time if the Pod is moved to another node, or recreated. So the IP address becomes a "moving target". The destination(s) that clients should reach is unstable, and hard to track.

To make it easier for clients to access the web application, you can create a Kubernetes Service that has a stable IP address. Clients can then connect to that IP, and their requests will be routed to one of the Pods running the web application.

One of the key benefits of using a Service is that it **provides a stable endpoint that doesn't change even if the underlying Pods are recreated or replaced**. This makes it much easier to update and maintain the application, as clients don't need to be updated with new IP addresses.

Furthermore, the Service also provides some simple load balancing. If clients would connect to a certain IP address of a specific Pod, that Pod would be overused, while the other ones would be sitting idle, doing nothing. But the Service can spread out requests to multiple Pods (load balance). By spreading these out, all Pods are used equally. However, each one has less work to do, as it only receives a small part of the total number of incoming requests.

### 8\. Namespaces

A Kubernetes namespace is **a way to divide a single Kubernetes cluster into multiple virtual clusters**. This allows resources to be isolated from one another. Once a namespace is created, you can launch Kubernetes objects, like Pods, which will only exist in that namespace.

For example, imagine you have a Kubernetes cluster running two applications, "AppA" and "AppB". To keep things organized, you create two namespaces, "AppA-Namespace" and "AppB-Namespace".

Now, when you deploy Pods for "AppA", you can do so within the "AppA-Namespace". Similarly, when you deploy Pods for "AppB", you can do so within the "AppB-Namespace". What's a possible use case?

Well, imagine AppA, and AppB are almost identical. One is version 1.16 of an app, the other is version 1.17. They use almost the same objects, the same Pod structures, the same Services, and so on. Since they're so similar, there's a risk of them interfering with each other. For example, AppA might accidentally send requests to a similar Service or Pod used by AppB. But you want to test the new 1.17 version in a realistic scenario in the same cluster, using the same objects and definitions.

By using namespaces, you can **perform as many operations as you need while eliminating the risk of impacting resources that are in another namespace**. It's almost as if you have a second Kubernetes cluster. AppA runs in its own (virtual) cluster. AppB runs in a separate (virtual) cluster. But you don't actually have to go through the trouble of setting up an additional cluster. AppA and AppB are logically isolated from each other when they exist in separate namespaces. Even if they run identical Pods that want to access Services with identical names, there's no risk of them interfering with each other.

### 9-10. ConfigMaps & Secrets

ConfigMaps and Secrets are two very important objects that **allow you to configure the apps that run in your Pods**. Configuring apps refers to setting various parameters or options that control the behaviors of the apps. This can include things like database connection strings or API keys.

**ConfigMaps are used to store non-sensitive configuration values**. For example, environment variables used to provide runtime configuration information such as the URL of an external API, rather than confidential information such as passwords, are considered non-sensitive data.

**Secrets, on the other hand, are meant to hold sensitive configuration values**, such as database passwords, API keys, and other information that only authorized apps should be able to access.

ConfigMaps and Secrets can be injected into Pods with the help of environment variables, command-line arguments, or configuration files included in the volumes attached to those Pods.

By using ConfigMaps and Secrets, you decouple the applications running in your Pods from their configuration values. This means you can easily update the configuration of your applications without having to rebuild or redeploy them.

### 11\. Job

A job object is used to **run specific tasks** that have the following properties:

*   They are short-lived.
*   They need to be executed once.
*   But most importantly, Kubernetes has to make sure that the task has been executed correctly and finished its job.

An example of where a Kubernetes job can be useful is a **database backup**. This does not run continuously, so it's a short-lived process. It just needs to start, complete, then exit. It has to be executed once. Even if the backup needs to happen weekly, there will be one separate job per week (CronJobs can be used for jobs that repeat periodically).

Each job has to finish its own weekly task. But it needs to ensure that the Pod executing the backup fully completes this job. For example, a Pod might start a backup. But the database is huge, so this can take hours. For some reason, the backup process fails at 68% progress. Kubernetes sees that the Pod has failed the task, so it can create another one to retry. It will keep on retrying until, finally, one Pod manages to back up the entire database.

In this case, the job required one Pod, and one successful run for one Pod (to ensure the task was completed successfully). But other jobs might require multiple Pods (which can run in parallel) and/or multiple successful runs. For example, a job will be considered complete, only when at least 3 Pods had successful runs and achieved 100% progress on their tasks.

Conclusion
----------

Kubernetes objects are the building blocks of the workload running on top of a Kubernetes cluster. They are used to define and manage the desired state of your application. It's how you tell Kubernetes about the structures you want to run on top of it. What containers should run, how they should be networked, what passwords/keys they should use, and so on.

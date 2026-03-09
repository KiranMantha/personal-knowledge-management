---
title: "All About Kubernetes Port Types: NodePort,TargetPort,Port,ContainerPort"
url: https://medium.com/p/e9f447330b19
---

# All About Kubernetes Port Types: NodePort,TargetPort,Port,ContainerPort

[Original](https://medium.com/p/e9f447330b19)

# All About Kubernetes Port Types: NodePort,TargetPort,Port,ContainerPort

[![Deepesh Tripathi](https://miro.medium.com/v2/resize:fill:64:64/0*Ip0tCxSHHvl-ALe4.)](/@deepeshtripathi?source=post_page---byline--e9f447330b19---------------------------------------)

[Deepesh Tripathi](/@deepeshtripathi?source=post_page---byline--e9f447330b19---------------------------------------)

3 min read

·

Jan 15, 2020

--

8

Listen

Share

More

Press enter or click to view image in full size

![]()

If you have reached this article. I can safely assume either you are a Kubernetes learner or seeking more clarity on different port types being used in service and pod container spec.

Kubernetes uses different types of ports when you write pod container specs or when you create a service for your deployment or set of pods as endpoints.

These are nodePort, port, targetPort and containerPort. what is the difference between all these? and when to use what? let us understand this in detail.

Kubernetes spins up different object types in k8s cluster, some basic objects are called pods which you need to create to spin up a single container. As you already know that Kubernetes does not manage loose containers but manages them in units called a pod. A pod could be a single container or set of app containers launched as a service.

when you wish to spin a pod or deployment up in your cluster. You are required to write a pod spec. Pod spec mainly contains AKMS (API, kind, metadata, spec). With AKMS your pod gets the definition to spin up freshly in the cluster.

In pod manifest file, under pod spec, you need to define the container spec. This spec carries information like container image name and image version to be fetched from Docker hub or custom repository.

In container spec you need to define port which container is going to use.This can be defined by containerPort directive in the container spec of pod manifest.

“containerPort” defines the port on which app can be reached out inside the container.

once your container is spun up and the pod is running. You may need to expose the POD as a service to the external world sometimes. Kubernetes service comes into the picture here. The service object of Kubernetes exposes the internal pod endpoints as service to the outer world.

A service is a k8s object and basically a firewall rule. This rule is created basically for two reasons.

1. To expose PODs to the external world.
2. You can load balance between a set of pods and get rid of pod ip change if it dies.

To expose a pod to external world you need to create a service with nodePort type. nodePort sends external traffic to the Kubernetes cluster which is received on “port” defined in service object YAML.

But before nodePort, there are two other ports that service uses in order to correctly route external traffic requests to pod endpoints.

1. port
2. targetPort

Too many port types in multiple specs like pod and service may create confusion about information flow from the external world till container but not after this point.

Let’s understand this in detail.

We already know that the service uses nodePort to expose internal pods for external traffic. What this port literally used for?. In practical use nodePort is used to access exposed service from the external world.

When you wish to access a pod as via a service, you are going to hit host-ip:nodePort in order to reach till k8s pod or deployment object.

Once service receives traffic from an external source it does two things.

1. First, it sends the traffic received on nodePort and forwards that to port service is listening to i.e to the port defined in “Port” directive of service object YAML.
2. The second thing what a service does. It redirects the traffic received on “Port” to “targetPort” which is the directive used to define port on which container has exposed the application.

Hence, in the context of service spec “Port” is used to define the port on which service listens.

targetPort and containerPort must be identical most of the time because whatever port is open for your application in a container that would be the same port you will wish to send traffic from service via targetPort.

Whereas nodePort is the port on which your service is exposed to the outer world. so this will be the port to be typed in your browser when you want to access the service.
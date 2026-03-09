---
title: "Service Mesh vs API Gateway"
url: https://medium.com/p/a6d814b9bf56
---

# Service Mesh vs API Gateway

[Original](https://medium.com/p/a6d814b9bf56)

# Service Mesh vs API Gateway

[![Kasun Indrasiri](https://miro.medium.com/v2/resize:fill:64:64/1*evOTt1jlg_CN0592nkXi8w.jpeg)](/@kasunindrasiri?source=post_page---byline--a6d814b9bf56---------------------------------------)

[Kasun Indrasiri](/@kasunindrasiri?source=post_page---byline--a6d814b9bf56---------------------------------------)

3 min read

·

Oct 9, 2017

--

11

Listen

Share

More

In [one of my previous articles on service mesh](/microservices-in-practice/service-mesh-for-microservices-2953109a3c9a), there were a couple of questions related to the relationship between Service Mesh and API Gateway. So, in this post, I’m planning to discuss the usage of Service Mesh and API Gateway.

[## Microservices for the Enterprise: Designing, Developing, and Deploying

### Microservices for the Enterprise: Designing, Developing, and Deploying [Kasun Indrasiri, Prabath Siriwardena] on…

www.amazon.com](https://www.amazon.com/Microservices-Enterprise-Designing-Developing-Deploying/dp/1484238575?source=post_page-----a6d814b9bf56---------------------------------------)

In order to differentiate API Gateways and service mesh, let’s have a closer look at the key characteristics API Gateways and Service Mesh.

### API Gateway: Exposes your services as managed APIs

The key objective of using API Gateway is to expose your (micro) services as managed APIs. So, the API or Edge services that we develop at the API Gateway layer serves a specific business functionality.

* API/Edge services call the downstream (composite and atomic) microservices and contain the business logic that creates compositions/mashups of multiple downstream services.
* API/Edge services also need to call the downstream services on the resilient manner and apply various stability patterns such as Circuit Breakers, Timeouts, Load Balancing/Failover. Therefore most of the API Gateway solutions out there have these features built in.
* API Gateways also come inbuilt support for service discovery, analytics(observability: Metrics, monitoring, distributed logging, distributed tracing.) and security.
* API Gateways closely work with several other components of the API Management ecosystem, such as API marketplace/store, API publishing portal.

### Service Mesh

Now let’s look at how we can differentiate [Service Mesh](/microservices-in-practice/service-mesh-for-microservices-2953109a3c9a).

* Service Mesh is a network communication infrastructure which allows your to decouple and offload most of the application network functions from your service code.
* Hence when you do service-to-service communication, you don’t need to implement resilient communication patterns such as Circuit breakers, timeouts in your service’s code. Similarly, service mesh provides other functionalities such as service discovery, observability etc.

### Coexistence of API Gateway and Service Mesh

The key differentiators between API Gateways and service mesh is that API Gateways is a key part of exposing API/Edge services where service mesh is merely an inter-service communication infrastructure which doesn’t have any business notion of your solution.

Figure 1 illustrates how API Gateway and service mesh can coexist. As we discussed above, there are also some overlapping features (such as circuit breakers etc.) but it’s important to understand these two concepts are serving fundamentally different requirements.

Press enter or click to view image in full size

![]()

As shown in figure 1, service mesh is used alongside most of the service implementations as a [sidecar](/microservices-in-practice/service-mesh-for-microservices-2953109a3c9a) and it’s independent of the business functionality of the services.

On the other hand, API Gateway hosts all the API services (which has a clearly defined business functionality) and it’s a part of the business functionality of your solution. API Gateway may have in-built inter-service communication capabilities but that doesn’t prevent API Gateway using service mesh to call downstream services(API Gateway->service mesh->microservices).

> At API Management level, you can either use in-built inter-service communication capabilities of API Gateway or API Gateway can call downstream services via service mesh by offloading application network functions to service mesh.

### Replacing API Gateway with Service Mesh sidecar proxy

In certain use cases, we can eliminate API Gateway altogether and offload the API Gateway capabilities to the Sidecar proxy that is colocated with the service that you want to expose as an API. The API management plane/control plane needs to communicate with the sidecar proxy to apply the API Management capabilities.

Press enter or click to view image in full size

![]()

However, this model force us to expose services through the sidecar proxy layer which is colocated with the microservice.

## References

[## Microservices for the Enterprise: Designing, Developing, and Deploying

### Microservices for the Enterprise: Designing, Developing, and Deploying [Kasun Indrasiri, Prabath Siriwardena] on…

www.amazon.com](https://www.amazon.com/Microservices-Enterprise-Designing-Developing-Deploying/dp/1484238575?source=post_page-----a6d814b9bf56---------------------------------------)
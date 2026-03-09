---
title: "My Favourite Software Architecture Patterns"
url: https://medium.com/p/0e57073b4be1
---

# My Favourite Software Architecture Patterns

[Original](https://medium.com/p/0e57073b4be1)

Member-only story

# My Favourite Software Architecture Patterns

## Exploring my most loved Software Architecture patterns and their practical applications.

[![Matt Bentley](https://miro.medium.com/v2/resize:fill:64:64/1*nUZ_xcK6heGCMT4SHpSsuA.jpeg)](https://medium.com/@mattbentley_67939?source=post_page---byline--0e57073b4be1---------------------------------------)

[Matt Bentley](https://medium.com/@mattbentley_67939?source=post_page---byline--0e57073b4be1---------------------------------------)

10 min read

·

Nov 12, 2024

--

127

Listen

Share

More

Press enter or click to view image in full size

![]()

Software Architecture is an art that requires experience and broad knowledge about lots of different technical concepts. Unfortunately, there are no Architectural silver bullets which work in all scenarios. Software Architecture must be designed to meet the specific requirements of the application and team in question. Considerations may include the likes of:

> Performance, Scalability, Elasticity, Flexibility, Simplicity, Reliability, Cost, Team Technical Capability…

Patterns are the building block of any Software Architecture. Luckily there’s lots of different patterns which can be used in combination, depending on your needs. Picking the correct patterns usually depends on trade-offs that you’re willing to make based on your requirements. Before starting any journey in Software Architecture, you must first understand which patterns work well in certain scenarios. In this article I’ll talk through some of my favourite patterns, and where they excel.

## Bounded Contexts

My first Architecture pattern is not actually even a pattern at all. However, Bounded Contexts are one of the most powerful techniques for building maintainable code. Bounded Contexts are a concept taken from Domain-Driven Design’s Strategic Design, but I now see them being applied in lots of projects that don’t use DDD.

Bounded Contexts are used to represent well-defined logical boundaries around concepts within an application. They represent a distinct area of the application where a specific domain model is used, and where the terminology, rules, and data representations are consistent and cohesive.

Here’s how the concepts in an eCommerce app might be broken down into Bounded Contexts for: Catalogue, Ordering, Payments and Identity.

Press enter or click to view image in full size

![]()

Bounded Contexts help combat tight coupling and complexity, as the number of concepts in an application grow over time.

I also find it really useful to also organise code in a project by Bounded Context. This is particularly helpful if you plan on splitting your code into a Modules or Microservices in the future.

Here’s how this might look for the same eCommerce application using **Clean Architecture**. This is referred to as **Domain-Centric Architecture**.

![]()

### Example: Vertical Slice Architecture

Vertical Slice Architecture is becoming super popular at the moment. It takes this concept to the next level, by breaking the whole application into vertical segments. Understanding your Bounded Contexts are key to doing this.

Rather than using a layered approach that might be found in Clean Architecture, the Bounded Contexts are split into independent vertical slices instead.

![]()

### Example: Event Storming

A great approach for mapping out your Bounded Contexts is Event Storming: [Why You Should Be Using Event Storming](https://medium.com/better-programming/why-you-should-be-using-event-storming-2f32e5280c8c).

I have been using Event Storming across my teams for a while now, and so far, it has proved to be the most powerful tool for solution design and discovery. If you are using domain-driven design or are trying to model a particularly complex problem, then Event Storming is especially powerful!

![]()

### When to use?

* Medium to High domain complexity
* Applications where the number of features or concepts is expected to grow over time
* App might be broken apart into separate apps/deployments in the future

## Sidecar

A **Sidecar** is an application which sits in-front of another application running on the same host. The host could be anything from a server or virtual machine, to a container or Kubernetes pod. Sidecars are generally used to intercept traffic to and from the downstream app.

Press enter or click to view image in full size

![]()

Sidecars can be used to transparently extend the functionality of the downstream app, without having to modify it at all. The most typical use-case for Sidecars is for adding additional security features, such as Authentication, Authorization or network policies, which aren’t present on downstream application.

Sidecars can also be used to add generic cross-cutting concerns in a standardized way across your portfolio of apps. Here’s a few examples:

* Logging
* Performance Monitoring
* Tracing
* Authentication and Authorization
* Retry Policies and Circuit Breakers
* Transparent Encryption

### Example: Service Mesh

A Service Mesh takes the Sidecar concept to the extreme, by pairing every single application across a cluster ***data-plane*** with its own Sidecar Proxy. All app-to-app communication is done through the Sidecars. This allows all traffic to be encrypted, monitored and secured in a standard way by the ***control-plane***.

Press enter or click to view image in full size

![]()

My team use a Service Mesh on all of our Kubernetes clusters, so that we can secure and monitor them in a standard way.

### When to use?

* Application cannot be modified but requires additional cross-cutting features
* Centralized or Standardized cross-cutting concerns required across multiple applications

## Publisher-Subscriber

This pattern is used to support ***Asynchronous*** communication through a **Message Broker**, between a **Publisher** and a **Subscriber**. Message Brokers contain one or more **Topics**, which can be Published and Subscribed to.

Press enter or click to view image in full size

![]()

Messages are queued in a Topic and dispatched to downstream Subscribers in a f***irst in, first out*** (FIFO) manner. This pattern is used to allow data or events to be integrated across connected applications. It can also be used to schedule long-running tasks asynchronously in a **Worker Service**.

### Delivery Mechanisms

There are 2 main Delivery Mechanisms for Publisher-Subscriber:

* **Competing Consumers**: Each Message published is only consumed ***once*** by ***any*** Subscriber. This pattern can be used to scale-out the processing of long-running tasks in parallel by lots of Subscriber Worker Services.
* **Fanout**: Each Message published is consumed by ***all*** Subscribers. This pattern is generally used for syncing events or data across lots of downstream applications.

Press enter or click to view image in full size

![]()

### When to use?

* Asynchronous communication required
* Scale and load-balance long-running tasks
* Integrate data changes or events across multiple downstream applications

## Application Gateway

An Application Gateway does a similar job to a Load Balancer, by routing network traffic to multiple downstream applications. Whilst a Load Balancer operates at Layer 3/4 using port/IP address, an Application Gateway operates at **Layer 7**. This allows Application Gateways to perform deep packet inspection, so that routing can be achieved based on application information such as request ***hostname***, ***path*** and ***headers***.

Press enter or click to view image in full size

![]()

The most common routing scenario for Application Gateways is ***Path-Based***. If an organization has lots of different backend services to host (e.g. Service Oriented or Microservices Architectures), then using an Application Gateway can hugely simplify maintenance by serving all services behind a single URL. Application Gateways often also provide additional security features such as *SSL termination* or *Web Application Firewall*.

### Example: Infrastructure Platform

Application Gateways perform a crucial role in the Infrastructure Platform that my team have built for hosting all of our products: [How We Built an Infrastructure Platform on Top of Kubernetes](https://medium.com/better-programming/how-we-built-an-infrastructure-platform-on-top-of-kubernetes-a39e67d85680).

![]()

Our Application Gateway allows us to host lots of different tenant products on the same URL, so that the number of SSL Certificates and DNS Registrations to setup and maintain is kept to a minimum.

### When to use?

* Require hosting lots of applications behind the same URL or set of URLs
* Routing to downstream services using a path prefix or hostname

## Microservices

Microservices are used to break down an application into small independent services. A Microservice must have its own dedicated API and database. Microservices can each use different underlying technologies, and they should be independently deployable and scalable.

Press enter or click to view image in full size

![]()

Microservices often use a single monolithic Frontend and an Application Gateway to serve all traffic from a single URL.

Microservices can be extremely powerful and flexible, however they also add huge complexity. If you are going to use Microservices, then make sure you have a good reason to take-on all of this complexity.

### When to use?

* Different parts of the application have different requirements for Performance, Scaling or Availability
* Different parts of the application require different Database technologies
* Different parts of the application require independent deployments
* Large Development teams can be split into smaller more efficient teams and work on Microservices independently

## Microfrontends

Whilst Microservices are used to split backend applications, Microfrontends are used to split-up web Frontends. A Frontend can be composed from a number of different smaller Microfrontends, all hosted independently. This now means that features can be developed and released in isolation, across both a backend Microservice and web Microfrontend component.

Press enter or click to view image in full size

![]()

Each Microfrontend must have its own independent screens in a Frontend web application. Usually, some kind of Portal wrapper UI is used to render the various Microfrontends.

Most web frameworks have their own ways of supporting Microfrontends. More recently, frameworks have been standardizing on using **Web Components**. Web Components are packaged into single JavaScript files which allow UI components to be hosted in a web app using a custom HTML element. Web Components are completely encapsulated, which means that each Microfrontend can even use a different JavaScript framework if required.

### When to use?

* Same requirements as Microservices
* Different teams must be responsible for maintaining and deploying different sections of a web app UI
* Different sections of a web app UI must be independently deployable

## Command Segregation Responsibility Segregation (CQRS)

Microservices allow each service to use different database technologies; but what if each Microservice also needs to use different database technologies too? CQRS allows different techniques to be used for writing data (Write Side) and reading data (Read Side). That might mean different representations of the same data, or maybe even using completely different database technologies. The idea is that each side can be optimised for the responsibility it is performing and expecting usage patterns.

Press enter or click to view image in full size

![]()

You might want to use something simple and cheap like S3 Buckets for the Write side and something with better query support on the Read side, such as Elastic Search. A relational SQL database may fit better on one side and a NoSQL database on the other. Depending on data access patterns, we can also scale each side completely independently.

If different databases are being used, then a Message Broker is often used to integrate changes of data between the Write Side and the Read Side using Eventual Consistency.

CQRS is a complex pattern to understand and maintain; if you are going to use it, then make sure that your application really requires taking on this extra complexity.

### Different CQRS Architectures

There are lots of different flavours of CQRS, ranging in complexity: [Choosing a CQRS Architecture That Works for You](https://medium.com/better-programming/choosing-a-cqrs-architecture-that-works-for-you-02619555b0a0). You can pick an option to meet your specific needs.

Press enter or click to view image in full size

![]()

### Example: Event Sourcing

Event Sourcing is one of my favourite forms of CQRS. Instead of storing the current state of a model, append-only event stores are used to record the full series of actions taken on a model. When a new Command occurs, the current state of the Model/Entity is ‘rehydrated’ by replaying all of the events that have ever happened for that instance.

![]()

The analogy often given to help people understand ES is a Bank Account. All of the Transactions are stored as Events, and the Balance is calculated by replaying all Transactions.

Each model instance on the Write side is stored as its own independent **Event Stream**. The stream of events can be replayed at any time to materialise different views of the data. If the Read side gets out of sync, we can query all of the events from the Write side and rebuild our models.

Press enter or click to view image in full size

![]()

### When to use?

* Extremely high performance and load requirements
* Different technologies required for Read and Write sides
* Event Sourcing required for enhanced audit capabilities

## Putting it all together: Polyglot Architecture

All of these patterns can even be pulled together across your solution architecture and matched to the specific requirements of each Bounded Context.

Here’s another example of how the same eCommerce app could be architected using the patterns discussed.

Press enter or click to view image in full size

![]()

This architecture pulls in the best technologies and patterns to match the requirements for each Bounded Context; this is known as **Polyglot Architecture**.

Each Bounded Context has its own Microservice and Microfrontend. All Microservices are served behind a common URL through an Application Gateway.

Catalogue uses Redis for optimizing query performance. Ordering uses PostgreSQL for strong relational consistency. Payments uses CQRS and Event Sourcing to model the complex payments flows over time.

Most Microservices have their own Message Broker Topic to publish events to. There are also multiple Orchestration Services consuming events for integrating data changes from other Bounded Contexts and processing long-running tasks asynchronously.

The Identity Microservice uses KeyCloak for authentication. There is also a common Identity Sidecar implementation for enforcing Authentication and Authorization in a standard way across the other Microservices.

The different Architecture patterns demonstrated here can be powerful in lots of different scenarios, however, they may also be overkill for some situations. Remember, always be guided by the requirements in your project and the capabilities of your team. Having a good understanding of which patterns excel in certain situations is key to designing an optimal architecture!
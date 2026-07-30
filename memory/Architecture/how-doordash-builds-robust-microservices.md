---
type: Learning
title: How DoorDash Builds Robust Microservices
topic: Architecture
tags:
  - microservices
  - doordash
status: stable
generated:
  by: agent-kiran/seed-script
  at: '2026-07-30T07:06:34.091Z'
---
Original article: https://blog.neetcode.io/p/doordash-robust-microservices

# How DoorDash Builds Robust Microservices
DoorDash is the largest food delivery marketplace in the US with over 30 million users in 2022. You can use their mobile app or website to order items from restaurants, convenience stores, supermarkets and more.

In 2020, [DoorDash migrated](https://doordash.engineering/2020/12/02/how-doordash-transitioned-from-a-monolith-to-microservices/?utm_source=blog.quastor.org&utm_medium=referral&utm_campaign=scaling-microservices-at-doordash) from a Python 2 monolith to a microservices architecture. This allowed them to:

1.  Increase developer velocity by having smaller teams that could deploy independently.
    
2.  Use different tech stacks for different classes of services.
    
3.  Scale the engineering platform/organization and more.
    

However, microservices bring a ton of added complexity and introduce new failures that didn’t exist with the monolithic architecture. DoorDash engineers wrote a great [blog post](https://doordash.engineering/2023/03/14/failure-mitigation-for-microservices-an-intro-to-aperture/?utm_source=blog.neetcode.io&utm_medium=referral&utm_campaign=how-doordash-builds-robust-microservices) going through the most common microservice failures they’ve experienced and how they dealt with them.

**Failure 1 - Cascading Failures**
----------------------------------

Cascading failures describes a general issue where the failure of a single service can lead to a chain reaction of failures in other services.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/f42b1256-7ddc-44aa-9e8d-760458c73826/doordash-mitigation-1.png?t=1725760349)

This diagram shows how issues within a single component, in this case the database, can cascade and impact services that depend on it. Even if those services would be otherwise healthy.

DoorDash talked about an [example of this in May](https://doordash.engineering/2022/05/13/doordashs-may-12th-outage/?utm_source=blog.quastor.org&utm_medium=referral&utm_campaign=scaling-microservices-at-doordash) of 2022, where some routine database maintenance temporarily increased read/write latency for the service. This caused higher latency in upstream services which caused errors from timeouts. The increase in error rate then triggered a misconfigured circuit breaker which resulted in an outage in the app that lasted for 3 hours.

When you have a distributed system of interconnected services, failures can easily spread across your system and you’ll have to put checks in place to manage them (discussed below).

**Failure 2 - Retry Storms**
----------------------------

One of the ways a failure can spread across your system is through retry storms.

Making calls from one backend service to another is unreliable and can often fail due to completely random reasons. A garbage collection pause can cause increased latencies, network issues can result in timeouts and more.

Therefore, retrying a request can be an effective strategy for temporary failures (distributed systems experience these _all the time_).

However, retries can also worsen the problem while the downstream service is unavailable/slow. The retries result in work amplification (a failed request will be retried multiple times) and can cause an already degraded service to degrade further.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/b6fb9433-680f-4a5a-8c6b-2c24d20156c4/doordash-mitigation-3.png?t=1725762012)

**Failure 3 - Death Spiral**
----------------------------

With cascading failures, we were mainly talking about issues spreading _vertically_. If there is a problem with service A, then that impacts the health of service B (if B depends on A). Failures can also spread _horizontally_, where issues in some nodes of service A will impact (and degrade) the other nodes within service A.

An example of this is a death spiral.

You might have service A that’s running on 3 machines. One of the machines goes down due to a network issue so the incoming requests get routed to the other 2 machines. This causes significantly higher CPU/memory utilization, so one of the remaining two machines crashes due to a resource saturation failure. All the requests are then routed to the last standing machine, resulting in significantly higher latencies.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/494cbe08-d65d-495b-8316-e8d71bb9fe8d/doordash-mitigation-4.png?t=1725762795)

This diagram shows a service with multiple instances. When individual nodes go down they are automatically replaced with replacements. But the replacements are not immediately ready so all of the remaining traffic is redirected to Node 3. This results in Node 3 receiving too much traffic, which may result in its failure.

**Failure 4 - Metastable Failure**
----------------------------------

Many of the failures experienced at DoorDash are _metastable failures_. This is where there is some positive feedback loop within the system that is causing failures _even after_ the initial trigger is gone.

![](https://media.beehiiv.com/cdn-cgi/image/fit=scale-down,format=auto,onerror=redirect,quality=80/uploads/asset/file/5c7480a0-3ea4-4c64-9d3c-9e2c1f6b578a/doordash-mitigation-2.png?t=1725760198)

This diagram shows the possible state transitions that can bring an entire system into a metastable state. After a metastable state is reached, unfortunately it requires manual developer intervention, such as restarting servers, to bring the system back to a health state.

For example, the initial trigger might be a surge in users. This causes one of the backend services to load shed and respond to certain calls with a [429](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/429?utm_source=blog.quastor.org&utm_medium=referral&utm_campaign=scaling-microservices-at-doordash) (rate limit).

Those callers will retry their calls after a set interval, but the retries (_plus_ calls from new traffic) overwhelm the backend service _again_ and cause even more load shedding. This creates a positive feedback loop where calls are retried (along with new calls), get rate limited, retry again, and so on.

This is called the [Thundering Herd problem](https://en.wikipedia.org/wiki/Thundering_herd_problem?utm_source=blog.quastor.org&utm_medium=referral&utm_campaign=scaling-microservices-at-doordash) and is one example of a Metastable failure. The initial spike in users can cause issues in the backend system even after the surge has ended.

**Countermeasures**
-------------------

DoorDash has a couple techniques they use to deal with these issues. These are

1.  **Load Shedding** - a degraded service will drop requests that are “unimportant” (engineers configure which requests are considered important/unimportant)
    
2.  **Circuit Breaking** - if service A is sending service B requests and service A notices a spike in B’s latencies, then circuit breakers will kick in and reduce the number of calls service A makes to service B
    
3.  **Auto Scaling** - adding more machines to the server pool for a service when it’s degraded. However, DoorDash avoids doing this reactively (discussed further below).
    

**Local Countermeasures**
-------------------------

### **Load Shedding**

With many backend service, you can rank incoming requests by how important they are. A request related to logging might be less important than a request related to a user action. This is preferable to rate limiting all requests, without taking any other factors into account.

With **Load Shedding**, you temporarily reject some of the less important traffic to maximize the [goodput (good + throughput)](https://en.wikipedia.org/wiki/Goodput?utm_source=blog.quastor.org&utm_medium=referral&utm_campaign=scaling-microservices-at-doordash) during periods of stress (when CPU/memory utilization is high).

*   DoorDash instrumented servers with an adaptive concurrency limit using Netflix’s [concurrency-limit](https://github.com/Netflix/concurrency-limits?utm_source=blog.quastor.org&utm_medium=referral&utm_campaign=scaling-microservices-at-doordash) library.
    
*   It automatically adjusts the maximum number of concurrent requests according to changes in the response latency.
    
*   When a machine takes longer to respond, the library will reduce the concurrency limit to give each request more compute resources.
    
*   It can also be configured to recognize the priorities of requests from their headers.
    

#### **Cons of Load Shedding**

*   Load shedding is very difficult to configure and properly test. A misconfigured load shedder can increase latency in your system and can be a source of outages.
    
*   Services will require different configuration parameters depending on their workload, CPU/memory resources, time of day, etc. Auto-scaling services might mean you need to change the latency/utilization level at which you start to load shed.
    

### **Circuit Breaker**

While load shedding rejects incoming traffic, circuit breakers will reject outgoing traffic from a service.

They’re implemented as a proxy inside the service and monitor the error rate from downstream services. If the error rate surpasses a configured threshold, then the circuit breaker will start rejecting all outbound requests to the troubled downstream service.

DoorDash built their circuit breakers into their internal gRPC clients.

#### **Cons of Circuit Breaking**

*   Similar to Load Shedding, it’s extremely difficult to determine the error rate threshold at which the circuit breaker should switch on.
    
*   Many online sources use a 50% error rate as a rule of thumb, but this depends entirely on the downstream service, availability requirements, etc.
    

### **Auto-Scaling**

When a service is experiencing high resource utilization, an obvious solution is to add more machines to that service’s server pool.

However, DoorDash recommends that teams _do not_ use reactive-auto-scaling. Doing so can temporarily reduce cluster capacity, making the problem worse.

*   Newly added machines need time to warm up (fill cache, compile code, etc.) and complete startup tasks.
    
*   These behaviors can reduce resources for the warmed up nodes that are serving requests.
    
*   Additionally, in DoorDash’s case auto-scaling occurs infrequently, so having a sudden increase can produce unexpected results.
    

_Instead_, DoorDash recommends predictive auto-scaling, where you expand the cluster’s size based on expected traffic levels throughout the day.

Initially, DoorDash implemented these _locally_ without a global view of the system. For example, a service will just look at its dependencies when deciding to circuit break, or will solely look at its own CPU utilization when deciding to load shed.

To further improve reliability, DoorDash is now taking a global approach. They have started using an open-source tool called [Aperture](https://github.com/fluxninja/aperture?utm_source=blog.neetcode.io&utm_medium=referral&utm_campaign=how-doordash-builds-robust-microservices) which takes counter-measures based on the global state of their systems. Rather than exclusively mitigating issues based on a local view of individual services.

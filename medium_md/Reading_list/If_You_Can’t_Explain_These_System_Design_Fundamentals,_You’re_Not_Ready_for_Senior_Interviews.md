---
title: "If You Can’t Explain These System Design Fundamentals, You’re Not Ready for Senior Interviews"
url: https://medium.com/p/3597df110b12
---

# If You Can’t Explain These System Design Fundamentals, You’re Not Ready for Senior Interviews

[Original](https://medium.com/p/3597df110b12)

# If You Can’t Explain These System Design Fundamentals, You’re Not Ready for Senior Interviews

[![Felipe Limeira](https://miro.medium.com/v2/resize:fill:64:64/1*3PX5boJoTWucwF5WhPVdBA.png)](/@limeira.felipe94?source=post_page---byline--3597df110b12---------------------------------------)

[Felipe Limeira](/@limeira.felipe94?source=post_page---byline--3597df110b12---------------------------------------)

5 min read

·

Feb 11, 2026

--

6

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D3597df110b12&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40limeira.felipe94%2Fif-you-cant-explain-these-system-design-fundamentals-you-re-not-ready-for-senior-interviews-3597df110b12&source=---header_actions--3597df110b12---------------------post_audio_button------------------)

Share

![]()

If you’re preparing for international interviews — or simply want to think like a senior engineer — these are the foundations you cannot ignore.

System Design interviews are not about memorizing architectures.

They are about understanding trade-offs.

Every scalable system is the result of decisions: consistency vs availability, latency vs throughput, simplicity vs scalability. If you understand the fundamentals, you can design almost anything.

This article consolidates the core concepts every software engineer should master.

## Storage: Choosing the Right Data Model

Before scaling anything, you must answer one question:

> How should data be stored?

Press enter or click to view image in full size

![]()

### **Relational Databases (SQL)**

Structured data stored in tables with predefined schemas and relationships (foreign keys).

Examples: PostgreSQL, MySQL.

Best for:

* Strong consistency
* Complex queries
* Financial transactions
* ACID guarantees

Relational databases prioritize **data integrity**.

### **Document-Based Databases (NoSQL)**

Data stored as flexible JSON/BSON documents.

Examples: MongoDB.

Best for:

* Rapid iteration
* Flexible schemas
* Hierarchical or semi-structured data

You trade rigid structure for flexibility.

### Key-Value Stores (NoSQL)

The simplest model: a giant distributed hash map.

Examples: Redis, DynamoDB.

Best for:

* Caching
* Sessions
* High-speed lookups
* Massive horizontal scale

Extremely fast. Extremely scalable.

### **ACID vs BASE**

Understanding this difference is critical in interviews.

### ACID (Typical in SQL)

* **Atomicity** — All or nothing.
* **Consistency** — Valid state to valid state.
* **Isolation** — Transactions behave sequentially.
* **Durability** — Once committed, it stays committed.

Strong correctness guarantees.

### BASE (Typical in Distributed/NoSQL)

* **Basically Available**
* **Soft State**
* **Eventually Consistent**

You accept temporary inconsistency in exchange for availability and scalability.

This trade-off appears everywhere in system design.

## Scalability: Growing Without Breaking

There are two primary ways to scale.

Press enter or click to view image in full size

![]()

### Vertical Scaling (Scale Up)

Increase CPU, RAM, SSD in one machine.

Pros:

* Simple

Cons:

* Hardware limits
* Single Point of Failure (SPOF)

### Horizontal Scaling (Scale Out)

Add more machines.

Pros:

* Near infinite scale
* High availability

Cons:

* Operational complexity
* Data consistency challenges

Most modern large systems scale horizontally.

### Sharding (Partitioning)

Split a massive database into smaller pieces across servers.

Example:

* Users A–M → Server 1
* Users N–Z → Server 2

Goal:

* Parallel writes
* Reduced load per node

### Consistent Hashing

Used in distributed caches and sharded systems.

Nodes are organized in a logical ring.

When adding/removing servers:

* Only a small fraction of keys are remapped.

This avoids massive redistribution and downtime.

This is the kind of detail that differentiates mid-level from senior engineers in interviews.

## Networking: How Data Actually Moves

If you can’t explain networking basics, your system design will collapse under pressure.

### The OSI Model (Simplified View)

* **Layer 7 — Application (HTTP, DNS)**
* **Layer 4 — Transport (TCP, UDP)**
* **Layer 3 — Network (IP routing)**

For system design, Layers 7, 4, and 3 matter most.

### Application Layer (L7)

### **HTTP/HTTPS**

Stateless protocol.  
HTTPS adds TLS encryption.

### REST vs GraphQL vs gRPC

### **REST**

* Resource-based
* Cache-friendly
* Simple

### **GraphQL**

* Client asks exactly what it needs
* Avoids over-fetching
* Harder to cache

### **gRPC**

* Binary protocol (Protobuf)
* Extremely fast
* Ideal for microservices

Choose based on:

* Performance needs
* Flexibility
* Internal vs external APIs

### WebSockets vs SSE

### **WebSockets**

* Bidirectional
* Real-time chats, games

### **SSE**

* Server → Client only
* Notifications, logs, feeds

### Transport Layer (L4)

### **TCP**

Reliable and ordered.  
Used for web traffic.

### **UDP**

Fast but unreliable.  
Used for streaming and gaming.

### Request Lifecycle

1. DNS lookup
2. TCP 3-way handshake
3. Data transfer
4. Connection teardown

Each step adds latency.

### Load Balancing

* **L4 (Network Load Balancer)** → Based on IP/Port
* **L7 (Application Load Balancer)** → Based on HTTP content (URL, headers, cookies)

L7 enables smarter routing.

## Latency vs Throughput

These are not the same.

### **Latency**

Time for one request to complete.

### Throughput

Number of requests per second.

### The Water Pipe Analogy

* Latency = speed of one drop
* Throughput = width of the pipe

### Orders of Magnitude (Critical for Interviews)

* RAM ~ 100 ns
* SSD ~ 100 µs
* HDD ~ 1–10 ms
* Same-region network ~ 1–10 ms
* Cross-region/internet ~ 50–100+ ms

Network calls are expensive.

Unnecessary round trips kill performance.

This is why caching exists.

## Fault Tolerance & Redundancy

Distributed systems fail.

The question is not *if*.  
It’s *when*.

### Fault Tolerance

System continues working even if a component fails.

Goal:  
Eliminate Single Points of Failure.

![]()

### Redundancy Models

### Active-Active

All nodes handle traffic.  
If one fails, others absorb.

### Active-Passive

One active.  
One standby.  
Failover when needed.

### Failure Types

* **Crash Failure** — Server stops.
* **Omission Failure** — Messages lost.
* **Timing Failure** — Delayed responses.
* **Byzantine Failure** — Malicious/incorrect behavior.

Byzantine is the hardest to handle.

### Failure Recovery Techniques

* **Heartbeat** — “I’m alive” signal.
* **Checkpointing** — Save system state.
* **Replication** — Maintain copies of data.

Replication is fundamental for resilience.

## CAP Theorem

In distributed systems, you can only guarantee two of:

* **Consistency**
* **Availability (A)**
* **Partition Tolerance (P)**

Network partitions are inevitable.

So in practice, you choose:

![]()

### CP (Consistency + Partition Tolerance)

Prioritizes correctness.  
May sacrifice availability.

Example:

* Financial systems
* Traditional SQL databases

### AP (Availability + Partition Tolerance)

Always responds.  
May return stale data.

Example:

* Social media feeds
* DNS
* Cassandra
* DynamoDB

CA (Consistency + Availability) only works if networks never fail — which is unrealistic in distributed systems.

System Design is not about knowing tools.

It’s about understanding:

* Trade-offs
* Bottlenecks
* Failure modes
* Latency costs
* Data consistency models

If you deeply understand these fundamentals, you can design:

* A chat app
* A distributed cache
* A video streaming platform
* A payment processor

Because underneath every system is the same set of principles.

Master the fundamentals.

The architecture becomes a consequence.
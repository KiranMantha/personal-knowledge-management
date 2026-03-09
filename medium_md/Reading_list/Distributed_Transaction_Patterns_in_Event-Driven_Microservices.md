---
title: "Distributed Transaction Patterns in Event-Driven Microservices"
url: https://medium.com/p/1743a584176d
---

# Distributed Transaction Patterns in Event-Driven Microservices

[Original](https://medium.com/p/1743a584176d)

Member-only story

# Distributed Transaction Patterns in Event-Driven Microservices

[![Laksh Chauhan](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*w9ulQsFVy23crRFl)](https://medium.com/@laksh.ch21?source=post_page---byline--1743a584176d---------------------------------------)

[Laksh Chauhan](https://medium.com/@laksh.ch21?source=post_page---byline--1743a584176d---------------------------------------)

4 min read

·

Jan 5, 2025

--

8

Listen

Share

More

Software services today can consist of multiple micro-services working together to maintain the “state” of the system. One of the most common challenges in distributed software design is maintaining consistency. An **inconsistent system** can cause all kinds of issues where different services that constitute the overall service don’t agree with the system’s state.

## Example

Consider this, in an e-commerce website, when a customer places an order, we must update the *orders table* to record the order placed and the *rewards table* to record the reward points earned.

Press enter or click to view image in full size

![]()

In a monolithic architecture like above, this is simple. Start a transaction, update the necessary tables, and commit the transaction. If anything goes wrong, all changes are rolled back. But what happens when different services handle order history and rewards?

Press enter or click to view image in full size

![]()

This is known as a **distributed transaction**. For our system to be consistent, multiple services must process an event and in case of any failures in even one of the services, all the other services must roll back their changes.

### The not-so-happy path

But what if an error happens right after writing to the *orders* *table*? The server may crash, the request may timeout, or the *rewards* *service* may even fail to process the event. This makes the system’s state inconsistent. The user will have placed an order but will not receive the reward points.

[Event-driven architecture](https://en.wikipedia.org/wiki/Event-driven_architecture) can ensure the *rewards* service processes the event at least once ***after*** an event is published to the event queue. After inserting into the *orders* *table*, the *orders* *service* sends an event to the *rewards* *service*, and it can eventually process the event and update the required reward points in the *rewards table*.

Press enter or click to view image in full size

![]()

We have achieved [eventual consistency](https://en.wikipedia.org/wiki/Eventual_consistency). But not quite yet. We still haven’t addressed the server crashing right before writing the event to an *event queue*. What if we fail to send the event to the *events queue* itself?

> **Note**: when using message brokers, potential duplicate messages are always a possibility. It is important to design your services to be idempotent regardless of the pattern you go forward with.

Let’s check out some patterns we can use to guarantee the rewards service receives the event.

## Pattern 1: The outbox pattern

The outbox pattern stores the event in an *outbox table* in the same database (in this case) as the *orders table*. Writing to the database can be done under a single transaction so we can insert the order and the outbox event in a single transaction. If either operation fails, the other is rolled back as well.

To emit the events, [Change Data Capture (CDC)](https://en.wikipedia.org/wiki/Change_data_capture) can be used by the rewards service to track changes in the table and process them. CDC refers to tracking the changes made to data in a dataset. For example, Amazon DynamoDB offers [DynamoDB streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html) to capture changes made to a table.

Press enter or click to view image in full size

![]()

### Remember to housekeep the outbox table

This is often forgotten about. The processed events should be removed from the outbox table. This prevents the table from growing larger and larger.

## Pattern 2: Raw event processing

We discussed inserting events in the outbox table and treating these data change events in the rewards service. If emitting events to the rewards service is only required when a change is made to the order history table, Change Data Capture can be used on the order history table along with event filters in favor of creating a separate outbox table. Whenever a new order is added to the order history table, this data change can be captured and treated as an event to the rewards service.

Press enter or click to view image in full size

![]()

## Pattern 3: Reading Yourself Pattern

In both the above examples, we want there to be a single point that emits events that can emit events under a single transaction. We can achieve this by emitting this event through the order history service and consuming it by both the order history service and the rewards service.

Press enter or click to view image in full size

![]()

Here, if step (2) succeeds, it is guaranteed that eventually, both orders and rewards services will process the event and our system’s state will be consistent.

### Other Articles you may be interested in

1. [Why Distributed Locks are important](https://medium.com/dev-genius/why-distributed-locks-are-important-17dfef01a6db)
2. [Load balancing](https://medium.com/@laksh.ch21/the-what-and-how-of-system-design-concepts-load-balancing-1bf435f5adc5)
3. [Database replication](https://medium.com/@laksh.ch21/the-what-and-how-of-system-design-concepts-ii-data-replication-fbe79e38215e)
4. [Database partitioning](https://medium.com/@laksh.ch21/the-what-and-how-of-system-design-concepts-iii-database-partitioning-7a3f78a9e8bd)

Please leave a clap if you liked the content of this article, or leave a comment for any feedback. Thanks for reading! ❤️
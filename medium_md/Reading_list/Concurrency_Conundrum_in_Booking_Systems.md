---
title: "Concurrency Conundrum in Booking Systems"
url: https://medium.com/p/2e53dc717e8c
---

# Concurrency Conundrum in Booking Systems

[Original](https://medium.com/p/2e53dc717e8c)

# Concurrency Conundrum in Booking Systems

[![Abhishek Ranjan](https://miro.medium.com/v2/resize:fill:64:64/1*zLOZXXaU-IkTzRIUXARVlQ.jpeg)](/@abhishekranjandev?source=post_page---byline--2e53dc717e8c---------------------------------------)

[Abhishek Ranjan](/@abhishekranjandev?source=post_page---byline--2e53dc717e8c---------------------------------------)

5 min read

·

Mar 23, 2023

--

6

Listen

Share

More

Recently I was involved in a discussion with a colleague about an age-old problem of handling duplicates while booking. I was surprised to find out that even after all these years, there isn’t a good collection of all the different ways this can be handled.

So here is me telling you the problem and various ways of solving this :

### Problem

This is a common problem which can appear in any of the following ways :

1. The same user clicks on the “book” button multiple times.
2. Multiple users try to book the same Seat/Room/Slot at the same time.
3. How do Airbnb, BookMyShow, MakeMyTrip handle concurrent booking requests

To understand the problem properly let’s assume the following :

1. Let’s say we have a table named *booking*, I have assumed a simplistic design where it can be used for any of the cases mentioned above.

![]()

2. There are two ways this can have a double booking :

> Users Click on Book Button / API multiple times
>
> Multiple users try to book the same seat, *especially in case of a popular movie/show and flights this will happen a lot*

3. The first problem is easy to solve and can be solved by the client as well as the server, which I will discuss in a different article. Here let’s focus in detail on the problem of multiple users trying to book the same seat/room.

### Solutions

**Multiple users try to book the same seat**

Press enter or click to view image in full size

![]()

In the above case If our service just checks before making a new booking if the seat is reserved, then we will have a problem if there are n concurrent requests, thus making multiple bookings for the same seat.

The simplest way to solve the above problem is: ***Database Locking (Optimistic and Pessimistic)***

### ***Optimistic Locking***

This is the simplest way to ensure the quality of data is preserved. [Optimistic Locking](http://en.wikipedia.org/wiki/Optimistic_locking) is a strategy where you read a record, take note of a version number and check that the version hasn’t changed before you write the record back.

With frameworks like Spring Data JPA, it is easy to implement with annotations. You can read more about it at <https://www.baeldung.com/jpa-optimistic-locking>.

For a system like Hotel Booking where the *Number of request/query/transactions per second* might not be very high, this is a great option.

### When this is not sufficient

When there are a lot of concurrent requests, let’s say like in the case of Flight Booking or a Popular movie this has big performance ramifications. Optimistic Lock performs badly if there’s a lot of contention at the same time because this leads to many transactions needing to be abandoned.

If the system is already running at its maximum throughput, retrying a transaction could make performance worse. The system will eventually be able to process all transactions in order, but in the meantime, some may experience delays.

### Pessimistic Locking

[Pessimistic Locking](http://en.wikipedia.org/wiki/Lock_(database)) is when you lock the record for your exclusive use until you have finished with it. It has much better integrity than optimistic locking but requires you to be careful with your application design to avoid [Deadlocks](http://en.wikipedia.org/wiki/Deadlock).

It is based on the principle that if anything might potentially go wrong, it’s better to wait until a situation is safe again before doing anything (*Similar to mutual exclusion in Multi-Threading*)

RDBMS systems like Postgres, MYSQL, and ORACLE all provide ways of doing this.

Even ORMS like Spring Data JPA have a simple way of doing it. This article explains in detail more about this   
<https://www.baeldung.com/java-jpa-transaction-locks#:~:text=When%20using%20Pessimistic%20Locking%2C%20the,specify%20the%20lock%20timeout%20value>.

Now Between the above two, we would assume that all issues will be solved but that’s where the complexity kicks in

> What happens in a distributed system

A Lock in a distributed environment is more than just a mutex in multi-threaded applications. It is more sophisticated and complex because now this lock can be acquired by different nodes in the system and any of them can fail. This increases the complexity manifold as we need the rest of our system to still work flawlessly even if one or more nodes fail.

### Distributed Locks

Distributed locking is a technique used to coordinate access to shared resources among multiple processes in a distributed system. The main objective is to ensure that only one process at a time can access a particular resource, preventing race conditions, data corruption, or inconsistency.

For implementation, we can use some solutions like :

* [**Redis**](https://redis.io/topics/distlock), uses libraries that implement lock algorithms like [ShedLock](https://github.com/lukas-krecan/ShedLock), and [Redisson](https://github.com/redisson/redisson/wiki/8.-Distributed-locks-and-synchronizers). Using this is not advisable as discussed in (<https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html>)
* [**Hazelcast**](https://hazelcast.com/blog/long-live-distributed-locks/) offers a lock system based on its [CP subsystem](https://docs.hazelcast.org/docs/3.12.3/manual/html-single/index.html#cp-subsystem). (<https://hazelcast.com/blog/long-live-distributed-locks/>)
* **Zookeeper**, I will be discussing this in detail below

## Implementing Distributed Locking with Apache ZooKeeper

Apache ZooKeeper is a distributed coordination service that can be used to implement distributed locking. The following Java code sample demonstrates a basic distributed lock using ZooKeeper

```
import org.apache.zookeeper.ZooKeeper;  
import org.apache.curator.framework.CuratorFramework;  
import org.apache.curator.framework.CuratorFrameworkFactory;  
import org.apache.curator.retry.ExponentialBackoffRetry;  
import org.apache.curator.framework.recipes.locks.InterProcessMutex;  
  
import java.util.concurrent.TimeUnit;  
  
public class DistributedLock {  
    private CuratorFramework client;  
    private InterProcessMutex lock;  
  
    public DistributedLock(String zkConnectionString, String lockPath) {  
        client = CuratorFrameworkFactory.newClient(zkConnectionString, new ExponentialBackoffRetry(1000, 3));  
        client.start();  
        lock = new InterProcessMutex(client, lockPath);  
    }  
  
    public boolean acquire(long waitTime, TimeUnit timeUnit) {  
        try {  
            return lock.acquire(waitTime, timeUnit);  
        } catch (Exception e) {  
            e.printStackTrace();  
            return false;  
        }  
    }  
  
    public void release() {  
        try {  
            lock.release();  
        } catch (Exception e) {  
            e.printStackTrace();  
        }  
    }  
  
    public void close() {  
        client.close();  
    }  
}
```

### Usage

```
public static void main(String[] args) {  
    String zkConnectionString = "127.0.0.1:2181";  
    String lockPath = "/my_resource_lock";  
  
    DistributedLock lock = new DistributedLock(zkConnectionString, lockPath);  
  
    // Acquire the lock  
    if (lock.acquire(100, TimeUnit.MILLISECONDS)) {  
        // Access the shared resource  
        // Perform your operations here  
  
        // Release the lock  
        lock.release();  
    }  
  
    // Close the ZooKeeper connection  
    lock.close();  
  
}
```

### Lock Acquisition

Press enter or click to view image in full size

![]()

## Lock Release

Press enter or click to view image in full size

![]()

By using Apache ZooKeeper, we have implemented a distributed locking mechanism in Java that helps maintain consistency and coordinate access to shared resources in a distributed system. This mechanism allows processes to acquire and release locks, ensuring that only one process has access to a particular resource at a time.
---
title: "How to Prevent 10,000 Concurrent Database Hits in 2 Seconds"
url: https://medium.com/p/16fc9b912526
---

# How to Prevent 10,000 Concurrent Database Hits in 2 Seconds

[Original](https://medium.com/p/16fc9b912526)

Member-only story

# How to Prevent 10,000 Concurrent Database Hits in 2 Seconds

[![Byte Me Daily](https://miro.medium.com/v2/resize:fill:64:64/1*8llr8wr5dCePTTffP3pcvQ.png)](/?source=post_page---byline--16fc9b912526---------------------------------------)

[Byte Me Daily](/?source=post_page---byline--16fc9b912526---------------------------------------)

4 min read

·

Dec 29, 2025

--

5

Listen

Share

More

## 1. The Cache That Took the Database Down

The graph looked fine until it didn’t.

Traffic spiked — nothing unusual. The cache hit ratio hovered around 95%, right where it should be. Then, within two seconds, the database CPU went vertical. Connections piled up. Latency exploded. Alerts cascaded like dominoes.

Nothing was “wrong” in the usual sense. No deploy. No schema change. No bad query. Just a hot cache key that expired at exactly the wrong moment.

What followed was a classic cache stampede: thousands of requests discovering the same missing key and politely — then desperately — asking the database for answers at the same time.

Press enter or click to view image in full size

![]()

This article isn’t a blame-filled postmortem. It’s a practical guide to making sure you never have to explain why a healthy cache took down a healthy database in under two seconds.

## 2. What a Cache Stampede Actually Looks Like

At a mechanical level, cache stampedes are boring. That’s what makes them dangerous.

Here’s the sequence almost every time:

* You have a **hot key** (homepage config, pricing, feature flags).
* It has a **shared TTL** across instances.
* The TTL expires.
* Thousands of concurrent requests miss simultaneously.
* All of them fall through to the database.

A simplified timeline looks like this:

```
Time →  
---------------------------------------------------  
t=0s      Cache hit (TTL about to expire)  
t=1s      TTL expires  
t=1.1s    Request 1 → DB  
t=1.1s    Request 2 → DB  
t=1.1s    Request 3 → DB  
...  
t=1.1s    Request 10,000 → DB  
---------------------------------------------------
```

The database isn’t slow because it’s bad. It’s slow because it was never meant to handle synchronized curiosity from 10,000 polite application servers.

## 3. Why Naive TTLs Fail Under Load

“Just cache it for five minutes” works — until it doesn’t.

The problem isn’t the TTL value. It’s **synchronization**.

In distributed systems, caches don’t expire independently. They expire together. Every instance shares roughly the same clock, the same TTL, and the same access pattern.

Under load, that creates a cliff:

* Before expiration: near-zero database load.
* After expiration: a sudden, synchronized collapse onto the database.

This isn’t bad tuning or missing hardware. It’s a design flaw. Fixed TTLs assume requests are evenly distributed over time. Real traffic never is.

## 4. Pattern #1: Stale-While-Revalidate

The first fix feels wrong until you ship it: **serve stale data on purpose**.

Stale-while-revalidate means:

* If cached data is expired but present, serve it immediately.
* Trigger a background refresh.
* Update the cache when the refresh completes.

Users almost never notice. Systems always do.

Flow-wise, it looks like this:

```
Request  
   |  
   v  
Cache (expired but present)  
   |  
   +--> Serve stale data immediately  
   |  
   +--> Trigger async refresh  
              |  
              v  
           Database  
              |  
              v  
           Update cache
```

You trade a few seconds of staleness for massive load protection. For most “hot” data — configs, metadata, counters — this is an easy call. Perfect freshness is expensive. Slight staleness is cheap.

## 5. Pattern #2: Probabilistic Early Expiration

Even with stale-while-revalidate, you don’t want everyone refreshing at once.

Probabilistic early expiration spreads refreshes over time by introducing randomness. Instead of expiring strictly at TTL, each request has a small chance of triggering a refresh *before* expiry.

Conceptually:

```
TTL window  
------------------------------------------------  
|        |        |        |        |        |  
|   R    |        |   R    |        |    R   |  
------------------------------------------------  
R = random early refresh
```

Instead of one giant spike, you get many small refreshes. The database sees a steady trickle instead of a synchronized flood.

The key insight: **expiration is not a single moment**. It’s a probability distribution. Once you accept that, the herd disappears.

## 6. Pattern #3: Mutex / Single-Flight Refresh

Sometimes you need freshness — or the data is expensive enough that duplicate refreshes hurt.

In those cases, use a mutex (or “single-flight”) pattern:

* The first request acquires a lock and refreshes the cache.
* Others either wait briefly or serve stale data.
* Only one database hit happens.

Visually:

```
Requests  
   |  
   v  
Cache miss  
   |  
   v  
Acquire lock?  
   |  
   +--> Yes → Refresh from DB → Update cache → Release lock  
   |  
   +--> No  → Serve stale OR wait
```

The tradeoff is latency for the unlucky request holding the lock. But that latency is contained. Database collapse isn’t.

Used carefully, this pattern turns stampedes into orderly queues.

## 7. What This Actually Buys You (With Numbers)

When these patterns are applied together, the impact is dramatic.

Before:

```
DB Load  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
|                                   |  
|                                   |  
|            SPIKE                  |  
|^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^|  
------------------------------------- Time
```

After:

```
DB Load  
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  
|     ~~~     ~~~     ~~~           |  
|   ~~~   ~~~   ~~~                 |  
| ~~~                               |  
|                                   |  
------------------------------------- Time
```

In real systems, this translates to:

* **50–90% reduction** in database load during expiration events.
* Smoother latency curves.
* Fewer cascading failures when traffic spikes.

You don’t eliminate load. You shape it.

## 8. Common Mistakes That Reintroduce Stampedes

Most teams regress accidentally.

Common failure modes:

* TTLs so short they negate all smoothing.
* Blocking *all* requests on refresh instead of serving stale data.
* No fallback when refresh fails, causing retries to pile up.
* Treating cache expiry as an error instead of a normal state.

Every one of these shows up only under pressure — when it’s hardest to debug.

## 9. When You Can Ignore This

Not every system needs this sophistication.

You can probably ignore stampedes if:

* Traffic is low and burst-free.
* Keys aren’t hot.
* The service is short-lived or internal-only.

That’s not laziness — that’s proportional engineering. The danger is assuming you’re still in this category after growth.

## 10. Stale Data Is Cheaper Than Downtime

The hardest lesson is psychological: caching isn’t about correctness. It’s about **load shaping**.

Perfect freshness is a luxury. Availability is not.

Every high-traffic system eventually learns this — either calmly in design, or painfully during an incident. Serving slightly stale data for a few seconds is almost always cheaper than explaining why your database melted in two.

If you’ve lived through a cache expiry horror story, you’re not alone. Share it in the comments. Someone else is one TTL away from learning the same lesson.
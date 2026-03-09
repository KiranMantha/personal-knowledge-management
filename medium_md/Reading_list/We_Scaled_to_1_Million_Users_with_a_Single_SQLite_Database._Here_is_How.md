---
title: "We Scaled to 1 Million Users with a Single SQLite Database. Here is How"
url: https://medium.com/p/c57e965d580d
---

# We Scaled to 1 Million Users with a Single SQLite Database. Here is How

[Original](https://medium.com/p/c57e965d580d)

Member-only story

# We Scaled to 1 Million Users with a Single SQLite Database. Here is How

[![The Thread Whisperer](https://miro.medium.com/v2/resize:fill:64:64/1*1OJwhDGJkOyNc7-ya2TA7w.jpeg)](/@maahisoft20?source=post_page---byline--c57e965d580d---------------------------------------)

[The Thread Whisperer](/@maahisoft20?source=post_page---byline--c57e965d580d---------------------------------------)

3 min read

·

Jan 12, 2026

--

3

Listen

Share

More

The scariest scaling plan I have ever shipped was a file named app.db.

Press enter or click to view image in full size

![]()

Not a cluster. One SQLite database on one machine, while the user count kept climbing and my stomach tightened every time the latency chart twitched.

If you have ever felt that mix of pride and fear when the product finally works, this is for you.

## Reality Check Before The Hot Takes

This was a read heavy app: feeds, profiles, notifications, and search results. Writes existed, but most requests were reads. Peak traffic reached about 25,000 requests per minute. The database lived on local NVMe with enough RAM to cache hot pages.

## The Failure That Forced Us To Grow Up

Some requests started timing out for no clear reason. I blamed the network. Then I blamed the cloud. Then I added retries and called it a fix.

It got worse.

The truth was boring: readers were getting blocked by writers, and a few queries were scanning tables because we never earned our indexes. SQLite was not breaking. Our habits were.

## The Architecture That Stopped The Lock Fights

At first, every app server opened its own connection and hammered the same database file. That works until it does not.

We moved database access behind a small internal DB worker. App servers stayed stateless. The worker handled reads, batched writes, and gave us one place to tune SQLite.

```
Users → CDN/Cache → App Servers → DB Worker → SQLite (Local NVMe)  
                          │  
                          └→ Write Queue (Batch Flush)
```

Once there was one door to the database, nobody could sneak in a surprise write on the request path.

We capped connections, kept the file on the same disk as the process, and hourly snapshot backups ran quietly in the background.

## The Pragmas That Changed The Mood

We enabled WAL so reads could continue while a writer was active. We set synchronous to NORMAL for a sane balance on modern disks. We added a busy timeout so lock contention waited briefly instead of failing instantly. Then we sized the cache so hot pages stayed hot.

```
func Open(path string) (*sql.DB, error) {  
  db, err := sql.Open("sqlite3", path+"?_busy_timeout=5000&_foreign_keys=1")  
  if err != nil { return nil, err }  
  db.Exec("PRAGMA journal_mode=WAL;")  
  db.Exec("PRAGMA synchronous=NORMAL;")  
  db.Exec("PRAGMA temp_store=MEMORY;")  
  db.Exec("PRAGMA cache_size=-200000;")  
  db.SetMaxOpenConns(8)  
  db.SetMaxIdleConns(8)  
  return db, nil  
}
```

## Treat Writes Like A Budget

Our breakthrough was not faster hardware. It was deciding that writes were expensive.

We stopped writing on every request. We pushed non critical updates into a queue. The DB worker flushed them in batches inside transactions. One transaction per event is a tax. One transaction per batch is a different economy.

The product felt faster because it was. The database stopped thrashing on small commits and started doing work in clean chunks.

## The Indexes That Made The Claim True

At one million users, guessing is not engineering.

We pulled the slow queries, looked at filters and sort order, and built indexes that matched the access path. Our most common pattern was user\_id plus created\_at, so we indexed for that shape. The query planner stopped scanning and started behaving.

This is the part that hurt my ego: the outage energy came from a missing composite index, not from SQLite limits.

## What The Numbers Looked Like

On a single 8 vCPU machine with NVMe and 32 GB RAM:

```
| Metric              | Typical              |  
| ------------------- | -------------------- |  
| Read P95            | 8 to 12 ms           |  
| Write P95 (Batched) | 25 to 40 ms          |  
| Database Size       | 18 GB                |  
| Peak Requests       | About 25k per minute |
```

Those numbers are not universal. They came from a workload that respected SQLite’s strengths.

## When We Outgrew It

We eventually migrated, not because SQLite failed, but because our product changed. We added features that created heavier concurrent writes. That is when a single file stops being an advantage and starts being a ceiling.

SQLite did not scale our app. Measurement, batching, and restraint did.
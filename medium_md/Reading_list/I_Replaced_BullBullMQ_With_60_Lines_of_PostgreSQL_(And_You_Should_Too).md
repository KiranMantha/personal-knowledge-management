---
title: "I Replaced Bull/BullMQ With 60 Lines of PostgreSQL (And You Should Too)"
url: https://medium.com/p/cad77c8ffdc6
---

# I Replaced Bull/BullMQ With 60 Lines of PostgreSQL (And You Should Too)

[Original](https://medium.com/p/cad77c8ffdc6)

# I Replaced Bull/BullMQ With 60 Lines of PostgreSQL (And You Should Too)

[![Ignatius Sani](https://miro.medium.com/v2/resize:fill:64:64/1*vfJuP8Hu5o8CXDGYP-U5oQ.jpeg)](/@Iggy01?source=post_page---byline--cad77c8ffdc6---------------------------------------)

[Ignatius Sani](/@Iggy01?source=post_page---byline--cad77c8ffdc6---------------------------------------)

4 min read

·

Jan 15, 2026

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

## Why your database is already a message queue — and why Redis might be killing your productivity

Last month, I debugged a startup’s “job queue” that was actually just Redis eating $200/month to process 47 emails per day. When I asked why they chose Bull + Redis, the answer was: “We read that Uber uses Kafka.”

This happens everywhere. A developer with 500 users sets up Redis clusters, manages job priorities, and debugs connection pool issues because they assumed they needed the same architecture as companies processing billions of events.

The real cost isn’t infrastructure. It’s cognitive overhead.

Every new developer needs to understand your queue topology. Every deploy coordinates Redis availability. Every bug requires distributed tracing across systems. You’ve added weeks of complexity to solve a problem that doesn’t exist yet.

**Here’s what actually works:** Use your database as a queue until it measurably breaks.

## Your Database Already Does This

PostgreSQL can handle job queues for 100,000+ jobs per day. It’s already running, already backed up, already understood by your team. The failure modes are simple. The debugging tools are familiar.

You don’t need Redis. You need a jobs table and a worker process.

That’s it.

## The Implementation

**Step 1: Create the jobs table**

```
CREATE TABLE jobs (  
  id SERIAL PRIMARY KEY,  
  job_type VARCHAR(100) NOT NULL,  
  payload JSONB NOT NULL,  
  status VARCHAR(20) DEFAULT 'pending',  
  attempts INT DEFAULT 0,  
  max_attempts INT DEFAULT 3,  
  scheduled_at TIMESTAMP DEFAULT NOW(),  
  created_at TIMESTAMP DEFAULT NOW(),  
  completed_at TIMESTAMP,  
  error TEXT  
);  
  
CREATE INDEX idx_jobs_pending ON jobs(status, scheduled_at)   
  WHERE status = 'pending';
```

This table handles retries, scheduling, and error tracking — everything Bull gives you, but you can debug it with `SELECT * FROM jobs WHERE status = 'failed'`.

**Step 2: Build the worker**

```
const { Pool } = require('pg');  
  
const pool = new Pool({  
  connectionString: process.env.DATABASE_URL  
});  
  
async function claimJob(client) {  
  const result = await client.query(`  
    UPDATE jobs  
    SET status = 'processing'  
    WHERE id = (  
      SELECT id FROM jobs  
      WHERE status = 'pending'   
        AND scheduled_at <= NOW()  
      ORDER BY scheduled_at  
      LIMIT 1  
      FOR UPDATE SKIP LOCKED  
    )  
    RETURNING id, job_type, payload  
  `);  
    
  return result.rows[0];  
}  
  
async function processJob(job) {  
  switch (job.job_type) {  
    case 'send_email':  
      await sendEmail(job.payload.to, job.payload.subject);  
      break;  
    case 'process_upload':  
      await processUpload(job.payload.file_id);  
      break;  
  }  
}  
  
async function markComplete(client, jobId) {  
  await client.query(  
    `UPDATE jobs   
     SET status = 'completed', completed_at = NOW()  
     WHERE id = $1`,  
    [jobId]  
  );  
}  
  
async function markFailed(client, jobId, error) {  
  await client.query(  
    `UPDATE jobs   
     SET attempts = attempts + 1,  
         status = CASE   
           WHEN attempts + 1 >= max_attempts THEN 'failed'  
           ELSE 'pending'  
         END,  
         scheduled_at = CASE  
           WHEN attempts + 1 < max_attempts   
           THEN NOW() + (POW(2, attempts) * INTERVAL '1 minute')  
           ELSE scheduled_at  
         END,  
         error = $1  
     WHERE id = $2`,  
    [error, jobId]  
  );  
}  
  
async function runWorker() {  
  while (true) {  
    const client = await pool.connect();  
      
    try {  
      const job = await claimJob(client);  
        
      if (!job) {  
        client.release();  
        await new Promise(resolve => setTimeout(resolve, 1000));  
        continue;  
      }  
        
      try {  
        await processJob(job);  
        await markComplete(client, job.id);  
      } catch (error) {  
        await markFailed(client, job.id, error.message);  
        console.error(`Job ${job.id} failed:`, error);  
      }  
        
      client.release();  
    } catch (error) {  
      client.release();  
      console.error('Worker error:', error);  
      await new Promise(resolve => setTimeout(resolve, 5000));  
    }  
  }  
}  
  
runWorker();
```

Sixty lines. No external queue. No Redis config. No Bull dashboard.

**Step 3: Enqueue jobs from your API**

```
async function uploadDocument(req, res) {  
  const fileId = await saveFile(req.file);  
    
  await pool.query(  
    `INSERT INTO jobs (job_type, payload)  
     VALUES ($1, $2)`,  
    ['process_upload', JSON.stringify({ file_id: fileId })]  
  );  
    
  res.json({ status: 'processing', file_id: fileId });  
}
```

*When something breaks, you query the jobs table. When you need to retry, you update the status. When you’re debugging at 2 am, you’re using SQL, not learning Bull’s retry semantics.*

## What You’re Avoiding

**Don’t use Redis for durable queues.** Redis is great as a cache. Terrible as a job queue. When your worker crashes, jobs disappear. Yes, Redis has persistence modes, but now you’re configuring RDB snapshots and worrying about data loss windows.

**Don’t introduce Bull until you have proof you need it.** These libraries add dependencies, configuration, and abstractions. The code above is 60 lines you can understand completely. Bull requires learning Redis configuration, serialization formats, and separate dashboard tools.

**Don’t build a microservice for jobs.** Your worker runs as a separate process on the same server as your API. Use PM2, Docker Compose, or systemd to manage it. A separate service means separate deploys, separate monitoring, and separate failure modes for no benefit.

**Don’t add frameworks “just in case.”** You might never need job priorities, job chaining, or complex retry logic. When you do, you’ll know exactly what you need and can migrate intentionally.

## When This Stops Working

This approach works until you hit real limits:

**Volume:** Processing 10,000+ jobs per second makes database polling expensive. But at that scale, you have other reasons for message queues (event-driven architecture, multiple consumers, real-time requirements).

**Latency:** Jobs that must start within milliseconds need something faster than database polling. But most background jobs don’t care. Sending emails, generating reports, and processing uploads can wait one second.

**Existing infrastructure:** If you already run Redis or RabbitMQ for caching or pub/sub, adding job queues makes sense. The marginal cost is low. But don’t introduce Redis just for jobs.

**Advanced patterns:** Pub/sub to multiple consumers, exactly-once processing, or complex fanout requires proper message brokers. But most apps never need these.

When you graduate to a real queue, you’ll have:

* Usage metrics prove the database is too slow
* A well-defined job structure that makes migration straightforward
* The operational capacity to run additional infrastructure properly

## The Point

Your database is already a queue. It’s durable, transactional, and has excellent tooling.

Use it until you have concrete evidence you’ve outgrown it.

The boring solution isn’t sexy. But it ships today and still works two years from now.

Real scaling happens after you have users, not before. Build the simple thing, ship it, and solve actual problems when they exist.
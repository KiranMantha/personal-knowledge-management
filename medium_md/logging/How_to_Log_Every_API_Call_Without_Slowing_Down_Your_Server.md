---
title: "How to Log Every API Call Without Slowing Down Your Server"
url: https://medium.com/p/8d3437bf7a33
---

# How to Log Every API Call Without Slowing Down Your Server

[Original](https://medium.com/p/8d3437bf7a33)

# How to Log Every API Call Without Slowing Down Your Server

[![Arunangshu Das](https://miro.medium.com/v2/resize:fill:64:64/1*2bvgMQpfaXC6QJlXSnR3tg.jpeg)](/?source=post_page---byline--8d3437bf7a33---------------------------------------)

[Arunangshu Das](/?source=post_page---byline--8d3437bf7a33---------------------------------------)

6 min read

·

Aug 12, 2025

--

11

Listen

Share

More

Press enter or click to view image in full size

![How to Log Every API Call Without Slowing Down Your Server]()

When you’re running an API — whether it’s a microservice powering part of a big system or a monolithic app — **logging is your black box recorder**.

Every request that comes in tells a story:

* Who made the request?
* What endpoint did they hit?
* How long did it take to respond?
* Did we return the right data or blow up with a 500 error?

These answers are critical for debugging, auditing, analytics, and compliance.

**But here’s the catch:**  
 If you log every API call the wrong way, you can unintentionally **slow down your server** — sometimes by a lot. Logging can block your event loop, fill up disk I/O, and even cause downtime during traffic spikes.

## Why Logging Hurts Performance (If Done Wrong)

Most developers start with something like:

```
app.use((req, res, next) => {  
  console.log(`${req.method} ${req.url}`);  
  next();  
});
```

It’s quick, it works… and it’s fine **until you get traffic**.

**The problems start when:**

* **Synchronous logging** (like `console.log`) blocks the event loop, especially if writing to a file.
* **Disk I/O** becomes the bottleneck when you dump logs directly to local files in real time.
* **Network latency** kicks in if you’re sending logs directly to a remote server for storage.
* **Log volume** grows faster than expected, eating disk space or hitting size limits.

A few milliseconds per request may not seem like much — until you multiply it by thousands of concurrent requests. Suddenly, your API is spending more time logging than processing requests.

## The Golden Rule of Fast Logging

> ***“Never make your main request handler wait for the logs to be written.”***

That means your logging system should work **asynchronously** and, ideally, **off the main execution path**.

## Step 1: Decide What to Log

Before thinking about optimization, nail down **what you actually need to capture**. Over-logging is a common mistake that wastes resources.

Typical API call logs include:

* **Timestamp**
* **HTTP Method** (GET, POST, PUT, DELETE…)
* **URL / Route**
* **Query Params** and **Body** (with sensitive data masked)
* **Client IP Address**
* **User Agent**
* **Response Status Code**
* **Response Time** (latency)
* **Error messages** (if any)
* **Authenticated User ID** (if applicable)
* **Request ID / Correlation ID** (for tracing across services)

**Example log entry:**

```
{  
  "time": "2025-08-11T14:23:45.123Z",  
  "method": "POST",  
  "url": "/api/orders",  
  "status": 201,  
  "responseTimeMs": 123,  
  "userId": "usr_1a2b3c",  
  "ip": "203.0.113.42",  
  "userAgent": "Mozilla/5.0 (Macintosh...)",  
  "requestId": "req_abcd1234"  
}
```

## Step 2: Use a Non-Blocking Logger

Forget `console.log` for production. Use a logger designed for **high performance and async writes**.

Some great Node.js logging libraries:

* **Pino** — extremely fast JSON logger (~10x faster than `winston`)
* [**Bunyan**](https://github.com/trentm/node-bunyan) — structured logging with streams
* [**Winston**](https://github.com/winstonjs/winston) — flexible, multiple transports, good for enterprise
* **Log4js** — feature-rich, inspired by Java’s Log4j

**Example with Pino:**

```
const pino = require('pino');  
const logger = pino({  
  level: 'info',  
  transport: {  
    target: 'pino-pretty'  
  }  
});  
  
app.use((req, res, next) => {  
  const start = Date.now();  
    
  res.on('finish', () => {  
    logger.info({  
      method: req.method,  
      url: req.originalUrl,  
      status: res.statusCode,  
      responseTime: Date.now() - start  
    });  
  });  
    
  next();  
});
```

Why Pino? Because it’s:

* **Asynchronous by default**
* Uses **fast JSON serialization**
* Built for **high throughput**

## Step 3: Write Logs to a Buffer, Not Directly

If you write every log line straight to disk or a remote server, you’re asking for latency.

Instead:

* **Buffer logs in memory** (e.g., store them in an array for a few seconds)
* **Flush periodically** or when a buffer size limit is reached
* This turns thousands of tiny writes into fewer large writes

**Example:**

```
let logBuffer = [];  
const BUFFER_SIZE = 50;  
const FLUSH_INTERVAL = 5000; // ms  
  
function flushLogs() {  
  if (logBuffer.length > 0) {  
    // Imagine writing to a file or sending to a log server  
    logger.info({ batch: logBuffer });  
    logBuffer = [];  
  }  
}  
  
setInterval(flushLogs, FLUSH_INTERVAL);  
  
app.use((req, res, next) => {  
  const start = Date.now();  
  
  res.on('finish', () => {  
    logBuffer.push({  
      method: req.method,  
      url: req.originalUrl,  
      status: res.statusCode,  
      time: Date.now(),  
      latency: Date.now() - start  
    });  
  
    if (logBuffer.length >= BUFFER_SIZE) {  
      flushLogs();  
    }  
  });  
  
  next();  
});
```

## Step 4: Offload Logging to a Worker Process

For **heavy traffic APIs**, even in-process buffering might slow you down.

**Better approach:**

* Send logs to a **separate logging service** or a **background worker**
* Main API process → pushes log data to a **message queue** (e.g., RabbitMQ, Kafka, Redis Streams)
* Worker consumes logs and writes to storage asynchronously

**Example using Redis Pub/Sub:**

```
const Redis = require('ioredis');  
const pub = new Redis();  
  
app.use((req, res, next) => {  
  const start = Date.now();  
  
  res.on('finish', () => {  
    pub.publish('api_logs', JSON.stringify({  
      method: req.method,  
      url: req.originalUrl,  
      status: res.statusCode,  
      latency: Date.now() - start  
    }));  
  });  
  
  next();  
});
```

Worker:

```
const sub = new Redis();  
sub.subscribe('api_logs');  
sub.on('message', (channel, message) => {  
  const logData = JSON.parse(message);  
  // Write logData to database or log storage  
});
```

## Step 5: Use Asynchronous Remote Logging

If you must send logs to a **centralized system** like:

* ELK Stack (Elasticsearch, Logstash, Kibana)
* Datadog
* Graylog
* Loggly
* AWS CloudWatch

… make sure you **batch** or **async send** logs to avoid blocking requests.

Example with **Winston + CloudWatch**:

```
const winston = require('winston');  
require('winston-cloudwatch');  
  
winston.add(new winston.transports.CloudWatch({  
  logGroupName: 'my-api-logs',  
  logStreamName: 'production',  
  awsRegion: 'us-east-1',  
  jsonMessage: true  
}));  
  
app.use((req, res, next) => {  
  const start = Date.now();  
  res.on('finish', () => {  
    winston.info({  
      method: req.method,  
      url: req.originalUrl,  
      status: res.statusCode,  
      latency: Date.now() - start  
    });  
  });  
  next();  
});
```

## Step 6: Mask Sensitive Data

You **must** protect user privacy and security while logging.  
 Never log:

* Passwords
* Credit card numbers
* API keys / Tokens
* Personal Identifiable Information (PII) without encryption

**Example masking:**

```
function maskSensitive(obj) {  
  const clone = { ...obj };  
  if (clone.password) clone.password = '******';  
  if (clone.cardNumber) clone.cardNumber = '**** **** **** ' + clone.cardNumber.slice(-4);  
  return clone;  
}  
  
app.use(express.json());  
app.use((req, res, next) => {  
  req.body = maskSensitive(req.body);  
  next();  
});
```

## Step 7: Measure & Tune Logging Overhead

You won’t know if logging slows you down unless you measure.

Track:

* **Average Response Time before vs after logging**
* **CPU usage during peak traffic**
* **Memory usage** (buffers shouldn’t grow uncontrollably)
* **Disk I/O stats**

Tools:

* `ab` (ApacheBench)
* `autocannon` (for Node)
* APM tools (New Relic, Datadog, AppDynamics)

## Step 8: Rotate & Archive Logs

If you log every API call, your logs will grow fast.  
 Set up **log rotation**:

* Rotate daily or when the file hits a size limit (e.g., 100 MB)
* Compress old logs
* Move them to cheaper storage (AWS S3, Glacier)

With Pino:

```
pino server.js | tee >(pino-pretty) | rotatelogs ./logs/api-%Y-%m-%d.log 86400
```

## Step 9: Go Distributed for High Scale

At very high scale:

* **Avoid writing logs locally** at all (use remote collectors)
* Use **log shippers** like Filebeat or Fluent Bit to forward logs
* Consider **Kafka + ELK** for processing millions of log events per minute
* Apply **sampling** if not every request needs full details (e.g., log only 1% of successful 200 OKs but 100% of 500 errors)

## Step 10: A Real-World Production Setup

Here’s what a **high-scale, low-latency API logging pipeline** looks like:

1. **API Gateway** (e.g., Nginx, Kong) logs request metadata → sends to Kafka
2. **App Server** logs enriched info (user IDs, business data) → sends to Kafka asynchronously
3. **Kafka Consumers** process logs → write to Elasticsearch for searching
4. **Kibana / Grafana** dashboards visualize logs in real time
5. **Alerts** trigger on error spikes, slow endpoints, or unusual traffic patterns

This setup ensures your **API is never blocked** by logging overhead, even during traffic bursts.

## Key Takeaways

* **Don’t block the request path** — log asynchronously.
* **Use a fast logger** like Pino for Node.js.
* **Buffer and batch logs** before writing or sending.
* **Offload logs** to workers or remote queues.
* **Mask sensitive data** before storing.
* **Rotate logs** and archive old data to save storage.
* **Monitor performance** to ensure logging doesn’t become a bottleneck.

**You may also like:**

1. [5 Benefits of Using Worker Threads in Node.js](/5-benefits-of-using-worker-threads-in-node-js-455dac1e4e92)

2. [7 Best Practices for Sanitizing Input in Node.js](https://medium.com/devmap/7-best-practices-for-sanitizing-input-in-node-js-e61638440096)

3. [5 AI Developer Tools to Double Your Coding Speed](/top-10-large-companies-using-node-js-for-backend-f32aa3e55cdd)

4. [10 Essential Steps to Organize Node.js Projects on Cloudways](/10-essential-steps-to-organize-node-js-projects-on-cloudways-5f4bdba2eefe)

5. [10 Mistakes Developers Make When Deploying to AWS EC2](https://medium.com/@arunangshudas/10%20Mistakes%20Developers%20Make%20When%20Deploying%20to%20AWS%20EC2)

6. [6 Common Misconceptions About Node.js Event Loop](https://dev.to/arunangshu_das/6-common-misconceptions-about-nodejs-event-loop-3kio)

7. [Deploy a Node.js App on Cloudways in 10 Minutes](/deploy-a-node-js-app-on-cloudways-in-10-minutes-a779cb8528b2)

8. [5 Reasons to Deep Copy Request Payloads in Node.js](/5-reasons-to-deep-copy-request-payloads-in-node-js-8ee6bc275ff9)

9. [5 Essential Tips for Managing Complex Objects in JavaScript](/5-essential-tips-for-managing-complex-objects-in-javascript-b7cd63d52e6e)

10. [7 API Best Practices Every Backend Developer Should Follow](/7-api-best-practices-every-backend-developer-should-follow-dfc10b5a9c88)

**Read more blogs from** [**Here**](https://arunangshudas.com/blog)

**You can easily reach me with a** [**quick call right from here.**](https://topmate.io/arunangshudas)

Share your experiences in the comments, and let’s discuss how to tackle them!

**Follow me on** [**LinkedIn**](https://www.linkedin.com/in/arunangshu-das/)
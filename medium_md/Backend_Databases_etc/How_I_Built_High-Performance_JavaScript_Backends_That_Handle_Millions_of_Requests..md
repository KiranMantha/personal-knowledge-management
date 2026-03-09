---
title: "How I Built High-Performance JavaScript Backends That Handle Millions of Requests."
url: https://medium.com/p/083af8028ebf
---

# How I Built High-Performance JavaScript Backends That Handle Millions of Requests.

[Original](https://medium.com/p/083af8028ebf)

# How I Built High-Performance JavaScript Backends That Handle Millions of Requests.

[![Owen Miles](https://miro.medium.com/v2/resize:fill:64:64/1*DkQEYEW84qWks2o2EUiTXQ.jpeg)](https://medium.com/@official.owenmiles?source=post_page---byline--083af8028ebf---------------------------------------)

[Owen Miles](https://medium.com/@official.owenmiles?source=post_page---byline--083af8028ebf---------------------------------------)

3 min read

·

Feb 8, 2026

--

Listen

Share

More

Engineering Node.js Systems That Stay Fast Under Extreme Load.

For a long time, I believed performance was about hardware.  
Bigger servers.  
More memory.  
More cores.  
So I kept upgrading machines.  
And my systems still slowed down.  
Latency spikes.  
Timeouts.  
Dropped connections.  
Angry users.  
That’s when I learned the uncomfortable truth:  
Most performance problems are architectural.  
Not infrastructural.  
This article is how I design JavaScript backends that handle millions of requests per day without sweating.

**1) Understanding Why Most Node.js Servers Slow Down.**  
Node.js is single-threaded.  
That’s its power.  
That’s its weakness.  
Bad code:

```
app.get("/report", async (req, res) => {  
  const data = fs.readFileSync("bigfile.json");  
  res.send(data);  
});
```

One blocking call.  
Every user waits.  
Better:

```
import { promises as fs } from "fs";  
  
app.get("/report", async (req, res) => {  
  const data = await fs.readFile("bigfile.json");  
  res.send(data);  
});
```

Rule:  
Never block the event loop.  
Ever.

**2) Designing APIs Around Asynchronous Pipelines.**  
Request handling should be pipelines.  
Not scripts.  
Pipeline pattern:

```
async function handler(req, res) {  
  const auth = await authenticate(req);  
  const data = await fetchData(auth);  
  const result = await transform(data);  
  await cache(result);  
  res.json(result);  
}
```

Parallelizing:

```
const [user, quota] = await Promise.all([  
  getUser(id),  
  getQuota(id)  
]);
```

This doubles throughput.  
Without extra servers.

3**) Clustering and Horizontal Scaling.**  
One process = one core.  
Wasteful.  
Cluster setup:

```
import cluster from "cluster";  
import os from "os";  
  
if (cluster.isPrimary) {  
  const cpus = os.cpus().length;  
  
  for (let i = 0; i < cpus; i++) {  
    cluster.fork();  
  }  
} else {  
  startServer();  
}
```

Each core gets a worker.  
Now your server scales vertically.

4**) Memory Management and Leak Prevention.**  
Most slowdowns are leaks.  
Example leak:

```
const cache = [];  
  
function handle(req) {  
  cache.push(req.body);  
}
```

This never clears.  
Solution:

```
import LRU from "lru-cache";  
  
const cache = new LRU({  
  max: 5000,  
  ttl: 1000 * 60  
});
```

Monitoring:

```
setInterval(() => {  
  console.log(process.memoryUsage());  
}, 5000);
```

If memory grows forever, you have a leak.

**5) High-Speed Caching with Redis and In-Memory Stores.**  
Databases are slow.  
Caches are fast.  
Redis setup:

```
import Redis from "ioredis";  
  
const redis = new Redis();  
  
async function getUser(id) {  
  const cached = await redis.get(`user:${id}`);  
  
  if (cached) return JSON.parse(cached);  
  
  const user = await db.find(id);  
  
  await redis.set(  
    `user:${id}`,  
    JSON.stringify(user),  
    "EX",  
    300  
  );  
  
  return user;  
}
```

This reduces DB load by 80%.

6**) Load Balancing and Connection Management.**  
Connections are expensive.  
Use keep-alive.  
Agent:

```
import http from "http";  
  
const agent = new http.Agent({  
  keepAlive: true,  
  maxSockets: 500  
});
```

Axios:

```
axios.create({  
  httpAgent: agent  
});
```

Behind Nginx:

```
upstream api {  
  least_conn;  
  server 10.0.0.1;  
  server 10.0.0.2;  
}
```

This evens traffic.

7**) Profiling and Benchmarking in Production.**  
Guessing is useless.  
Measure.  
Autocannon:

```
npx autocannon http://localhost:3000
```

Node profiler:

```
node --prof server.js
```

Clinic:

```
clinic doctor -- node app.js
```

CPU hotspots appear immediately.  
Fix those first.

**8) Observability and Adaptive Throttling.**  
High traffic means abuse.  
Rate limiter:

```
import rateLimit from "express-rate-limit";  
  
const limiter = rateLimit({  
  windowMs: 60000,  
  max: 100  
});  
  
app.use(limiter);
```

Circuit breaker:

```
import CircuitBreaker from "opossum";  
  
const breaker = new CircuitBreaker(callAPI, {  
  timeout: 3000,  
  errorThresholdPercentage: 50  
});
```

This prevents cascade failures.

**9) Deployment, Rollouts, and Zero-Downtime Scaling.**  
Bad deploys kill performance.  
PM2 cluster:

```
pm2 start app.js -i max
```

Reload:

```
pm2 reload all
```

Docker:

```
FROM node:20-alpine  
  
WORKDIR /app  
COPY . .  
  
RUN npm install --production  
  
CMD ["node", "server.js"]
```

Kubernetes:

```
strategy:  
  rollingUpdate:  
    maxUnavailable: 0
```

No downtime.  
No panic.

**Final Thoughts: Performance Is a Discipline.**  
After building systems at scale, I learned:  
Fast code is written once.  
Fast systems are maintained daily.  
Monitoring.  
Profiling.  
Refactoring.  
Automating.  
Do this consistently…  
And your backend becomes invisible.  
Which is the highest compliment in engineering.
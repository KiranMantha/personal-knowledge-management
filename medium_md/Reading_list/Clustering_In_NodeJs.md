---
title: "Clustering In NodeJs"
url: https://medium.com/p/dcd1dec3f0a2
---

# Clustering In NodeJs

[Original](https://medium.com/p/dcd1dec3f0a2)

# Clustering In NodeJs

[![Jatin Jain Saraf](https://miro.medium.com/v2/resize:fill:64:64/1*X_LsKR8U3DCn0US2eUv0Tw.jpeg)](/@jatinjainsaraf?source=post_page---byline--dcd1dec3f0a2---------------------------------------)

[Jatin Jain Saraf](/@jatinjainsaraf?source=post_page---byline--dcd1dec3f0a2---------------------------------------)

4 min read

·

Aug 7, 2023

--

Listen

Share

More

When multiple CPU cores are available, Node.js does not utilize them all by default. Fortunately, Node.js has a native cluster module that allows for the creation of child processes (workers) that can run simultaneously while sharing the same server port. Each child process has its own event loop, memory, and V8 instance. These child processes communicate with the main parent Node.js process through interprocess communication. Clusters of Node.js processes can be used to distribute workloads among application threads, or if process isolation is not needed, the module can be used to run multiple application threads within a single Node.js instance. The cluster module makes it easy to create child processes that can share server ports.

## The need for clustering in Node.js

An instance of Node.js runs on a single thread (you can read more about [threads in Node.js here](https://blog.logrocket.com/a-complete-guide-to-threads-in-node-js-4fa3898fe74f/)). The official [Node.js “About” page](https://nodejs.org/en/about/) states: “Node.js being designed without threads doesn’t mean you can’t take advantage of multiple cores in your environment.” That’s where it points to the cluster module.

The [cluster module doc](https://nodejs.org/api/cluster.html) adds: “To take advantage of multi-core systems, the user will sometimes want to launch a cluster of Node.js processes to handle the load.” So, to take advantage of the multiple processors on the system running Node.js, we should use the cluster module.

Exploiting the available cores to distribute the load between them gives our Node.js app a performance boost. As most modern systems have multiple cores, we should be using the cluster module in Node.js to get the most performance juice out of these newer machines.

## How does the Node.js cluster module work?

In a nutshell, the Node.js cluster module acts as a load balancer. It distributes a load to the child processes running simultaneously on a shared port. Node.js is not great with blocking code, so if there is only one processor and it’s blocked by a heavy and CPU-intensive operation, other requests are just waiting in the queue for this operation to complete.

With multiple processes, if one process is busy with a relatively CPU-intensive operation, other processes can take up the other requests coming in and utilize the other CPUs/cores available. This is the power of the cluster module — workers share the load and the app does not stop.

The master process can distribute the load to the child process in two ways. The first (and default) is a round-robin fashion. The second way is the master process listens to a socket and sends the work to interested workers. The workers then process the incoming requests.

However, the second method is not super clear and easy to comprehend like the basic round-robin approach.

![]()

## Prerequisites

To follow this guide about Node.js clustering, you should have the following:

* Node.js running on your machine, the latest LTS is advisable. It is Node.js 18 at the time of writing.
* Working knowledge of Node.js and Express
* Basic knowledge of how processes and threads work
* Working knowledge of Git and GitHub

## **Implementation & Configuration**

```
import cluster from 'node:cluster';  
import http from 'node:http';  
import { availableParallelism } from 'node:os';  
import process from 'node:process';  
  
const numCPUs = availableParallelism();  
  
if (cluster.isPrimary) {  
  console.log(`Primary ${process.pid} is running`);  
  
  // Fork workers.  
  for (let i = 0; i < numCPUs; i++) {  
    cluster.fork();  
  }  
  
  cluster.on('exit', (worker, code, signal) => {  
    console.log(`worker ${worker.process.pid} died`);  
  });  
} else {  
  // Workers can share any TCP connection  
  // In this case it is an HTTP server  
  http.createServer((req, res) => {  
    res.writeHead(200);  
    res.end('hello world\n');  
  }).listen(8000);  
  
  console.log(`Worker ${process.pid} started`);  
}
```

Running Node.js will now share port 8000 between the workers:

```
$ node server.js  
Primary 3596 is running  
Worker 4324 started  
Worker 4520 started  
Worker 6056 started  
Worker 5644 started
```

Before implementing clustering in your Node.js project, it's crucial to comprehend its advantages and constraints to determine if it's the most suitable option for your application's requirements.

## **Benefits of Clustering:**

1. By using clustering, you can make the most of the multiple CPU cores on your machine. This can greatly enhance the speed and efficiency of your application, particularly for tasks that rely heavily on the CPU.
2. By clustering, your application can effectively handle a greater number of simultaneous requests through the distribution of workload among several worker processes. This results in improved scalability and performance.
3. In terms of fault tolerance and availability, the ability of the remaining worker processes to handle incoming requests even if one crashes is a significant advantage.

## **Limitations of Clustering:**

1. Adding clustering to your application code can increase its complexity. You must be careful in managing inter-process communication, handling shared resources, and avoiding potential race conditions.
2. The usage of memory increases with each worker process, which could be problematic if the server has limited memory resources.
3. Managing states can become complicated with clustering, as each worker process has its own memory space. If your application heavily depends on in-memory states, you will have to develop methods to synchronize and share states among worker processes.
4. Clustering may not always be necessary for applications that are I/O-bound, such as network requests or database queries. This is because the bottleneck often lies in the I/O operations rather than CPU processing, making clustering less beneficial in these cases.

## **When to Use Clustering:**

If your application is CPU-bound and receives high requests, clustering can be a valuable solution. It is particularly useful for tasks that involve complex computations, image processing, video encoding, and specific types of data analysis. By distributing the workload, clustering can enhance overall efficiency and help overcome any limitations to performance caused by CPU utilization.
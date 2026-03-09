---
title: "Make NodeJs handle 5x request with 99.9% uptime adding 10 lines of code"
url: https://medium.com/p/e264006d35cf
---

# Make NodeJs handle 5x request with 99.9% uptime adding 10 lines of code

[Original](https://medium.com/p/e264006d35cf)

# Make NodeJs handle 5x request with 99.9% uptime adding 10 lines of code

## Scale your NodeJs Server to Utilize Full Resources

[![Biplap Bhattarai](https://miro.medium.com/v2/resize:fill:64:64/1*9_8lM2zmpYqHA27YZlmjKg.jpeg)](/?source=post_page---byline--e264006d35cf---------------------------------------)

[Biplap Bhattarai](/?source=post_page---byline--e264006d35cf---------------------------------------)

9 min read

·

Apr 29, 2021

--

12

Listen

Share

More

Press enter or click to view image in full size

![]()

Node.js works in single-threaded, non-blocking performance, working as a single process in CPU. No matter how powerful server is used and the resources utilized, what a single-threaded process can do is limited. Node.js is designed for building distributed applications with multiple nodes, hence the name Node.js.

Workload is one of the main reasons we start scaling our application, including availability and fault tolerance among others. Scaling can be done in multiple ways, one of the easiest available solution is Cloning. We can perform cloning using [**Cluster Module**](https://nodejs.org/dist/latest-v14.x/docs/api/cluster.html)provided by Node.js.

Before we start handling requests with our resource-utilized Node.Js server, let’s take the basics of how the Cluster module works.

## **How Cluster Module Works?**

The cluster module has got two types of processes, Master and Worker. All incoming requests are handled by Master process and Master process decides which Worker should handle the incoming requests. Worker process can be thought of as normal Node.Js single instance server which serves the requests.

How does Master process distribute the incoming connections?

1. The first method (and the default one on all platforms except Windows), is the round-robin approach, where the master process listens on a port, accepts new connections, and distributes them across the workers in a round-robin fashion, with some built-in smarts to avoid overloading a worker process.

Press enter or click to view image in full size

![]()

2. The second approach is where the master process creates the listen socket and sends it to interested workers. The workers then accept incoming connections directly.

The second approach should, in theory, give the best performance. In practice, however, distribution tends to be very unbalanced due to operating system scheduler vagaries. Loads have been observed where over 70% of all connections ended up in just two processes, out of a total of eight.

## Creating a Simple Node.js Server

Let’s create a basic Node.js server that handles the request:

```
/*** server.js ***/  
const http = require(“http”);// get the process ID of Node Server  
const processId = process.pid;// Creating server and handling request  
const server = http.createServer((req, res) => {  
    // Simulate CPU Work  
    for (let index = 0; index < 1e7; index++);  
      
    res.end(`Process handled by pid: ${processId}`);  
});// start server and listen the request  
server.listen(8080, () => {  
    console.log(`Server Started in process ${processId}`);  
});
```

The server gives us the following response:

Press enter or click to view image in full size

![]()

**Load Testing this Simple Node.Js Server:**

We are going to use [ApacheBench Tool](https://httpd.apache.org/docs/2.4/programs/ab.html), there are other tools that perform similar testing. They can be used according to personal choice.

We are going to hit our Node.js server with 500 concurrent requests for a span of 10 seconds.

```
➜ test_app ab -c 500 -t 10 http://localhost:8080/  
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>  
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/  
Licensed to The Apache Software Foundation, http://www.apache.org/Benchmarking localhost (be patient)  
Finished 3502 requestsServer Software:   
Server Hostname: localhost  
Server Port: 8080Document Path: /  
Document Length: 29 bytesConcurrency Level: 500  
Time taken for tests: 11.342 seconds  
Complete requests: 3502  
Failed requests: 0  
Total transferred: 416104 bytes  
HTML transferred: 116029 bytes  
Requests per second: 308.76 [#/sec] (mean)  
Time per request: 1619.385 [ms] (mean)  
Time per request: 3.239 [ms] (mean, across all concurrent requests)  
Transfer rate: 35.83 [Kbytes/sec] receivedConnection Times (ms)  
 min mean[+/-sd] median max  
Connect: 0 6 3.7 5 17  
Processing: 21 1411 193.9 1412 2750  
Waiting: 4 742 395.9 746 1424  
Total: 21 1417 192.9 1420 2750Percentage of the requests served within a certain time (ms)  
 50% 1420  
 66% 1422  
 75% 1438  
 80% 1438  
 90% 1624  
 95% 1624  
 98% 1624  
 99% 1625  
 100% 2750 (longest request)
```

This Simple server, on the level of **500 Concurrent requests,** a **Total of 3502 Requests** were served. And **308** **requests per second** with **Time Per Request of 1619(ms)** was done.

The number of requests handled is good and it should work for most small to medium scale applications. But we haven’t fully utilized the resources and most of the available resources are sitting idle.

## Implementing the Cluster Module

Now that we are up and running, let’s implement the Cluster for our server.

```
/** cluster.js **/  
const os = require(“os”);  
const cluster = require(“cluster”);if (cluster.isMaster) {  
    const number_of_cpus = os.cpus().length;  
     
    console.log(`Master ${process.pid} is running`);  
    console.log(`Forking Server for ${number_of_cpus} CPUs\n`);    // Create a Worker Process for each Available CPU  
    for (let index = 0; index < number_of_cpus; index++) {  
        cluster.fork();  
    }    // When Worker process has died, Log the worker  
    cluster.on(“exit”, (worker, code, signal) => {  
        console.log(`\nWorker ${worker.process.pid} died\n`);  
    });} else {  
    // if Worker process, master is false, cluster.isWorker is true  
    // worker starts server for individual cpus  
    // the worker created above is starting server   
    require(“./server”);  
}
```

My personal PC with i7 8th Generation has got 8 processor Cores. Considering that most of the CPUs available nowadays have a minimum of dual-core processor, the resources for the 7 remaining cores were sitting idle\*.

Now, let’s run created cluster.js file, the server gives us the following response:

Press enter or click to view image in full size

![]()

If you implemented the above cluster, you will have utilized your full CPU/Server power. The request is handled by Master process from same server port, which will be served by any one of the 8 Worker Processes (Servers).

**Load Testing with Cluster Implemented:**

```
➜  test_app ab -c 500 -t 10  http://localhost:8080/  
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>  
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/  
Licensed to The Apache Software Foundation, http://www.apache.org/Benchmarking localhost (be patient)  
Completed 5000 requests  
Completed 10000 requests  
Completed 15000 requests  
Completed 20000 requests  
Finished 20374 requestsServer Software:          
Server Hostname:        localhost  
Server Port:            8080Document Path:          /  
Document Length:        29 bytesConcurrency Level:      500  
Time taken for tests:   10.000 seconds  
Complete requests:      20374  
Failed requests:        0  
Total transferred:      2118896 bytes  
HTML transferred:       590846 bytes  
Requests per second:    2037.39 [#/sec] (mean)  
Time per request:       245.412 [ms] (mean)  
Time per request:       0.491 [ms] (mean, across all concurrent requests)  
Transfer rate:          206.92 [Kbytes/sec] receivedConnection Times (ms)  
              min  mean[+/-sd] median   max  
Connect:        0    0   1.3      0      12  
Processing:     6  242  15.6    241     369  
Waiting:        6  242  15.5    241     368  
Total:         18  242  15.5    241     371Percentage of the requests served within a certain time (ms)  
  50%    241  
  66%    244  
  75%    246  
  80%    247  
  90%    251  
  95%    259  
  98%    283  
  99%    290  
 100%    371 (longest request)
```

Remember the above simple Node.js server which handled *308 Requests Per Seconds*on our load test now that number has **increased** to **2037 Requests Per Seconds** that’s an outstanding **6X Increase** in the number of requests handled. Also, previously *Time per Request was 1619 ms* now it has been **decreased to 245ms**. We were serving a *Total of 3502 Requests* before, now it has **increased** to a **Total of 20374 Requests (That’s 5.8X increase).** If you look at the implementation above this great improvement is caused by **10 lines of code.** And we also didn’t have to refactor our existing server code.

## Availability and Zero Down Time

*Excited with the progress we have made so far, now it gets better.*

When we have a single instance of server and that server crashes. There will be downtime when the server has to be restarted. Even if the process is automated, there will be delay and not a single request can be served in that time.

### Simulating the Server Crashing:

```
/*** server.js ***/  
const http = require(“http”);// get the process ID of Node Server  
const processId = process.pid;// Creating server and handling request  
const server = http.createServer((req, res) => {  
    // Simulate CPU Work  
    for (let index = 0; index < 1e7; index++);  
      
    res.end(`Process handled by pid: ${processId}`);  
});// start server and listen the request  
server.listen(8080, () => {  
    console.log(`Server Started in process ${processId}`);  
});// Warning: Only For Testing and Visualization Purpose  
// Don't add the code below in production// Let's simulate Server Randomly Crashing using process.exit()  
setTimeout(() => {  
    process.exit(1);  
}, Math.random() * 10000);
```

Now for simulation purposes if we add highlighted code above to our server code. And start our server we can see that one by one all server is crashing and eventually the whole process exists. Master Process also exists due to no available Worker. The server could crash and these scenarios could exist due to any problem.

Now, remember this is the case when we have 8 servers created by our Cluster Module. When we have a single instance of server and that crashes, no requests can be served in that time.

```
➜  test_app node cluster.js  
Master 63104 is running  
Forking Server for 8 CPUsServer Started in process 63111  
Server Started in process 63118  
Server Started in process 63112  
Server Started in process 63130  
Server Started in process 63119  
Server Started in process 63137  
Server Started in process 63142  
Server Started in process 63146Worker 63142 died  
Worker 63112 died  
Worker 63111 died  
Worker 63146 died  
Worker 63119 died  
Worker 63130 died  
Worker 63118 died  
Worker 63137 died  
➜  test_app
```

### Handling the Zero Down-Time

When we have multiple instances of a server, the availability of the server could be easily increased.

Let’s open up our cluster.js file and add the highlighted code to cluster.js:

```
/** cluster.js **/  
const os = require(“os”);  
const cluster = require(“cluster”);if (cluster.isMaster) {  
    const number_of_cpus = os.cpus().length;  
     
    console.log(`Master ${process.pid} is running`);  
    console.log(`Forking Server for ${number_of_cpus} CPUs\n`);    // Create a Worker Process for each Available CPU  
    for (let index = 0; index < number_of_cpus; index++) {  
        cluster.fork();  
    }    // When Worker process has died, Log the worker  
    cluster.on(“exit”, (worker, code, signal) => {  
        /**  
        * The condition checks if worker actually crashed and  
        * wasn't manually disconnected or killed by master process.  
        *  
        * The condition can be changed by desired error code,  
        * and condition.  
        */  
        if (code !== 0 && !worker.exitedAfterDisconnect) {  
            console.log(`Worker ${worker.process.pid} died`);            cluster.fork();  
        }  
    });} else {  
    // if Worker process, master is false, cluster.isWorker is true  
    // worker starts server for individual cpus  
    // the worker created above is starting server  
    require(“./server”);  
}
```

**Load Testing with Server Restart Implemented:**

Let’s run the server with cluster changes implemented (Run: *node cluster.js*). Now let’s open up our [benchmarking tool](https://httpd.apache.org/docs/2.4/programs/ab.html) and start benchmarking our server.

```
➜  test_app ab -c 500 -t 10 -r http://localhost:8080/  
This is ApacheBench, Version 2.3 <$Revision: 1843412 $>  
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/  
Licensed to The Apache Software Foundation, http://www.apache.org/Benchmarking localhost (be patient)  
Completed 5000 requests  
Completed 10000 requests  
Completed 15000 requests  
Completed 20000 requests  
Finished 20200 requestsServer Software:          
Server Hostname:        localhost  
Server Port:            8080Document Path:          /  
Document Length:        29 bytesConcurrency Level:      500  
Time taken for tests:   10.000 seconds  
Complete requests:      20200  
Failed requests:        12  
   (Connect: 0, Receive: 4, Length: 4, Exceptions: 4)  
Total transferred:      2100488 bytes  
HTML transferred:       585713 bytes  
Requests per second:    2019.91 [#/sec] (mean)  
Time per request:       247.536 [ms] (mean)  
Time per request:       0.495 [ms] (mean, across all concurrent requests)  
Transfer rate:          205.12 [Kbytes/sec] receivedConnection Times (ms)  
              min  mean[+/-sd] median   max  
Connect:        0    0   1.5      0      13  
Processing:    13  243  15.7    241     364  
Waiting:        0  243  16.0    241     363  
Total:         22  243  15.5    241     370Percentage of the requests served within a certain time (ms)  
  50%    241  
  66%    245  
  75%    248  
  80%    250  
  90%    258  
  95%    265  
  98%    273  
  99%    287  
 100%    370 (longest request)  
➜  test_app
```

In the above load test on the level of **500 Concurrent requests** and **2019 requests per second.** With a **Total of 20200 Requests,** only **12 requests failed** which means we had **99.941%** **uptime** of the server, even with servers crashing one by one and restarting. That’s really sweet considering we only added **3 extra lines** of code.

What to learn more, lookout for my previous articles:

[## How NodeJs require module actually works?

### Requiring a Module in NodeJs seems like a simple concept, you require a module using require(“module\_name”) function…

bhattaraib58.medium.com](/how-nodejs-require-module-actually-works-7b0ac2d67b5e?source=post_page-----e264006d35cf---------------------------------------)

[## Comparison with “==” and “===” is just a difference of type checking in JavaScript, think again?

### The way in which JavaScript handles types is presumably the most misjudged and controversial part. People just consider…

bhattaraib58.medium.com](/comparison-with-and-is-just-a-difference-of-type-checking-in-javascript-think-again-ef4045a091bb?source=post_page-----e264006d35cf---------------------------------------)

**Meet me** • [LinkedIn](https://www.linkedin.com/in/bhattaraib58/) • [Twitter](https://twitter.com/bhattaraib58) •
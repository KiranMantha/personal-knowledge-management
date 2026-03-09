---
title: "Parallel programming in JavaScript using Web Workers"
url: https://medium.com/p/8f921f2d26db
---

# Parallel programming in JavaScript using Web Workers

[Original](https://medium.com/p/8f921f2d26db)

Member-only story

## JavaScript

# Parallel programming in JavaScript using Web Workers

[![Uday Hiwarale](https://miro.medium.com/v2/resize:fill:64:64/1*B4PQwnTacbDmtJgKYY7CzA.jpeg)](/@thatisuday?source=post_page---byline--8f921f2d26db---------------------------------------)

[Uday Hiwarale](/@thatisuday?source=post_page---byline--8f921f2d26db---------------------------------------)

16 min read

·

Mar 31, 2018

--

6

Listen

Share

More

Press enter or click to view image in full size

![]()

JavaScript is one of the most popular programming languages of all. It is the language of the web browser. Another reason why JavaScript has become so popular is the adoption of Node.js on the server-side.

Even though JavaScript is one of the most beloved languages, it also disliked by some programmers. One reason is that JavaScript is a single threaded language. It is horrible when it comes to non-blocking operations.

Whenever you do something in JavaScript (for example, inserting text inside a DOM element), the whole web page freezes and become unresponsive.

We usually don’t notice, because modern browsers are so fast. But throughout the lifecycle of a web page, this difference can become quite noticeable.

### Single-threaded languages perform only one computation at a time.

This means when your browser is running a script, all other operations (like DOM manipulation, animation, drawing, deferred executions and other operations that happens on the main thread) will come to a halt.

The browser simply won’t be responsive until that script execution is finished.

Fortunately, modern browsers come with Web APIs which can defer the execution of a script until their execution is demanded by the runtime.

This happens with the help of the event loop. This whole single threaded execution is explained brilliantly by Philip Roberts in video below. You should definitely watch it.

No matter what you do, you can’t get away from the single-threaded nature of JavaScript.

Let’s talk about how a long running script can block Web UI or how it can freeze browser tabs. A long running script could be a for-loop that loops forever or performs a relatively large number of iterations.

Just for confirmation, we’ll run such a for-loop in a web browser’s console. In Google Chrome, the JavaScript console uses the main thread of the tab. So, if we run such a loop in the console, it will freeze that tab.

Below is an example of a long running for-loop:

```
// benchmark testvar start = Date.now(); // milliseconds  
var x = 0;for (var i = 0; i < 200000000; i++){  
 x = x + i;  
}console.log('ended in : ', -(start - Date.now())/1000, ' seconds');// ended in :  9.867  seconds
```

In above example, the for-loop is performing computations 200,000,000 times (which is a lot).

If your paste above code in [your browser’s console](https://developers.google.com/web/tools/chrome-devtools/console/) and hit Enter, you will see that tab is unresponsive for long time. You can’t even close the tab! You won’t be able to interact with that web page at all.

But other tabs are working fine, as they are running on separate threads or perhaps separate processes.

In my case, the above program completes in about ten seconds. If in your case it runs immediately, then perhaps increase the iteration count to 500,000,000 or more. This will be our benchmark test.

Some people advise using the `setTimeout` function to get around this blocking behaviour. But you can try for yourself. It doesn’t work in any case. This means single-threaded JavaScript execution can be a big problem for us developers.

### Introducing Web Workers

At least, this was the case until HTML5 introduced a new Web API called Web Workers. This was a collaborative effort between the Mozilla foundation and Google to make their browsers more powerful.

Later, many other browsers adopted this API. As of today, most of the major browsers support it.

Press enter or click to view image in full size

![]()

So what are Web Workers?

**A web worker is a JavaScript program running on a different thread, in parallel with main thread.**

The browser creates one thread per tab. The main thread can spawn an unlimited number of web workers, until the user’s system resources are fully consumed. As soon as a browser tab is closed, the main thread ‘dies’ and ‘kills’ any web workers it spawned.

JavaScript programs in the main thread communicate with web workers using events. This communication happens using only the ‘message’ event and a data payload.

A main thread can ‘kill’ web workers which it spawned, and a web worker can ‘kill’ itself. When a web worker dies, threads attached to it die as well.

### But first, where we can use web workers?

Think about most annoying things you face while using a web browser. Most of us hate the Page Unresponsive dialog that shows up when some script is taking long time to execute.

This can be a good use case for web workers. By moving computationally intensive tasks to web workers, we can allow them to lift heavy loads while our web page (main thread) is open to do other important jobs.

But generally, you will run in to Page Unresponsive problem due to a bad design.

Most importantly, web workers should be used in following cases

* Data and web page caching
* Image manipulation and encoding (base64 conversion)
* Canvas drawing and image filtering
* Network polling and web sockets
* Background I/O operations
* Video/Audio buffering and analysis
* Virtual DOM diffing
* Local database (indexedDB) operations
* Computationally intensive data operations

Looks like there is a long list of things JavaScript doesn’t recommend you do on the main thread. But trust me, when you start using web workers for tasks like above, user experience (UX) for your web application will increase by a huge margin.

Enough talking, let’s get into the code and implement our first web worker.

Due to security policies of Google Chrome, you won’t be able to test web workers on `file://` protocol. Instead, it’s better to use the [http-server](https://www.npmjs.com/package/http-server) or [live-server](https://www.npmjs.com/package/live-server) npm modules to start a localhost server. I will explain how to use live-serverlater in this blog.

HTML5 gives a `Worker` constructor function (or class) to create web workers from. It accepts a string argument, which is a path to a JavaScript file. This file contains JavaScript code to listen to message event and perform tasks.

`Worker` function must be used in conjugation with `new` keyword to create an instance or object of type Worker. Hence, multiple instances of same web worker script can be created.

```
<script>  
    // inside -> index.html    // resolved relative to index.html url path  
    var worker = new Worker('worker.js');....
```

In above code, we are creating a web worker from file `worker.js`.

Here, the browser will try to resolve `worker.js` relative to the current path of the page where it was created. If you are at `http://localhost`, then it will fetch `http://localhost/worker.js`[.](http://localhost/worker.js.) If you are at `http://localhost/app` then it will fetch `http://localhost/app/worker.js`[.](http://localhost/app/worker.js.) To avoid this problem , you can implement it inside an external JavaScript file.

If above implementation is done in external JavaScript file, for example `main.js`, then this worker file will be resolved relative to it.

```
// inside -> main.js// resolved relative to main.js url path  
var worker = new Worker('worker.js');
```

If the file specified to `Worker` constructor exists, then the browser will spawn a worker thread where this file will be downloaded and executed. If there is an error downloading this file, the worker will fail silently and thread will be killed.

Let’s create a simple project to test our first web worker. Below is the project structure we are going to use. Let’s create a `web-workers` folder and create below empty files.

```
web-workers  
|_ scripts  
  |_ main.js   // to hold script for index.html  
|_ workers  
  |_ for.js    // to hold web worker code  
|_ index.html  // main page
```

From above structure of our application, `index.html` will import `main.js` which will create a web worker using the `for.js` script.

So `index.html` will look like below:

```
<!-- index.html --><!DOCTYPE html>  
<html>  
    <head>  
        <title>Web Workers</title>        <!-- main.js -->  
        <script src="./scripts/main.js"></script>  
    </head>    <body>  
        <div id="result">loading...</div>  
    </body></html>
```

In `index.html`, we are only importing `main.js` script in the head section. There is a `div` element with the id `result` which we will use to print the result from the web worker. You will see in a bit how that works.

In `main.js`, we are going to create a web worker from the `for.js` script. As we talked about relative path of script for web workers, the path of `for.js` relative to `main.js` will be `../workers/for.js`, hence `main.js` will look like below.

You can also use absolute path `/workers/for.js`, as it will also resolve against `main.js` file, but generally the relative path convention is followed.

```
// main.jsvar workerFor = new Worker('../workers/for.js');// listen to message event of worker  
workerFor.addEventListener('message', function(event) {  
    console.log('message received from workerFor => ', event.data);  
});// listen to error event of worker  
workerFor.addEventListener('error', function(event) {  
    console.error('error received from workerFor => ', event);  
});
```

From above code, we have created a web worker `workerFor` from script `for.js`.

A web worker emits two events viz. messageand errorthroughout its lifetime. We can listen to this event using `addEventListener` method on worker instance.

This method takes two arguments. The first one is the name of the event we are listening on. The second is the callback function we want to execute when this event is emitted by the web worker. This callback function receives one argument which is `event`.

`event` contains many properties, one of which is `data` for the `message` event. `data` property on event is the actual data or payload sent by the web worker. In case of `error` event, event is actually a JavaScript Error object.

**message** event is received when web worker successfully sends the data which is a **non Error object**. **error** event is received when worker is not successfully registered or when workers sends an **Error object** as payload.

So far we have understood how to deal with web workers. Now let’s have a look at how web workers works in practice. Below is a very simple example of web worker.

We will get down to implementation of **for loop** inside web worker soon but it’s very useful to break down working on web workers step by step, which will help us clear many concepts related to web workers.

```
// for.jsself.postMessage('Hello World!');
```

In `for.js`, we have a strange variable `self`. `self` is context variable provided by JavaScript runtime which refers to the global context. I am pretty sure you have never used `self` while accessing global variables (let’s say `x`) in JavaScript, because when a variable is globally defined, you just use the variable name `x` and not `window.x` as `window` is the global context and all global variables are accessible with `window.varName` syntax. `self` in JavaScript also refers to global context `window`. Hence any global variable can also be is accessed with `self.varName` syntax.

In case of web workers, `self` is used to access global scope which is worker itself. Hence if you remove `self` from `self.postMessage` function, this would be fine too. `postMessage` is a method provided by worker to emit **message** event. This method accepts one parameter which is **data or payload** to transmit along with the event (*which* ***main.js*** *will accessed with* ***event.data***).

> You can also use `this` instead of `self` but I don’t recommend it because they are very different from each other. Here is the explanation <https://stackoverflow.com/a/16876159/2790983>.

Let’s add some **5s** timeout to `postMessage` call to make this example more interesting. Below code will call `postMessage` function after 5 seconds. Hence in ***main.js***, we should receive this event after 5 seconds.

```
setTimeout(() => {  
    postMessage('Hello World!');  
}, 5000);
```

Let’s also modify `main.js` to print data received from web worker in the `#result` div. This can be done by simple DOM manipulation.

```
// modifications in main.js...workerFor.addEventListener('message', function(event) {  
    var div = document.getElementById('result');  
    div.innerHTML = 'message received => ' + event.data;  
});...
```

Let’s start out application. But before that, we need a program that start a static web server to host our project on `http` protocol. For that, we are going to use `live-server` npm module which gives us CLI commands to start a static web server from any directory. To install `live-server` using npm, use below command

```
$ npm install -g live-server
```

After installation is done, from our project folder, use command `live-server` which should start the web server on `8080` port. It should automatically open a browser tab but if it doesn’t, then use URL `http://localhost:8080` to navigate to `index.html` page.

Whenever you make changes to any files served by `live-server`, you don’t need to reload the web page, `live-server` will do it automatically for you.

You will see that first, `loading...` is printed on screen but after 5 seconds, it changes to `message received => Hello World!`. We got our service worker running.

Chrome Developer Tools gives lot of support for web workers. Inside sources tab, navigate to threads section on right panel. You can see Main thread and `for.js` thread. While on left panel, you can actually see web worker `for.js` and it’s location. Using this panel, you can also debug web workers just like normal script.

Press enter or click to view image in full size

![]()

Until now, we saw only one way communication, from web worker ***for.js*** to ***main.js***. We can also communicate from ***main.js*** to web worker ***for.js*** using same `postMessage` method on worker instance `workerFor` in ***main.js***. Since `postMessage` emits the **message** event, web worker should also listen to **message** event in similar fashion as done in **main.js**. Using this, web worker can understand when **main.js** is asking for the execution of a task.

Now let’s add our horrible **for loop** inside web worker and return the result. Originally, this **for loop** used the freeze our browser tab. This time it should not do that. Let’s create a button in ***index.html*** to emit **message** event from ***main.js***.

```
<!-- index.html --><!DOCTYPE html>  
<html>  
    <head>  
        <title>Web Workers</title>         <!-- main.js -->  
        <script src="./scripts/main.js"></script>  
    </head>    <body>  
        <div id="result">no results</div>        <br/>        <button onclick="loadResult()">Load Result</button>        <!-- breaks for page scroll -->  
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>  
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>  
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>  
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>  
        <br/><br/><br/><br/><br/><br/><br/><br/><br/><br/><br/>  
    </body></html>
```

In **main.js**, we will add `loadResult` function which will emit message event to web worker.

```
// main.jsvar workerFor = new Worker('../workers/for.js');// listen to message event of worker  
workerFor.onmessage = function(event){  
    var div = document.getElementById('result');  
    div.innerHTML = 'message received => ' + event.data;  
};// listen to error event of worker  
workerFor.onerror = function(event) {  
    console.error('error received from workerFor => ', event);    var div = document.getElementById('result');  
    div.innerHTML = 'Error!';  
};// load results from web worker  
function loadResult() {  
    // add loading text until `message` event listener replaces it  
    var div = document.getElementById('result');  
    div.innerHTML = 'loading...';    // emit message event to worker  
    workerFor.postMessage(null); // we don't need payload here  
};
```

> `elem.addEventListener(‘message’, callback)` is equivalent to `elem.onmessage = callback`. Hence you can makeup your mind on what approach you are going to use.

Since when button is clicked, ***main.js*** sends message event to ***for.js*** using `postMessage` method on `workerFor`, ***for.js*** should listen to it and run **for loop** inside the callback function. Right after for loop code, we should return the result back to **main.js** using same `postMessage` method. This can be implemented like below.

```
// for.jsself.onmessage = function(event) {  
    var x = 0;  
    for (var i = 0; i < 200000000; i++) {  
        x = x + i;  
    }    self.postMessage(x);  
}
```

After saving this file, `live-reload` should reload the page automatically. Now you can click the button and wait for 10 seconds to get the result back.

Press enter or click to view image in full size

![]()

## Wait, what?

It look less than a second in web worker thread to calculate the same thing which look almost 10 seconds in main thread. That’s why web workers are so awesome. Since they work on separate thread, runtime only has one job to look after and it does it efficiently and blazing fast. To simulate large computational delay, I am going to increase **for loop** iteration count to **2000M**. Let’s see how our page behaves now.

![]()

We can see that while web worker was executing for loop, our page or tab did not freeze at all. Hence we proved that **web workers are non-blocking**.

There might be one case when you are done with a web worker and you want to kill it, let’s say, to free up some system resources (thread). This can be done from both **main.js** and **for.js**. There is `terminate` method on web worker object which kills the web worker or you can use `self.close` method from within the web worker to do the same thing. Once web work dies, the thread it was spawned on goes away as well. **When you are trying to send message event to dead web worker, no messages will go through and this also won’t throw any errors**.

```
// modifications in for.js  
self.onmessage = function(event) {  
    ...    self.postMessage(x);  
    self.close();  
}  
////////////////////// OR ///////////////////////  
// modifications inmain.js  
...// listen to message event of worker  
workerFor.onmessage = function(event){  
    var div = document.getElementById('result');  
    div.innerHTML = 'message received => ' + event.data;  
    workerFor.terminate();  
};...
```

So **looks like we owned the web workers world** 😀 but there are few more things to discuss.

### Transferable objects

When we send payload on event using `postMessage` event, we are cloning the payload from one context to another. This is also known as **pass by value**. For example, let’s say that we have a huge file blob in **ArrayBuffer** in **main thread** which we needs to processed inside a web worker. When we send this blob as payload, runtime copies this data and then sends to the web worker so that any modifications done inside web worker does not affect the original copy. That’s neat but it has significant disadvantages. If this payload, in this case the image blob, is significantly large in size, then making a copy of it will take huge time and since that happens in main thread, it will block the entire page and browser tab.

Hence, what we need is **pass by reference** transmission where no copy is being made but simply a reference to the data (value) is passed. This obviously is problematic and **non thread safe**.

But JavaScript offers a new way to transfer data between different contexts using **Transferable** interface. Any types which implements this interface known as **Transferable objects**. So far, **ArrayBuffer**, **MessagePort** and **ImageBitmap** types implement this interface. When these objects are transferred to new context, in our case from **main thread to service worker thread**, their original copies get emptied and their values are assigned to event payload. Once these objects are transferred, they become neutered or unusable and can not be transferred again.

**Transferable objects** in web workersare transferred using slightly different syntax of `postMessage` method.

```
worker.postMessage(payload, transferableObjects)
```

`transferableObjects` in above syntax is an **array of transferable objects** which should be transferred to web worker without making a copies of it. `transferableObjects` can be `[payload]` when `payload` is **Non JavaScript Object/Array** or it can be values/elements of `payload` object when `payload` is **JavaScript Object/Array**. Remember, `transferableObjects` is always an array of **Transferable objects**.

Let’s see a simple example.

Event payload in case of Transferred objects are received in normal fashion. Above example yields following result to the console.

![]()

As you can see on the *[onmessage]* lines, **transferred array buffers are empty**. **Transfer can happen from both sides** as events can be sent from both **main.js** and service worker.

### Available objects and APIs

Web worker do not have access to all the browser APIs due to its execution in different thread. It can not access DOM because DOM does not belong to its context. `window` and `document` objects are also not available.

But it has read only access to `location` object and full access to `navigator` object along with web APIs like `setTimeout`, `setInterval` and `application cache`.

### Child workers

As we talked earlier, a web worker has ability to spawn other web workers and communicating with them. This follows same principles like spawning web workers from main thread. Whenever you want to create new child web workers from a parent web worker, **imagine you are inside main thread and apply same principles**.

### **importScript()**

We can import any external JavaScript inside web worker using **importScript** function using `importScript(file.js, [...files])`. This function is available in global context of web worker hence you can use `self` as well to access it.

```
importScript('file1.js');  
self.importScript('file2.js', 'file3.js');
```

**importScript** function will load JavaScript files synchronously, hence web worker is blocked until file is downloaded completely and executed. After execution, you can use code inside that file like it was inlined. External JavaScript files can be used to store some common code which might be used across different web workers.

### Inline web workers

So far, we have seen web worker code in external JavaScript file but we can inline web worker code by creating a blob URL from JavaScript code using Blob constructor function. Then this blob URL is passed to Worker constructor function. This is achieved like below.

```
// create blob from JavaScript code (ES6 template literal)  
var blob = new Blob([`  
    self.onmessage = function(e) {  
        postMessage('msg from worker');  
    }  
`]);// create blob url from blob  
var blobURL = window.URL.createObjectURL(blob);// create web worker from blob url  
var worker = new Worker(blobURL);// send event to web worker  
worker.postMessage(null);// listen to message event from web worker  
worker.onmessage = function (event) {  
    console.log(event.data);  
};
```

**The *Web Workers* we have learned so far about, are called *Dedicated Workers***. That means, a web worker spawned by main thread will not be accessible by other main thread (from separate browser tabs). But if you need that kind of functionality in web workers, **Shared Workers** are here to help.

Until now we used `Worker` constructor function, but for Shared Web Workers, we used `SharedWorker` constructor function. Dedicated Workers and Shared Workers more or less works in the same fashion but in case of Shared Web Workers, they can communicate with and communicated by any thread running on same origin (example.com). I am not going write about Shared Workers as they are not implemented in all browser, in fact, only Chrome and Firefox support it at the moment. Hence there is no point implementing that in production.

Press enter or click to view image in full size

![]()

But if you are interested to have a look at implementation of Shared Worker, then please visit this short blog at <https://www.sitepoint.com/javascript-shared-web-workers-html5/>

### This was rather a big blog about Workers. But wait!

There is still one more thing missing when it comes to workers. **Service Workers**. Service worker is the main ingredient to develop progressive web apps and it is much powerful that web worker.

Press enter or click to view image in full size

![]()

![]()
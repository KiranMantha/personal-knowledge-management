---
title: "Quick Tip — Creating an XMLHttpRequest Interceptor"
url: https://medium.com/p/1da23cf90b76
---

# Quick Tip — Creating an XMLHttpRequest Interceptor

[Original](https://medium.com/p/1da23cf90b76)

# Quick Tip — Creating an XMLHttpRequest Interceptor

[![Gil Fink](https://miro.medium.com/v2/resize:fill:64:64/0*814AS_UGOi09hbI7.jpg)](/?source=post_page---byline--1da23cf90b76---------------------------------------)

[Gil Fink](/?source=post_page---byline--1da23cf90b76---------------------------------------)

2 min read

·

Apr 11, 2017

--

4

Listen

Share

More

A few weeks ago I got a request from a customer to hook into XMLHttpRequest object and to log some aspects of the communication in their website. Some of their third party add-ins were acting strange and they wanted to understand what those add-ins were doing. As a result, I created a small piece of code that helped them to monitor the communication.

In this post I’ll show you how you can add your own interceptor to **XMLHttpRequset**.

## Creating a JavaScript Interceptor

Whenever you want to intercept some built-in JavaScript object functionality the first thing that I suggest to do is to read the object and function documentation. I know that it can be a boring thing, but it will be precious later on when you create your interceptor. For example, if you want to intercept the **eval** function you will learn from the documentation that the **eval** function receives an expression string and evaluates it. So if you want to intercept the **eval** function you can just do something like:

```
let oldEval = window.eval;window.eval = function(str) {  
 // do something with the str string you got  
 return oldEval(str);  
}
```

In the example I overridden the **eval** function with my own implementation and later on I could do something with the string I got. The last thing in the code example is running the old **eval** functionality.

So in order to create an interceptor, we first need to save the old function implementation and then somewhere in our implementation we need to run the old functionality. In some circumstances you might not want to run the old functionality but then you just replaced it with your own implementation and this is called override and not intercept.

## Creating the XMLHttpRequest Interceptor

Now that you know how to make your own interceptor, let’s get back to the customer needs and let’s create an **XMLHttpRequest** interceptor. If you want to intercept the communication in **XMLHttpRequest** the main place to do that is the **open** function. In that function you can hook into the **load** event and then run your own functionality. Let’s see and example:

```
let oldXHROpen = window.XMLHttpRequest.prototype.open;window.XMLHttpRequest.prototype.open = function(method, url, async, user, password) {  
 // do something with the method, url and etc.  
 this.addEventListener('load', function() {  
  // do something with the response text  
  console.log('load: ' + this.responseText);  
 });  
                 
 return oldXHROpen.apply(this, arguments);  
}
```

## Summary

After we intercepted the communication in the customer website they found out that some third party ads add-in they were using was sending tons of requests to some remote service. As a result they remove the add-in code and there was improvement in their website performance.

In this post you learned how to create JavaScript interceptors (sometimes called JavaScript hooks).
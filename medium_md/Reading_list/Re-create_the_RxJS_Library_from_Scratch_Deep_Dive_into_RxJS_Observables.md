---
title: "Re-create the RxJS Library from Scratch: Deep Dive into RxJS Observables"
url: https://medium.com/p/cb9a3c000e0
---

# Re-create the RxJS Library from Scratch: Deep Dive into RxJS Observables

[Original](https://medium.com/p/cb9a3c000e0)

# Re-create the RxJS Library from Scratch: Deep Dive into RxJS Observables

[![Arseniy Tomkevich](https://miro.medium.com/v2/resize:fill:64:64/1*vuya5-YRRodHOG93lQgFtg.jpeg)](https://medium.com/@jsmuster?source=post_page---byline--cb9a3c000e0---------------------------------------)

[Arseniy Tomkevich](https://medium.com/@jsmuster?source=post_page---byline--cb9a3c000e0---------------------------------------)

5 min read

·

Mar 13, 2023

--

Listen

Share

More

In this article, I’ll explore the concept of Observables by creating a small library from scratch. Through this exercise, we’ll delve into the inner workings of observables, how they can be created, and how they can be used to handle asynchronous data streams.

Press enter or click to view image in full size

![]()

So how do we go about making Observables from scratch? Lets take a look at the RxJS documentation for a recipe, as you see an Observable class extends a **Subscribable**, and **Subscribable** is an interface with a method ***subscribe, so our Observable should have a subscribe method, am I right?***

![]()

![]()

The **constructor** is another important aspect, it has an optional parameter, which is a function that gets called when the Observable is subscribed to.

This function receives a **subscriber** object of type **Observe**r, which can be used to emit new values using the `next` method, or signal an error using the `error` method, or indicate successful completion using the `complete` method.

Based on above information the **Observable** should work like this:

```
let obs = rxjs.Observable.create((subscriber) => {  
    
  subscriber.next(1);  
  subscriber.next(2);  
  subscriber.next(3);  
  
  subscriber.complete();  
});  
  
obs.subscribe((value) => {  
  console.log(value);  
});
```

1. Create the Observable and pass a method into the constructor that will dispatch the values into the subscriber of the observable.
2. Finally subscribe to the Observable by passing a method which will receive the values.

The `subscribe` method invokes the constructor function passed into the **Observable**. Which means that subscribing to an **Observable** is the point when it starts executing its logic, rather than during creation, as is commonly believed. The constructor method is saved as a reference, and waits for the subscribe method to execute it.

In my example, I am passing a function into the **Observable**'s **constructor**, which gets executed right away when we subscribe, BUT it's usually provided by a library implementation that specifies what the Observable will emit and when it will emit it. And its often asynchronous.

So for example, in the real world scenario, the following service will execute the ***subscribe******method*** asynchronously, only when data is received from an HTTP service successfully.

```
getConfigFromServer() {  
  
  this.configService.getConfig()  
    .subscribe((data: Config) => this.config = {  
        heroesUrl: data.heroesUrl,  
        textfile:  data.textfile,  
        date: data.date,  
    });  
  
}
```

or here is an ***Observable*** that will emit a value every second **after** we subscribe to it:

```
var observable = rxjs.Observable.create((subscriber) =>{  
  let count = 0;  
  let interval;  
           
   interval = setInterval(()=>{  
        subscriber.next('Hello world (' + count++ + ')');  
          
        if(count > 5)  
        {  
         clearInterval(interval);  
            
          subscriber.complete();  
    }  
   }, 1000);  
  
});
```

Now, lets implement the **Observable** and finally execute these code samples.

![]()

Here is the sample code using the **rxjs** library to execute it:  
<https://jsfiddle.net/jsmuster/tgkc05vy/>

And here is my version with custom **Observable** implementation:  
<https://jsfiddle.net/jsmuster/u39t6bh8/>

Both function the same. We get the following console log in both examples:

![]()

Now lets take a look at the ***example*** where Observable is emitting a value every second:

We get the following console output:

![]()

With only 80 lines of code, we were able to achieve basic **Observable** functionality and everything seems to be working perfectly. Fantastic!

Let’s have some fun and enhance the functionality! We can create a lean version of the Observables library that caters to most of our use cases, without having to include the complete RxJS package in our projects.

The following snippet is part of the **RxJS** documentation, to make this work, we need to add the "**of**" method as demonstrated in the following example from the **RxJS** documentation.

![]()

I have implemented the “**of**” operator in the updated version, and made some modifications to how the methods are executed within the **Observable**. Essentially, I call them through a wrapper method via a “**call**” to make sure subscriber object is “**this**” within the **next**, **complete** and **error** methods. Check out the following example:

```
sub.complete = () => {  
  subscriber.complete.call(subscriber);  
};
```

You should get the following console log when running it:

![]()

On the RxJS Observable page, there’s another illustration of behavior that employs the “**interval**” method. This method returns a subscription object that is unsubscribed after 2.5 seconds using the **setTimeout** function.

For this to work, we must include the **interval** operator that generates the **subscription**, which we can later **unsubscribe** from.

![]()

Here is the example working using the standard **rxjs** library:

Here we have an instance of our custom rxjs library in action, as demonstrated by this example:

It’s amazing that both will produce output — this demonstrates how much our custom **rxjs** library has expanded. We can now utilize the **interval** operator to send numbers through the **Observable** and **unsubscribe** when necessary.

![]()

In conclusion, creating a custom Observable library from scratch is a great exercise to understand the inner workings of Observables and how they handle asynchronous data streams. With just a few lines of code, we were able to achieve basic Observable functionality and enhance it to cater to most use cases.

The beauty of Observables lies in their flexibility and ease of use. They can be used to handle data streams in a variety of scenarios, from simple data emissions to complex network requests. By understanding how Observables work, we can unlock a whole new level of functionality in our applications.

Thank you for reading and I hope this article has given you a better understanding of Observables and how to create your own custom Observable library.

## Check out my open source framework QQ:

<https://github.com/jsmuster/qq>

## Check out my other articles

[## Angular Routing in 5 Minutes

### You can use the Angular Route (angular/router) if you’d like to have your users navigate to different pages in your…

javascript.plainenglish.io](https://javascript.plainenglish.io/angular-routing-in-5-minutes-fe7300a0d174?source=post_page-----cb9a3c000e0---------------------------------------)

[## Angular Injector In 5 Minutes

### The best practice when creating a complex software is to adopt modular design. Functionality that is abstracted and…

levelup.gitconnected.com](/angular-injector-in-5-minutes-54d173c97541?source=post_page-----cb9a3c000e0---------------------------------------)

[## Searching for a good JavaScript Developer — the Interview Questions

### As a consultant in the IT industry for over 18 years, with a portfolio of 21+ products. I still find it difficult…

javascript.plainenglish.io](https://javascript.plainenglish.io/searching-for-a-good-javascript-developer-the-interview-questions-1691f0b925e6?source=post_page-----cb9a3c000e0---------------------------------------)

Please give the article some 👏 and *share it!*
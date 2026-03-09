---
title: "Understand JavaScript’s Event Loop"
url: https://medium.com/p/36c021f850f7
---

# Understand JavaScript’s Event Loop

[Original](https://medium.com/p/36c021f850f7)

# Understand JavaScript’s Event Loop

## Get in the loop

[![Hadar Raab](https://miro.medium.com/v2/resize:fill:64:64/1*1H9tSIBgFQqU_wjRTwXP_w.jpeg)](https://hadarraab.medium.com/?source=post_page---byline--36c021f850f7---------------------------------------)

[Hadar Raab](https://hadarraab.medium.com/?source=post_page---byline--36c021f850f7---------------------------------------)

5 min read

·

Jun 9, 2022

--

Listen

Share

More

Press enter or click to view image in full size

![]()

I recently watched [Philip Roberts](https://www.youtube.com/watch?v=8aGhZQkoFbQ)’ and [Erin Zimmer](https://www.youtube.com/watch?v=u1kqx6AenYw)’s great talks from JSConf EU on the JavaScript event loop, which inspired me to read the [HTML5 spec](https://www.w3.org/TR/2016/CR-html51-20160621/webappapis.html#event-loops) itself and make sure I truly understand it. I now think I’ve got a good grasp on what the event loop is, and I’d like to summarize that here.

## The Call Stack

The call stack is a data structure that remembers where we are in the code. Whenever we enter a new function, an execution context is pushed onto the stack, and when we return from the function the execution context is popped off, so that we can continue running the code from after the function invocation.

JavaScript is single-threaded, which means it can only execute one task at a time — there is only one thread, and only one call stack. If there’s “slow” code on the stack, it prevents the rest of the code from running, and it can also cause the UI to appear unresponsive. Because of this, we want this “slow” code (for example, network calls) to stay off the stack as much as possible.

## Task Queue and Event Loop

Blocking code is solved by using asynchronous callbacks — functions that are passed to another function that executes code in the background and then runs the functions that we passed. When it’s time to actually run these callbacks, we can’t put them directly back on the call stack, so we put them in a separate data structure where they can wait — the **task queue**. In order to execute the tasks that are waiting on the queue, we have the **event loop**, an infinite loop that is responsible (among other things) for taking the first task from the queue and pushing it onto the stack. The event loop runs once the call stack is empty.

A basic example for showing how the task queue and event loop work is using `setTimeout` . Let’s look at the following code:

```
console.log('Hello');  
setTimeout(() => console.log('World!'), 2000);
```

When this code is run, the following steps are executed:

1. `console.log('Hello')` is put on the call stack. It’s executed, and ‘hello’ is printed to the console.
2. `setTimeout(() => console.log('World'), 2000)` is put on the call stack. The method `setTimeout` is executed, which sends the callback and timer to the setTimeout API that is provided by the browser.
3. After 2 seconds, it’s time for the callback `() => console.log('World')` to run, so the web API pushes it onto the task queue.
4. The call stack is empty, so the event loop can take the callback off the task queue and push it onto the call stack, where it runs and prints ‘World’ to the console.

An important side note is that we can understand from these steps that `setTimeout(cb, 0)` doesn’t run the callback immediately, but rather the web API puts the callback directly onto the task queue. Because the tasks on the queue need to wait for the call stack to be empty, it can still take more time before the callback actually runs. This makes the timeout actually the *minimal* amount of time that is going to pass before the callback is executed, rather than the exact time.

## Rendering

After every task execution, the browser can decide if it’s time to run the rendering pipeline. Most browsers render the window about 60 times a second, which is about every 16ms, but the browser can choose to delay the render and prioritize other tasks. It’s important to note that because the rendering pipeline doesn’t run until after a task is complete, very long tasks delay the rendering of the window.

So far, we have described a basic event loop, consisting of one task queue and a rendering pipeline. So the logic looks like this:

## Multiple Task Queues

The HTML5 spec specifies that an event loop can have more than one task queue, as long as all tasks from a specific source (such as mouse clicks, timers, etc.) go to the same queue. The browser can set a different priority for each queue. On every tick, the event loop chooses which queue it wants to take a task from, and this task is put on the call stack. Just like with a single queue, the rendering pipeline can only run after the chosen task is complete.

A disadvantage of using multiple task queues is that you have less control over the timing of events — for instance, if there is a queue for timeouts and another for mouse events, the event loop can decide to empty the mouse event queue completely before running the events on the timeout queue, causing a greater delay for the timeout events than expected.

So now, our event loop looks like this:

## Microtask Queue

The event loop can also have a microtask queue (generally, microtasks are promises), which is handled after the chosen task from the “regular” queues is complete. This queue is unique in that on every tick of the event loop it is emptied completely before the loop moves on to the rendering pipeline.

When adding the microtask queue to the event loop, we get the following:

## Animation Frame Callback Queue

Finally, the event loop can also have an animation frame callback queue, where all the `requestAnimationFrame` callbacks go. These tasks run only once the browser has decided to run the rendering pipeline, and are executed before the repaint itself in order to update an animation. Only the tasks that are in the queue at the time of the repaint are run, and any new tasks that enter the queue are executed on the next tick of the event loop. This is so that if the code is setting up an animation, it updates the animation one frame at a time.

## Putting It All Together

That’s it! We’ve gone over all the different types of queues an event loop can have, and we now have a complete understanding of how the event loop works. When we put everything together, we get the following logic:

I hope you found this explanation as interesting as I did, and I’d be happy to hear any comments or insights you may have. See you next time!

*More content at* [***PlainEnglish.io***](https://plainenglish.io/)*. Sign up for our* [***free weekly newsletter***](http://newsletter.plainenglish.io/)*. Follow us on* [***Twitter***](https://twitter.com/inPlainEngHQ) *and* [***LinkedIn***](https://www.linkedin.com/company/inplainenglish/)*. Check out our* [***Community Discord***](https://discord.gg/GtDtUAvyhW) *and join our* [***Talent Collective***](https://inplainenglish.pallet.com/talent/welcome)*.*
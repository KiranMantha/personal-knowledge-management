---
title: "Promises vs Async/Await in JavaScript: What Actually Happens Under the Hood"
url: https://medium.com/p/c4d4161538f4
---

# Promises vs Async/Await in JavaScript: What Actually Happens Under the Hood

[Original](https://medium.com/p/c4d4161538f4)

# Promises vs Async/Await in JavaScript: What Actually Happens Under the Hood

[![devonmobile](https://miro.medium.com/v2/resize:fill:64:64/1*y8dGyx2R432It6C--ujVCg.png)](/@devonmobile?source=post_page---byline--c4d4161538f4---------------------------------------)

[devonmobile](/@devonmobile?source=post_page---byline--c4d4161538f4---------------------------------------)

2 min read

·

Apr 27, 2026

--

1

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dc4d4161538f4&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40devonmobile%2Fpromises-vs-async-await-in-javascript-what-actually-happens-under-the-hood-c4d4161538f4&source=---header_actions--c4d4161538f4---------------------post_audio_button------------------)

Share

*Understand the difference between Promises and async/await beyond syntax with real execution insights*

Press enter or click to view image in full size

![]()

At first glance, async/await looks like just a cleaner way to write Promises.

But under the hood, something more interesting is happening.

If you truly understand how Promises and async/await work internally, you’ll:

* write better async code
* debug issues faster
* avoid subtle bugs

Let’s break it down.

## What is a Promise?

A Promise represents a value that may be available:

* now
* later
* or never

It has 3 states:

* pending
* fulfilled
* rejected

## Basic Example

```
const fetchData = () => {  
  return new Promise((resolve) => {  
    setTimeout(() => resolve("Data loaded"), 1000);  
  });  
};  
  
fetchData().then((data) => console.log(data));
```

## What Happens Behind the Scenes

When a Promise resolves:

* its `.then()` callback goes into the **microtask queue**

This connects directly to the **event loop**

## What is async/await?

Async/await is syntactic sugar over Promises.

It makes async code look synchronous.

## Example

```
async function getData() {  
  const data = await fetchData();  
  console.log(data);  
}
```

## What Actually Happens Under the Hood

This:

```
await fetchData();
```

is roughly equivalent to:

```
fetchData().then((data) => {  
  // continue execution  
});
```

So async/await is still using Promises internally.

## Execution Flow Difference

## Promise (.then)

* chained execution
* callbacks stored in microtask queue

## Async/Await

* pauses function execution
* resumes after Promise resolves
* still uses microtasks internally

## Common Mistakes

## 1. Forgetting await

```
const data = fetchData(); // returns Promise
```

Fix:

```
const data = await fetchData();
```

## 2. Sequential awaits (slow)

```
const a = await fetchA();  
const b = await fetchB();
```

Fix with parallel execution:

```
const [a, b] = await Promise.all([fetchA(), fetchB()]);
```

## 3. Poor error handling

```
try {  
  await fetchData();  
} catch (e) {  
  console.log(e);  
}
```

Always handle errors properly.

## When to Use What

## Use Promises when:

* chaining multiple operations
* working with functional patterns

## Use async/await when:

* writing readable, sequential code
* handling complex flows

## Key Insight

Async/await doesn’t replace Promises.

> *It’s built on top of them.*

Understanding Promises deeply means you already understand async/await.

## Real-World Takeaway

Most bugs in async JavaScript come from:

* misunderstanding execution order
* ignoring microtasks
* improper error handling

Fix these and your code becomes predictable.

## Final Thoughts

Async JavaScript is not just about syntax.

It’s about understanding execution.

> *Once you understand what happens under the hood, async code stops being confusing and starts becoming powerful.*
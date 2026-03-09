---
title: "Fetch API Trick: Auto Retry Request When It Fails"
url: https://medium.com/p/284ed95a9107
---

# Fetch API Trick: Auto Retry Request When It Fails

[Original](https://medium.com/p/284ed95a9107)

Press enter or click to view image in full size

![]()

Member-only story

# Fetch API Trick: Auto Retry Request When It Fails

[![Developer Awam](https://miro.medium.com/v2/resize:fill:64:64/1*qsQhNmEIR5gX0DX8yCa_YQ.jpeg)](https://medium.com/@developerawam?source=post_page---byline--284ed95a9107---------------------------------------)

[Developer Awam](https://medium.com/@developerawam?source=post_page---byline--284ed95a9107---------------------------------------)

3 min read

·

Sep 3, 2025

--

Listen

Share

More

If you’ve been working with the **JavaScript Fetch API**, you’ve probably run into this frustrating scenario:

* Your network is unstable → the request randomly fails.
* The server is under heavy load → it times out.
* Or worse, the request just fails for no clear reason.

The problem is: **fetch only tries once**. If it fails, it throws an error right away. But sometimes, all you need is just **a retry or two** to make it work.

In this article, we’ll explore how to build a simple **auto retry mechanism** for Fetch API that makes your requests more reliable and your app much more user-friendly.

[You can read the full story for free by clicking here](https://medium.com/@developerawam/fetch-api-trick-auto-retry-request-when-it-fails-284ed95a9107?sk=cd206f22bd5b2c058e055881a8fd1a2d)

## Why Auto Retry Matters?

Imagine you’re building an app that relies on external APIs.

* 📶 **Unstable Wi-Fi:** your request might fail randomly.
* 🖥️ **Busy server:** trying again a second later could succeed.
* 🔔 **Critical data fetching:** you can’t afford to just give up after one failure.

That’s why auto retry can save you — and your users — from unnecessary frustration.

## Basic Implementation: Fetch with Retry

Here’s a simple implementation of Fetch with retry support 👇

```
// custom fetch with auto retry  
async function fetchWithRetry(url, options = {}, maxRetry = 3, delay = 1000) {  
    for (let attempt = 1; attempt <= maxRetry; attempt++) {  
        try {  
            const response = await fetch(url, options);  
  
            if (!response.ok) {  
                throw new Error(`Request failed: ${response.status}`);  
            }  
            return await response.json(); // return JSON if successful  
  
        } catch (err) {  
            console.warn(`Attempt ${attempt} failed: ${err.message}`);  
  
            if (attempt < maxRetry) {  
                console.log(`Retrying in ${delay / 1000}s...`);  
  
                await new Promise(resolve => setTimeout(resolve, delay));  
            } else {  
                throw new Error(`Request failed after ${maxRetry} attempts`);  
            }  
        }  
    }  
}
```

## Usage Example

```
fetchWithRetry("https://jsonplaceholder.typicode.com/posts/1", {}, 5, 1500)  
    .then(data => console.log("Data received:", data))  
    .catch(error => console.error("Still failed:", error.message));
```

Parameters explained:

* `maxRetry = 5` → maximum retry attempts.
* `delay = 1500` → 1.5 seconds delay between retries.

## Smarter Approach: Exponential Backoff

A better practice is to use **exponential backoff**. Instead of retrying at the same interval, you gradually increase the delay. This prevents spamming the server with too many requests.

```
async function fetchWithBackoff(url, options = {}, maxRetry = 4, baseDelay = 500) {  
    for (let attempt = 1; attempt <= maxRetry; attempt++) {  
        try {  
            const response = await fetch(url, options);  
  
            if (!response.ok) {  
                throw new Error(`Error: ${response.status}`);  
            }  
  
            return await response.json();  
  
        } catch (err) {  
            const delay = baseDelay * Math.pow(2, attempt - 1); // 500ms, 1000ms, 2000ms, ...  
            console.log(`Attempt ${attempt} failed. Retrying in ${delay / 1000}s...`);  
              
            if (attempt < maxRetry) {  
                await new Promise(resolve => setTimeout(resolve, delay));  
            } else {  
                throw new Error(`Request failed after ${maxRetry} attempts`);  
            }  
        }  
    }  
}
```

## Final Thoughts

Adding retry logic to Fetch makes your application:

* **More resilient** against network or server hiccups
* **Better user experience**, instead of showing instant error messages
* **Production-ready**, with exponential backoff to avoid hammering the server

Next time you’re building with Fetch, don’t just let your request fail once and give up — add retry logic and make your app bulletproof. 💪

## A message from our Founder

**Hey,** [**Sunil**](https://linkedin.com/in/sunilsandhu) **here.** I wanted to take a moment to thank you for reading until the end and for being a part of this community.

Did you know that our team run these publications as a volunteer effort to over 3.5m monthly readers? **We don’t receive any funding, we do this to support the community. ❤️**

If you want to show some love, please take a moment to **follow me on** [**LinkedIn**](https://linkedin.com/in/sunilsandhu)**,** [**TikTok**](https://tiktok.com/@messyfounder), [**Instagram**](https://instagram.com/sunilsandhu). You can also subscribe to our [**weekly newsletter**](https://newsletter.plainenglish.io/).

And before you go, don’t forget to **clap** and **follow** the writer️!
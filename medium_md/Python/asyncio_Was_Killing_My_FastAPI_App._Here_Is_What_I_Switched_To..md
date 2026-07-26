---
title: "asyncio Was Killing My FastAPI App. Here Is What I Switched To."
url: https://medium.com/p/96b0a9c22200
---

# asyncio Was Killing My FastAPI App. Here Is What I Switched To.

[Original](https://medium.com/p/96b0a9c22200)

Member-only story

# asyncio Was Killing My FastAPI App. Here Is What I Switched To.

## Three async libraries later. One actually solved the problem.

[![inprogrammer](https://miro.medium.com/v2/resize:fill:64:64/1*J7jk5vCGbEhewExz70dAAg.png)](https://medium.com/@inprogrammer?source=post_page---byline--96b0a9c22200---------------------------------------)

[inprogrammer](https://medium.com/@inprogrammer?source=post_page---byline--96b0a9c22200---------------------------------------)

6 min read

·

Apr 20, 2026

--

4

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D96b0a9c22200&operation=register&redirect=https%3A%2F%2Fai.plainenglish.io%2Fasyncio-was-killing-my-fastapi-app-here-is-what-i-switched-to-96b0a9c22200&source=---header_actions--96b0a9c22200---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![asyncio Was Killing My FastAPI App. Here Is What I Switched To.]()

**Friendlink for nonmembers-** [**https://medium.com/@inprogrammer/asyncio-was-killing-my-fastapi-app-here-is-what-i-switched-to-96b0a9c22200?sk=78bc5d9041277ce8eb857b4dd2a67f3a**](https://medium.com/@inprogrammer/asyncio-was-killing-my-fastapi-app-here-is-what-i-switched-to-96b0a9c22200?sk=78bc5d9041277ce8eb857b4dd2a67f3a)

My FastAPI app was fully async.  
Every endpoint used `async def`. Every DB call was awaited. I followed the docs perfectly.

Still, it was slow.

Not broken. Just slower than it should be.  
Requests that should take 50ms were taking 140ms.  
At just 200 users, performance dropped even more.

Async was supposed to handle thousands. Mine struggled with hundreds.

I spent two weeks debugging everything.

Turns out, the problem was not my code.

It was the async layer underneath.

Here is what I discovered and what I switched to.

## Why asyncio Falls Short Under Load

`asyncio` is Python’s default async system. It is what FastAPI uses out of the box. For most apps, it works fine and you never notice any issues.
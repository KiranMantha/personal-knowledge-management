---
title: "We Thought React Native Was the Answer — Until Our App Hit 190% CPU"
url: https://medium.com/p/f0e849073334
---

# We Thought React Native Was the Answer — Until Our App Hit 190% CPU

[Original](https://medium.com/p/f0e849073334)

# We Thought React Native Was the Answer — Until Our App Hit 190% CPU

[![Matt Sellars](https://miro.medium.com/v2/resize:fill:64:64/1*Y1AVeVGZUo-BwAvcnWU--w.jpeg)](https://medium.com/@matt_41344?source=post_page---byline--f0e849073334---------------------------------------)

[Matt Sellars](https://medium.com/@matt_41344?source=post_page---byline--f0e849073334---------------------------------------)

3 min read

·

Jul 9, 2025

--

5

Listen

Share

More

Like most startups, Motion’s mobile efforts began with React Native. We had a small team of Javascript developers, and the promise of React Native was a no brainer:

* A common way to target both mobile platforms, so that we could keep our team small and not hire dedicated iOS or Android developers
* Code that we could share and re-use between our backend, frontend, and mobile which was particularly useful since we were on a shared Typescript monorepo (using [Turborepo](https://turborepo.com/))
* The allure that *any* developer could contribute — it’s just Typescript, after all

The reality was not so clean. Frequently, we’d run into archaic build issues that needed some level of platform-specific knowledge. Then there were the app store requirements and limitations. And like any startup, we’d eventually have feature requests that required us to cross the native bridge (widgets, Siri integrations, etc).

So as we grew, we eventually made a dedicated mobile team of native mobile engineers who are writing mostly Typescript. And for the most part, this worked! From our experience, it’s much better to have native-capable engineers doing React Native than folks with only Javascript experience.

But as usage and feature requests grew, the app would grind to a halt on certain heavy screens. Take the calendar, for example. This was the first screen users saw whenever they launched the app.

Press enter or click to view image in full size

![]()

When we started profiling in XCode, the reason became obvious: the sheer number of views is effectively tripled due to the number of bridges going between JS to native and back. The CPU is pegged at 190%!

Technically, this screen is rendering 4 calendar days (each big rectangle) to make swiping between days quick and snappy. We could limit it to just one day and improve the initial load, but then the UX of switching between days would degrade. Our users deserved to have their cake and eat it, too.

We didn’t immediately jump to a giant Swift / Kotlin rewrite. Here is a quick sampling of the things we tried first:

1. **Caching the end view data model and not just the HTTP response in React Query**

Instead of using react query to just cache the http response have it cache the end processing result that is directly used by the react views that show the calendar.

**2. Lazy / deferred queries for React Query**

Instead delay enabling the query to let the chrome of the page render without data then enable the query to allow the data to render. This allowed for better perceived latency as the app rendered appearing to start up more quickly but was actually slightly slower to display the user’s calendar.

**3. Minimizing the DateTime parsing by having the backend return the exact format mobile needed**

DateTime parsing in the JS thread over a bunch of data for the calendar is expensive. Minimizing this freed up the thread to do more during the busy app startup time.

Overall these techniques did helped performance but did not ultimately allow us to reach the performance we were aiming for. Even with a 100% react query cache hit and no further data processing the app was just slow to render the views. Limiting the number of days rendered in the calendar added better performance but the trade off was swiping between calendar days was less performance especially when swiping quickly. It just didn’t feel like a native iOS or Android app.

Here’s the same screen after converting just the calendar screen to native code (still loading 4 calendar days’ of data) — note the CPU at just 5%.

Press enter or click to view image in full size

![]()

Going forward, we decided to do all new features on mobile with React Native first for iteration and speed. Then, based on the usage and performance demands, we convert them to native at our choosing. This hybrid approach has worked really well — especially since LLMs are *very* good at translating Swift code to Kotlin.
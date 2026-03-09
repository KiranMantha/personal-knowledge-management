---
title: "Why Silicon Valley CTOs Are Secretly Moving Away from React"
url: https://medium.com/p/bdf64f0b6072
---

# Why Silicon Valley CTOs Are Secretly Moving Away from React

[Original](https://medium.com/p/bdf64f0b6072)

Member-only story

Featured

# Why Silicon Valley CTOs Are Secretly Moving Away from React

[![Coders Stop](https://miro.medium.com/v2/resize:fill:64:64/1*AgkC3EIuY6TgqPe3kWr59w.jpeg)](https://medium.com/@coders.stop?source=post_page---byline--bdf64f0b6072---------------------------------------)

[Coders Stop](https://medium.com/@coders.stop?source=post_page---byline--bdf64f0b6072---------------------------------------)

8 min read

·

Apr 21, 2025

--

39

Listen

Share

More

“React isn’t failing because it’s bad. It’s failing because it succeeded too well.”

Those words from a CTO at one of Silicon Valley’s unicorn companies stuck with me. We were having drinks at a tech leadership meetup in Palo Alto — the kind where people speak more freely after the second round. The conversation had turned to frontend architecture, and I’d noticed a pattern in these closed-door conversations that wasn’t reflected in public discourse.

While React still dominates job postings, conference talks, and Twitter debates, a quiet shift is happening behind the scenes at many top tech companies. CTOs and engineering leaders are questioning their long-term commitment to React and exploring alternatives — often without public announcements.

Press enter or click to view image in full size

![]()

Over the past six months, I’ve spoken with engineering leaders at 24 high-growth tech companies. What I discovered surprised me, and it might change how you think about your own technology stack decisions.

## The Honeymoon is Over

React has been the dominant frontend framework for nearly a decade. It changed how we build web applications, popularized component-based architecture, and created a massive ecosystem of libraries, tools, and patterns.

But several converging factors are causing tech leaders to reconsider their commitment:

Sandeep M., VP of Engineering at a fintech unicorn that processes over $2 billion in annual transactions, explained: “We went all-in on React in 2017. By 2021, we had a major application with over 200 developers working on it. That’s when the scaling problems became impossible to ignore.”

His company hasn’t abandoned React, but they’ve stopped expanding their React footprint and are building new projects with different technologies.

“The React ecosystem made a series of bets that haven’t paid off for large-scale applications,” he told me. “The constant churn, the performance challenges at scale, the growing complexity of the mental model — they’ve created a perfect storm for teams building serious applications.”

## The Five Patterns Driving the Shift

After dozens of conversations, clear patterns emerged in why engineering leaders are questioning their React investment:

## 1. Performance Ceiling Effects

A recurring theme was hitting what CTOs described as a “performance ceiling” with React applications.

“We’ve got a team of incredible React developers who’ve optimized everything they possibly can,” explained Lisa K., CTO at a Series-C productivity SaaS company. “We’ve implemented virtualization, memoization, code splitting, server components — all of it. And we’re still hitting fundamental limits that are baked into React’s core design.”

The specific issues cited included:

* Rendering performance for large, data-heavy dashboards
* Memory usage patterns that become problematic at scale
* Initial load performance, especially on mobile devices
* The growing complexity of performance debugging

An engineering director at a major e-commerce platform shared their internal metrics: “Our React frontend hits performance bottlenecks at around 60% of the interaction complexity of our native apps, despite having 3x the engineering investment.”

## 2. The Growing “Meta-work” Problem

Another consistent complaint was what several leaders called “meta-work” — the growing amount of developer time spent on React-specific architectural patterns rather than actual business logic.

“In 2016, React felt lightweight. You could be productive quickly,” said Omar J., CTO of a digital health startup. “Now, to build a production-grade React application, my developers spend 60–70% of their time on React-specific patterns, configurations, and optimization techniques instead of solving our actual business problems.”

The list of required knowledge has grown enormously:

* Component lifecycles and hooks
* Complex state management strategies
* Memoization and re-render optimization
* Data fetching patterns
* Server components vs. client components
* Suspense and error boundaries
* Build tooling and configuration

“We calculated that our React developers spend only about 30% of their time writing code that directly implements features. The rest is spent on the React meta-layer,” one engineering VP told me.

## 3. The Talent and Onboarding Crisis

Several CTOs mentioned a surprising problem: while React developers are plentiful, truly skilled ones who understand the deeper patterns are increasingly rare and expensive.

“We can find a hundred developers who can write React components. But finding people who deeply understand React’s mental model and can architect large applications? That talent pool is shockingly small,” said Emily R., CTO of a developer tools company.

The growing complexity has also created an onboarding challenge:

“In 2018, we could onboard a new engineer to our React codebase in about two weeks. By 2022, it took new hires 2–3 months to become truly productive in the same application,” shared a VP of Engineering at a B2B SaaS platform. “The learning curve has become exponentially steeper.”

Several companies reported that their most experienced engineers were getting frustrated with the growing complexity and leaving for roles using other technologies.

## 4. The Framework Churn Tax

React’s ecosystem has seen significant conceptual shifts over the years:

* Class components → Function components + hooks
* Redux → Context API → Signals/Zustand/Jotai/etc.
* Render props → Higher-order components → Custom hooks
* Create React App → Next.js → Remix → Vite → etc.
* Client-side rendering → Server-side rendering → Server components

Each shift requires significant refactoring, retraining, and often complete rewrites of shared libraries and patterns.

“We’ve spent over 40% of our frontend engineering budget since 2020 just keeping up with the React ecosystem’s evolutions rather than building new features,” revealed a CTO at a major marketplace platform.

Another leader framed it more bluntly: “We’re forced to constantly rebuild the foundation while trying to add more floors to the building.”

## 5. The Dependency Security Nightmare

The final concern mentioned by almost every engineering leader was dependency management.

“The average React application we audit has between 1,500 and 2,000 npm dependencies. The security and maintenance burden has become untenable,” explained Wei C., head of engineering at a cybersecurity company.

A fintech CTO shared, “When we did an audit, we discovered that our main React application had 86 known vulnerabilities in its dependency tree, and resolving them would break 40% of our components. It’s a maintenance nightmare.”

This package bloat also impacts build times, developer experience, and architectural flexibility.

## Where Are They Going Instead?

The most interesting part of these conversations wasn’t just why leaders were moving away from React, but where they were going instead. No single alternative has emerged as the clear successor, which is partly why this shift is happening quietly rather than as a unified movement.

Here’s where companies reported investing:

## 1. Back to Vanilla JS with Targeted Libraries

Surprisingly, many companies reported shifting to a more vanilla approach:

“We’ve stripped React out of our highest-traffic user flows and replaced it with vanilla JavaScript using small, focused libraries for specific needs,” said the CTO of a streaming service. “Our page load times dropped by 60% and our conversion rates improved by 14%.”

Several mentioned Lit, Alpine.js, and Petite-Vue as lightweight alternatives for adding reactivity only where needed.

## 2. Compiler-Focused Frameworks

Svelte and Solid were frequently mentioned for new projects, with their compilation approach addressing many of React’s runtime performance issues.

“We rebuilt our account management portal with Svelte after struggling with React performance. The same team delivered the project in half the time, and the performance is dramatically better,” shared a VP of Engineering at a cloud infrastructure company.

Several mentioned that the mental model of these frameworks is significantly simpler for new developers to grasp, reducing onboarding time.

## 3. Islands Architecture

Another pattern was shifting to an “islands architecture” where interactive components are isolated within a mostly static page.

“We’re using Astro for most of our marketing and content sites now. We only use React for the complex interactive components, which is maybe 20% of our frontend,” explained the CTO of a content platform.

This approach limits React to just the pieces that truly need its capabilities, reducing the overall complexity and performance impact.

## 4. WebAssembly for Performance-Critical Paths

Some companies are making a more radical shift:

“For our data visualization dashboards, we’ve moved to a WebAssembly approach using Rust and the Yew framework,” said the CTO of a data analytics startup. “The performance difference is not incremental — it’s transformative.”

Several mentioned exploring WebAssembly for high-performance parts of their applications while using simpler approaches for standard CRUD interfaces.

## 5. Internal UI Libraries

A handful of the largest companies reported building their own lightweight alternatives:

“We’ve created an internal UI framework that’s specifically optimized for our use cases. It’s about 20% of the size of React, with vastly better performance characteristics for what we need,” shared a principal engineer at a streaming company.

The rise of compiler tools like SWC has made this approach more viable than it would have been in the past.

## The PR Problem: Why This Shift Is Happening Quietly

If so many companies are moving away from React, why aren’t we hearing more about it? Several factors are at play:

1. **The Incremental Nature of the Shift**: Most companies aren’t doing wholesale rewrites but rather moving new projects to different technologies while maintaining existing React codebases.
2. **Recruiting Concerns**: “We don’t want to publicly announce we’re moving away from React when there are still so many React developers in the job market,” explained one VP of Engineering.
3. **The Career Investment Factor**: Many developers and engineering leaders have invested years in React expertise, creating institutional resistance to change.
4. **The Meta/Facebook Effect**: React’s association with Meta/Facebook still carries significant weight in technology decisions.

## Is React “Dying”? No, But Its Role Is Changing

To be clear, React isn’t disappearing anytime soon. What’s happening is more nuanced — React is transitioning from “the default choice for everything” to “one tool in a more specialized toolbox.”

“We still use React for our admin dashboards and internal tools,” said James L., CTO of a sustainable transportation startup. “But we’ve stopped using it for customer-facing applications where performance is critical.”

Another engineering leader put it this way: “React solved an important set of problems for a specific era of web development. We’re entering a new era with different challenges.”

## The Lessons for Engineering Leaders

The most valuable insights from these conversations weren’t about React specifically, but about how technology choices evolve:

1. **Beware the Monoculture Effect**: When one technology becomes too dominant, it can create blind spots about its limitations.
2. **Evaluate Carrying Costs, Not Just Capabilities**: Many CTOs mentioned they initially underestimated the long-term maintenance and complexity costs of their React investment.
3. **Watch the Innovators, Not the Majority**: The companies making these shifts are often at the leading edge — their challenges today may be yours tomorrow.
4. **Consider Business Impact, Not Technical Purity**: The companies making changes were motivated by business metrics like performance, conversion rates, and engineering velocity — not just technical preferences.

## What’s Your Experience?

I’ve shared what I’ve learned from conversations with Silicon Valley engineering leaders, but I’m curious about your experience. Are you seeing similar patterns in your organization? Have you hit the limits of React for certain use cases, or is it still serving your needs well?

The most enlightening discussions happen when we move beyond framework tribalism and honestly evaluate what’s working, what’s not, and why. Let me know your thoughts in the comments.

*Note: Some names and identifying details have been changed at the request of the individuals interviewed for this article.*

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/@InPlainEnglish) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0) | [**Differ**](https://differ.blog/inplainenglish) | [**Twitch**](https://twitch.tv/inplainenglish)
* [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)
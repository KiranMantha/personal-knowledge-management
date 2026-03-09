---
title: "Why You Should Avoid Using Server Actions for Data Fetching in Next.js 15"
url: https://medium.com/p/434156814dbd
---

# Why You Should Avoid Using Server Actions for Data Fetching in Next.js 15

[Original](https://medium.com/p/434156814dbd)

Press enter or click to view image in full size

![]()

Member-only story

# Why You Should Avoid Using Server Actions for Data Fetching in Next.js 15

[![Alvis Ng](https://miro.medium.com/v2/resize:fill:64:64/1*kKJHnRlneR5oCtJw0ahXiQ.jpeg)](https://medium.com/@iamalvisng?source=post_page---byline--434156814dbd---------------------------------------)

[Alvis Ng](https://medium.com/@iamalvisng?source=post_page---byline--434156814dbd---------------------------------------)

13 min read

·

Apr 6, 2025

--

11

Listen

Share

More

> ⭐⭐⭐ ️️Note: If you’re not a Medium member, you can still read this article for free using this [**link**](https://medium.com/@iamalvisng/why-you-should-avoid-using-server-actions-for-data-fetching-in-next-js-15-434156814dbd?sk=e3907cd66f62275ec48c65553ac9f19c)

Next.js 13+ introduced **Server Actions** — functions that run on the server in response to client events. At first glance, it’s tempting to use Server Actions for all data needs, even simple data fetching, because they let you call server code directly from your components. However, just because you can, doesn’t mean that you should. In this piece, I’ll lay out why **you should avoid using Server Actions for data fetching** in Next.js, and what to doinstead.

## What are Server Actions meant for?

Server Actions were introduced to simplify server-side mutations (e.g. form submissions or database writes) in the Next.js App Router. They enable an RPC-like mechanism. When you call a Server Action from a client component, Next.js serializes the call and sends a `POST` request under the hood to execute that function on the server, then returns the result to your app​. This is powerful for things like creating a new record or processing a form without setting up a separate API route. After the action runs, Next.js can automatically re-render affected UI parts for you.

Crucially, though, Server Actions were designed for mutations, not queries. The React team explicitly notes that Server Actions are designed for mutations that update server-side state; [they are not recommended for data fetching](https://react.dev/reference/rsc/use-server#caveats). In fact, Next.js documentation reiterates that data loading should primarily happen in Server Components, whereas [Server Actions are not intended for data fetching but for mutations](https://nextjs.org/docs/app/building-your-application/data-fetching/server-actions-and-mutations). Using them purely to read data breaks the intended separation of concerns. Let’s dive into why using Server Actions for fetching data is problematic.

## Performance Drawbacks of Using Server Actions for Fetching Data

### Waterfall Requests and Latency

One of the biggest performance pitfalls is that Server Actions execute **sequentially**. Even if you invoke multiple actions at once, Next.js will typically run them one-by-one rather than in parallel​. This means if your page or component tries to fetch data from, say, three different sources using three Server Actions, they will fire in a waterfall: the second starts only after the first finishes, and so on​. What could have been three parallel fetches becomes a chained series, adding significant latency to your UI.

This sequential processing is by design (to keep server state consistent during mutations), but for data retrieval, it’s pure overhead. A normal `fetch` or database query can often be done in parallel, whereas a series of Server Actions introduces unnecessary waiting. The result is slower data delivery to the user, especially noticeable if you naively call multiple actions for different data pieces.

Imagine a dashboard that needs user info, notifications, and messages. If you implemented each data fetch as a Server Action and call them together, the user might wait for the user info action to complete before the notifications action even begins, and so on. In contrast, using standard data fetching, those requests could happen concurrently. The sequential nature of Server Actions thus risks turning your data loading into a slow waterfall.

### Extra Network Round Trips and Server Compute

When you call a Server Action to fetch data, you’re incurring an **extra network round trip** that might not be needed. That is because a Server Action from the browser triggers a behind-the-scenes `POST` call to your Next.js server. This is effectively an internal API call for data that you could often fetch directly. Every Server Action invocation carries the overhead of serializing the input (and output) and establishing a network connection to your server​. That’s on top of whatever database or API calls the action itself makes.

For example, if your Server Action just calls `fetch('/api/posts')` internally to get some data, you’ve added an extra step. The client could have called `/api/posts` itself, but instead it called the action, which then called the API route – double the handling. Each additional hop increases latency. In performance-sensitive applications, these extra milliseconds add up, especially on high-latency connections.

Furthermore, if you deploy on a serverless platform (like Vercel), each Server Action might run in a separate function invocation. This can lead to more cold starts and overhead compared to batching work in a single request. Compared to traditional approaches like API routes or batched procedures, this setup can be less efficient and harder to optimize at scale.

### Direct DB Calls from Server Actions Still Hurt Performance

Even if you skip the extra network call and use a Server Action to directly query your database, say with [Prisma](https://www.prisma.io/) or [Drizzle](https://orm.drizzle.team/), the performance drawbacks don’t disappear. Here’s why:

Press enter or click to view image in full size

![]()

**You’re Still Incurring a Separate Server Roundtrip**From the browser’s perspective, you’re calling a function (`await getData()`) that under the hood makes a `POST` request to your app’s server. It doesn’t matter if the action then talks directly to the DB; the initial client-to-server hop still happens. That roundtrip adds latency compared to data already fetched during SSR or inside a Server Component.

**No Caching or Deduplication**Actions invoked like this are not cached. Every time a Server Action is called , even with the same args, it triggers a fresh run. Unlike `fetch()` in a Server Component (which Next can cache and dedupe), Server Actions are always treated as dynamic `POST` requests.

This applies even within the same request. If two components call the same Server Action with the same parameters, Next will run both actions independently, hitting the DB twice for no reason.

While React 19 introduced a `cache()` utility to memoize function calls, it’s still experimental at the time of writing. And relying on unstable internals to patch over a misuse is unnecessary when better patterns already exist.

**Sequential Execution Still Applies**Even if you’re making multiple DB queries (e.g. user info, posts, stats), and each is encapsulated in its own Server Action, they’ll still run **sequentially**. That means you’re delaying rendering while the backend does work that could’ve been parallelized inside a Server Component or batched in a loader.

**Reduced Observability and Control**Fetching in Server Components or API routes gives you more control. You can trace queries, add caching headers, monitor performance, or plug into logging systems. Server Actions hide those behind framework internals, harder to profile, harder to fine-tune.

## Violating Separation of Concerns (Queries vs. Mutations)

The misuse of Server Actions for data fetching isn’t just a technical issue — it’s an architectural one. Web applications have long distinguished between **queries** (reading data) and **mutations** (changing data). This separation is there for good reasons. It clarifies intent, enables caching for reads, avoids unintended side effects, and often informs how we design our APIs (think REST `GET` vs `POST`).

Server Actions, by nature, handle `POST` **requests and side effects**. In fact, Next.js only allows actions to be invoked via `POST` under the hood. Using a `POST` mechanism to perform what is fundamentally a `GET` operation subverts HTTP semantics. You’re using the wrong tool for the job, fetching data through a POST-only tunnel, misusing a write-only mechanism for reads.

For one, when everything is an action, you lose the ability to leverage HTTP caching or even to think in terms of idempotent operations. A normal `GET` request for data can be retried safely, cached at multiple levels, and generally treated as a read. A `POST` (like how Server Actions work) is not cached by default and might accidentally be retried, causing duplicate processing. It also makes monitoring and logging harder, your data fetch calls won’t appear as neat `GET` requests in logs or browser dev tools, but as opaque calls to an internal endpoint.

Moreover, mixing concerns can lead to muddled code. You might start putting what are effectively data loaders into your action files. Some community tutorials have even encouraged moving all data-fetching logic into Server Actions for “co-location” purposes. While the intention (separating presentation from data logic) is good, doing this via Server Actions is misguided. It turns your action functions into a pseudo-API layer living inside your Next app, with no clear distinction between “get” and “change” operations. This can confuse developers about what an action does. Is it safe to call just to get data, or will it also update something? Over time, such ambiguity harms maintainability.

In short, using the same abstraction for both queries and mutations violates the principle of separation of concerns. It’s better to have dedicated patterns for data reads that allow caching, composition, and clarity, and save Server Actions for what they’re meant for, which is handling server-side mutations — creating, updating, or deleting data, **not** for fetching it.

## Maintainability and Scalability in Larger Codebases

Even if your app is small, the drawbacks of using Server Actions for fetching data can bite you. And they only grow with scale.

**Tight Coupling and Lock-In**Building your data fetching around Server Actions ties your front-end directly to Next.js internals. This tight coupling becomes a problem if you ever need to extract a service, reuse logic in a non-Next context, or migrate away from the framework. Server Actions are a Next-specific abstraction, useful in the right context, but also a form of vendor lock-in. In a large codebase, that can limit your flexibility. For example, if you later want to share backend logic with a mobile app, you’ll probably need to rewrite those actions as real APIs anyway.

**Testing and Tooling Limitations** A conventional API layer can be tested in isolation. You can unit test your `fetchData()` function, your route handler, your backend service. But Server Actions live inside the framework’s runtime, testing them often means spinning up a Next environment or mocking internals. Not ideal for teams that care about clean test boundaries. On top of that, most devtools and observability platforms expect a standard request/response flow. With Server Actions, you’re dealing with opaque `POST` requests to internal endpoints. This means less visibility, more guesswork.

**Scaling Team Collaboration** In bigger teams, separation of concerns isn’t just theory, it’s how you divide work. Backend engineers build APIs. Frontend engineers consume them. But when all your reads live inside Server Actions in React files, you’re implicitly assigning backend responsibilities to frontend code. That might be fine in a small team, but as the codebase grows, it creates ownership confusion. Is this component calling a query or a mutation? Is it safe to call twice? Should this logic live on the server or move out?

**Unpredictable Performance at Scale** The performance issues mentioned earlier, no caching, sequential execution, which only get worse as your app grows. It might be fine if one or two Server Actions are fetching data. But if you scale this pattern across dozens of components, now your app is firing a bunch of `POST` requests that can’t be batched, deduped, or cached. That doesn’t scale well, and it can easily turn into a maintenance nightmare.

Also worth noting that Next.js is still figuring out the best practices here. Server Actions were marked as experimental in 13 and 14. Even in 15, the docs still lean on `fetch()` and Server Components for reads. There's a reason for that. If your app is long-lived or mission-critical, it’s safer to stick with patterns that are battle-tested and better understood.

## Better Alternatives for Data Fetching in Next.js 15

The good news is you don’t need Server Actions to craft a solid data-loading strategy in Next.js. Here are some **more predictable and performant alternatives** for various scenarios:

**Use Server Components for Initial Data**  
In the App Router, **Server Components** are the recommended way to fetch data on the server. You can make your data requests (to databases or external APIs) directly in an async Server Component and leverage Next.js’s built-in caching and streaming. For example, you might fetch a list of products in a page component or loader component on the server side, and Next will stream the rendered HTML to the client. This approach is straightforward and benefits from automatic memoization of identical fetches​. It also keeps your data fetching within the initial render cycle, which is ideal for SEO and time-to-first-byte performance. Next.js explicitly *“recommends that data fetching should happen in Server Components”,* passing data down to client components via props.

**Use** `getServerSideProps` **or** `getStaticProps`**(Pages Router)**  
If you’re still on the older Pages Router (or using a mix of App and Pages), the classic methods like `getServerSideProps`(for SSR) or `getStaticProps`(for SSG) are very reliable for data fetching. They ensure data is fetched before rendering the page, and they enforce separation by running outside of your component tree. This way, your pages receive all needed data as props. It might feel a bit boilerplate compared to the new App Router style, but it’s proven and straightforward. You won’t risk waterfalls since you can parallelize fetches inside these functions, and you can utilize caching (e.g. static generation or incremental static regeneration) easily.

**Leverage Route Handlers for APIs**Next.js 13+ supports **Route Handlers** (`app/api/*/route.ts`) which let you create custom endpoints. If you have client-side interactivity that requires data (especially after initial load), create an API route for it rather than a Server Action. For instance, instead of an action `searchProducts(query)` that returns results, set up `app/api/products/search/route.ts` to handle `GET` requests with the query. Then call it with a normal `fetch` from your client component or, better yet, via a data-fetching library. Route Handlers give you full control over caching headers, can be optimized independently, and don’t run into the one-at-a-time limitation. Do note that on platforms like Vercel, heavy use of API routes could count against function invocation quotas​, but at least you can cache `GET` responses at the edge if needed. The key benefit is clarity: you have a defined, testable API endpoint and you treat data fetching as a regular HTTP call.

**Adopt SWR or React Query on the Client**For purely **client-side stateful data** (especially data that updates frequently or needs caching/revalidation on the client), libraries like [**SWR**](https://swr.vercel.app/) or [**TanStack Query**](https://tanstack.com/query/latest) are excellent. These libraries handle caching, deduping requests, background refetching, and loading states in a very predictable way. Instead of `await myServerAction()` in a click handler, you might use TanStack Query’s `useQuery` hook to fetch from an API route, or SWR’s hook to fetch a resource and keep it fresh. By doing so, you get a richer DX (with devtools to see query states) and avoid the black-box nature of Server Actions. These libraries also encourage a clear separation. Your UI reacts to data from a cache, and the fetching logic is abstracted away, which aligns nicely with React’s ethos—declarative UIs that update in response to state changes, not imperative data flows.

**Use Parallel Routes or Prefetching for UI Interactions**Next.js 15 introduced advanced routing patterns like [**Parallel Routes**](https://nextjs.org/docs/app/building-your-application/routing/parallel-routes) **and** [**Interception**](https://nextjs.org/docs/app/building-your-application/routing/intercepting-routes). These can address scenarios like modals or sidebars that need data only when opened. Instead of using a Server Action to fetch data when a modal opens, you can structure your app such that the modal is a separate route that loads its data on the server. Next can even **prefetch** those routes when it suspects the user might navigate (e.g., hover), so by the time the user clicks, the data is already there. This pattern keeps data fetching declarative (as part of routing) rather than imperative (as an `onClick` event). The Next.js docs show examples of using parallel routes to load secondary content without additional client fetches. This approach maintains separation of concerns. Your modal’s data requirements are handled by the framework’s routing and data loading, not by a manually triggered Server Action.

By sticking to these alternatives, you regain predictability. Data fetching becomes either a part of your initial render (SSR/Server Components) or an explicit client-side operation (with an API and cache in place). You can reason about performance, adding a new data requirement won’t suddenly serialize all other requests or bypass your caching layer. And you avoid the many caveats that come with shoehorning reads into the Server Action mechanism.

## Conclusion

Server Actions are a powerful addition to Next.js, but with power comes responsibility. They shine in scenarios where a user performs a mutation, like submitting a form, saving a setting, creating or deleting something and have the UI updated. For data fetching, however, Server Actions introduce more problems than they solve**.** They degrade performance by forcing sequential, uncached calls. Complicate the DX with hidden network trips and debugging hurdles. Moreover, they muddy the architectural waters by mixing read and write concerns.

In an experienced full-stack team, clarity and reliability are paramount. It’s no surprise that neither the React nor Next.js recommend using Server Actions for queries​. The web already has a well-understood mechanism for that — HTTP `GET` or its equivalents—and a whole ecosystem of tools built around it. Embracing those patterns will lead to a more maintainable and scalable codebase.

So, be opinionated in your own projects. Use Server Actions when they help you securely handle mutations without the overhead of an extra API layer. But resist the temptation to use them as a catch-all data fetching shortcut. Your app and your team will be better off for it.

Using a Server Action for fetching is a complex way to handle an operation that doesn’t need to be complex. Stick to the simpler, more predictable methods for loading your data, and you will sleep better at night.

## Enjoyed this piece?

If this piece was helpful or resonated with you, you can support my work by buying me a [**Coffee**](https://buymeacoffee.com/iamalvisng)!

[![]()](https://buymeacoffee.com/iamalvisng)

✨ **Your support motivates me to create more insightful articles!**

👍 **Enjoyed the read?** Clap generously — every clap counts!

💡 **Tip:** Long-press the clap button on Medium to give multiple claps at once.

🔗 **Spread the word!** Share this article on your favorite platforms like **LinkedIn**, **Threads**, or other social media to help it reach more readers.

🐦 **Highlight and Tweet!** Select your favorite takeaway to share quickly on X.

[## Alvis Ng — Medium

### Read writing from Alvis Ng on Medium. Technical Lead at YOPESO | Building High-Impact Applications with Next.js, React…

medium.com](https://medium.com/@iamalvisng?source=post_page-----434156814dbd---------------------------------------)

***Alvis Ng*** *— Technical Lead at* [***YOPESO***](https://www.yopeso.com/)*. Having transitioned from product management through front-end to full stack development, I strive to intertwine design with functionality and convert user stories into values. Beyond the code, my guiding principle is CI/CD: Continuous Improvement & Continuous Development.*

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/@InPlainEnglish) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0) | [**Differ**](https://differ.blog/inplainenglish) | [**Twitch**](https://twitch.tv/inplainenglish)
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)
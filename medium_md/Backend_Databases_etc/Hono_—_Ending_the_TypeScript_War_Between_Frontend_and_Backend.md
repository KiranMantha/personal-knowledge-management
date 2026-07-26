---
title: "Hono — Ending the TypeScript War Between Frontend and Backend"
url: https://medium.com/p/ea9b2b7214e5
---

# Hono — Ending the TypeScript War Between Frontend and Backend

[Original](https://medium.com/p/ea9b2b7214e5)

# Hono — Ending the TypeScript War Between Frontend and Backend

[![Eva Matova](https://miro.medium.com/v2/resize:fill:64:64/1*fUYxZOsSVCUyyarQs92RuA.jpeg)](/@eva.matova6?source=post_page---byline--ea9b2b7214e5---------------------------------------)

[Eva Matova](/@eva.matova6?source=post_page---byline--ea9b2b7214e5---------------------------------------)

8 min read

·

Dec 15, 2025

--

3

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dea9b2b7214e5&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40eva.matova6%2Fhono-ending-the-typescript-war-between-frontend-and-backend-ea9b2b7214e5&source=---header_actions--ea9b2b7214e5---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

Have you ever fought with TypeScript… and lost?

Different types on the backend.   
Different types on the frontend.   
Types that usedto match until one small API change, and suddenly everything compiles but nothing works.

This is a problem almost every TypeScript backend runs into eventually. We duplicate types, hope they stay in sync, and trust the compiler a little more than we should.

Today I want to share with you my experience with **Hono** 🔥 that completely changed how I think about type-safe APIs. It turned out to be one of the cleanest DX experiences I’ve had in a long time, so it’s worth sharing a few words about it.

**In this article, I’ll show you:**

* 🚀 Why Hono is a compelling Express.js
* 🔗 How it unifies frontend and backend types
* 🧠 How Zod, and type inference work together

Let’s dive in.

## When Express Was Enough

If you’ve ever built a JavaScript server, you’ve probably used **Express.js**. And for a long time, it worked great…until it didn’t.

Express was first released around **2010**, and back then it was revolutionary. It gave Node.js developers a simple, flexible way to build servers when the ecosystem was still young. But it’s 2025, and the JavaScript world looks very different.

We now have **edge runtimes**, **Bun**, **Deno**, Cloudflare Workers, native **Web APIs**, and **TypeScript** as a default. Our expectations around performance, portability, and type safety have evolved, but Express hasn’t evolved at the same pace.

Express is still tightly coupled to Node.js, built on the legacy `http` module, and weakly typed. Even with TypeScript support it often feels bolted on rather than designed in.

None of this makes Express a bad framework. And for many developers, myself included, that’s the moment when you start looking for something more modern, faster, and more TypeScript-friendly.

That’s where frameworks like **Hono** enter the conversation.

## What is Hono?

[Hono](https://hono.dev/) (meaning *“flame”* in Japanese) is an **ultralight, web-standard web framework** for JavaScript and TypeScript. You can think of it as a modern counterpart to Express. It feels very familiar with its routing, middleware, and request handling, but it’s designed for today’s ecosystem.

### What Makes Hono Stand Out?

🛠️ **Multi-runtime support**   
Run the same code on Node.js, Bun, Deno, Cloudflare Workers, AWS Lambda, Edge environments

⚡ **Ultralight and fast**Hono is ~**14 KB minified**, has **zero dependencies**, and is built on native Web APIs like `fetch`.  
(For comparison, Express is **500+ KB** and tied to Node’s `http` module)

🔀 **RegExpRouter**One of the fastest routers in the JavaScript world, making routing both performant and predictable

🤜🤛 **Built-in middlewares and helpers**CORS, cookies, streaming, authentication, and more — all included, no extra packages

👌 **TypeScript-first**Strong type inference, especially when combined with Zod for runtime validation

## How Hono Works in Practice

The real magic of Hono isn’t just about types, it’s about having **one clear, consistent way** to build and consume your API.

With Hono, you define your logic on the backend, validate data at runtime, and let TypeScript **flow naturally to the frontend**. This is achieved through a combination of routes, Zod validation, and `hono/client` .

Let’s walk through how this works step by step 👇

Before we start, you should have Hono installed. Follow the [official guide](https://hono.dev/docs/getting-started/basic), it’s pretty straightforward.

### 🛠️ Step 1: Set up a server

In `app.ts`, we start with a simple Hono server. In this example below we also use one of the built-in middleware — the `logger`.

It’s a small addition, but incredibly useful. It lets you see the flow of requests and responses right in your console, which makes debugging easier and helps you spot issues early.

```
// server/app.ts  
  
import { Hono } from 'hono'  
import { logger } from 'hono/logger';  
  
const app = new Hono();  
  
app.use('*', logger());  
  
app.get('/', (c) => {  
  return c.text('Hello from Hono 🔥')  
});  
  
export default app;
```

### 🧩 **Step 2: Define Routes with Zod Validation**

Now, let’s create our first route. For this example, we’ll keep things simple and build a **“create expense”** endpoint. It accepts a JSON body and returns the newly created expense. Nothing fancy , just enough to show how Hono handles validation and types.

To do this, we’ll combine:

* 🗄️ **Drizzle** for the database
* 🛡️ **Zod** for runtime validation
* 🔥 **Hono** for routing

**Generate a Zod Schema from Drizzle**We start with our database schema that describes the shape of our data at the database level. Instead of manually duplicating this structure in Zod or TypeScript, we generate everything directly from Drizzle.

The database becomes the **single source of truth** for both frontend and backend.

```
// server/db/schema.ts  
  
import { integer, real, sqliteTable, text } from 'drizzle-orm/sqlite-core';  
import { createInsertSchema } from 'drizzle-zod';  
  
export const expenses = sqliteTable('expenses', {  
  id: text('id')  
    .primaryKey()  
    .$defaultFn(() => crypto.randomUUID()),  
  name: text('name').notNull(),  
  amount: real('amount').notNull(),  
  date: text('date').notNull(),  
  createdAt: integer('created_at', { mode: 'timestamp' })  
    .notNull()  
    .$defaultFn(() => new Date()),  
  updatedAt: integer('updated_at', { mode: 'timestamp' })  
    .notNull()  
    .$defaultFn(() => new Date()),  
});  
  
export const expenseInsertSchema = createInsertSchema(expenses);  
  
export type CreateExpense = InferInsertModel<typeof expenses>;
```

**Use the Schema in a Hono Route**Now we plug that schema into our `zValidator` in the route.

Zod validates the request **at runtime**, and at the same time provides TypeScript with everything it needs for full type inference on the client.

In the “create expense**”** endpoint, we validate the JSON body of the request, but that’s just one option. Hono allows you to validate every part of the request in the same way, and you can even chain them.

* `json` — request body
* `query` — query parameters
* `param` — route parameters
* `header` — request headers
* `form` — form data

> One more thing you might notice: unlike Express, where you work with separate `req` and `res` objects, Hono gives you a single parameter called `c` (in our case), short for **Context**. It contains the request, the response helpers, and all validated data in one place, which keeps handlers clean and easy to read.

```
// server/routes/expenses.ts  
  
import { Hono } from 'hono';  
import { z } from 'zod';  
import { zValidator } from '@hono/zod-validator';  
import { expenseInsertSchema } from '../db/schema';  
  
const app = new Hono();  
  
const createExpenseSchema = z.object({  
  name: z.string(),  
  amount: z.number(),  
});  
  
app.post(  
  '/expenses',  
  zValidator('json', expenseInsertSchema),  
  (c) => {  
    const expense = c.req.valid('json')  
    return c.json({ status: 'success', data: expense })  
  }  
);
```

### ➜] Step 3: Export Route Types

Next, we expose our routes to the frontend.

This is where Hono really starts to feel different. Instead of manually defining shared interfaces, we export the actual route tree**.**

```
// server/app.ts  
  
import { Hono } from 'hono';  
import { logger } from 'hono/logger';  
import { expensesRoute } from './routes/expenses';  
  
const app = new Hono();  
  
app.use('*', logger());  
  
const appRoutes = app.route('/expenses', expensesRoute);  
  
export default app;  
  
export type AppRoutes = typeof appRoutes;
```

⚠️ **Important Note:** **Route chaining matters!**Route chaining is **not optional** if you want proper type inference.

If you create multiple Hono instances or forget to keep the returned chained instance,TypeScript loses visibility of your full API. The server will still work perfectly at runtime, but on the frontend things quietly fall apart:

* Types become `unknown`
* Autocomplete disappears
* Hover hints stop working

Imagine you have not only `expenses` routes, but also `users` routes. You define both sets of routes, but each one lives in its own Hono instance. At runtime, everything works, but TypeScript can’t see the full API, so types don’t flow to the frontend.

Let’s look on what *not* to do and then the correct approach.

```
// server/app.ts  
// ❌ Wrong! Separate routes.  
  
import { Hono } from 'hono';  
import { expensesRoute } from './routes/expenses';  
import { usersRoute } from './routes/users';  
  
const app = new Hono();  
  
// Each call returns a new typed instance, but we throw it away  
app.basePath('/api/v1');  
app.route('/expenses', expensesRoute);  
app.route('/users', usersRoute);  
  
export type AppRoutes = typeof app;
```

This is how it should look like.

**The rule of thumb is simple:**❌ Separate typed instances → no type inference  
 ✅ One fully chained instance → full end-to-end types

```
// server/app.ts  
// ✅ Correct! Fully chained routes.  
  
import { Hono } from 'hono'  
import { expensesRoute } from './routes/expenses'  
import { usersRoute } from './routes/users'  
  
const app = new Hono()  
  
const appRoutes = app  
  .basePath('/api/v1')  
  .route('/expenses', expensesRoute)  
  .route('/users', usersRoute)  
  
export default app;  
  
export type AppRoutes = typeof appRoutes;
```

### 🔗 Step 4: Create a Typed Client on the Frontend

Now comes the part where everything really clicks.

On the frontend, use `hc` from `hono/client` to create a client that mirrors our backend routes, including paths, methods, inputs and responses.

```
// client/src/lib/api-client.ts  
  
import type { AppRoutes } from '@server/app';  
import { hc } from 'hono/client';  
  
const honoClient = hc<AppRoutes>('/');  
  
export const apiClient = honoClient.api.v1;
```

That’s it. From this moment on, your frontend *knows* your backend.

**Calling the API Feels Like Calling a Local Function ✨**You don’t have to write `fetch`, deal with `any`, or manually define request and response types. TypeScript automatically knows what the route expects and what it returns.

Now, let’s create `createExpense` API function.  
Notice something important here, we don’t define a new input type. We reuse the one we defined via Drizzle.

```
// client/src/api/create-expense.ts  
  
import { apiClient } from '@/api/client';  
import type { CreateExpense } from '@server/db/schema';  
  
export async function createExpense(input: NewExpense) {  
  const res = await apiClient.expenses.$post({  
    json: input,  
  });  
  if (!res.ok) {  
    throw new Error('Failed to create expense');  
  }  
  return res.json();  
}
```

You might wonder what updating an expense API function would look like when it involves both a JSON body and a route parameter. Here’s an example.

```
import { apiClient } from '@/api/client';  
import type { UpdateExpense } from '@server/db/schema';  
  
export async function updateExpense(id: string, input: UpdateExpense) {  
  const res = await apiClient.expenses[':id'].$patch({  
    param: { id },  
    json: input,  
  });  
  if (!res.ok) {  
    throw new Error('Failed to update expense');  
  }  
  const response = await res.json();  
  return response.data.expense;  
}
```

At this point:

* ✅ `apiClient.expenses.$post` is **fully typed**
* ✅ Request payload is validated **at runtime**
* ✅ Types are inferred **at compile time**
* ✅ Autocomplete and hover hints just work

## To Sum It Up

For me, using Hono was a very pleasant dev experience. The only hiccup I ran into at first was the wrong route chaining and `unknown` types — but now, after understanding the pattern, I won’t make that mistake again. And you won’t either! 😉

Another eye-opener was reusing inferred types for requests and responses. I was so used to manually creating interfaces, but with Hono + Zod + Drizzle, that’s no longer necessary. TypeScript just works and it let us focus on real problems instead of fighting with interfaces.

💬 **Have you tried Hono yet? I’d love to hear how your experience has been.**

## 📚 Useful Resources

Here are some great resources to help you go from 0 to hero with Hono, TypeScript, Drizzle, Zod, and more:

📖 **Official Hono Documentation**  
The best place to learn about routing, middleware, helpers, RPC, deployment targets, and Web‑Standard design.  
<https://hono.dev/>

🎥 **Go From Beginner to Advanced with Hono**  
A long-form walk‑through that shows how to build a full app from scratch using Hono. Perfect if you have a few hours and want a deep dive.  
<https://www.youtube.com/watch?v=jXyTIQOfTTk>

🎥 **Type‑Safe API with Hono, Zod, and OpenAPI**A deeper dive into real‑world API patterns with docs and validation.  
<https://www.youtube.com/watch?v=sNh9PoM9sUE>

### Was This Article Useful?

If this breakdown brought you clarity, here’s how you can show some love:

👏 Hit the clap button (yes, you can do it up to 50 times!)  
🧠 Follow me for more deep-dives on FE, productivity and engineering  
💬 Share your thoughts: What’s the first thing you’ll apply from this guide?  
📢 Spread the word — share this with your team or tag it on socials

Your support fuels more hands-on content like this.  
Thanks for reading, and keep building smarter!👋
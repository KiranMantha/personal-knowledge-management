---
title: "🧩 What is Multi-Zone in Next.js?"
url: https://medium.com/p/d8e5b88487bb
---

# 🧩 What is Multi-Zone in Next.js?

[Original](https://medium.com/p/d8e5b88487bb)

Member-only story

## Next.js

# 🧩 What is Multi-Zone in Next.js?

[![Vijayasekhar Deepak](https://miro.medium.com/v2/resize:fill:64:64/1*2CxnV3GcJL9DlVWWjuUp3A.jpeg)](https://vijayasekhar-deepak.medium.com/?source=post_page---byline--d8e5b88487bb---------------------------------------)

[Vijayasekhar Deepak](https://vijayasekhar-deepak.medium.com/?source=post_page---byline--d8e5b88487bb---------------------------------------)

4 min read

·

Jan 31, 2026

--

3

Listen

Share

More

> ***Not a Member? Read for FREE*** [***here***](https://tarzzotech.medium.com/d8e5b88487bb?sk=161ac00768014c0c2d48e721c190c7e3)***.***

Press enter or click to view image in full size

![]()

Recently, I was researching the Micro frontend implementation with Next.js 16, as after Next.js 15, they stopped the modular federation support for it. In their official documentation, they have introduced a concept called **Multi-Zone** to achieve Micro Frontend Architecture.

So I started working on an article on Micro Frontend implementation with Next.js. Instead of directly going into the implementation i thought of writing this article to understand **Multi-Zone** a little more.

## What is *Multi-Zone*?

**Multi-Zone** is a way to run **multiple independent Next.js applications** under a **single domain**, each handling a different part of the URL space.

Think of it as:

> ***One domain → multiple Next.js apps → seamless user experience***

**Example:**

```
example.com        → Main app  
example.com/blog   → Blog app (separate Next.js project)  
example.com/shop   → Shop app (another Next.js project)
```

Each of these is:

* Its **own repository**
* Its **own build & deployment**
* But appears as one site to users

This is extremely useful for:

* **Micro-frontend architecture**
* Large teams owning different parts of the site
* Gradual migration from monolith to modular apps

## 🏗 Architecture Concept

```
                 ┌────────────┐  
                 │  Reverse   │  
Browser ───────▶ │   Proxy    │───▶ Main Next.js App  
                 │ (Vercel /  │───▶ Blog Next.js App  
                 │  Nginx)    │───▶ Shop Next.js App  
                 └────────────┘
```

Routing is done at the **platform/proxy level**, not inside Next.js itself.

## 🔹 How Multi-Zone Works (High Level)

1. You create **multiple Next.js apps**
2. Each app owns a specific route prefix (`/blog`, `/docs`, etc.)
3. A proxy (Vercel rewrites, Nginx, Cloudflare, etc.) forwards requests to the correct app

Next.js itself doesn’t “know” it’s in a multi-zone setup — it just serves its own routes.

## 🔧 Example with Vercel

### 1️⃣ Folder Structure (Monorepo)

```
/apps  
  /main-site  
  /blog  
  /shop
```

Each is its own Next.js project.

### 2️⃣ Configure rewrites in the main project

`vercel.json` in the root:

```
{  
  "rewrites": [  
    { "source": "/blog/(.*)", "destination": "https://blog.example.com/$1" },  
    { "source": "/shop/(.*)", "destination": "https://shop.example.com/$1" }  
  ]  
}
```

Or route internally if deployed in the same Vercel project.

### 3️⃣ Configure each zone app

Each zone app (`blog`, `shop`) is a normal Next.js app:

```
npx create-next-app blog
```

With routes:

```
/blog/page.tsx  
/blog/[slug]/page.tsx
```

### 4️⃣ Result

Press enter or click to view image in full size

![]()

## 🧠 Why Use Multi-Zone?

Press enter or click to view image in full size

![]()

## ⚠️ Things to Watch Out For

Press enter or click to view image in full size

![]()

## 🆚 Multi-Zone vs Module Federation

Press enter or click to view image in full size

![]()

## When should you use it?

Since you:

* Are building **micro-frontends**
* Are using **Next.js 16**

👉 **Multi-Zone is a very clean solution** for:

* Separating domains of ownership
* Avoiding hydration conflicts
* Avoiding CSS bleed
* Avoiding runtime coupling

If you read this entire article, now you might have some understanding of what **Multi-Zone** is**.** In my next Articles i wll share the practical implementations with **Multi-Zone.** See you in my next articles.

## Thank You for Reading!

I hope you found it helpful and informative. If you have any questions or feedback, feel free to leave a comment below. Your support and engagement mean a lot to me.

![]()

If you enjoyed this article and would like to support my work, consider buying me a coffee. Your contributions help me to keep creating valuable content.

[![]()](https://www.buymeacoffee.com/vijaydeepak)

I appreciate your support. See you in the next blog!

## Happy Coding!
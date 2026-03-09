---
title: "The Rendering Guide Nobody Explains Properly — SSR, ISR, and CSR in Next.js"
url: https://medium.com/p/fee4b35e7a26
---

# The Rendering Guide Nobody Explains Properly — SSR, ISR, and CSR in Next.js

[Original](https://medium.com/p/fee4b35e7a26)

Member-only story

# The Rendering Guide Nobody Explains Properly — SSR, ISR, and CSR in Next.js

[![Ronik Dedhia](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*fhn1MGY7simNMtDx)](https://medium.com/@ronikdedhia?source=post_page---byline--fee4b35e7a26---------------------------------------)

[Ronik Dedhia](https://medium.com/@ronikdedhia?source=post_page---byline--fee4b35e7a26---------------------------------------)

9 min read

·

Dec 26, 2025

--

Listen

Share

More

Press enter or click to view image in full size

![]()

## Understanding when to use Server-Side Rendering, Incremental Static Regeneration, and Client-Side Rendering — and what breaks when you choose wrong

Next.js gives you three powerful rendering strategies: Server-Side Rendering (SSR), Incremental Static Regeneration (ISR), and Client-Side Rendering (CSR). Most tutorials explain *what* they are. Few explain *when* to use them and *what fails* when you don’t. I’ve made every mistake possible with Next.js rendering. Let me save you the pain.

## The Core Problem Next.js Solves

Traditional React apps render everything client-side:

1. Browser downloads empty HTML
2. Browser downloads JavaScript bundle (often 500KB+)
3. JavaScript executes and renders content
4. User finally sees something (3–5 seconds later)

This creates three problems:

* **SEO suffers**: Google sees empty HTML
* **Performance suffers**: Nothing renders until JavaScript loads
* **User experience suffers**: Blank screen, then sudden content flash

Next.js fixes this by rendering HTML on the server. But *when* and *how* you render matters enormously.

## Server-Side Rendering (SSR): Fresh Data, Every Request

HTML is generated on the server for **every request**. The user gets a fully rendered page immediately.

```
// app/dashboard/page.tsx  
import { prisma } from '@/lib/prisma'  
import { auth } from '@/lib/auth'  
export default async function DashboardPage() {  
  // This runs on the server, on EVERY request  
  const user = await auth.getUser()  
    
  const stats = await prisma.stats.findMany({  
    where: { userId: user.id },  
    orderBy: { date: 'desc' },  
    take: 10  
  })  
    
  return (  
    <div>  
      <h1>Welcome back, {user.name}</h1>  
      <StatsGrid stats={stats} />  
    </div>  
  )  
}
```

## When to Use SSR

**User-specific content**: Dashboards, profiles, personalized feeds   
**Frequently changing data**: Live scores, stock prices, real-time analytics **Authentication-required pages**: Admin panels, account settings   
**Dynamic URL parameters that affect content**: Product pages with user-specific pricing

## What to Watch Out For

**1. Performance Bottlenecks**

Every request hits your database. If your query is slow, users wait.

```
// BAD - Slow SSR  
export default async function SlowPage() {  
  // This query takes 2 seconds  
  const data = await prisma.post.findMany({  
    include: {  
      author: true,  
      comments: {  
        include: {  
          author: true,  
          replies: {  
            include: {  
              author: true  
            }  
          }  
        }  
      },  
      tags: true  
    }  
  })  
    
  return <PostList posts={data} />  
}  
  
// GOOD - Optimized SSR  
export default async function FastPage() {  
  // Only fetch what you need  
  const data = await prisma.post.findMany({  
    select: {  
      id: true,  
      title: true,  
      excerpt: true,  
      author: {  
        select: { name: true, avatar: true }  
      },  
      _count: {  
        select: { comments: true }  
      }  
    }  
  })  
    
  return <PostList posts={data} />  
}
```

**2. Caching Implications**

By default, Next.js 13+ caches everything aggressively. You need to opt out:

```
// Force fresh data on every request  
export const dynamic = 'force-dynamic'  
export default async function RealTimePage() {  
  const data = await fetchLiveData()  
  return <LiveDashboard data={data} />  
}
```

**3. Environment Variables**

Server components can access all environment variables. Be careful:

```
// DANGEROUS - Secret exposed in client bundle if this becomes a client component  
export default function Page() {  
  const apiKey = process.env.SECRET_API_KEY  
  return <div>{apiKey}</div>  
}  
// SAFE - Only accessible in server component  
export default async function Page() {  
  const data = await fetch('https://api.example.com', {  
    headers: {  
      Authorization: `Bearer ${process.env.SECRET_API_KEY}`  
    }  
  })  
  const result = await data.json()  
  return <Display data={result} />  
}
```

**4. Request Waterfalls**

Avoid sequential fetches:

```
// BAD - Takes 3 seconds  
export default async function SlowPage() {  
  const user = await fetchUser()  // 1 second  
  const posts = await fetchPosts(user.id)  // 1 second  
  const comments = await fetchComments(user.id)  // 1 second  
  return <Dashboard user={user} posts={posts} comments={comments} />  
}  
  
// GOOD - Takes 1 second (parallel)  
export default async function FastPage() {  
  const [user, posts, comments] = await Promise.all([  
    fetchUser(),  
    fetchPosts(userId),  
    fetchComments(userId)  
  ])  
  return <Dashboard user={user} posts={posts} comments={comments} />  
}
```

## Incremental Static Regeneration (ISR): Static + Fresh

Pages are generated at build time and cached. After a specified interval, Next.js regenerates the page in the background.

```
// app/blog/[slug]/page.tsx  
import { prisma } from '@/lib/prisma'  
export const revalidate = 3600 // Revalidate every hour  
export async function generateStaticParams() {  
  const posts = await prisma.post.findMany({  
    select: { slug: true }  
  })  
    
  return posts.map(post => ({  
    slug: post.slug  
  }))  
}  
export default async function BlogPost({   
  params   
}: {   
  params: { slug: string }   
}) {  
  const post = await prisma.post.findUnique({  
    where: { slug: params.slug },  
    include: {  
      author: true,  
      tags: true  
    }  
  })  
    
  return (  
    <article>  
      <h1>{post.title}</h1>  
      <div dangerouslySetInnerHTML={{ __html: post.content }} />  
    </article>  
  )  
}
```

## When to Use ISR

**Content sites**: Blogs, documentation, marketing pages   
**E-commerce product pages**: Stock changes occasionally, not every second **News sites**: Content updates periodically   
**Public profile pages**: User data changes infrequently

## What to Watch Out For

**1. Stale Data Window**

With `revalidate: 3600`, users might see data up to 1 hour old:  
If your product sells out at 2:30 PM, and revalidate happened at 2:00 PM,   
users will still see “In Stock” until 3:00 PM

```
export const revalidate = 60 // Reduce to 1 minute for critical data
```

**2. On-Demand Revalidation**

Use `revalidatePath()` to update immediately:

```
// app/api/revalidate/route.ts  
import { revalidatePath } from 'next/cache'  
import { NextRequest, NextResponse } from 'next/server'  
export async function POST(request: NextRequest) {  
  const { path } = await request.json()  
  // Verify secret to prevent abuse  
  const secret = request.headers.get('x-revalidate-secret')  
  if (secret !== process.env.REVALIDATE_SECRET) {  
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })  
  }  
  try {  
    revalidatePath(path)  
    return NextResponse.json({ revalidated: true })  
  } catch (error) {  
    return NextResponse.json({ error: 'Failed to revalidate' }, { status: 500 })  
  }  
}
```

Now when content updates:

```
// After updating a blog post  
await fetch('https://yoursite.com/api/revalidate', {  
  method: 'POST',  
  headers: {  
    'Content-Type': 'application/json',  
    'x-revalidate-secret': process.env.REVALIDATE_SECRET  
  },  
  body: JSON.stringify({ path: `/blog/${post.slug}` })  
})
```

**3. Build Time Considerations**

If you have 10,000 blog posts, generating all at build time is slow:

```
// BAD - Generates 10,000 pages at build time  
export async function generateStaticParams() {  
  const posts = await prisma.post.findMany()  // 10,000 posts  
  return posts.map(post => ({ slug: post.slug }))  
}  
  
// GOOD - Only generate popular posts, rest on-demand  
export async function generateStaticParams() {  
  const popularPosts = await prisma.post.findMany({  
    where: { views: { gt: 1000 } },  
    take: 100  // Top 100 posts  
  })  
  return popularPosts.map(post => ({ slug: post.slug }))  
}  
export const dynamicParams = true // Generate others on first request
```

**4. Memory Usage**

ISR pages stay in memory. Too many pages = high memory consumption:  
Monitor your Vercel function memory usage  
Consider SSR for very large datasets instead

## Client-Side Rendering (CSR): Interactive UI

The page shell renders on the server, but data fetching happens in the browser.

```
// app/dashboard/page.tsx  
import { StatsClient } from '@/components/StatsClient'  
export default function DashboardPage() {  
  // This HTML renders immediately  
  return (  
    <div>  
      <h1>Dashboard</h1>  
      <StatsClient />  {/* This fetches data client-side */}  
    </div>  
  )  
}
```

```
// components/StatsClient.tsx  
"use client"  
import { useEffect, useState } from 'react'  
export function StatsClient() {  
  const [stats, setStats] = useState(null)  
  const [loading, setLoading] = useState(true)  
    
  useEffect(() => {  
    fetch('/api/stats')  
      .then(res => res.json())  
      .then(data => {  
        setStats(data)  
        setLoading(false)  
      })  
  }, [])  
    
  if (loading) return <Skeleton />  
    
  return <StatsGrid stats={stats} />  
}
```

## When to Use CSR

**Highly interactive components**: Real-time charts, live feeds, collaborative editors   
**User-triggered data**: Search results, filtered lists, paginated data   
**Frequent updates**: Chat messages, notifications, live data   
**Non-critical content**: Comments, related items, recommendations

## What to Watch Out For

**1. SEO Impact**

Client-rendered content is invisible to search engines:

```
// BAD - Product details won't be indexed  
"use client"  
export default function ProductPage({ id }) {  
  const [product, setProduct] = useState(null)  
    
  useEffect(() => {  
    fetch(`/api/products/${id}`)  
      .then(res => res.json())  
      .then(setProduct)  
  }, [id])  
    
  return <ProductDisplay product={product} />  
}  
// GOOD - Server-render critical content, client-render interactive parts  
export default async function ProductPage({ params }) {  
  const product = await prisma.product.findUnique({  
    where: { id: params.id }  
  })  
    
  return (  
    <div>  
      <ProductDetails product={product} />  {/* Server rendered */}  
      <RelatedProducts productId={product.id} />  {/* Client rendered */}  
    </div>  
  )  
}
```

**2. Loading States**

Always handle loading and error states:

```
"use client"  
import { useQuery } from '@tanstack/react-query'  
export function DataDisplay() {  
  const { data, isLoading, error } = useQuery({  
    queryKey: ['data'],  
    queryFn: fetchData  
  })  
    
  if (isLoading) {  
    return <Skeleton />  
  }  
    
  if (error) {  
    return (  
      <div className="error">  
        <p>Failed to load data</p>  
        <button onClick={() => refetch()}>Retry</button>  
      </div>  
    )  
  }  
  return <Display data={data} />  
}
```

**3. Request Overhead**

Client-side fetching means extra network requests:

```
// BAD - 3 separate requests on page load  
"use client"  
export function Dashboard() {  
  const [user, setUser] = useState(null)  
  const [posts, setPosts] = useState([])  
  const [stats, setStats] = useState(null)  
    
  useEffect(() => {  
    fetch('/api/user').then(res => res.json()).then(setUser)  
    fetch('/api/posts').then(res => res.json()).then(setPosts)  
    fetch('/api/stats').then(res => res.json()).then(setStats)  
  }, [])  
}  
  
// GOOD - Single request with combined data  
export default async function Dashboard() {  
  const data = await fetch('/api/dashboard-data').then(r => r.json())  
    
  return (  
    <div>  
      <UserInfo user={data.user} />  
      <PostList posts={data.posts} />  
      <StatsWidget stats={data.stats} />  
    </div>  
  )  
}
```

**4. Hydration Mismatches**

Client state must match server HTML:

```
// BAD - Hydration error  
export default function Page() {  
  const randomNumber = Math.random()  // Different on server and client  
  return <div>{randomNumber}</div>  
}  
// GOOD - Use useEffect for client-only code  
"use client"  
export function Page() {  
  const [randomNumber, setRandomNumber] = useState(0)  
    
  useEffect(() => {  
    setRandomNumber(Math.random())  
  }, [])  
  return <div>{randomNumber}</div>  
}
```

## Choosing the Right Strategy: Decision Tree

```
Is the content user-specific or changes frequently?  
│  
├─ YES → Is real-time data critical?  
│   │  
│   ├─ YES → Use SSR (force-dynamic)  
│   │         Example: Stock ticker, live chat  
│   │  
│   └─ NO → Can you accept slightly stale data?  
│       │  
│       ├─ YES → Use ISR with short revalidation  
│       │         Example: Social media feed (60s revalidate)  
│       │  
│       └─ NO → Use SSR  
│                Example: Banking dashboard  
│  
└─ NO → Is SEO important?  
    │  
    ├─ YES → Use ISR with long revalidation  
    │         Example: Blog posts (3600s revalidate)  
    │  
    └─ NO → Is interactivity more important than initial load?  
        │  
        ├─ YES → Use CSR  
        │         Example: Admin dashboard charts  
        │  
        └─ NO → Use ISR  
                  Example: Documentation
```

## Real-World Example: E-commerce Product Page

```
// Perfect combination of all three strategies  
import { prisma } from '@/lib/prisma'  
import { ProductGallery } from '@/components/ProductGallery'  
import { RelatedProducts } from '@/components/RelatedProducts'  
import { ProductReviews } from '@/components/ProductReviews'  
import { AddToCart } from '@/components/AddToCart'  
// ISR: Revalidate every 5 minutes  
export const revalidate = 300  
export default async function ProductPage({   
  params   
}: {   
  params: { id: string }   
}) {  
  // SSR: Product details (ISR cached, revalidated every 5 min)  
  const product = await prisma.product.findUnique({  
    where: { id: params.id },  
    include: {  
      images: true,  
      category: true  
    }  
  })  
    
  return (  
    <div>  
      {/* Static: Product info for SEO */}  
      <h1>{product.name}</h1>  
      <p>{product.description}</p>  
      <span>${product.price}</span>  
        
      {/* Static: Image gallery */}  
      <ProductGallery images={product.images} />  
        
      {/* CSR: Shopping cart interaction */}  
      <AddToCart productId={product.id} />  
        
      {/* CSR: Load reviews lazily (not critical for SEO) */}  
      <ProductReviews productId={product.id} />  
        
      {/* CSR: Personalized recommendations */}  
      <RelatedProducts productId={product.id} />  
    </div>  
  )  
}
```

## Common Pitfalls and Solutions

## 1. Using Client Components Everywhere

```
// BAD - Everything client-side  
"use client"  
export default function Page() {  
  return (  
    <div>  
      <Header />  
      <Content />  
      <Footer />  
    </div>  
  )  
}  
// GOOD - Only interactive parts client-side  
export default function Page() {  
  return (  
    <div>  
      <Header />  {/* Server component */}  
      <InteractiveContent />  {/* Client component */}  
      <Footer />  {/* Server component */}  
    </div>  
  )  
}
```

## 2. Fetching in useEffect

```
// BAD - Race conditions, no caching  
"use client"  
export function BadComponent() {  
  const [data, setData] = useState(null)  
    
  useEffect(() => {  
    fetch('/api/data').then(r => r.json()).then(setData)  
  }, [])  
    
  return <Display data={data} />  
}  
// GOOD - Use React Query or SWR  
"use client"  
import { useQuery } from '@tanstack/react-query'  
export function GoodComponent() {  
  const { data } = useQuery({  
    queryKey: ['data'],  
    queryFn: () => fetch('/api/data').then(r => r.json())  
  })  
    
  return <Display data={data} />  
}
```

## 3. Ignoring Loading States

Users see blank screens. Always show skeletons or loading indicators.

## 4. Over-fetching Data

```
// BAD - Fetch entire object  
const user = await prisma.user.findUnique({  
  where: { id: userId }  
})  
// GOOD - Fetch only needed fields  
const user = await prisma.user.findUnique({  
  where: { id: userId },  
  select: {  
    id: true,  
    name: true,  
    email: true  
  }  
})
```

## Best Practices Summary

**SSR:**

* Use parallel data fetching
* Add appropriate caching headers
* Optimize database queries
* Set `export const dynamic = 'force-dynamic'` when needed

**ISR:**

* Choose appropriate revalidation intervals
* Implement on-demand revalidation
* Generate only popular pages at build time
* Monitor memory usage

**CSR:**

* Always handle loading and error states
* Use data fetching libraries (React Query, SWR)
* Avoid for SEO-critical content
* Implement proper error boundaries

## Conclusion

Next.js rendering strategies aren’t about picking one. They’re about using the right tool for each part of your application:

* **SSR** for personal, frequently changing data
* **ISR** for public, occasionally changing content
* **CSR** for interactions and non-critical data

Master this, and your Next.js apps will be fast, SEO-friendly, and maintainable.

The framework gives you the tools. Understanding when to use them is what separates good developers from great ones.

**What rendering strategy do you use most? What challenges have you faced? Share below.**

*Building with Next.js? I’d love to hear about your architecture decisions.*
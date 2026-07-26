---
title: "Taming Supabase & Next.js Auth: Why Your Users Keep Getting Logged Out (And How to Fix It)"
url: https://medium.com/p/ff858efdced5
---

# Taming Supabase & Next.js Auth: Why Your Users Keep Getting Logged Out (And How to Fix It)

[Original](https://medium.com/p/ff858efdced5)

# Taming Supabase & Next.js Auth: Why Your Users Keep Getting Logged Out (And How to Fix It)

[![Daniru Perera](https://miro.medium.com/v2/resize:fill:64:64/1*VduXvp83peS6hqk_5Fdicg@2x.jpeg)](https://danirudp.medium.com/?source=post_page---byline--ff858efdced5---------------------------------------)

[Daniru Perera](https://danirudp.medium.com/?source=post_page---byline--ff858efdced5---------------------------------------)

5 min read

·

May 20, 2026

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dff858efdced5&operation=register&redirect=https%3A%2F%2Fjavascript.plainenglish.io%2Ffix-nextjs-supabase-auth-logouts-ff858efdced5&source=---header_actions--ff858efdced5---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

When I step into an existing Next.js project for a codebase rescue, the most common and most expensive failure point I see isn’t state management or database schemas.

It’s the authentication layer.

Here is the exact scenario: A startup launches their Next.js (App Router) application backed by Supabase. Everything works perfectly on localhost. But in production, the cracks start to show. Users report being randomly logged out after a few hours. The UI says they are a guest, but if they hit refresh, they are magically logged back in. Sometimes, clicking a protected link bounces them to the login screen, only to redirect them right back.

Startups bleed active users when this happens. Authentication issues destroy trust faster than any other bug.

If this sounds familiar, you aren’t dealing with a failing database; you are dealing with a **race condition between the Edge, the Server, and the Client**.

Here is exactly why your Next.js and Supabase session is dropping, and the production-grade patch to fix it.

## The Root Cause: The Three-Headed Auth Monster

In the old days of React, auth was simple: you grabbed a JWT, stuck it in `localStorage`, and called it a day.

With the Next.js App Router, your application is split across three entirely different environments:

1. **The Middleware (Edge):** Runs before a request is completed.
2. **Server Components (Node.js):** Render on the server and have zero access to the browser.
3. **Client Components (Browser):** Run on the user’s device.

Supabase handles authentication using secure, HTTP-only cookies. The session desync happens because Next.js Server Components aggressively cache data, and Client Components don’t automatically know when the Middleware has refreshed a stale auth cookie.

When an access token expires, Supabase uses a refresh token to get a new one. If your Middleware updates the cookie, but your Client Component is still holding onto the old state, your app panics and logs the user out.

Let’s patch the system, layer by layer, using the modern `@supabase/ssr` package.

## Patch 1: The Middleware Trap (Fixing the Edge)

The biggest mistake developers make is treating the Next.js `middleware.ts` file as just a router guard. When using Supabase, your middleware has a much more critical job: **silently refreshing expired sessions.**

If you don’t explicitly pass the updated cookies from the Supabase client back to the Next.js response, the new session dies at the Edge, and the user gets logged out on their next click.

Here is the bulletproof middleware setup:

```
// middleware.ts  
import { createServerClient } from '@supabase/ssr'  
import { NextResponse, type NextRequest } from 'next/server'  
  
export async function middleware(request: NextRequest) {  
  // Create an unmodified response  
  let supabaseResponse = NextResponse.next({  
    request,  
  })  
  
  const supabase = createServerClient(  
    process.env.NEXT_PUBLIC_SUPABASE_URL!,  
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,  
    {  
      cookies: {  
        getAll() {  
          return request.cookies.getAll()  
        },  
        setAll(cookiesToSet) {  
          // 1. Update the request cookies  
          cookiesToSet.forEach(({ name, value }) => request.cookies.set(name, value))  
          // 2. Update the response cookies  
          supabaseResponse = NextResponse.next({  
            request,  
          })  
          cookiesToSet.forEach(({ name, value, options }) =>  
            supabaseResponse.cookies.set(name, value, options)  
          )  
        },  
      },  
    }  
  )  
  
  // IMPORTANT: You MUST call getUser() to trigger the token refresh  
  const { data: { user } } = await supabase.auth.getUser()  
  
  // Protect routes based on user presence  
  if (!user && request.nextUrl.pathname.startsWith('/dashboard')) {  
    const url = request.nextUrl.clone()  
    url.pathname = '/login'  
    return NextResponse.redirect(url)  
  }  
  
  return supabaseResponse  
}  
  
export const config = {  
  matcher: [  
    /*  
     * Match all request paths except for the ones starting with:  
     * - _next/static (static files)  
     * - _next/image (image optimization files)  
     * - favicon.ico (favicon file)  
     * Feel free to modify this pattern to include more paths.  
     */  
    '/((?!_next/static|_next/image|favicon.ico|.*\\.(?:svg|png|jpg|jpeg|gif|webp)$).*)',  
  ],  
}
```

**Why this works:** When `supabase.auth.getUser()` detects an expired access token, it uses the refresh token to get a new one. The `setAll` method immediately intercepts those new cookies and attaches them to `supabaseResponse`. The session survives.

## Patch 2: Client-Side Desync (The UI Glitch)

Your server is now keeping the token alive, but your Client Components are still clueless.

Imagine a user leaves their dashboard open in a tab for three hours. The token expires. They click a button that triggers a Server Action. The Server Action fails because the browser hasn’t refreshed the session.

To fix this, we need a global Client Component that listens to Supabase’s auth state changes and forces the Next.js App Router to re-evaluate the page data when a session shifts.

Create an `AuthProvider` and wrap it around your `app/layout.tsx` children.

```
// components/AuthProvider.tsx  
'use client'  
  
import { createBrowserClient } from '@supabase/ssr'  
import { useRouter } from 'next/navigation'  
import { useEffect, useState } from 'react'  
  
export default function AuthProvider({ children }: { children: React.ReactNode }) {  
  const router = useRouter()  
  const [supabase] = useState(() =>   
    createBrowserClient(  
      process.env.NEXT_PUBLIC_SUPABASE_URL!,  
      process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!  
    )  
  )  
  
  useEffect(() => {  
    const {  
      data: { subscription },  
    } = supabase.auth.onAuthStateChange((event, session) => {  
      if (event === 'SIGNED_OUT') {  
        router.refresh()  
        router.push('/login')  
      } else if (event === 'SIGNED_IN' || event === 'TOKEN_REFRESHED') {  
        // Force Next.js to re-fetch Server Components with the new token  
        router.refresh()  
      }  
    })  
  
    return () => {  
      subscription.unsubscribe()  
    }  
  }, [router, supabase])  
  
  return <>{children}</>  
}
```

**Why this works:** The `onAuthStateChange` listener acts as the bridge between Supabase and Next.js. Whenever Supabase detects a token refresh in the background, we fire `router.refresh()`. This tells the Next.js router: *"Hey, the cookies just changed. Re-run your Server Components so the UI reflects the actual server state."* No more stale UI. No more "ghost" logouts.

## Patch 3: The Server Action Cache Trap

Finally, if you are mutating data with Server Actions, you have to be ruthless with Next.js caching.

If a user logs out via a Server Action, but you forget to revalidate the cache, Next.js will serve a cached, authenticated version of the layout to an unauthenticated user until the cache expires. This looks like a massive security flaw to the user.

Always call `revalidatePath` when modifying auth state on the server:

```
// actions/auth.ts  
'use server'  
  
import { createServerClient } from '@supabase/ssr'  
import { cookies } from 'next/headers'  
import { revalidatePath } from 'next/cache'  
import { redirect } from 'next/navigation'  
  
export async function signOut() {  
  const cookieStore = cookies()  
  const supabase = createServerClient(  
    process.env.NEXT_PUBLIC_SUPABASE_URL!,  
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!,  
    {  
      cookies: {  
        getAll() { return cookieStore.getAll() },  
        setAll() { /* Handled securely on the server */ },  
      },  
    }  
  )  
  
  await supabase.auth.signOut()  
    
  // Nuke the cache for the entire layout  
  revalidatePath('/', 'layout')  
  redirect('/login')  
}
```

## The Reality of Architecture

Most tutorials end at the “Hello World” login screen. But when you are building enterprise-grade applications, the “happy path” isn’t enough. You have to architect for the edge cases: stale tabs, expired tokens, and aggressive server caching.

By properly configuring your Edge Middleware to refresh tokens, and wiring a global listener to force router refreshes on the client, you completely eliminate the desync that causes random logouts. Your app stops bleeding users, and your architecture becomes truly production-ready.

**Need help with your application?**

I am a Front-End Developer specializing in codebase rescues and complex integrations. If your Next.js UI isn’t communicating with your backend, your Supabase/NextAuth implementation is failing, or your project is stalled out, I can help.

I don’t upsell complete rewrites. I dive into existing repositories, diagnose the failing components, patch the root cause, and get your app moving again.

📩 **Available for freelance contracts.** Let’s get your app running perfectly today. 🔗 **Connect:** [**[LinkedIn]**](https://linkedin.com/in/daniru-perera) | [**[Portfolio]**](https://www.daniruperera.dev/) | [**[Upwork]**](https://www.upwork.com/freelancers/~01fdb8ecdfac6205e7)
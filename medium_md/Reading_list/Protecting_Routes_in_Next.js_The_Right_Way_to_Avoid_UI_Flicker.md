---
title: "Protecting Routes in Next.js: The Right Way to Avoid UI Flicker"
url: https://medium.com/p/f90934947b0c
---

# Protecting Routes in Next.js: The Right Way to Avoid UI Flicker

[Original](https://medium.com/p/f90934947b0c)

# Protecting Routes in Next.js: The Right Way to Avoid UI Flicker

[![Joshua Akintemi](https://miro.medium.com/v2/resize:fill:64:64/1*wms0G1mgbIZ7QSyH0deEGA.webp)](/@jakintemi?source=post_page---byline--f90934947b0c---------------------------------------)

[Joshua Akintemi](/@jakintemi?source=post_page---byline--f90934947b0c---------------------------------------)

3 min read

·

Feb 18, 2026

--

1

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Df90934947b0c&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40jakintemi%2Fprotecting-routes-in-next-js-the-right-way-to-avoid-ui-flicker-f90934947b0c&source=---header_actions--f90934947b0c---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

I want to share something that humbled me recently.

It’s one of those bugs you may not notice during development. Everything *looks* fine. Your redirect works. Your auth logic works. Your dashboard is “protected.”

Until production reminds you that “working” and “secure” are not always the same thing

If you are using **Next.js App Router**, this is something you absolutely need to understand.

## The Mistake Most people Make

A very common pattern for protecting routes looks like this:

```
// ❌ Insecure: Renders content BEFORE redirecting  
export default function Dashboard({ user }) {  
  const router = useRouter();  
  
  useEffect(() => {  
    if (!user) router.push('/login');  
  }, [user]);  
  
  return <AdminPanel />;  
}
```

At first glance, this feels correct.

* If there’s no user → redirect to `/login`
* If there’s a user → show the dashboard

Simple, right?

Not exactly.

## What is Actually Happening?

Here is the subtle issue:

`useEffect` runs **after the component renders**.

That means:

1. The page renders.
2. `<AdminPanel />` gets sent to the browser.
3. Then `useEffect` runs.
4. Then the redirect happens.

That tiny moment before the redirect, Your protected UI is visible.

Maybe just for a split second. Maybe barely noticeable. But it’s there.

And if it’s visible, it can potentially be captured, scraped, or inspected.

That tiny flash?  
That’s your Admin Panel leaking before redirect ⚠️

## The Production Humbling Moment

In development, you might never notice this because

Local builds are fast.  
Your machine is fast.  
The redirect feels instant.

But in production:

* Slower devices
* Slower networks
* Real users

Suddenly that “instant” redirect becomes a visible flash.

And that is when you realize client-side redirects are not protection - they are just navigation.

## The Safer Approach (App Router Way)

With the Next.js App Router, there’s a better way.

Instead of redirecting after render, you abort rendering entirely using `redirect()`.

```
import { redirect } from 'next/navigation';  
  
// ✅ Secure: Aborts rendering immediately  
export default async function Dashboard({ user }) {  
  if (!user) {  
    redirect('/login'); // Stops execution here  
  }  
  
  return <AdminPanel />; // Never sent if user is missing  
}
```

What is different here?

* This runs on the server.
* If there’s no user, `redirect()` throws and stops execution.
* The component never renders.
* The HTML for `<AdminPanel />` is never sent to the browser.

No flash.  
No leak.  
No risk.

## Why This Matters

In client-side React apps, we’re used to thinking:

> *“If I redirect, I’ve protected the route.”*

But in modern frameworks like Next.js, especially with Server Components and the App Router, we have stronger tools.

Security should happen **before rendering**, not after.

Redirecting inside `useEffect` is like locking the door after the visitor already stepped inside.

## The Bigger Lesson

This isn’t just about Next.js.

It’s about understanding *where* your code runs:

* Client-side logic controls UX.
* Server-side logic controls access.

If something must not be seen, even for a millisecond, don’t rely on client-side effects to protect it.

## Final Thoughts

This is one of those small details you may not notice…

If you are working with Next.js App Router, make sure you are handling authentication **before render** using `redirect()`.

Your future self (and your security posture) will thank you.

Have you ever faced something like this - where everything looked correct until production exposed the flaw?
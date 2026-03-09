---
title: "Why I Stopped Using CSS Box-Shadow — It Slows Your Page by Up to 70%"
url: https://medium.com/p/5e78513b5447
---

# Why I Stopped Using CSS Box-Shadow — It Slows Your Page by Up to 70%

[Original](https://medium.com/p/5e78513b5447)

Member-only story

# Why I Stopped Using CSS Box-Shadow — It Slows Your Page by Up to 70%

## And what to use instead

[![Arnold Gunter](https://miro.medium.com/v2/resize:fill:64:64/1*TAhisa8nN_coYYb4QZuehw.jpeg)](/@arnoldgunter?source=post_page---byline--5e78513b5447---------------------------------------)

[Arnold Gunter](/@arnoldgunter?source=post_page---byline--5e78513b5447---------------------------------------)

4 min read

·

Aug 1, 2025

--

13

Listen

Share

More

Press enter or click to view image in full size

![Minimal scene lll]()

Not a member? [Read it here for free.](/@arnoldgunter/5e78513b5447?sk=4f635b54f9114e78caddf081ea23d0d6)

At least three times a week, I open the Leonardo AI website to generate images. And to be honest, their UI is a feast for the eyes.

Until you try to scroll or open a modal — suddenly, even your computer starts slowing down.

I noticed this phenomenon on a few other sites as well, and what they all had in common was the heavy use of `box-shadow`.

Naturally, I opened DevTools.

What I found was a CSS jungle of shadows. Big shadows. Multiple shadows per element. Shadows inside shadows. The CPU was working harder than a barista during a morning rush!

That’s when I knew: it was time to break up with `box-shadow`.

> **💌 Want more tips like this every week?**  
> I send out a free, no-fluff web dev newsletter packed with frontend dev tips, HTML/CSS/JS tricks, and copy-paste code snippets.
>
> [Join 370+ developers and get smarter every week!](https://arnold-gunter.kit.com/f34239fd44)

## Why Box-Shadow Is the Performance Killer

Let’s be clear: using `box-shadow` is not a crime.

But it is **computationally expensive**, especially when:

* You use **large blur radii** (anything over 20px starts getting spicy).
* You apply shadows to **dozens or hundreds of elements**.
* You animate them (which triggers repaint and layout recalculations).
* You’re targeting **mobile devices**, where GPU/CPU power is limited.

## Here’s what happens under the hood

When you apply `box-shadow`, especially with blur, you're not just adding a visual effect — you're triggering a series of heavy paint and raster operations that can significantly impact performance, especially on mobile and lower-end devices.

1. **Rasterization**: The browser rasterizes the element into a bitmap during the paint phase — this includes the shadow region, which often expands well beyond the element’s bounds.
2. **Blur Calculation**: If the shadow includes a blur (which most do), the browser runs a **convolution algorithm** (like Gaussian blur) over the shadow area. This is expensive because:  
   The blur radius grows **quadratically** — a `30px` blur affects a `60x60` pixel area per element. Each affected pixel samples from a large neighborhood, leading to **thousands of calculations**.
3. **Compositing**: The shadow is blended behind the element using alpha blending. This isn’t hardware-accelerated unless the element is promoted to a **compositing layer** (e.g., via `will-change`), which itself consumes GPU memory.

* **No Caching if Animated**: If you animate or change the `box-shadow` (like on hover), the browser **must repaint** the element every frame — including recalculating the blur and redrawing the entire visual layer.
* **Multiplied Cost**: On scroll or hover, if you have 50+ elements with shadows, this overhead **multiplies across the viewport**, leading to frame drops, jank, and high CPU/GPU usage.

> **Bottom line:** `box-shadow` isn’t just “one more style.” It’s a paint-time blur operation that doesn’t scale well — and when used heavily or dynamically, it can quietly wreck performance without showing up as obvious JavaScript bottlenecks.

## Real-World Data

When I profiled Leonardo AI’s website on my mid-range laptop using Chrome’s Performance tab, the results were eye-opening:

* **First Contentful Paint (FCP):** 2.6 seconds
* **Largest Contentful Paint (LCP):** 4.1 seconds
* **Frame rate during scroll:** dropped below **30 FPS**, resulting in noticeable stutter
* **CPU usage:** hovered around **90%**, just from scrolling through a grid of elements
* **Interaction delays:** clicks and modals felt laggy and unresponsive

After replacing those shadows with more performance-friendly alternatives — subtle `border-bottom`s, blurred pseudo-elements, and GPU-accelerated transforms — the performance metrics drastically improved:

* **LCP:** dropped to **1.7 seconds**
* **Time to Interactive (TTI):** improved by over **60%**
* **Frame rate:** stabilized at a consistent **60 FPS**
* **CPU usage:** dropped by nearly half during scroll and hover states

> Same layout. Same content. Same styling intent.  
> The only thing that changed? **We stopped using** `box-shadow.`

## So What Can You Do Instead?

You don’t have to throw out the aesthetic. But you can trade brute force for smarter techniques:

### 1. Use Borders

If you’re just trying to separate a card from the background, borders work surprisingly well:

```
.card {  
  border: 1px solid rgba(0, 0, 0, 0.05);  
  border-bottom-color: rgba(0, 0, 0, 0.15);  
}
```

**Pros**: Cheap. Easy to override. No GPU stress.

**Cons**: Not as soft or immersive as real shadows.

### 2.Gradients and Blurs

```
.card::after {  
  content: '';  
  position: absolute;  
  bottom: -4px;  
  left: 4px;  
  right: 4px;  
  height: 6px;  
  background: linear-gradient(to bottom, rgba(0, 0, 0, 0.2), transparent);  
  filter: blur(2px);  
}
```

**Pros**: Looks like a shadow. Doesn’t trigger expensive layout or repaints.

**Cons**: Requires absolute positioning and pseudo-elements.

### 3. Use `transform` Instead of Animating Box-Shadow

```
.card {  
  box-shadow: 0 10px 25px rgba(0,0,0,0.2); /* static */  
  transition: transform 0.3s ease;  
}  
  
.card:hover {  
  transform: translateY(-4px);  
}
```

**Pros**: `transform` is GPU-accelerated.

**Cons**: Doesn’t actually change the shadow, only the element’s position — but the illusion is usually good enough.

### 4. If You Must Animate Shadow: Use `will-change` Carefully

```
.card {  
  will-change: box-shadow;  
}
```

This tells the browser: “Hey, I’m about to do something heavy, please prepare accordingly.”

But keep in mind: leaving `will-change` on everything is like hoarding GPU memory. Please clean it up after transitions finish.

## TL;DR

I still think `box-shadow` is one of the most visually satisfying CSS properties.

But when you care about performance — especially for users on mobile, low-end hardware, or inside apps with high UI density — shadows need to earn their place.

Use shadows, but don’t abuse them.

Sometimes, the best shadow is just smart lighting — not an overloaded blur on every block.

**Happy coding!**

> **💌 Want more tips like this every week?**  
> I send out a free, no-fluff web dev newsletter packed with frontend dev tips, HTML/CSS/JS tricks, and copy-paste code snippets.
>
> [Join 370+ developers and get smarter every week!](https://arnold-gunter.kit.com/f34239fd44)
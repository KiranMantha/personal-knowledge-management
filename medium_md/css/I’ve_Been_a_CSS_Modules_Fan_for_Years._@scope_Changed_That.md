---
title: "I’ve Been a CSS Modules Fan for Years. @scope Changed That"
url: https://medium.com/p/d1f476224c07
---

# I’ve Been a CSS Modules Fan for Years. @scope Changed That

[Original](https://medium.com/p/d1f476224c07)

# I’ve Been a CSS Modules Fan for Years. @scope Changed That

## A practical comparison of two approaches to scoped CSS — and why the native solution might finally be ready to challenge the tool I love

[![Martin Metodiev • Mev](https://miro.medium.com/v2/resize:fill:64:64/1*0O1ukuNrG8Z3sdDpd-eLDA.jpeg)](/@mevbg?source=post_page---byline--d1f476224c07---------------------------------------)

[Martin Metodiev • Mev](/@mevbg?source=post_page---byline--d1f476224c07---------------------------------------)

7 min read

·

Mar 28, 2026

--

2

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd1f476224c07&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40mevbg%2Five-been-a-css-modules-fan-for-years-scope-changed-that-d1f476224c07&source=---header_actions--d1f476224c07---------------------post_audio_button------------------)

Share

Press enter or click to view image in full size

![]()

I want to be honest with you from the start: I like [*CSS Modules*](https://github.com/css-modules/css-modules). A lot. It has been my go-to solution for component-scoped styles for years, and I have recommended it to almost every team I have worked with. So when I started hearing more and more about the native CSS **@scope** rule, my first reaction was skepticism.

But I decided to dig in properly. I read the specs, the browser release notes, the developer discussions. And what I found changed my perspective — not completely, but enough to write this article.

This is not a *“CSS Modules is dead”* piece. It is a genuine comparison between two tools that solve the same problem in very different ways. My goal is to help you understand both well enough to make your own decision.

## The Problem Both Are Trying to Solve

CSS is global by nature. When you write `.title { font-size: 2rem; }`, that rule applies everywhere in your page — inside your card component, inside your footer, inside your modal. It does not care about component boundaries. It just cascades.

This has been a headache for front-end developers since the very beginning. The bigger the project, the worse it gets. You end up with an ever-growing list of workarounds: longer class names, deeper selectors, more `!important` than you are proud of.

*CSS Modules* and *CSS @scope* both try to solve this. But they come from very different directions.

## How CSS Modules Works

*CSS Modules* is a build-time solution. When you write a *.module.css* file, your build tool (Webpack, Vite, or another bundler) transforms every class name into a unique, hashed identifier. So `.title` in your file becomes something like `.title_x5j2l` in the final HTML.

Because every class name is unique, styles cannot leak from one component to another. The scoping is guaranteed not by the browser, but by your build process.

```
/* Button.module.css */  
.button {  
  background: blue;  
  color: white;  
}
```

```
import styles from ‘./Button.module.css’;  
  
function Button() {  
  return <button className={styles.button}>Click me</button>;  
}
```

The result in the browser might look like `<button class="button_a7f3k">`. Clean isolation, zero risk of collision.

## How CSS @scope Works

CSS `@scope` is a browser-native solution. No build step. No hashing. You tell the browser: *“apply these styles only inside this specific part of the DOM”.*

```
@scope (.card) {  
  .title {  
    font-size: 1.5rem;  
    font-weight: 700;  
  }  
}
```

Any `.title` element inside `.card` gets those styles. Any `.title` outside stays untouched. The browser handles everything at runtime, based on the DOM structure.

You can also define where the scope ends — something *CSS Modules* simply cannot do:

```
@scope (.card) to (.user-bio) {  
  p {  
    color: #555;  
  }  
}
```

This is called the *“donut pattern”*. Styles apply inside `.card`, but stop before they reach `.user-bio`. You get a hole in the middle of your scope — like a donut.

## Similarities: More Than You Might Think

Both tools share the same core goal: **preventing style leakage between components**. Beyond that, they have more in common than it first appears.

Both allow you to write simple, readable selectors inside a defined boundary. With *CSS Modules*, that boundary is the file. With `@scope`, that boundary is a DOM subtree. In both cases, you write `.title` instead of `.card__title — large`.

Both reduce specificity wars. *CSS Modules* eliminates them through uniqueness. `@scope` reduces them through proximity — the closest scope wins, not the most specific selector.

And both make large codebases easier to reason about. When you know that styles are contained, you can refactor with more confidence.

## Key Differences: Where They Diverge

This is where things get interesting.

### Build Step vs. Native Browser

*CSS Modules* requires a build pipeline. If you are already using Vite or Webpack for a React project, this is no problem at all — it just works. But if you are building something simpler, a static site, a small vanilla JS project, or a Web Component, adding a bundler just for scoped CSS is a heavy price to pay.

`@scope` needs nothing. It is just CSS. You write it in a `<style>` tag or a `.css` file, and the browser understands it.

### Readability in DevTools

One of my personal frustrations with *CSS Modules* has always been debugging. When I open DevTools and inspect an element, I see `.button_x5j2l`. That hashed class tells me nothing about where it comes from without going back to my source files. It makes live debugging slower and more frustrating.

With `@scope`, the class names stay exactly as you wrote them. You see `.title` inside `.card`, and it all makes sense immediately in the browser.

DOM Awareness

*CSS Modules* is file-based. The scoping does not know or care about the DOM structure — it just generates unique names. This means you cannot express rules like “apply this style inside `.card` but not inside `.user-bio`”. The boundary is fixed at the file level.

`@scope` is DOM-aware. It understands parent-child relationships, nesting, and proximity. This is a fundamentally more powerful model for component-based styling.

### Proximity-Based Resolution

This is the feature of `@scope` that surprised me the most. In traditional CSS, when two rules target the same element, the one with higher specificity wins. If they have equal specificity, the one declared last wins. Proximity to the element in the DOM does not matter at all.

With `@scope`, that changes. If two scopes both match the same element, the **closer** scope wins — regardless of source order or specificity. This maps much more naturally to how we think about component hierarchies.

### Framework Dependency

*CSS Modules* works great with React, and it is well-integrated with the major bundlers. But it is essentially a framework-ecosystem tool. You are unlikely to use it in a plain HTML project.

`@scope` works everywhere. It works in Astro, Svelte, React, vanilla HTML, or any combination. It is a CSS feature, not a JavaScript ecosystem tool.

## Advantages and Disadvantages Side by Side

### **CSS Modules strengths:**

* Rock-solid isolation — the scoping is guaranteed by build output, not runtime behavior
* Mature tooling with excellent TypeScript support
* Works extremely well in large React codebases
* No risk of class name collision whatsoever

### **CSS Modules weaknesses:**

* Requires a build step
* Hashed class names make DevTools debugging painful
* Cannot express “scope with exceptions” (no donut pattern)
* Not DOM-aware — purely file-based scoping

### **CSS @scope strengths:**

* Zero build tooling required
* Readable class names everywhere, including DevTools
* DOM-aware — supports proximity resolution and donut scoping
* Works in any project, any framework, any context
* Lower specificity footprint — easier to override when needed

### **CSS @scope weaknesses:**

* Newer — many developers are still unfamiliar with it
* No TypeScript type checking for scoped class names
* Does not prevent someone from accidentally writing global styles that override your scope
* Requires conscious discipline — the isolation is not enforced by a build tool

## Architecture and Real-World Usage

In a *CSS Modules* workflow, scoping is enforced automatically. You do not have to think about it — the build process guarantees it. This is valuable in large teams where not everyone has the same level of CSS expertise.

With `@scope`, you are working with the cascade, not against it. The browser resolves conflicts by proximity, which means your component hierarchy in the DOM directly reflects how styles are resolved. This is elegant and powerful, but it does require that your team understands how `@scope` works.

The inline `<style>` scoping is particularly interesting for certain architectures:

```
<article>  
  <style>  
    @scope {  
      h2 { color: var(--brand-color); }  
      p  { line-height: 1.7; }  
    }  
  </style>  
  <h2>This heading is scoped automatically</h2>  
  <p>So is this paragraph.</p>  
</article>
```

When you write `@scope` without arguments inside a `<style>` tag, it automatically scopes to the parent element. No class needed. This is a genuinely new way of thinking about co-located styles.

## When Should You Choose One Over the Other?

### Choose **CSS Modules** if:

* You are already in a React + Vite or Webpack project and *CSS Modules* is working well for you
* Your team is large and you need the build tool to enforce isolation automatically
* You want TypeScript support for your class names
* You are not ready to introduce a newer CSS feature yet

### Choose **CSS @scope** if:

* You are starting a new project, especially one using Astro, Svelte, or vanilla HTML
* You want to reduce tooling complexity
* You value readable class names in DevTools
* You need the donut pattern or proximity-based style resolution
* You are working on a design system or component library that should be framework-agnostic

## Conclusion: A Different Tool, Not a Better One

Coming into this research as a *CSS Modules* enthusiast, I was prepared to find `@scope` underwhelming. I did not.

`@scope` solves the same core problem in a way that is, in many respects, more elegant and more powerful. The donut pattern, proximity resolution, and zero build-step requirement are genuine improvements on what *CSS Modules* can offer. The DevTools experience alone is something I have wanted for years.

But *CSS Modules* is not going anywhere. For large React applications with mature build pipelines, it remains an excellent choice. The automatic, build-enforced isolation is a real advantage in teams where consistency matters more than flexibility.

What I take away from this comparison is that `@scope` is finally a first-class alternative — not a replacement, but a genuine option. The fact that it reached **Baseline status in July 2024** and is now safe to use in production without any polyfill means the decision is no longer hypothetical.

If you are starting something new today, I would encourage you to try `@scope` first. You might find, as I did, that the browser has caught up to the problem we have been solving with build tools for a decade.
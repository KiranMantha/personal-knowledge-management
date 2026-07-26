---
title: "How To Hydrate A Server-Side Rendered Web Component"
url: https://medium.com/p/2e795651e07c
---

# How To Hydrate A Server-Side Rendered Web Component

[Original](https://medium.com/p/2e795651e07c)

Member-only story

# How To Hydrate A Server-Side Rendered Web Component

[![Danny Moerkerke](https://miro.medium.com/v2/resize:fill:64:64/1*LNE7VNHhYk__VDTzO8InnA.jpeg)](https://medium.com/@dannymoerkerke?source=post_page---byline--2e795651e07c---------------------------------------)

[Danny Moerkerke](https://medium.com/@dannymoerkerke?source=post_page---byline--2e795651e07c---------------------------------------)

12 min read

·

May 11, 2023

--

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D2e795651e07c&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fhow-to-hydrate-a-server-side-rendered-web-component-2e795651e07c&source=---header_actions--2e795651e07c---------------------post_audio_button------------------)

Share

An in-depth guide to lazy loading Web Components

Press enter or click to view image in full size

![]()

*In part 1 of this series I explain you* [*how to server-side render a Web Component*](/how-to-server-side-render-a-web-component-770cd25efb6f)*.*

## Hydration

Declarative Shadow DOM enables us to attach a Shadow root to a Custom Element and fully render it without any JavaScript. This is a *huge* step for web components since they can now be rendered on the server. But there is a slight problem though.

Our component doesn’t *do* anything, it’s not interactive.

Even worse, *it’s not even a Custom Element!*

If you check the server-side rendered components from [my previous article](/how-to-server-side-render-a-web-component-770cd25efb6f) in the browser’s dev tools you will notice they all have a Shadow root attached to it. But when you check the `CustomElementsRegistry` to find the `constructor` of the element:

```
const el = await customElements.get('my-element');  
  
console.log(el) // undefined 😱
```

you will notice that it hasn’t even been registered as a Custom Element.

This is an important fact to realise about Declarative Shadow DOM: *it only attaches a Shadow root to an element*.

In other words, it only takes care of rendering the HTML of the component and nothing else. The benefit of this approach is that it…
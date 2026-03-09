---
title: "JavaScript Sanitizer API: The Modern Way to Safe DOM Manipulation"
url: https://medium.com/p/828d5ea7dca6
---

# JavaScript Sanitizer API: The Modern Way to Safe DOM Manipulation

[Original](https://medium.com/p/828d5ea7dca6)

# JavaScript Sanitizer API: The Modern Way to Safe DOM Manipulation

## How to use sanitizer API to render HTML strings securely

[![Piumi Liyana Gunawardhana](https://miro.medium.com/v2/resize:fill:64:64/1*ey_8dtAaqyUTvbgmnPfAJw.jpeg)](https://piumi-16.medium.com/?source=post_page---byline--828d5ea7dca6---------------------------------------)

[Piumi Liyana Gunawardhana](https://piumi-16.medium.com/?source=post_page---byline--828d5ea7dca6---------------------------------------)

5 min read

·

Nov 9, 2021

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

Web applications often need to work with HTML input. But, rendering them securely on a web page is challenging since they are vulnerable to cross-site scripting (XSS) attacks.

In this article, I will discuss how we can use the new Sanitizer API to address these security concerns with examples while highlighting its features.

[![Build in AI speed — Compose enterprise-grade applications, features, and components]()](https://bit.cloud)

## What is HTML Sanitizer API?

The Sanitizer API was first announced in a draft specification in early 2021. It gives native browser support for removing malicious code from dynamically updated markup on websites.

> We can use the HTML Sanitizer API to sanitize unsafe HTML strings and `Document` or `DocumentFragment` objects before inserting them into the DOM.

The main goals of building a separate API for sanitation are:

* To reduce the attack surface for cross-site scripting in web applications.
* To keep HTML output safe for usage within the current user agent.
* To increase the availability of the sanitizer and make it convenient to use.

## Features of Sanitizer API

The Sanitizer API brings a variety of new features to the string sanitization process. However, all these features can be grouped and presented as follows:

### **1. Sanitization of user input**

The main feature of this API is to accept and convert strings into safer ones. These converted strings will not execute JavaScript accidentally and make sure your application is protected against XSS attacks.

### **2. Browser-maintained**

The library comes pre-installed with the browser and will be updated when bugs or new attack vectors are discovered. So, now you have a built-in sanitizer and no need to import any external libraries.

### **3. Safe and simple to use**

Shifting sanitization to the browser makes it more convenient, secure, and faster. Since the browser already has a robust and secure parser, it knows how each active element in the DOM should be treated. Compared to the browser, an external parser developed in JavaScript can be costly and get outdated soon.

## How to Use the Sanitizer API?

Using the Sanitizer API is pretty straightforward. All you need to do is instantiate the `Sanitizer` class using the `Sanitizer()` constructor and configure the instance.

For sanitizing data, the API provides three basic methods. Let’s see how and when we should use them.

## 1. Sanitizing a String with Implied Context

`Element.setHTML()`is used to parse and sanitize strings and immediately insert them into the DOM.

It is suitable for situations where the target DOM element is known and the HTML content is in the form of a string.

## 2. Sanitizing a String with a Given Context

`Sanitizer.sanitizeFor()`is used to parse, sanitize and prepare strings to be added into the DOM later.

It is most suitable when the HTML content is in the form of a string, and the target DOM element type is known (e.g. `div`, `span`).

> **Note:** You may use `.innerHTML` from the `HTMLElement` to get the sanitization result as a string.

When using `sanitizefor()`, the result of the parsing HTML string is determined by the context/element it was entered. For example, an HTML string containing `<td>` element is only allowed if it is inserted within a `<table>` element. If it is inserted in a `<div>` element, it will be removed.

So that, the tag of the intended target element must be specified as a parameter when using `Sanitizer.sanitizeFor().`

## 3. Sanitizing With Nodes

`Sanitizer.sanitize()`is used to sanitize DOM tree nodes when you already have a user-controlled `DocumentFragment.`

Apart from that, Sanitizer API modifies the HTML strings by removing and filtering attributes and tags. For example, Sanitizer API:

* Removes certain tags (`script`, `marquee`, `head`, `frame`, `menu`, `object`, etc.) and retain `content` tags.
* Removes most of the attributes. Only `hrefs` on `<a>` tag and `colspans`on `<td>`, `<th>` tags will be kept without removal.
* Filters out strings that would cause a script execution.

By default Sanitizer instance only works for preventing XSS. But, there can be situations where we need custom-configured sanitizers. So, let’s see how we can customize the Sanitizer API.

## Customizing the Sanitization Process

If you want to create a custom configuration for sanitization, all you need to do is to create a configuration object and pass it to the constructor when you initialize the Sanitizer API.

The following configuration parameters define how the sanitization result should handle a given element.

* `allowElements` - Specify elements that the sanitizer should keep in the input.
* `blockElements` - Specify elements that the sanitizer should drop from the input but keep their children.
* `dropElements` - Specify elements that the sanitizer should drop from the input, including the input’s children.

With `allowAttributes` and `dropAttributes` parameters, you can define which attribute to be allowed or removed.

`AllowCustomElements` parameter allows or denies the use of custom elements.

> **Note:** If you create the `Sanitizer`without any parameters and with no explicitly defined configurations, the default configuration value will be applied.

## Browser Support

Current browser support for the Sanitizer API is limited and the specification is still in progress. But, there are major development happening and we can expect a fully complete Sanitizer API within the next few months.

> The API is still in the experiment stage, and therefore keep a close eye on its progress for changes before using it in production.

Press enter or click to view image in full size

![]()

> **Note:** In Chrome 93+ you can try out Sanitizer API by enabling `about://flags/#enable-experimental-web-platform-features` flag. It is also available as an experimental feature in Firefox. You just have to set the `dom.security.sanitizer.enabled` flag to `true` in `about:config` to enable it.

## Build composable web applications

Don’t build web monoliths. Use [Bit](https://bit.dev/) to create and compose decoupled software components — in your favorite frameworks like React or Node. Build scalable frontends and backends with a powerful and enjoyable dev experience.

Bring your team to [Bit Cloud](https://bit.cloud/) to host and collaborate on components together, and greatly speed up, scale, and standardize development as a team. Start with composable frontends like a Design System or Micro Frontends, or explore the composable backend. [**Give it a try →**](https://bit.dev/)

[![https://cdn-images-1.medium.com/max/800/1*ctBUj-lpq4PZpMcEF-qB7w.gif]()](https://bit.dev)

## Learn More

[## How We Build Micro Frontends

### Building micro-frontends to speed up and scale our web development process.

blog.bitsrc.io](/how-we-build-micro-front-ends-d3eeeac0acfc?source=post_page-----828d5ea7dca6---------------------------------------)

[## How we Build a Component Design System

### Building a design system with components to standardize and scale our UI development process.

blog.bitsrc.io](/how-we-build-our-design-system-15713a1f1833?source=post_page-----828d5ea7dca6---------------------------------------)

[## The Composable Enterprise: A Guide

### To deliver in 2022, the modern enterprise must become composable.

blog.bitsrc.io](/the-composable-enterprise-a-guide-609443ae1282?source=post_page-----828d5ea7dca6---------------------------------------)

[## 7 Tools for Faster Frontend Development in 2022

### Tools you should know to build modern Frontend applications faster, and have more fun.

blog.bitsrc.io](/7-tools-for-faster-frontend-development-in-2022-43b6f663c607?source=post_page-----828d5ea7dca6---------------------------------------)
---
title: "Exploring Different Types of Micro Frontends"
url: https://medium.com/p/76fee6ac8697
---

# Exploring Different Types of Micro Frontends

[Original](https://medium.com/p/76fee6ac8697)

# Exploring Different Types of Micro Frontends

[![Vivek Malhan](https://miro.medium.com/v2/resize:fill:64:64/1*our9-to0HSILK95KUq5ZKA.jpeg)](/@amalhan43?source=post_page---byline--76fee6ac8697---------------------------------------)

[Vivek Malhan](/@amalhan43?source=post_page---byline--76fee6ac8697---------------------------------------)

5 min read

·

Jul 30, 2024

--

Listen

Share

More

> **written by** [**Vivek Malhan**](https://vivekmalhan-cb919.web.app/)

Press enter or click to view image in full size

![]()

Micro Frontends have become increasingly favored as a scalable framework for constructing contemporary web applications. This methodology empowers teams to craft, deploy, and expand autonomous features or components, nurturing enhanced collaboration and sustainability.

### Agenda

* [What are micro frontends​](#ca56)
* [Approach​](#6eec)
* [Use case of different types of micro frontends](#4310)

### What are micro frontends?

You may have heard from your backend team that they are using a microservices approach for building the backend. But what if we can use the same approach in building our front end?

This way, we can benefit from that approach while building our front end, such as teams being able to work individually, having fewer conflicts on the codebase, and reducing the time to solve those conflicts.

**The extended concept of microservices in the world of frontend is called micro frontend**.

Here are some examples of architectures that are available in the market:

Press enter or click to view image in full size

![]()

Here is a detailed guide of how micro frontend architecture looks like

Press enter or click to view image in full size

![]()

You can learn further about Microfrontends using this [link](https://javascript.plainenglish.io/exploring-micro-frontends-and-implementation-with-react-vite-7178aa1886d4)

### Approaches:

* Client-Side Composition​
* Server-Side Composition​
* Edge-Side Composition​
* Build-Time Integration​
* Web Components​
* Iframe-Based Integration​
* Module Federation

### Use Case of Different Types of Micro Frontends

> CLIENT-SIDE COMPOSITION​:

**Description:**​

* The composition of micro frontends happens in the browser. Each micro frontend is loaded and integrated into the main application at runtime.​

**Use Case Scenarios:**​

* Suitable for applications where different teams own different parts of the UI and can deploy independently.​
* Useful when you want to update parts of your application without redeploying the entire app.​
* Ideal for Single Page Applications (SPAs) where the performance impact of multiple network requests is acceptable.​​

**Example:**​

* **Amazon**: Different parts of the Amazon web application, such as the product detail page, reviews, and recommendations, can be developed and deployed by different teams and integrated on the client side.

> Server-Side Composition​​

**Description:**​

* The composition happens on the server before sending the HTML to the browser. Each micro frontend is rendered on the server and stitched together.​

**Use Case Scenarios:**​

* Ideal for applications where SEO is important, as server-side rendering improves search engine indexing.​
* Suitable for applications where initial load performance is critical.​
* Beneficial when the complexity of managing client-side routing and state sharing is too high.​

**Example:**​

* **Spotify**: The main Spotify web application composes different parts of the UI server-side before sending it to the client, ensuring fast initial load times and better SEO for public pages like artist profiles.​

> ​EDGE-SIDE COMPOSITION​

**Description:**​

* The composition is done at the CDN (Content Delivery Network) or edge server level. Each micro frontend is fetched and integrated close to the user.​

**Use Case Scenarios:**​

* Best for applications with global audiences to reduce latency by serving content from the nearest edge server.​
* Suitable for applications with high availability and performance requirements.​
* Useful when you want to leverage CDN capabilities for caching and reducing server load.​

**Example:**​

* **Netflix**: Netflix uses edge-side composition to serve different parts of the UI from the closest CDN server, ensuring high performance and low latency for a global user base.​

> BUILD-TIME INTEGRATION​

**Description:**​

* The integration of micro frontends happens at build time. Each micro frontend is built into the main application as part of the build process.​

**Use Case Scenarios:**​

* Suitable for applications where deployment frequency is low and there is less need for independent deployments.​
* Beneficial when there is a need to ensure a tight coupling between different parts of the application.​
* Ideal for environments where the overhead of runtime integration is not justified.​

**Example:**​

* **Airbnb**: Airbnb’s web application can integrate micro frontends at build time, ensuring a seamless user experience with tight coupling between different parts of the site.​

> WEB COMPONENTS​

**Description:**​

* Using web standards like Custom Elements and Shadow DOM to create encapsulated, reusable components that can be integrated into any web application.​

**Use Case Scenarios:**​

* Useful for creating highly reusable components that can be shared across multiple applications.​
* Suitable for applications that need to support different technology stacks and frameworks.​
* Ideal for legacy systems that need incremental modernization without a complete rewrite.​

**Example:**​

* **IKEA**: IKEA uses web components to create reusable UI elements that can be integrated across different parts of its site, regardless of the underlying technology stack.​

> IFRAME-BASED INTEGRATION

**Description:**​

* Each micro frontend is loaded into an iframe, providing a high level of isolation and security.​

**Use Case Scenarios:**​

* Best for integrating third-party applications where you have little control over the code.​
* Suitable for applications requiring strong isolation between different parts of the UI.​
* Useful when dealing with applications that have different security requirements or potential conflicts in CSS/JavaScript.​

**Example:**​

* **PayPal**: PayPal can integrate various third-party payment options and services via iframes, ensuring secure and isolated transactions.​

> ​​Module Federation

**Description:**​

* Using tools like Webpack Module Federation to dynamically load micro frontend modules at runtime, allowing for shared dependencies and runtime composition.

**Use Case Scenarios:**​

* Ideal for applications requiring shared states or libraries between micro frontends.​
* Suitable for large-scale applications with complex dependency management needs.​
* Beneficial when you want to reduce the duplication of code and improve loading performance.​​

**Example:**​

* **Shopify** uses module federation to dynamically load and integrate various modules such as the product catalog, shopping cart, and checkout process. This allows Shopify to maintain a high degree of modularity and flexibility in its platform.

### Use Case Summary​

1. **Client-Side Composition**: Dynamic, independent deployment, SPAs.​
2. **Server-Side Composition**: SEO, initial load performance.​
3. **Edge-Side Composition**: Global audience, high performance.​
4. **Build-Time Integration**: Tight coupling, infrequent deployments.​
5. **Web Components**: Reusability, technology agnostic, legacy systems.​
6. **Iframe-Based Integration**: Strong isolation, third-party integration.​
7. **Module Federation**: Shared dependencies, runtime composition, large-scale apps.​

Thank You, I am delighted you made it to the end.

Let’s connect. Here is a link to [know me more](https://vivekmalhan-cb919.web.app/).

[Subscribe](/@amalhan43/subscribe) to get notified when I publish my next blog. Until Next time.
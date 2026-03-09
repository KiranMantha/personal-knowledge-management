---
title: "AEM with traditional(headfull) sites and AEM with SPA"
url: https://medium.com/p/8b9fdcbe8cdd
---

# AEM with traditional(headfull) sites and AEM with SPA

[Original](https://medium.com/p/8b9fdcbe8cdd)

Member-only story

# **AEM with traditional(headfull) sites** and **AEM with SPA**

[![Shankar Angadi](https://miro.medium.com/v2/resize:fill:64:64/0*-1pQrVD3TD58V6lb.jpg)](/@angadi.saa?source=post_page---byline--8b9fdcbe8cdd---------------------------------------)

[Shankar Angadi](/@angadi.saa?source=post_page---byline--8b9fdcbe8cdd---------------------------------------)

4 min read

·

Dec 2, 2024

--

1

Listen

Share

More

Non members can access from [here](/@angadi.saa/aem-with-traditional-headfull-sites-and-aem-with-spa-8b9fdcbe8cdd?sk=2355e8d656644439e54d3ffbcec7687b)

Here’s a comparison between **AEM with traditional websites** and **AEM with SPA** (Single Page Application) to highlight the differences in terms of content management, performance, user experience, and developer experience

## 1. Content Management

**AEM with Traditional Sites**

* **Authoring Experience**: Traditional AEM sites offer an intuitive, drag-and-drop authoring experience, with full control over page structure and layout using AEM’s page editor. Content authors can preview and publish pages easily.
* **Flexibility**: Authors have fine-grained control over the entire page and can customize the look and feel using templates and components provided by developers

**AEM with SPA**

* **Authoring Experience**: AEM’s out-of-the-box SPA Editor allows content authors to manage and edit content, but the full layout flexibility is often limited compared to traditional AEM pages, as the frontend logic and layout are largely controlled by the SPA framework (React, Angular, Vue).
* **Component Reuse**: While authoring flexibility may be more limited in SPAs, component-based architectures allow for easier reuse and consistent content presentation across devices.

## 2. Performance

**AEM with Traditional Sites**

* **Page Reloads**: Each time a user navigates to a new page, the entire page is loaded from the server, which can increase load times, especially for large or media-heavy pages.
* **Caching**: Traditional sites benefit heavily from caching at the dispatcher level, allowing faster delivery of static resources and reducing server load. However, too many page reloads can still make the user experience slower compared to SPAs.

**AEM with SPA**

* **Dynamic Loading**: SPAs load content dynamically, meaning only the necessary parts of the page are updated during navigation, leading to faster user interactions after the initial load.
* **Initial Load**: SPAs often have a heavier initial load since they pull in all the necessary JS and CSS files at the beginning, but once loaded, navigation is much faster.
* **Complex Caching**: Caching strategies for SPAs are often more complex, as the SPA is responsible for deciding which content to load dynamically and which parts are cached.

## 3. User Experience (UX)

**AEM with Traditional Sites**

* **Page-by-Page Navigation**: Traditional sites often feel more static, with full page reloads for every navigation event. This may lead to longer wait times and a less seamless experience, especially for users on mobile or slower connections.
* **Consistent Behavior**: The interaction patterns are predictable, making it straightforward for non-technical users to navigate.

**AEM with SPA**

* **Smooth, App-like Experience**: SPAs provide a fluid, seamless experience by loading content dynamically without reloading the entire page. This leads to a faster and more engaging experience for users.
* **Rich Interactivity**: SPAs allow for complex, real-time interactions on the front end, such as live updates, drag-and-drop interfaces, and infinite scroll, which improve the overall user engagement.

## 4. Development Complexity

**AEM with Traditional Sites**

* **Tight Coupling**: Traditional AEM development tightly couples backend logic (Java/HTL/Sightly) with frontend rendering (HTML, CSS, JS). This simplifies integration but also limits the separation of concerns between backend and frontend teams.
* **Faster Development for Simple Sites**: Traditional AEM development works well for simpler, content-focused websites that don’t need heavy interactivity. The development is usually faster for such scenarios because of AEM’s well-integrated templating system.

**AEM with SPA**

* **Decoupled Architecture**: SPA development decouples the backend (AEM) from the frontend (React, Angular, Vue.js), which allows frontend and backend teams to work independently. This provides flexibility but increases complexity, as teams need to manage the API interactions between the SPA and AEM.
* **Advanced Tooling**: SPAs require more advanced tooling, such as Webpack for bundling, Babel for transpiling, and often more sophisticated build pipelines. This requires a higher skill level and longer development cycles for the initial setup.

## 5. SEO and URL Handling

**AEM with Traditional Sites**

* **SEO-Friendly**: Traditional AEM sites are inherently SEO-friendly since each page has its own URL and metadata. The structure is easy for search engines to crawl, and tools like AEM’s SEO console make it simple to manage metadata and optimize search rankings.
* **Easy URL Management**: URLs are straightforward to manage, as they correspond directly to page structures within AEM.

**AEM with SPA**

* **SEO Challenges**: SPAs can face challenges with SEO because they load content dynamically and do not always present a full page to search engines by default. However, this can be mitigated using server-side rendering (SSR) or pre-rendering techniques.
* **Custom URL Handling**: In SPAs, URL handling is often done within the SPA router, which requires additional configuration to ensure clean URLs and that search engines properly index content.

## 6. Multichannel and Headless Capabilities

**AEM with Traditional Sites**

* **Limited Headless**: Traditional AEM setups are designed primarily for web pages, though AEM has content fragments and experience fragments that can be used for headless delivery, the overall architecture is not optimized for multi-channel content delivery.

**AEM with SPA**

* **Headless Friendly**: AEM’s content fragments and experience fragments integrate well with SPAs, allowing for omnichannel content delivery. Using AEM as a headless CMS while the SPA handles the rendering provides flexibility for web, mobile, and other digital touchpoints.

## 7. Content Personalization and Analytics

**AEM with Traditional Sites**

* **Out-of-the-Box Personalization**: AEM’s personalization tools, like Adobe Target, work seamlessly with traditional sites. It allows for easy implementation of personalized content based on user segments and behaviors.
* **Integrated Analytics**: AEM Analytics (integrated with Adobe Analytics) is easy to set up with traditional AEM sites and provides robust reporting on content performance.

**AEM with SPA**

* **Custom Personalization**: Personalization with SPAs requires additional work, especially since the page content is dynamically updated. While Adobe Target can still be integrated, it requires custom configuration to track and personalize dynamic content in the SPA.
* **Advanced Analytics Setup**: Analytics tracking in SPAs requires custom implementations because page views don’t work the same way as in traditional sites (due to dynamic page loading). Analytics needs to be tracked manually for route changes and user interactions.

Press enter or click to view image in full size

![]()
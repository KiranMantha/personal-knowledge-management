---
title: "9 Web Components UI Libraries You Should Know in 2021"
url: https://medium.com/p/9d4476c3f103
---

# 9 Web Components UI Libraries You Should Know in 2021

[Original](https://medium.com/p/9d4476c3f103)

# 9 Web Components UI Libraries You Should Know in 2021

## Looking for framework-agnostic web components? Take a look

[![Jonathan Saring](https://miro.medium.com/v2/resize:fill:64:64/1*pLN3R5sML3dcjAvUZDWtOA.png)](https://medium.com/@JonathanSaring?source=post_page---byline--9d4476c3f103---------------------------------------)

[Jonathan Saring](https://medium.com/@JonathanSaring?source=post_page---byline--9d4476c3f103---------------------------------------)

7 min read

·

Apr 18, 2019

--

33

Listen

Share

More

Press enter or click to view image in full size

![]()

When I began searching for web components libraries to compose this post, I initially thought “Where can I find a cool lit-html lib?” This is because I’ve yet to grok the full potential of web components. This is a framework/library way of thinking. It’s like asking, I want a cool html library. All web components are interoperable by definition to play well with others.

Custom components and widgets that build on the Web Component standards, will work across modern browsers, and can be used with any JavaScript library or framework that works with HTML.

With all the chatter around web components, [Stencil](https://stenciljs.com/), [Svelte](https://github.com/sveltejs/svelte), [Lit HTML](https://github.com/Polymer/lit-html) etc, I decided to take a look at what web component libraries are available around the web today to get a head start on the future. Feel free to suggest more!

[![Build in AI speed — Compose enterprise-grade applications, features, and components]()](https://bit.cloud)

> **Tip**: Build your own library! Today it’s easier than ever with tools like [**bit.dev**](https://bit.dev)that let you dynamically collect existing UI components from your apps, and [share them across projects as a team](/how-we-build-our-design-system-15713a1f1833).

**Learn more:**

[## Introducing Stencil Component Development Environment

### As a developer working with Bit components, you understand the importance of generating previews ('compositions') to…

bit.dev](https://bit.dev/blog/introducing-stencil-component-development-environment-lfs5dfqw/?source=post_page-----9d4476c3f103---------------------------------------)

[## Introducing Lit Component Development Environment

### Lit support was first introduced to Bit in early 2022. Since then, numerous teams have used it to streamline the…

bit.dev](https://bit.dev/blog/introducing-lit-component-development-environment-lfhd699k/?source=post_page-----9d4476c3f103---------------------------------------)

## 1. Material components web

Press enter or click to view image in full size

![]()

Usually, the title “Material” positions a UI component library right at the top of the star-count and downloads count. Google’s Material-components-web library is the web-component version of the Material-UI library. While still a work in progress, these Web Components can be incorporated into a wide range of contexts and frameworks. Definitely keep track of this one.

[## material-components/material-components-web-components

### Material Web Components — Material Design implemented as Web Components …

github.com](https://github.com/material-components/material-components-web-components?source=post_page-----9d4476c3f103---------------------------------------)

## 2. Polymer elements

Press enter or click to view image in full size

![]()

Google’s [Polymer library](https://github.com/Polymer/polymer) lets you build encapsulated, reusable Web Components that work like standard HTML elements with an experience as simple as importing and using any other HTML element. [Polymer elements](https://github.com/PolymerElements?page=3) is a GitHub organization containing over 100 reusable Polymer components as standalone repositories you can browse and use off-the-shelf. Example:

```
<!-- Import a component -->  
<script src="https://unpkg.com/@polymer/paper-checkbox@next/paper-checkbox.js?module" type="module" ></script><!-- Use it like any other HTML element -->  
<paper-checkbox>Web Components!</paper-checkbox>
```

[## PolymerElements

### PolymerElements has 30 repositories available. Follow their code on GitHub.

github.com](https://github.com/PolymerElements?page=3&source=post_page-----9d4476c3f103---------------------------------------)

* Thought: Maintain all components in one repo and make all of them individually available to find and use in one [Bit](https://github.com/teambit/bit) collection?

## 3. Vaadin web components

Press enter or click to view image in full size

![]()

I think this one is promising. It’s a rather new library containing a set of nearly 30 evolving open source web components for building the UI of mobile and desktop web applications across modern browsers. Development is active and I’ll definitely keep track of this library. Check it out.

[## vaadin/vaadin

### An evolving set of open source web components for building mobile and desktop web applications in modern browsers. …

github.com](https://github.com/vaadin/vaadin?source=post_page-----9d4476c3f103---------------------------------------)

## 4. Wired elements

[![]()](https://bit.dev/wiredjs/wired-elements)

Wired elements is a 7K stars collection of elements that appear hand drawn. Built for wireframes, the elements are drawn so that no two renderings will be exactly the same — just like two separate hand-drawn shapes. Useful? maybe. Awesome? definitely :) Play with them online [here](https://codesandbox.io/s/p77jkn13nq), even with [React](https://codesandbox.io/embed/xrll5wyl8w) and [Vue](https://codesandbox.io/embed/vj389y9375).

[## wiredjs/wired-elements

### Collection of elements that appear hand drawn. Great for wireframes. - wiredjs/wired-elements

github.com](https://github.com/wiredjs/wired-elements?source=post_page-----9d4476c3f103---------------------------------------)

[## wired-elements by wiredjs · Bit

### Collection of elements that appear hand drawn. Great for wireframes. - 19 Javascript components. Examples…

bit.dev](https://bit.dev/wiredjs/wired-elements?source=post_page-----9d4476c3f103---------------------------------------)

## 5. Elix

Press enter or click to view image in full size

![]()

Elix is a community-driven reusable set of customizable web components for common user interface patterns. To ensure high-quality standards the components are measured against the [Gold Standard checklist for web components](https://github.com/webcomponents/gold-standard/wiki), which uses the built-in HTML elements as the quality bar. I’m really excited about this one, and they’re looking for contributors… :)

[## elix/elix

### High-quality, customizable web components for common user interface patterns — elix/elix

github.com](https://github.com/elix/elix?source=post_page-----9d4476c3f103---------------------------------------)

## 6. Time elements

```
<local-time datetime="2014-04-01T16:30:00-08:00">  
  April 1, 2014 4:30pm  
</local-time>--<local-time datetime="2014-04-01T16:30:00-08:00">  
  1 Apr 2014 21:30  
</local-time>
```

This rather old 1.5K stars library is basically a component that provides custom subtypes of the standard HTML `<time>` element. By formatting a timestamp as a localized string or as relative text that auto-updates in the user’s browser, you can create custom extensions to use anywhere. Nice.

[## github/time-elements

### Web component extensions to the standard element. - github/time-elements

github.com](https://github.com/github/time-elements?source=post_page-----9d4476c3f103---------------------------------------)

## 7. UI5-webcomponents

Press enter or click to view image in full size![]()

Press enter or click to view image in full size![]()

Built by SAP’s [UI5](https://openui5.org/), this library is a set of lightweight, reusable and independent UI elements. The components are not however built on top of UI5, but are standalone elements. You can use across frameworks and apps. The design of the components is aligned to the [SAP Fiori Design Guidelines](https://experience.sap.com/fiori-design-web/) and incorporates the Fiori 3 design. Check out the [live playground and APIs](http://UI5).

[## SAP/ui5-webcomponents

### UI5 Web Components - the enterprise-flavored sugar on top of native APIs! Build SAP Fiori user interfaces with the…

github.com](https://github.com/SAP/ui5-webcomponents?source=post_page-----9d4476c3f103---------------------------------------)

## 8. Patternfly

*Run demo:*

```
git clone git@github.com:patternfly/patternfly-elements.git  
cd patternfly-elements  
npm install # this will take a while due to lerna bootstrap  
npm run storybook
```

PatternFly Elements is a collection of nearly 20 flexible and lightweight Web Components, and the tools to build them. PatternFly Elements are lightweight in size and boilerplating (which is pretty much the web component standard), work in React, Vue, Angular, vanilla JS, anywhere HTML elements are used.

[## patternfly/patternfly-elements

### PatternFly Elements: A set of UI web components. Contribute to patternfly/patternfly-elements development by creating…

github.com](https://github.com/patternfly/patternfly-elements?source=post_page-----9d4476c3f103---------------------------------------)

## 9. Web components org

This isn’t a library, but rather Google’s web component discovery portal built around Polymer elements and friends. I’m listing it here since it’s a useful way to update on new web components from the Polymer team and provides some useful resources to read when starting with web components.

[## webcomponents.org

### Justin Willis from Ionic joins us this week to talk about hybrid app development with Ionic and some amazing work they…

www.webcomponents.org](https://www.webcomponents.org/?source=post_page-----9d4476c3f103---------------------------------------)

## Honorable mentions

[## HTML Elements

### HTML Custom Elements Framework. HTML Elements has 18 repositories available. Follow their code on GitHub.

github.com](https://github.com/HTMLElements?source=post_page-----9d4476c3f103---------------------------------------)

[## GitHub(web-components)

### How people build software. GitHub has 30 repositories available. Follow their code on GitHub.

github.com](https://github.com/github?source=post_page-----9d4476c3f103---------------------------------------)

[## michaelauderer/stencil-styled-components

### Small library to bring the concept of styled-components to StencilJS. - michaelauderer/stencil-styled-components

github.com](https://github.com/michaelauderer/stencil-styled-components?source=post_page-----9d4476c3f103---------------------------------------)

[## obetomuniz/awesome-webcomponents

### A curated list of awesome Web Components tools, articles and resources. - obetomuniz/awesome-webcomponents

github.com](https://github.com/obetomuniz/awesome-webcomponents?source=post_page-----9d4476c3f103---------------------------------------)

[## mateusortiz/webcomponents-the-right-way

### This is a guide intended to introduce to Web Components. Everyone can contribute here! …

github.com](https://github.com/mateusortiz/webcomponents-the-right-way?source=post_page-----9d4476c3f103---------------------------------------)

[## nepaul/awesome-web-components

### A curated list of awesome web components. Contribute to nepaul/awesome-web-components development by creating an…

github.com](https://github.com/nepaul/awesome-web-components?source=post_page-----9d4476c3f103---------------------------------------)

[## mappmechanic/awesome-stenciljs

### List of Awesome Web Components Built with StencilJS - mappmechanic/awesome-stenciljs

github.com](https://github.com/mappmechanic/awesome-stenciljs?source=post_page-----9d4476c3f103---------------------------------------)

[## RIAEvangelist/awesome-webcomponents

### Contribute to RIAEvangelist/awesome-webcomponents development by creating an account on GitHub.

github.com](https://github.com/RIAEvangelist/awesome-webcomponents?source=post_page-----9d4476c3f103---------------------------------------)

[## webcomponents.org

### Justin Willis from Ionic joins us this week to talk about hybrid app development with Ionic and some amazing work they…

www.webcomponents.org](https://www.webcomponents.org/?source=post_page-----9d4476c3f103---------------------------------------)

## Build Apps with reusable components, just like Lego

![]()

[**Bit**](https://bit.cloud/)**’s open-source tool** help 250,000+ devs to build apps with components.

Turn any UI, feature, or page into a **reusable component** — and share it across your applications. It’s easier to collaborate and build faster.

**→** [**Learn more**](https://bit.dev/)

Split apps into components to make app development easier, and enjoy the best experience for the workflows you want:

### → [Micro-Frontends](/how-we-build-micro-front-ends-d3eeeac0acfc)

### → [Design System](/how-we-build-our-design-system-15713a1f1833)

### → [Code-Sharing and reuse](https://bit.cloud/blog/how-to-reuse-react-components-across-your-projects-l4pz83f4)

### → [Monorepo](https://www.youtube.com/watch?v=5wxyDLXRho4&t=2041s)

### Learn more

[## How We Build Micro Frontends

### Building micro-frontends to speed up and scale our web development process.

blog.bitsrc.io](/how-we-build-micro-front-ends-d3eeeac0acfc?source=post_page-----9d4476c3f103---------------------------------------)

[## How We Build a Design System

### Building a design system with components to standardize and scale our UI development process.

blog.bitsrc.io](/how-we-build-our-design-system-15713a1f1833?source=post_page-----9d4476c3f103---------------------------------------)

[## Creating a Developer Website with Bit components

### How I built my portfolio using independent React components.

blog.bitsrc.io](/creating-a-developer-website-with-bit-components-3f4083a7f050?source=post_page-----9d4476c3f103---------------------------------------)

[## How to Reuse and Share React Components in 2023: A Step-by-Step Guide

### Learn how easy code sharing and collaboration can be, with Bit’s intuitive approach to reusable React components.

blog.bitsrc.io](/how-to-reuse-and-share-react-components-in-2023-a-step-by-step-guide-85642e543afa?source=post_page-----9d4476c3f103---------------------------------------)

[## 11 React UI Component Libraries you Should Know in 2019

### 11 React component libraries with great components for building your next app’s UI interface in 2019.

blog.bitsrc.io](/11-react-component-libraries-you-should-know-178eb1dd6aa4?source=post_page-----9d4476c3f103---------------------------------------)

[## 11 Vue UI Component Libraries You Should Know In 2019

### 11 Vue.js component libraries tools and frameworks for your next app in 2019.

blog.bitsrc.io](/11-vue-js-component-libraries-you-should-know-in-2018-3d35ad0ae37f?source=post_page-----9d4476c3f103---------------------------------------)

[## 11 Angular Component Libraries You Should Know In 2019

### 11 popular Angular component libraries for building your Angular app in 2019.

blog.bitsrc.io](/11-angular-component-libraries-you-should-know-in-2018-e9f9c9d544ff?source=post_page-----9d4476c3f103---------------------------------------)
---
title: "On Styling Web Components"
url: https://medium.com/p/b74b8c70c492
---

# On Styling Web Components

[Original](https://medium.com/p/b74b8c70c492)

# On Styling Web Components

[![Harshal Patil](https://miro.medium.com/v2/resize:fill:64:64/0*BPr4lXZxMW-gpCsY.jpeg)](/@mistyHarsh?source=post_page---byline--b74b8c70c492---------------------------------------)

[Harshal Patil](/@mistyHarsh?source=post_page---byline--b74b8c70c492---------------------------------------)

6 min read

·

Apr 8, 2019

--

3

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Db74b8c70c492&operation=register&redirect=https%3A%2F%2Fmedium.com%2Fwebf%2Fon-styling-web-components-b74b8c70c492&source=---header_actions--b74b8c70c492---------------------post_audio_button------------------)

Share

Doing it the right way — Tapping into the CSS Object Model

Press enter or click to view image in full size

![]()

Encapsulation is the primary reason why you might want to start using Web Components. In particular, Shadow DOM is the mechanism to achieve true encapsulation. Over the years, web community invented patterns to fix global nature of CSS and JavaScript. These solutions worked but they were not perfect. It took Shadow DOM to really provide the perfect scoping for our CSS.

In this article, we will explore ways to apply styles to web components and attempt to arrive at the most idiomatic way of doing it. Further, we will try to integrate our solution with today’s build tools.

## The naive way — Plain `<style>` tag

When using Shadow DOM, for a style sheet to work, it currently must be specified using a `<style>` element within each shadow root. As such most of the articles around Web Components will illustrate this idea on its face value:

The solution is simple and straight-forward. However, there is a problem:

> For each instance of a component added to the page, a browser will parse the style sheet rules.

This will have an impact on performance on both time and memory axes. Time increases because browsers need to parse the raw strings and Memory cost increases as style rules are stored for every instance of the component. Browsers do not have a way to know if two instances of the same component share the same styles.

> Update: As 
>
> [Eric Bidelman](https://medium.com/u/443b43fab64?source=post_page---user_mention--b74b8c70c492---------------------------------------)
>
>  pointed out in the [comments](/@ebidel/nice-write-up-815f17e78937), the performance aspect need not be really true. It is possible that browsers may internally perform an optimization so that it doesn’t have to parse `style` tag each time an instance is created. In fact, **Blink** (Chrome, Opera, etc.) engine has already optimized this.

## Can we do something better?

Indeed, we can prevent re-parsing of the style rules by creating a `style` node and then deep cloning it for each instance of component:

Again, this approach is easy but still has problems.

* First, it doesn’t really help us share the style across component instances. New `style` node is still created.
* It is awkward to use it with declarative solutions like **lit-html** or **hyperHTML**.

## Enter the Constructible Stylesheets

As the name suggests, constructible stylesheets allow to create and share styles when using Shadow DOM.

Press enter or click to view image in full size

![]()

Besides solving the problems of duplicate copies, it has a few more characteristics:

* Styles are not only shared by instances of the same component but also by the multiple web components.
* It also has support handling asynchronous style. For example, when you have `url` or `@import` rules in your CSS codes.
* Finally, `adoptedStyleSheets` is an array. It means you can really compose your reusable stylesheets in ways that we could not possibly do before. To start with, you can split your CSS rules in small chunks and only apply chucks that are required. You can even do something like:

```
shadowRoot.adoptedStyleSheets = [sheet];// Remove stylesheets after two seconds  
setTimeout(() => shadowRoot.adoptedStyleSheets = [], 2000);
```

## Using with Webpack and SCSS

SCSS as a CSS pre-processor and Webpack as a module bundler and a build tool is a pretty common setup. `CSSStyleSheet.replace()` and `CSSStyleSheet.replaceSync()` expects a CSS rules a raw string. We can use a simple loader chain of **sass-loader** and **raw-loader** as follows:

In your code you can then import **SCSS** file:

```
// Read SCSS file as a raw CSS text  
import styleText from './my-component.scss';  
const sheet = new CSSStyleSheet();sheet.replaceSync(styleText);
```

A similar setup is possible with Rollup.js. Further, new library from Polymer Team — **LitElement** is already using this approach with fallback:

[## Styles - LitElement

### A simple base class for creating fast, lightweight web components

lit-element.polymer-project.org](https://lit-element.polymer-project.org/guide/styles?source=post_page-----b74b8c70c492---------------------------------------)

*\*Note: Currently constructible stylesheets are implemented in Chromium family of browsers. However, with reasonable progressive enhancement practices, it should be easy to provide support for non-supporting browsers.*

## Under the hood — CSSOM

*\*You can skip this section if you are not interested in finer details.*

If HTML markup is transformed into a Document Object Model (DOM) then CSS markup is transformed into a **CSS Object Model (CSSOM)**. These are both independent data structure. Final render tree constructed using these two data structures. As a front-end developer, **it is not really important** to understand the mechanics of CSS Object Model and thus it is a lesser known concept.

Roughly speaking, one `<link type='text/css' href='' />` tag corresponds to one CSS stylesheet. It is represented by `CSSStyleSheet` interface in **CSSOM**. One `CSSStyleSheet` consists of multiple rules. Each rule is represented by `CSSRule` interface.

To access all the `CSSStyleSheet` objects applied to a given document, you can use `document.styleSheets` property. Traditionally, if you wanted to create a `CSSStyleSheet` object, you would have to create a `style` tag; add it to document and use `sheet` property:

```
const styleNode = document.createElement('style');// It is important to add style node to the document  
document.head.appendChild(styleNode);const sheet = styleNode.sheet;
```

However, constructible stylesheet enables two APIs — `CSSStyleSheet()` constructor and `document.adoptedStyleSheets`.

> With constructible stylesheet, you can use CSSStyleSheet() constructor to create stylesheets using JavaScript.

Property `adoptedStyleSheets` is available on Shadow Roots and Documents. It allows us to apply the styles defined by a `CSSStyleSheet` to a given DOM sub-tree. Note that `adoptedStyleSheets` is an immutable array and thus `push` or `splice` will not work.

Press enter or click to view image in full size

![]()

As far as `CSSRule` is concerned, there are many types of `CSSRule`, all of which extends `CSSRule` interface. MDN provides a list of all these rules:

[## CSSRule

### The CSSRule interface represents a single CSS rule. There are several types of rules, listed in the Type constants…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/CSSRule?source=post_page-----b74b8c70c492---------------------------------------)

CSS Object Model is huge and continues to grow every day. You can find the detailed Object model here:

[## CSS Object Model (CSSOM)

### The CSS Object Model is a set of APIs allowing the manipulation of CSS from JavaScript. It is much like the DOM, but…

developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Object_Model?source=post_page-----b74b8c70c492---------------------------------------)

Also, do not forget that the new CSS Typed Object Model is being actively developed. It will surely have an impact on how to write our CSS in JavaScript. You can read more about it in the following article:

[## Working with the new CSS Typed Object Model | Web | Google Developers

### CSS Typed Object Model (Typed OM) brings types, methods, and a flexible object model to working with CSS values…

developers.google.com](https://developers.google.com/web/updates/2018/03/cssom?source=post_page-----b74b8c70c492---------------------------------------)

## Side notes

Irrespective of how you approach Styling in the context of Shadow DOM, following things should be kept in mind:

* You can use external styles with Shadow DOM with the help of `@import` statement.
* Slot items can be styled by global CSS or container component stylesheets.
* **CSS Custom properties** cross the Shadow DOM boundaries.

> As such, these custom properties are the preferred mechanism to style Shadow DOM contents from the outer world.

* Beside custom properties, you can use new CSS selectors like `:host`, `:part`, `:theme` to further provide styling customization from the outer context.
* To a good extent, Style encapsulation with Shadow DOM is a good alternative to CSS-in-JS approaches.
* Virtual components (Component without mount elements like Vue `<router-view />` or React `<Route />` ) are not possible with Web components.
* Web components are a very good candidate for replacing your leaf components like Inputs, Panels, Cards, Pickers, etc.

In the next article, we will explore concerns and design aspects related to web components in general. Stay in touch for future updates.

### *Credits & Artwork:*

Special thanks to [Charushila Patil](https://twitter.com/wakeupcharu) for all the illustrations.
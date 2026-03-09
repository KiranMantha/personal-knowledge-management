---
title: "Web Components Landscape in 2019"
url: https://medium.com/p/13b1e7f6f993
---

# Web Components Landscape in 2019

[Original](https://medium.com/p/13b1e7f6f993)

# Web Components Landscape in 2019

[![Vlad Fedosov](https://miro.medium.com/v2/resize:fill:64:64/2*wk1M5NbfkwFKpGSBXx22wg.jpeg)](/@vlad.fedosov?source=post_page---byline--13b1e7f6f993---------------------------------------)

[Vlad Fedosov](/@vlad.fedosov?source=post_page---byline--13b1e7f6f993---------------------------------------)

7 min read

·

Jul 11, 2019

--

Listen

Share

More

![]()

Recently I was working on a research of the Web Components technology for my company ([Namecheap, Inc](https://www.namecheap.com/)) and found that it’s relatively hard to get an understanding of the overall state of the things as for now. So this article attempts to resolve this problem and provide you with a starting point to your journey.

## Main concerns

* Browser support
* Frameworks compatibility
* SSR + SEO / Bots
* Styling
* Accessibility
* Versioning
* Delivery
* Available tools
* Web Components vs Frameworks

## Browser support

*TL;DR*: IE 10–11 and Edge (Chakra based) are **out of the game** as they do not support Shadow DOM. This makes use of the Web Components almost impractical due to the complexity of the polyfills.

All other browsers (Chrome, FF, Safari, considering 2 latest versions) work just fine with all major techs we need. Let’s looks at the table:

## Frameworks compatibility

**All major frameworks** that exist nowadays [fully support](https://custom-elements-everywhere.com/) Web Components. But let’s look closely:

* React/Preact — there are [some issues](https://custom-elements-everywhere.com/libraries/react/results/results.html) with advanced integration :( And you [may need](https://reactjs.org/docs/web-components.html#using-web-components-in-react) to build React wrappers for WCs ([can be automated](https://github.com/adobe/react-webcomponent)).
* Vue.js — works [out of the box](https://alligator.io/vuejs/vue-integrate-web-components/).
* Angular — works [out of the box](https://stenciljs.com/docs/angular).

## SSR (Server-side rendering) + SEO / Bots

It’s theoretically possible to fully render WC at server side (and it [even works](https://github.com/skatejs/skatejs/tree/master/packages/ssr) for simple ones), but… There is no stable implementation yet, as well as [way to represent](https://www.youtube.com/watch?v=yT-EsESAmgA) Shadow DOM in HTML 😟 Community is [actively working](https://github.com/w3c/webcomponents/blob/gh-pages/proposals/Declarative-Shadow-DOM.md) on a solution.

So what should we do then…? 🤯

The answer is simple – **you can live without it** (for Web Components). Of course this approach has some limitations but we have what we have… Let me explain the idea.

To render Web Components at client side only and do not sacrifice SEO / Bots compatibility you need to keep your content in Light DOM and use ARIA attributes. **Treat your Web Components as native HTML elements.** You can agree that you don’t need to render Shadow DOM for example for `<select>` element to see it’s content. If components are well designed, crawlers do not need a flattened tree to get text contents.

Let’s look at the Tab component markup as an example:

```
<my-tab-group role="tablist" aria-label="My test tabs">  
  <my-tab role="tab" slot="tab">Title for tab 1</my-tab>  
  <my-tab-panel role="tabpanel" slot="panel">Content 1</my-tab-panel>  
  <my-tab role="tab" slot="tab">Title for tab 2</my-tab>  
  <my-tab-panel role="tabpanel" slot="panel">Content 2</my-tab-panel>  
  <my-tab role="tab" slot="tab">Title for tab 3</my-tab>  
  <my-tab-panel role="tabpanel" slot="panel">Content 3</my-tab-panel>  
</my-tab-group>
```

As you can see from this example you as a Bot don’t need access to the Shadow DOM to understand the content present on a page.

## Styling

Because in our components we use Shadow DOM for their internal markup and slots for the content — writing CSS may become a challenging task at the beginning. Let’s go through the concepts we have here.

### CSS Isolation

Shadow DOM [**almost** completely](https://stackoverflow.com/questions/49709676/light-dom-style-leaking-into-shadow-dom) isolates its content from page CSS. In our example we have `<p>` tag (that resides under Shadow DOM) content in green because [color property was inherited](https://take.ms/KbJ6Q).

### How to include CSS into Shadow DOM

Nowadays the simplest way to deliver CSS for Web Components is to **embed them inline** into Web Component template. If you include them via `<link>` tag — you will see **Flash of unstyled content** during page load as in the example above (look at the “(I’m Shared CSS)” label).

However this limitation can be overcome by rather hiding all Shadow DOM content before linked CSS will be loaded or by additionally including component external CSS to the main page code (of course it should be scoped somehow in this case).

I’m looking forward to see [Constructable Stylesheets](https://developers.google.com/web/updates/2019/02/constructable-stylesheets) being available in all major browsers. This would give us more control over CSS.

### Context dependent styles

Often our components have different view modes depending on the passed arguments. Classic example is `<select multiple>`. When you pass `multiple` argument to “select” component — it fully changes its appearance. To achieve similar behaviour Web Platform offers `:host()` pseudo-class (don’t mix it with `:host` one).

Unfortunately this feature isn’t supported in Safari and iOS so we can’t really use it. As a workaround we can use power of JS to manually project host attributes and classes into root element within Shadow DOM to get an ability to write regular CSS.

### Styling slotted content

Stylesheets that were added to the Shadow DOM may be also applied to the `<slot>` content. To do this we have `::slotted()` CSS pseudo-element. However its browser support still non perfect. Look at the example above, Safari won’t handle `::slotted(p)::before` selector correctly.

As a workaround here we can inject styles that are responsible for slot content styling into the page CSS. So the following selector `::slotted(p)::before` written for `<my-component>` will be transformed into `my-component p::before`. Of course it breaks concept of the Shadow DOM a little bit but I don’t see another way out for now.

### Recommendation

At this stage I would recommend to keep CSS, as you likely have it now, in a separate file, include it into the page via `<link>` tag and every Shadow DOM you’ll have. Currently I use the following code to keep it rolling:

```
class MyComponent extends HTMLElement {  
  constructor() {  
    super();  
      
    this.attachShadow({ mode: 'open' });  
    this.__injectGlobalCSS();  
  };  __injectGlobalCSS() {  
    const globalCssInclude = document.querySelector(  
        'head > [data-global-css="true"]'  
    );  
  
    if (globalCssInclude === null) {  
        console.warn(`Can't find global CSS for component ${this.tagName}! Trying to render w/o it...`);  
        return;  
    }  
  
    this.shadowRoot.appendChild(globalCssInclude.cloneNode(true));  
  }  
};
```

## Accessibility

When users of assistive technology, like a screen reader, navigate a web page, it’s vitally important that the semantic meaning of the various controls is communicated. But how this can be achieved with Web Components considering that HTML tags will be custom and so will not have any semantic meaning?

Fortunately there is a solution, to bring semantic back to your custom elements you just need to follow [WAI-AIRA](https://www.w3.org/TR/wai-aria-practices-1.1/) specification. So if you already take care about accessibility — **no much changes here**.

Let’s look at the accessible slider component built with Web Components:

```
<custom-slider min="0" max="10" value="3" role="slider"  
               tabindex="0" aria-valuemin="0" aria-valuemax="10"  
               aria-valuenow="3" aria-valuetext="3"  
               aria-label="Movie rating"></custom-slider>
```

To see more examples of the fully accessible Web Components you can also refer to the [following samples from Google](https://developers.google.com/web/fundamentals/web-components/examples/).

## Versioning

Currently all Web Components must be [registered in global registry](https://developer.mozilla.org/en-US/docs/Web/API/CustomElementRegistry/define). So you can’t have 2 versions of the same component on a single page. This follows approach that Browser use for the DOM, you have single version of it at a time. Simple.

But if you use [Microservices approach at the Frontend](https://micro-frontends.org/) or just have multiple apps running side-by-side on the same page — it may become an issue for you.

Let’s look at the options we have here:

* *Never do breaking changes*. This is the principle that Browsers use. And while it’s possible to do it and it may even be the best option to start with, it’s obvious that it contradicts to the principle “fail fast, fail safe” and doesn’t facilitate innovations.
* *Tag based versioning*. So instead of having `<x-button>` you would have `<x-button-v1>` to accommodate further major versions. So if “Fragment 1” requires `button@1.1.5` and “Fragment 2” requires `button@1.2.1` — `button@1.2.1` only will be used. And if “Fragment 1” needs `v1.1.5` and “Fragment 2” needs `v2.0.0`— both components will be registered.
* *Fragment based scoping*. So instead of having `<x-button>` you would have `<x-button-myfragment>`

## Delivery to Microservice based Frontend

> You can skip it if you have single app at the client side. More info about Microservice based Frontend [can be found here](https://micro-frontends.org/).

I would generally recommend to centrally manage bundle that reside outside of the Fragment and loads code of necessary components. Potentially Fragments may declare needed components and we can generate needed bundle on the fly.

Actual registration of the Web Component within Browser registry may happen globally or if picked up the last approach for versioning — at the Fragment level.

## Available tools

**Libraries you can use to author your Web Components (sorted by my preference, top to bottom):**

* [LitElement](https://lit-element.polymer-project.org/) – written by the guys from Polymer@Google. **Optimal choice** IMO.
* [Stencil](https://stenciljs.com/) – Web Components compiler plus base classes. Built by Ionic team. It has its own build system. Meaning components generated by Stencil can be consumed in any project, but components cannot live in the same project as the application consuming them.
* [SkateJS](https://skatejs.netlify.com/) – tiny wrapper around native APIs that allows to use various renderers. Built by 

  [Trey Shugart](/u/15cc8b14327c?source=post_page---user_mention--13b1e7f6f993---------------------------------------)

   who gave us [WC SSR PoC](/@treshugart/%C3%A5server-side-rendering-web-components-e5df705f3f48).
* [Svetle 3](https://svelte.dev/docs#svelte_compile) — it’s more a framework rather than library to simplify Web Components creation.
* [Riot.js](https://riot.js.org/)
* [Slim.js](http://slimjs.com/#/getting-started)
* [X-Tag](https://x-tag.github.io/) — latest version still in beta
* [Smart HTML Elements](https://www.htmlelements.com) – paid, framework agnostic library

But hey, do I **really need some tool** to comfortably write Web Components? And the **answer is no**, you can write them using Vanilla JS. And it will work for most of the (simple) components you will have.

## Web Components vs Frameworks

To be short: they’re different. Don’t try to replace good old frameworks like Vue.js or React with Web Components.

I would say at this stage Web Component are really useful only if you need to have an instrument that allows you to write framework agnostic code for basic UI components from which you will construct pages with the help of your favourite framework.

Another use case may if you write sharable UI components library (like Bootstrap or MDC) and want to keep it framework independent. Example of the Material Design Components in [pre-WC era](https://github.com/material-components/material-components-web) and [with WC](https://github.com/material-components/material-components-web-components).

As time goes frameworks may start to use Custom Elements and Shadow DOM internally but I wouldn’t expect to see it in the nearest 1–2 years.

## Notes

If you see any gaps or mistakes in the material provided above pls post them in the comments or send me an [email](mailto:vlad.fedosov@gmail.com).

In case of the positive feedback from the community I hope to continue this topic and provide more in depth materials about nuances of the Web Components usage.

## Other articles to read

* [Web Components: Mythbusters Edition](https://dev.to/bennypowers/lets-build-web-components-part-8-mythbusters-edition-3la#myth-web-components-cant-accept-complex-data)
* [Using templates & slots](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_templates_and_slots)
* [Complex guide & best practices from Google](https://developers.google.com/web/fundamentals/web-components/)
* [Duplicate IDs cross Shadow DOM trees](https://stackoverflow.com/questions/56023322/are-duplicate-ids-allowed-in-separate-shadow-roots)
* [The future of accessibility for custom elements](https://robdodson.me/the-future-of-accessibility-for-custom-elements/)
* [Why I don’t use web components](https://dev.to/richharris/why-i-don-t-use-web-components-2cia)
* [Ionic team: Why We Use Web Components](https://dev.to/ionic/why-we-use-web-components-2c1i)
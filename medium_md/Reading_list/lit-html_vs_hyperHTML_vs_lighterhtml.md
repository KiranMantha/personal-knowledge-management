---
title: "lit-html vs hyperHTML vs lighterhtml"
url: https://medium.com/p/c084abfe1285
---

# lit-html vs hyperHTML vs lighterhtml

[Original](https://medium.com/p/c084abfe1285)

# lit-html vs hyperHTML vs lighterhtml

[![Andrea Giammarchi](https://miro.medium.com/v2/resize:fill:64:64/1*54OyE6rg-MdELwb9mW56Xw.png)](/?source=post_page---byline--c084abfe1285---------------------------------------)

[Andrea Giammarchi](/?source=post_page---byline--c084abfe1285---------------------------------------)

10 min read

·

Feb 12, 2019

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dc084abfe1285&operation=register&redirect=https%3A%2F%2Fwebreflection.medium.com%2Flit-html-vs-hyperhtml-vs-lighterhtml-c084abfe1285&source=---header_actions--c084abfe1285---------------------post_audio_button------------------)

Share

![]()

When [**lit-html**](https://lit-html.polymer-project.org) released at the end of July 2017 as an experimental, not production ready, library, I’ve created few days after a huge *gist* comparing it with what was, at that time, the already production ready [**hyperHTML**](https://viperhtml.js.org).

However, over the weekend, I’ve decided to remove such gist, and its comparison, for various reasons, including:

* gists suck at being tracked. No notifications, no PR/MR possible, gists are just a quick “*trash bin*” for Markdown or snippets
* I sucked at remembering to update that complex Markdown table, so that everything written in it, or to be fair most of pain points regarding *lit-html* at that time, would be wrong today
* *lit-html* released its first stable 1.0
* [**lighterhtml**](https://github.com/WebReflection/lighterhtml#lighterhtml) was also recently born as *hyperHTML* drop-in simplified alternative, making the comparison actually fair

## One does not simply compare lit against hyper

There is quite a lot happening in *hyperHTML*, that it makes not much sense to compare it against *lit-html*.

To start with, *hyperHTML* has a [viperHTML](https://viperhtml.js.org/viper.html) node server side alter ego, with API features parity, asynchronous streamed renders, and components.

Speaking of which, lightweight components are part of *hyperHTML* too. These are yet another out-of-the-box feature that comes with *hyper/viperHTML*.

*hyperHTML*, as well as *viper*, also offer a way to extend their syntax, asynchronous renders through any “*thenable*”, and last, but not least, it offers an explicit way to relate DOM nodes with any kind of object, through an API that many found initially somehow difficult to grasp.

Removing all these features, plus simplifying the API, was the goal of *lighterhtml*, which in its 0.9 version is as fast as *lit-html*, but also always smaller, in size, than *hyperHTML* (about ~1K once gzipped but … still)

### So … is hyperHTML slow?

Hell **No**. You can [check by yourself this benchmark](https://rawgit.com/krausest/js-framework-benchmark/master/webdriver-ts-results/table.html) and realize it’s faster than *Preact*, *React*, *Vue*, *Angular*, you name it … but *hyperHTML* doesn’t fit into the *lit*-vs-*light* context ’cause it cannot, and it won’t, compete against them.

Press enter or click to view image in full size

![]()

### … and what about HyperHTMLElement ?

Yes, [HyperHTMLElement](https://github.com/WebReflection/hyperHTML-Element#hyperhtml-element) is based on top of *hyperHTML*, and its part of its ecosystem, but using *lighterhtml* instead would be a no brainer.

> Yet, in [ABP](https://adblockplus.org), we use hyperHTML due its battle-tested Desktop to Mobile compatibility and stability.

However, since *HyperHTMLElement* is something a part, as a part is also the [LitElement](https://github.com/Polymer/lit-element#litelement) class, I’ve left these “*easy to implement*” abstractions, or wrappers, out of this context, comparing instead only what’s meaningful for daily tasks.

## lit-html VS lighterhtml

This is the only comparison that makes sense these days, ’cause both libraries offer pretty much same functionalities, API, and performance.

It is true that *lit-html* might be slightly richer in features, if you use its directives, but what I consider important here, is what we can do with just their core, summarized as such:

* be as standard based as possible
* create, and use, arbitrary DOM content
* be able to quickly change content on the page (aka: *DOM diffing*)

These points are what *lit-html* core offers as a whole, while *lighterhtml* includes some extra feature we’ll see, and compare, later on.

### How much standard ?

Both *lighterhtml* and *lit-html* are based on “*just standards*”, meaning you can use JS without the need to transpile it, and you declare HTML, or SVG, through [template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals).

```
// lighterhtml and lit-html: the basics  
html`  
<div>  
  This will be the content of the div,  
  including this ${Math.random()} value.  
</div>`;
```

While above example will be equivalent for both libraries, *lit-html* would accept some sort of specialized, non standard, HTML syntax, to provide some feature such boolean attributes, events, or properties.

```
// lit-html specialized, non standard, syntax  
html`<input  
  .value=${value}  
  @click=${handler}  
  ?disabled=${disabled}  
>`;
```

Hopefully needless to explain what those fancy attributes would do once rendered, I’d like to provide anyway [a link that explains more](https://lit-html.polymer-project.org/guide/template-reference#binding-types) about.

The equivalent in *lighterhtml*, based on the same *hyperHTML* [syntax engine](https://github.com/WebReflection/domtagger#domtagger), would be the following one:

```
// lighterhtml standard syntax  
html`<input  
  value=${value}  
  onclick=${handler}  
  disabled=${disabled}  
>`;
```

As developer, you don’t need to do anything different than writing HTML as you know, the library will figure out at runtime, accordingly with the kind of node it’s dealing with, what should result as `input.value`, as `input.disabled`, and as `input.addEventListener("click", handler)` .

The only real non standard syntax available in *lighterhtml*, but already widely accepted by the community, is the self closing tag.

```
// lighterhtml simplifies closing tags  
html`<div><span/><span/></div>`;  
html`<custom-element attr=${value}/>`;  
html`<textarea value=${text}/>`;
```

The `<span/><span/>` case would produce a span inside another one in *lit-html*, while it will simply create two adjacent spans in *lighterhtml*.

I let you judge how confusing, or expected, this behavior is in either library, all I know is that I’ve never explicitly closed any tag if I wanted the next one to be part of its content, and I wish HTML would’ve done the same.

### What does `html` return ?

In the case of *lit-html*, the `html` function tag returns some instance of some internal class used by the library to understand its own content.

```
// FAILS in lit-html  
document.body.appendChild(html`<hr>`);  
..  
TypeError: Argument 1 ('node') to Node.appendChild must be an instance of Node
```

In *lighterhtml* though, you can use right away `html` or `svg` to create content:

```
// OK in lighterhtml  
document.body.appendChild(html`<hr>`);
```

The only special case, is when you have hybrid containers, those represented by more than a node, without being inside a single outer container:

```
// lighterhtml hybrid containers  
// (i.e. no <div> around)  
html`  
  <button>first</button>  
  <button>second</button>`;
```

In this case the library also uses an internal representation of a DOM fragment, but that will be returned through the standard method `valueOf()` , providing the ability to use any template as one off, without caring much about the content.

```
document.body.appendChild(html`...`.valueOf());
```

Bear in mind `valueOf()` works even if the returned content is a real node 😉

### How to create arbitrary DOM content, then?

The `render` function is there to accomplish the task.

```
import {render, html} from '//unpkg.com/lit-html?module';  
render(html`<div>Hello lit-html</div>`, document.body);
```

The same could be done via *lighterhtml*, but instead of `render(what, where)`, *lighterhtml* has a `render(where, what())` signature.

```
import {render, html} from '//unpkg.com/lighterhtml?module';  
render(document.body, () => html`<div>Hello lighterhtml</div>`);
```

The `what()` callback is handy when it comes to render components, as in `render(where, App)` case, but also to distinguish between internal renders VS one-off renders, as we’ve seen before.

### … and the simplicity trophy goes to … 🥁🥁🥁

Objectively esier to start with, through zero specialized syntax, if not the self closing tag, which is used by JSX and XML first since ever, and without any lock-in for rendering some one-off content, I’d say ***lighterhtml* wins the simplicity context** 🏆.

There is arguably the [partial attributes “*gotcha*”](https://viperhtml.js.org/hyperhtml/documentation/#essentials-7) that could make *lit-html* simpler to use in some case, but that’s one thing VS standard syntax, self closing least surprise, and one-off capability, keeping the trophy where it is.

### Update

Partial attributes are now supported in both *hyper* and *lighterhtml* 🎉

## What about performance ?

There are two sides to this metric: one is the bundled size, where smaller would mean faster time to be interpreted, and one is the raw rendering performance of the library itself.

### The bundle size

Using brotli as compressor, and executing the following in [any of the keyed or non-keyed folders](https://github.com/krausest/js-framework-benchmark/tree/master/frameworks) of the [js-framework-benchmark](https://github.com/krausest/js-framework-benchmark):

```
brotli -c9 dist/index.js | wc -c
```

We can observe that *lit-html* is 3880 non keyed, and 4441 keyed, while *lighterhtml* is steady at 5794.

Since both benchmarks use pretty much the same test code, this makes ***lit-html*** surely **winning the final production code size** 🏆.

However, the benchmark itself shows that when the difference in size is around 1.5K, when it comes to keyed results, the final performance score might not be impacted.

Currently, ***lighterhtml* wins in the keyed benchmark** 🏆 while ***lit-html* wins in the non keyed one** 🏆, but I’d be curious to see new results [once *lighterhtml* 0.9 goes in](https://github.com/krausest/js-framework-benchmark/pull/520).

Press enter or click to view image in full size

![]()

In few words, when you have slightly more horsepower, it doesn’t matter much if your car is a couple of kilos heavier, but if you’d like to know why *lighterhtml* is heavier, it’s mostly because it inherits the same compatibility granted by *hyperHTML*, and it patches [internally](https://github.com/ungap/create-content/blob/master/index.js#L5-L27), at runtime, a lot of little gotchas found in variuous [browsers or JavaScript transpilers](https://github.com/ungap/template-literal/blob/master/index.js#L7-L14).

*lit-html* also fixes through little [global](https://github.com/Polymer/lit-html/blob/master/src/polyfills/template_polyfill.ts#L50) runtime [shims](https://github.com/Polymer/lit-html/blob/master/src/polyfills/template_polyfill.ts#L16-L22) some browser, but it’s not as backward compatible as *lighterhtml* is.

**Update**, the 0.9 got merged and the score is now 1.01 vs 1.02 🎉

## What does keyed VS non-keyed mean?

In few words, keyed results are the one you’d expect the most, while non keyed results mean that any created node could represent any sort of data.

If it makes any sense, you can think of *non-keyed* as the result of any server side rendered page, where nodes that relate to specific articles, items, database results, or user preferences, are just on the layout with some info exposed through some attribute.

```
<ul id="user-list">  
  <li data-reason="wish" data-item-id="1234">Sony PS5</li>  
  <li data-reason="checkout" data-item-id="456">LG Mouse</li>  
</ul>
```

When content arrives from the server, items are usually identified by unique IDs, as in above `data-item-id` case, and rarely by objects or, even worse case, DOM nodes.

The relationship is between informations exposed through the rendered page, and its nodes with their attributes, plus some action to perform, on the client or the server, when some DOM node related to each item is added, modified, or removed.

This is somehow an example of non keyed results, where a single item ID could be the same in many nodes, or many panels, without binding it to any specific JavaScript object.

This is also a very common, non client side driven, scenario, but when part of the business logic is delegated to the client, keyed driven views relates nodes to specific items/objects, abstracting away the contract between an item, as JS entity itself, and one of its multiple representations on any part of the page.

The improvement is given by the fact whenever such JS entity is removed, updated, or modified, any related view would follow up the change, without needing to query every single time the whole document, or ask the server to refresh the entire page.

**Quick note**: non keyed results visually represent the same data, but there’s no guarantee that a node is directly related to any object held in the JS world.

With keyed results, `html.for(entity)` will always return the node associated to `entity` object, giving us the ability to eventually retrieve, or update, directly, any node associated to a single `entity` without even knowing if such node has been already rendered or not.

A classic *TODOs* could be a good example:

```
// items (used as references)  
const list = [  
  {id: 1, desc: 'some'},  
  {id: 2, desc: 'item'}  
];// shopping chart ...  
const ul = document.querySelector('#shopping-chart');  
render(  
  ul,  
  () => html.for(ul)`<ul>${  
    list.map(item => html.for(item, ul.id)`  
    <li>${item.desc}</li>`)  
  }</ul>`  
);// ... and a summary  
const summary = document.querySelector('#summary');  
render(  
  summary,  
  () => html.for(summary)`<p>${  
    list.map((item, i) => html.for(item, summary.id)`  
    ${i ? ', ' : ''}  
    <span>${item.desc}</span>`)  
  }</p>`  
);
```

Since all items are referenced, as soon as one gets updated, its related view state would be reflected in every place.

This is somehow an inverted control for the rendering path of the data you hold via JavaScript, and it’s basically representing server side renders on the fly, whenever any item gets modified.

Imagine asking the whole web page each time you need to update a single item in the chart, or even a button inside a runtime calculator … right?

Instead, only what needs to get updated will actually get updated, as you can see in the console.

**Quick note** about having keyed results in *lighterhtml*, all you need to do is to pass a reference with, or without, an id, while in *lit-html* you’d need a *repeater* from its directives, as [shown in this code pen](https://codepen.io/WebReflection/pen/bzKxyg).

### … wait a minute, what are those comments ?

Press enter or click to view image in full size

![]()

The *hyperHTML* technique to address anchors in the DOM to render partial updates has been used in both *lighterhtml* and somehow simulated as well in *lit-html*, but in latter library you’ll see duplicated comments in the wild, as boundaries of every dynamic portion of the DOM you will eventually update through its logic.

In both *hyper* and *lighterhtml* case, updates are performed throught the [**domdiff**](https://github.com/WebReflection/domdiff#domdiff) helper which uses just a node and any sort of algorithm to quickly compute the amount of changes needed between one DOM state, and another.

However, *lit-html* does also surprisingly well in common use cases for diffing, and I’ve created extra tests to be sure what I was testing made sense.

### Non Keyed *DOM diffing*

Press enter or click to view image in full size

![]()

Beside constant faster time in the initial creation, I wouldn’t say [lighterhtml](https://codepen.io/WebReflection/pen/WPyeGz?editors=0010) is any significantly faster than [lit-html](https://codepen.io/WebReflection/pen/omyvex?editors=0010) in these Code Pens.

### Keyed DOM diffing

Press enter or click to view image in full size

![]()

As already shown in the previous [js-framework-benchmark](https://github.com/krausest/js-framework-benchmark), [lighterhtml](https://codepen.io/WebReflection/pen/BMVBOx?editors=0010) is consistently faster, and yet I wouldn’t say it’s any relevantly faster than [lit](https://codepen.io/WebReflection/pen/MLXgPd?editors=0010).

## … so, who’s the winner ?

I think both *lighterhtml* and *lit-html* win on the Web, ’cause both provide a relatively straight forward and simple mechanism to create, and update, any sort of content.

In a Web populated by 50K minimum frameworks size on average, it makes literally no sense to compare *5K* VS *3.5K*, and what I’d rather compre, is what each framework provides for users.

### [lit-html](https://github.com/Polymer/lit-html#lit-html) pros

* [built-in directives](https://lit-html.polymer-project.org/guide/template-reference#built-in-directives) to simplified common tasks and easily extends the lib
* smallest core when *directives*, *repeat*, *style-map*, and *guard* functionalities are not needed
* blazing fast compared to any bigger framework 🏆

### [lighterhtml](https://github.com/WebReflection/lighterhtml#lighterhtml) pros

* [React like hooks](https://reactjs.org/docs/hooks-intro.html) out of the box through its `lighterhtml.hook(useRef)` feature and any *hooks* oriented project such as [augmentor](https://github.com/WebReflection/augmentor#augmentor), [dom-augmentor](https://github.com/WebReflection/dom-augmentor#dom-augmentor), or [TNG-Hooks](https://github.com/getify/TNG-Hooks), so that hooks can provide a way to extend renders as you need, just like *directives* would do
* simple to start, simpler to use when it comes to keyed items, with no need of a repeater and style maps out of the box
* widely backward compatible and transpilers resistant
* blazing fast compared to any bigger framework 🏆
* it always wins in terms of memory consumption
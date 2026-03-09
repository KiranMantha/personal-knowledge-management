---
title: "Implementing single file Web Components"
url: https://medium.com/p/22adeaa0cd17
---

# Implementing single file Web Components

[Original](https://medium.com/p/22adeaa0cd17)

# Implementing single file Web Components

[![Tomasz Jakut](https://miro.medium.com/v2/resize:fill:64:64/0*HXpQC8TeweXOa_am.)](/@ComandeerPL?source=post_page---byline--22adeaa0cd17---------------------------------------)

[Tomasz Jakut](/@ComandeerPL?source=post_page---byline--22adeaa0cd17---------------------------------------)

10 min read

·

Aug 21, 2018

--

12

Listen

Share

More

Press enter or click to view image in full size

![]()

Probably everyone who knows the [Vue framework](https://vuejs.org/) also heard about its [single file components](https://vuejs.org/v2/guide/single-file-components.html). This super simple idea allows web developers to define the entire code of a component in one file. It’s such a useful solution that [an initiative to include this mechanism in browsers](https://github.com/TheLarkInn/unity-component-specification) has already appeared. However, it seems quite dead as, unfortunately, no progress has been made since August 2017. Nevertheless, looking into this topic and trying to make single file components work in the browsers using the technologies already available was interesting enough to write an article about it!

## Single file components

Web developers who know the [Progressive Enhancement](https://www.smashingmagazine.com/2009/04/progressive-enhancement-what-it-is-and-how-to-use-it/) term are also aware of the “separation of layers” mantra. In case of components, nothing changes. In fact, there are even more layers, as now every component has at least 3 layers: content/template, presentation and behavior. If you use the most conservative approach, then every component will be divided into at least 3 files, e.g. a Button component could look like this:

In such an approach the separation of layers is equal to separation of technologies (content/template: HTML, presentation: CSS, behavior: JS). This means — if you don’t use any build tool — that the browser will have to fetch all 3 files. Therefore, an idea appeared to preserve the separation of layers, but without the separation of technologies. And then single file components were born.

Generally, I am quite sceptical about the “separation of technologies”. However, it comes from the fact that it’s often used as an [argument for abandoning the separation of layers](/@hayavuk/regardless-of-how-it-relates-to-styled-components-which-i-could-not-care-less-about-this-1c75825582d0) — and these two things are actually totally separated.

The Button component as a single file would look like this:

It’s clearly visible that a single file component is just Good Old HTML™ with internal styles and scripts + the `<template>` tag. Thanks to this approach that uses the simplest methods, you get a component that still has a strong separation of layers (content/template: `<template>`, presentation: `<style>`, behavior: `<script>`) without the need to create a separate file for every layer.

Yet the most important question remains: How do I use it?

## Fundamental concepts

Let’s start with creating a `loadComponent()` *global* function that will be used to load the component.

I used the [module pattern](https://addyosmani.com/resources/essentialjsdesignpatterns/book/#modulepatternjavascript) here. It allows you to define all necessary helper functions, but exposes only the `loadComponent()` function to the outer scope. For now this function does nothing.

And this is a good thing as you don’t have anything to be loaded yet. For the purpose of this article let’s say that you want to create a `<hello-world>` component that will be displaying text:

> Hello, world! My name is <*given name>*.

Additionally, after a click, the component should display an alert:

> Don’t touch me!

Save the code of the component as the `HelloWorld.wc` file (`.wc` stands for Web Component). At the beginning it will look like this:

For now you haven’t added any behavior for it. You only defined its template and styles. Using the `div` selector without any restrictions and the appearance of the `<slot>` element suggests that the component will be using [Shadow DOM](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_shadow_DOM). And it is true: all styles and the template will by default be hidden in shadows.

The use of the component on the website should be maximally simple:

You use the component like a standard [Custom Element](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_custom_elements). The only difference is the need to load it before using `loadComponent()` (that is located in the `loader.js` file). This function does the whole heavy lifting, like fetching the component and registering it via `customElements.define()`.

This sums up all the basic concepts, time to get dirty!

## Basic loader

If you would like to load the data from an external file, you must use immortal Ajax. But since it is already year 2018, you can use Ajax in the form of [Fetch API](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch):

Amazing! However, at the moment you only fetch the file, doing nothing with it. The best option to get its content is to convert the response to text:

As `loadComponent()` now returns the result of the `fetch()` function, it returns `Promise`. You can use that knowledge to check if the content of the component was really loaded and whether it was converted to text:

Press enter or click to view image in full size

![]()

It works!

## Parsing the response

However, the text itself doesn’t fulfill your needs. You were not writing the component in HTML just to [do the forbidden](https://stackoverflow.com/a/1732454). You are in the browser after all — the environment where the DOM was created. Use its power!

There is a nice `DOMParser` class in browsers that allows you to create a DOM parser. Let’s instantiate it to convert the component into some DOM:

First you create an instance of the parser (1), then you parse the text content of the component (2). It’s worth noting that you use the HTML mode (`'text/html'`). If you wanted the code to comply better with the JSX standard or original Vue components, you would use the XML mode (`'text/xml'`). However, in such case you would need to change the structure of the component itself (e.g. add the main element which will hold every other one).

If you now check what `loadComponent()` returns, you will see that it’s a complete DOM tree.

Press enter or click to view image in full size

![]()

And by saying “complete” I mean *really* complete. You have got a whole HTML document with `<head>` and `<body>` elements. As you can see, the contents of the component ended inside the `<head>`. It’s caused by the way in which the HTML parser works. [The algorithm of building the DOM tree](https://html.spec.whatwg.org/multipage/parsing.html#tree-construction) is described in details in HTML LS specifications. To TL;DR it, you could say that the parser will put everything inside the `<head>` element until it approaches an element that is allowed only in the `<body>` context. All elements (`<template>`, `<style>`, `<script>`) used by you, though, are also allowed in `<head>`. If you added e.g. an empty `<p>` tag to the beginning of the component, its entire content would be rendered in `<body>`.

To be honest, the component is treated as an *incorrect* HTML document, as it does not begin with a `DOCTYPE` declaration. Because of that it’s rendered using the so-called [quirks mode](https://developer.mozilla.org/en-US/docs/Web/HTML/Quirks_Mode_and_Standards_Mode). Fortunately, it does not change anything for you as you use the DOM parser only to slice the component into appropriate parts.

Having the DOM tree, you can get only the parts you need:

Move the whole fetching and parsing code into the first helper function, `fetchAndParse()`:

Fetch API is not the only way to get a DOM tree of an external document. `XMLHttpRequest` [has a dedicated document mode](https://jsfiddle.net/Comandeer/rokoxp7d/) that allows you to omit the whole parsing step. However, there is one drawback: `XMLHttpRequest` does not have a `Promise`-based API, which you would need to add by yourself.

## Registering the component

Since you have all the needed parts available, create the `registerComponent()` function which will be used to register the new Custom Element:

Just as a reminder: Custom Element must be a class inheriting from `HTMLElement`. Additionally every component will use Shadow DOM that will hold styles and template content. This means that every component will use the same class. Create it now:

You can create it inside `registerComponent()` as the class will use the information that will be passed to the mentioned function. The class will use a slightly modified mechanism for attaching Shadow DOM that I described in an [article about declarative Shadow DOM (in Polish)](https://blog.comandeer.pl/javascript/2017/10/31/deklaratywny-shadow-dom.html).

There is only one thing left connected with registering the component — giving it a name and adding to the collection of current page’s components:

If you tried to use the component now, it would work:

![]()

## Fetching the script’s content

The simple part is done. Now it’s time for something really hard: adding the layer of behavior and… a dynamic name for the component. In the previous step you hardcoded the component’s name, however, it should be delivered from the single file component. In the same way you should deliver information about event listeners that you want to bind to the Custom Element. Use the convention based on the one from Vue:

You can assume that the `<script>` inside the component is a module, so it can export something (1). That export is an object containing the component’s name (2) and event listeners hidden behind methods with a name starting with `on…` (3).

It looks nice and nothing leaks outside (as modules don’t exist in the global scope). Yet there is a problem: there is no standard for handling exports from internal modules (so the ones whose code is directly inside the HTML document). The import statement assumes that it gets a module identifier. Most often it’s a URL to the file containing the code. In case of internal modules, there is no such identifier.

But before you surrender, you can use a super dirty hack. There are at least two ways to force the browser to treat a given text as a file: [Data URI](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs) and [Object URI](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL).

[Stack Overflow also suggests the Service Worker](https://stackoverflow.com/a/46086545). However, for this case it looks like an overkill.

## Data URI and Object URI

Data URI is an older and more primitive approach. It’s based on converting the file content into a URL by trimming unnecessary whitespace and then, optionally, encoding everything using Base64. Assuming that you have such a simple JavaScript file:

It would look like this as Data URI:

You can use this URL just like a reference to a normal file:

However, the biggest drawback of Data URI becomes visible quite fast: as the JavaScript file is getting bigger, the URL becomes longer and longer. It’s also quite hard to put binary data into Data URI in a *sensible* way. This is why Object URI was created. It’s a descendant of several standards, including [File API](https://developer.mozilla.org/en-US/docs/Web/API/File/Using_files_from_web_applications) and HTML 5.x with its `<video>` and `<audio>` tags. The purpose of Object URI is simple: create a false file from the given binary data, which will get a unique URL working only in the context of the current page. To put it simpler: create a file in memory with a unique name. This way you get all advantages of Data URIs (a simple way to create a new “file”) without its drawbacks (you will not end up with a 100 MB string in your code).

Object URIs are often created from multimedia streams (e.g. in the `<video>` or `<audio>` context) or files sent via `input[type=file]` and drag&drop mechanism. Fortunately you can also create such files by hand, using the `File` and `Blob` classes. In this case use the `Blob` class, in which you will put the contents of the module and then convert it into Object URI:

## Dynamic import

There is one more issue, though: the import statement does not accept a variable as a module identifier. This means that apart from the used method to convert the module into a “file”, you will not be able to import it. So defeat after all?

Not exactly. This issue was noticed long ago and the [dynamic import proposal](https://developers.google.com/web/updates/2017/11/dynamic-import) was created. At the moment of writing this article (August 2018) it’s in the third phase of standardization, so the first implementations are appearing in browsers and other JavaScript environments. And using a variable as a module identifier alongside a dynamic import is no longer an issue:

As you can see, `import()` is used like a function and it returns `Promise`, which gets an object representing the module. It contains all declared exports, with the default export under the `default` key.

## Implementation

You already know what you must do, so you just need to do it. Add the next helper function, `getSettings()`. You will fire it before `registerComponents()` and get all necessary information from the script:

For now this function just returns all passed arguments. Add the entire logic that was described above. First, converting the script into an Object URI:

Next, loading it via import and returning the template, styles and component’s name received from `<script>`:

Thanks to that `registerComponent()` still gets 3 parameters, but instead of `<script>` it now gets the name. Correct the code:

*Voilà!*

## Layer of behavior

There’s one part of the component left: behavior, so handling events. At the moment you only get the component’s name in the `getSettings()` function, but you should also get event listeners. You can use the `Object.entries()` method for that. Return to `getSettings()` and add appropriate code:

The function became complicated. The new helper function, `getListeners()` (1), appeared inside it. You pass the module’s export to it (2). Then you iterate through all properties of this export using `Object.entries()` (3). If the name of the current property begins with `on…` (4), you add the value of this property to the `listeners` object, under the key equal to `setting[ 2 ].toLowerCase() + setting.substr( 3 )` (5). The key is computed by trimming the `on` prefix and switching the first letter after it to a small one (so you will get `click` from `onClick`). You pass the `listeners` object further (6).

Instead of `[].forEach()` you can use `[].reduce()`, which will eliminate the `listeners` variable:

Now you can bind the listeners inside the component’s class:

There is a new parameter in destructuring, `listeners` (1), and a new method in the class, `_attachListeners()` (2). You can use `Object.entries()` once more — this time to iterate through `listeners` (3) and bind them to the element (4).

After this the component should react to click:

![]()

And this is how you can implement single file Web Components 🎉!

## Browser compatibility and the rest of the summary

As you can see, a lot of work was put to create even a basic form of support for single file components. Many parts of the described system are created using dirty hacks (Object URIs for loading ES modules — FTW!) and the technique itself seems to have little sense without native support from the browsers. What’s more, at the moment of writing this article (August 2018) there is no support for Custom Elements nor dynamic import in Firefox. To be honest the whole thing works well only in Chrome. And because of that — for now — it’s a mere curiosity, not something really useful.

Yet creating something like that was a great fun. It was something *different* that touched many areas of the browser development and modern web standards. And I hope that there is at least one person that made it to this closing sentence!

Of course [the whole thing is available online](https://blog.comandeer.pl/assets/jednoplikowe-komponenty/).
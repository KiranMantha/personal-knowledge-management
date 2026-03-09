---
title: "Vanilla DOM VS hyperHTML"
url: https://medium.com/p/27e3c866acb5
---

# Vanilla DOM VS hyperHTML

[Original](https://medium.com/p/27e3c866acb5)

# Vanilla DOM VS hyperHTML

[![Andrea Giammarchi](https://miro.medium.com/v2/resize:fill:64:64/1*54OyE6rg-MdELwb9mW56Xw.png)](/?source=post_page---byline--27e3c866acb5---------------------------------------)

[Andrea Giammarchi](/?source=post_page---byline--27e3c866acb5---------------------------------------)

2 min read

·

Feb 11, 2018

--

1

Listen

Share

More

Comparing hyperHTML to [React](https://viperhtml.js.org/hyperhtml/examples/#!fw=React&example=Hello%2C%20world%20%26%20tick), [Vue.js](https://viperhtml.js.org/hyperhtml/examples/#!fw=Vue.js&example=Basic%20todos), [Marko](https://viperhtml.js.org/hyperhtml/examples/#!fw=Marko&example=basic%20counter) or others makes sense only if you are already one of these library/framework users and you’d like to see if it’s possible to implement the same via [hyperHTML](https://viperhtml.js.org/hyperhtml/documentation/).

But what if you are working on a good old school JS project, maybe helped by jQuery, and you’d like to simplify your life via some hyper magic?

## Relieving the boreDOM

Front End development is too often about repeating same tasks over and over and over again to create or update some content. I’ve personally learned by heart most of the DOM APIs writing same stuff infinite times: append some text content; create some element and set all the things … etcetera, etcetera

Not only I can finally type less to obtain exact same results in a safe, fast, and clean way, I can also write declarative layouts that better describe my intent.

## Custom Elements like life cycle hooks

Without needing any polyfill at all, it is possible to assign special life cycle events to any sort of DOM element via `onconnected` or `ondisconnected`.

Combined with third parts libraries or their plugins, these events make initialization of components horrendously simple.

If you’d like to know more in how many ways you could integrate a jQuery plugin with hyperHTML, have a look at [this Stack Overflow entry](https://stackoverflow.com/questions/48679519/using-an-external-library-with-hyperhtml) or this [live slider example](https://jsfiddle.net/4rc43sek/).

## Self closing tags & lightweight components

Inspired by XML and JSX, but unfortunately not a standard HTML behavior, hyperHTML makes creation of self contained elements a no brainer.

`` hyperHTML()`<i/><i/><i/>` ``

If we’d try to inject above string as `innerHTML` it will create an `<i>` containing an `<i>` containing an `<i>` instead of 3 `<i>` adjacent to each others.

Not only this is super handy when used together with `<custom-elements/>`, we can create our own components without even needing custom elements.

### … wait, and what about hyper.Component ?

Of course, there is the possibility to use classes too, and while I think this particular example would just work with a setup callback, for documentation sake this is how one could use the Component class:

## Pick your flavor!

As you can see, [hyperHTML](https://github.com/WebReflection/hyperHTML#hyperhtml) is flexible enough to adjust to any sort of coding style, simplifying layout creation beside just repeated updates.

It does not need its own render logic or container to be useful, it can be easily and gracefully integrated with any project you are working on right now.

Give it a try and if you really like it, [consider supporting it](https://opencollective.com/hyperhtml) too ❤️
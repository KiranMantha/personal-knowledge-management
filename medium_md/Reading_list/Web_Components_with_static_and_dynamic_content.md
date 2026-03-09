---
title: "Web Components with static and dynamic content"
url: https://medium.com/p/eb953d56e913
---

# Web Components with static and dynamic content

[Original](https://medium.com/p/eb953d56e913)

Press enter or click to view image in full size

![]()

# Web Components with static and dynamic content

## RE:DOM is the perfect tool for creating HTML components

[![Juha Lindstedt](https://miro.medium.com/v2/resize:fill:64:64/1*9fMF9SlF3LNVSulwIMaJkw@2x.jpeg)](/@pakastin?source=post_page---byline--eb953d56e913---------------------------------------)

[Juha Lindstedt](/@pakastin?source=post_page---byline--eb953d56e913---------------------------------------)

2 min read

·

Nov 10, 2017

--

Listen

Share

More

Google’s Polymer team have lately talked about this new way to create templates, [lit-html](https://github.com/PolymerLabs/lit-html), which is heavily copied from [HyperHTML](https://github.com/WebReflection/hyperHTML).

[Tagged template literals](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals#Tagged_template_literals_and_escape_sequences) provide a way to update components smarter, so that static content is untouched and only the dynamic part gets updated. There’s a lot of performance and memory benefits of doing that, compared to virtual dom approach, where you need to diff everything.

RE:DOM have always supported this by design. Instead of defining a single create/update method, you define constructor and update methods separately:

```
import { el } from 'redom';export class Hello {  
  constructor () {  
    this.el = el('h1', 'Hello world!');  
  }  
  update ({ greeting }) {  
    this.el.textContent = greeting;  
  }  
}
```

*Let’s use this component:*

```
import { mount } from 'redom';  
import { Hello } from './hello.js';const hello = new Hello();mount(document.body, hello);setTimeout(() => {  
  hello.update({ greeting: 'Hi RE:DOM!' });  
}, 2000);
```

*Result:*

```
<h1>Hi RE:DOM!</h1>
```

[*Fiddle with this example*](https://jsfiddle.net/gjkbwca1/)

The benefit of RE:DOM is that you can use **pure JavaScript** without learning and hassling with complicated templating languages. Browser support is also way better: [IE 6](https://redom.js.org/documentation/#browser-support) vs [latest evergreen](https://github.com/PolymerLabs/lit-html#status) (or with lots of polyfills).

RE:DOM is [one of the fastest](https://rawgit.com/krausest/js-framework-benchmark/master/webdriver-ts-results/table.html) view libraries there is, faster than almost any virtual dom library – including React. Memory usage is also very low, thanks to the class support and the way RE:DOM [uses the DOM](https://github.com/redom/redom/blob/master/src/setchildren.js).

Give RE:DOM a try: <https://redom.js.org>  
Questions? <https://gitter.im/redom/redom>

Happy JavaScripting! 😎
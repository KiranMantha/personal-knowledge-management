---
title: "Adopt a Design System inside your Web Components with Constructable Stylesheets"
url: https://medium.com/p/dd24649261e
---

# Adopt a Design System inside your Web Components with Constructable Stylesheets

[Original](https://medium.com/p/dd24649261e)

# Adopt a Design System inside your Web Components with Constructable Stylesheets

[![Benjamin Farrell](https://miro.medium.com/v2/resize:fill:64:64/0*XpFVw4HGa300sx7t.)](/@bengfarrell?source=post_page---byline--dd24649261e---------------------------------------)

[Benjamin Farrell](/@bengfarrell?source=post_page---byline--dd24649261e---------------------------------------)

11 min read

·

Jun 3, 2019

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

As someone who makes stuff on the web, there are two things that I’ve been seeing quite a bit lately: Web Component discussion and CSS debates. I think that Web Components, or more specifically the Shadow DOM, is poised to solve some long-standing CSS problems. I’m a big fan of Web Components. In fact, I’m just wrapping up a book with Manning Publications now, called [Web Components in Action](https://www.manning.com/books/web-components-in-action).

Let’s quickly review where we are with CSS. Personally, I really dig working with CSS, but I never got super fancy with it. Whenever I start working with Less or SASS, or start adopting BEM or similar methodologies, I keep coming back to just writing plain, no-frills CSS. Under normal conditions, what I’m doing is not maintainable…like, at all. One article that popped up on my twitter feed recently is [an argument against the Cascade](https://www.simontaggart.com/2019-01-11-im-super-good-at-css-and-i-dont-recommend-the-cascade-dont-@-me/). What?! “Cascading” is the first “C” in CSS!

Simon is right, though. Or, as right as you can be when generally speaking for all developers ever who make stuff on the web. Big projects have lots of CSS. As much as I love CSS, the more you have, the more brittle your page becomes. Rules start combining and snowballing together, until you’re debugging some crazy hard to find style or layout problems. It can also become a bit of a game of Wack-A-Mole. You spend an hour figuring out why a rule broke the thing it did, change it, but that breaks something else that you thought was unrelated.

It’s no wonder solutions keep being invented to manage this mess, including the latest CSS-in-JS and CSS Modules (not the upcoming CSS Modules browser feature). These two lean pretty heavily on your JS skills, not to mention your front-end tooling setups. I’m not going to argue against any solution that tries to solve a nasty problem that we’ve had for as long as CSS has been a thing, but I will say that I wish things didn’t have to be so complicated. I wish we could just use normal, straightforward CSS again.

### Web Components and the Shadow DOM

These days, I do! And it’s thanks to Web Components and the Shadow DOM. The Shadow DOM is the metaphorical moat around your UI component castle. It keeps out invading armies of selectors (both CSS and JS querySelectors).

Press enter or click to view image in full size

![]()

Saying the Shadow DOM keeps out selectors is an important distinction I’ve had to adjust to recently. I used to say it keeps out style, but something like the following actually does inject style through the Shadow DOM.

```
body {  
 color: red;  
}
```

The above style globally affects everything on your page. As such, all text will now be red (unless overridden by a more specific selector). It’s when you go deeper with some sort of selector, that the Shadow DOM successfully blocks your style. For example, if my Shadow DOM enabled Web Component contained a , we could style all buttons on the page leaving the Web Component buttons alone.

```
button {  
 color: red;  
}
```

The Shadow DOM doesn’t let outsiders know what’s inside. Your outside CSS has no idea that your Web Component contains a button, and therefore won’t style it. The button selector has nothing to latch onto inside the Shadow DOM.

Another way that styles can be let through is by using CSS Vars. These are simply variables that are defined in your CSS. If you really want that button inside your Shadow DOM to be red, you could define a button color var in CSS.

```
:root {  
  --button-color: red;  
}
```

Inside your component, your CSS could then use this variable to specify the button color.

```
button {  
  color: var(--button-color);  
}
```

All that is great — the Shadow DOM protects our Web Component from style intrusion, but how do you actually use CSS within the component? Well, it’s not perfect yet. In my mind, perfection would be to just point to a CSS file and load it up, styling the mini-DOM of your Web Component. Instead, we’re still relegated to using JS to do anything in the component.

As with most elements, the `shadowRoot` property of your Shadow DOM based Web Component has an `innerHTML` property that you can set. You'll typically set this to a long string of HTML and CSS to represent an entire mini-DOM making up your component. Don't worry, it's *really* not as bad as it sounds. With template literals (`), and ES6 Modules to separate out markup into different files to not clutter up your component logic, it's pretty clean. I cover this approach very extensively in my book.

```
this.shadowRoot.innerHTML = `  
<style>     
  :host {       
    background-color: blue;     
  }     
  button {       
    color: red;     
  }     
  #myspan {         
    color: green;   
  }   
</style>   
<div>   
  <span id="myspan"></span>   
  Example HTML Content    
  <button>Example Button</button>  
</div>`;
```

Regardless, we’re still putting CSS in a JS file. It’s not “CSS-in-JS”, because we’re not transforming it at all, but again, having a plain CSS file would be the dream. Aside from this minor hiccup, the brittleness in web development has been solved! Style won’t infect our component from the outside, and style from our component won’t affect the outside world. Notice in the code snippet above, where we’re styling a button with no extra class specificity. This isn’t just a simple example, it’s fairly routine not to worry about doing something like this because only the buttons in this Web Component are styled this way. Similar with the span with an ID. You’d never use the ID attribute like this in a small UI component because the ID has to be unique to the page. Not so with the Shadow DOM, the ID only needs to be unique within the component.

Using the Shadow DOM and Web Components is like going back to simpler times when web development wasn’t so complex and fragile, because we’ve redefined the scope of a huge application or page, to a *much* smaller and manageable one. But, there is a major missing piece in all of this.

The missing piece is a Design System, and that’s the rub. We want to bubble wrap our component and protect it from all outside style, yet at the same time, we want *just the right style* to come in and make the contents of our component look like the rest of the application or page.

CSS Vars are just the about the only established way to do this, but doing things one variable at a time is a Sisyphean task.

![]()

Wedging a Design System into a Web Component today means likely exploding an established CSS system into pieces, turning the bits into Javascript strings, and figuring out a way to bring them all together in a meaningful way inside your component, only loading the bits you need. The other bad thing with this approach, is that you’re creating a design system from scratch in each and every component instance on your page. Its tons of duplicated CSS inside every mini-DOM.

### Constructable Stylesheets

There are two brand new browser features poised to solve this problem. The first is CSS Shadow Parts/Theme. After spending a little time experimenting with Shadow Parts, it became clear that there is a lot of work to do around changing existing CSS to use “part” attributes in addition to classes. The design system is just one piece of the puzzle. There’s also a lot of onus on the Web Component developer to “export” parts through the the component into child components. The Shadow Theme feature sounds like it alleviates some of this, but unlike Shadow Parts, it’s not even supported by Chrome yet while Shadow Parts are *only* supported in Chrome right now.

The better option is the brand new “Constructable Stylesheets”. It’s not just better IMHO, it’s pretty close to perfect, and I think is poised to bring us back to our basic CSS roots in the Web Component world. Not, only is it already available in Chrome, but is easy to polyfill as well.

Constructable Stylesheets are an evolution rather than a brand new feature. Really we’re just extending the API of the Javascript `CSSStyleSheet` object. So, what's new?

It used to be that after creating a new stylesheet, you could only edit the list of CSS rules. Now, though, you can replace the entire sheet, wholesale.

```
const sheet = new CSSStyleSheet();  
sheet.replace(`@import url('directory/cssfile.css')  
  .then(sheet => {})  
  .catch(err => {});
```

Note that the above is using the async `replace` method. For loading stylesheets with the `@import` directive, the CSS won't be immediately loaded. That said, the new stylesheet is available right away.

The next question to answer is what can we do with that stylesheet? Well, now in Chrome, both the `document` and `shadowRoot` objects have an `adoptedStyleSheets` property. This property accepts an array of stylesheets.

So now, a CSS file, or multiple CSS files from a design system can be adopted by any number of Shadow DOM enabled Web Components on a page. Not only that, but these style sheets aren’t copies — you’re not loading your Web Component instances with tons of cloned design system instances as is the case today. Every component (and the document) can share the same sheets, as well as pick and choose *which* CSS to adopt.

Press enter or click to view image in full size

![]()

### Constructable Spectrum and Style Shelter

I hope you’re thinking this sounds as promising as I do! In theory, we can take a complete and unchanged design system and use it in Shadow DOM enabled Web Components! Instead of just writing a blog post that this is theoretically possible, I took that challenge on with a real design system. I just so happen to work as a prototyper at Adobe and love using Web Components in my work. [Adobe’s design system, Spectrum](http://opensource.adobe.com/spectrum-css), is something I use almost every day. Of course, I haven’t been able to use Spectrum in conjunction with the Shadow DOM, so I was really excited at the prospect of getting this to work.

Spectrum itself is pretty awesome, too. It’s recently been reworked with CSS Vars as the basis of everything. And then, if a monolithic design system isn’t what you’re after, individual components are delivered as well. With Spectrum, a developer can layer on CSS Vars, the Spectrum base, the theme (light/dark variations), and finally a handpicked set of component CSS.

Press enter or click to view image in full size

![]()

No *really*, I don’t just think Spectrum is awesome because I work at Adobe. It’s awesome because this fits extremely nicely with Web Components and Constructable Stylesheets. Each component can use some simple JS logic to adopt *exactly* the CSS it needs. Every component adopts the base CSS Vars and base system style. We can choose which theme to use and load those files as well. Last, each component should know exactly which Spectrum UI components it uses, and also load those CSS files. This also means that the index.html page doesn’t need to know anything about what components need to be included, nor link to any stylesheets itself. Every Web Component is completely self reliant.

All that’s missing is a global module that can keep a cache of all loaded sheets. Web Components can pull from this module, and if a CSS file has already been loaded, it will just deliver the cached sheet back. Before jumping in and getting Spectrum working inside my Web Components, I went to work and created [Style Shelter](https://github.com/bengfarrell/style-shelter) (also available on [NPM](https://www.npmjs.com/package/style-shelter)). In addition to caching, most sheets need to be adopted by the Web Components, but some (root level CSS Vars) need to be adopted by the `document`, so Style Shelter also handles adopting different sheets to different scopes.

I’m excited to say that my challenge to use Spectrum without changing any CSS worked like a charm! I knew I had to be thorough, too. Every CSS component needs to work, so I forked the Spectrum CSS repo and created [a Web Component based demo page](https://bengfarrell.github.io/spectrum-css). I did run into some nuances to solve that were Spectrum specific, but you can read all about those details on [the project’s readme](https://github.com/bengfarrell/spectrum-css).

### Browser Support

So, browser support makes us come crashing back to planet earth. Right now only Chrome (and one would assume the new Chromium powered Edge) supports Constructable Stylesheets. Firefox and Safari supposedly are considering or are working on the feature now, however. Good news, though! There is a [polyfill](https://www.npmjs.com/package/construct-style-sheets-polyfill), and it’s easy to use. The only downside is that styles *are* copied over and over again, just like I promised we didn’t need to do. Take this Shadow DOM in Chrome, and notice that even though the component is styled perfectly, there’s no style in shown — it’s all adopted.

Press enter or click to view image in full size

![]()

Now, compare that to Firefox. With the polyfill, the component is styled the same, but we can see all the adopted styles copied to the Shadow DOM.

![]()

So, hopefully Safari and Firefox deliver the goods reallllllll quick! Delivering an entire design system to a Shadow DOM with no changes is a really big deal. And I’m probably pushing my luck, but I’m going to need to ask all the browser vendors to deliver CSS Modules, too.

### CSS Modules

The reason I want CSS Modules is not design system related. At the start of this article, I stated that I wanted plain, simple CSS again. Actual files, not CSS inside JS strings. I think it’s incredibly important that a well-built and shareable component be self-contained and not dependent on anything in the outside world. You might guess we can use Constructable Stylesheets here too, but there’s a small complication.

In my Constructable Spectrum demo, I do just that. I load up each component’s local style as an actual CSS file to be adopted. The problem is that stylesheet @imports are relative to the main index.html. So instead of pointing to ./mycomponent.css, I need to use the full path to my component’s CSS from the root of the project. Not great. Web Components should not need to know where they live in a project to function. They should be able to be moved around and used anywhere without thinking about these things.

JS modules, however, are loaded relative to whoever imported them. CSS Modules should be the same, and theoretically, you’ll get a CSSStyleSheet back…ready to be adopted. A nice bonus would be if the same CSS file is imported, it would be a reference to the same one that was loaded from a different Web Component. I don’t know if that’s the case in the spec, but it would certainly be AMAZING.

The Constructable Stylesheet approach is just gaining steam now and only supported in Chrome. Because of it’s uncertain future, I really couldn’t put them in my [Web Components in Action](https://www.manning.com/books/web-components-in-action) book. That said, I’m excited that approaches like what I’ve outlined are a natural extension of Web Components today.

With the Shadow DOM, Web Components, Constructable Stylesheets, and possibly CSS Modules, we’ve got something great here. We’re on the verge of getting simple and easy to use CSS back, and it’s exciting!
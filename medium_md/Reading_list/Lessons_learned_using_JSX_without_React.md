---
title: "Lessons learned using JSX without React"
url: https://medium.com/p/bbddb6c28561
---

# Lessons learned using JSX without React

[Original](https://medium.com/p/bbddb6c28561)

# Lessons learned using JSX without React

[![Aleks](https://miro.medium.com/v2/resize:fill:64:64/0*Sf4pk0rbATdwE7VM.jpg)](https://sometimes-react.medium.com/?source=post_page---byline--bbddb6c28561---------------------------------------)

[Aleks](https://sometimes-react.medium.com/?source=post_page---byline--bbddb6c28561---------------------------------------)

6 min read

·

Mar 6, 2018

--

1

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dbbddb6c28561&operation=register&redirect=https%3A%2F%2Fitnext.io%2Flessons-learned-using-jsx-without-react-bbddb6c28561&source=---header_actions--bbddb6c28561---------------------post_audio_button------------------)

Share

> [Click here to share this article on LinkedIn »](https://www.linkedin.com/cws/share?url=https%3A%2F%2Fitnext.io%2Flessons-learned-using-jsx-without-react-bbddb6c28561%3Futm_source%3Dmedium_sharelink%26utm_medium%3Dsocial%26utm_campaign%3Dbuffer)

Starting the project was the easy part, as every node project `yarn init -y` will create the barebones and is almost an every week task for a JS enthusiast so let’s not dig into that command; now the dependencies are very minimum, personally, I like to use webpack but, to keep it simple let’s just use babel:

`yarn add -D @babel/cli @babel/core @babel/plugin-syntax-jsx @babel-plugin-transform-react`

The next step is also trivial, define a `.babelrc` file at the root and use this content:

```
{  
  “plugins”: [  
    “@babel/plugin-syntax-jsx”,  
    [“@babel/plugin-transform-react-jsx”, { “pragma”: “dom” }]  
  ]  
}
```

A little explanation is necessary at this point; with these steps, we are able to transpile `<h1>Hi</h1>` into `dom(“h1”, null, “Hi”)` by 2 things,

* Defining the pragma on the .babelrc is what will name the fn otherwise by default will do `React.createElement`
* Running one `@babel/cli` command but let’s use npm scripts from the `package.json` to keep it useful:

```
"scripts": {  
  "build": "babel example.js --out-dir lib"  
}
```

Now if you are reading this, chances are you already know what sort of thing is JSX (XML-based). With that out of the way, I had some struggle when I was asked to implement again a component that was previously written in React but in plain JS. the reason told was the component was so simple that became an overkill try to make every team at the organization use it as they will have to include a lot of dependencies for projects that little or nothing had to do with React, not that it wasn’t possible but a project that already includes angular 1.x or backbone just to name a few, barely wants to add React 16 without a heavy good reason.

### Starting the journey (research)

So how JSX works? Long story short transform HTML syntax inside js to a function with multiple arguments that replace the tag, attributes, and content like: `<h1 className=”headline”>Hi</h1>` into `dom(“h1”, { className: “headline” }, “Hi”)`, so my idea at the time was if I could reimplement what the dom() should do that’ll be it.

### Basic Steps

dom() has to read 3 arguments and the first argument will give me the name of the element that it’s supposed to be created then  
`const element = document.createElement(arg1)`, seems to be the way to go unless arg1 is not a string in which case will be a function from a component where `<CustomComponent />` will be `dom(CustomComponent, null, null)` and I’ll execute that function instead of creating a new element.  
The second argument, on the other hand, was an object so at least to start a basic merge should do the job.

```
function dom(tag, attrs, ...children) {  
  // Custom Components will be functions  
  if (typeof tag === 'function') { return tag() }  // regular html tags will be strings to create the elements  
  if (typeof tag === 'string') {  
      
    // fragments to append multiple children to the initial node  
    const fragments = document.createDocumentFragment()  
    const element = document.createElement(tag)    children.forEach(child => {  
       if (child instanceof HTMLElement) {   
         fragments.appendChild(child)  
       } else if (typeof child === 'string'){  
         const textnode = document.createTextNode(child)  
         fragments.appendChild(textnode)  
       } else {  
         // later other things could not be HTMLElement not strings  
         console.log('not appendable', child);  
       }  
    })    element.appendChild(fragments)    // Merge element with attributes  
    Object.assign(element, attrs)    return element  
  }  
}
```

For the second argument just `Object.assign(element, arg2)` and for the most part, it did it; finally for the third argument if is a string should add a node text, that was the defining part, because if the 3rd argument was a function just let the cycle begin again, So where we are:

* We can create new HTML elements
* We can also use custom components
* We can add classes and other simple string arguments
* We can add text or other elements as children
* We can render lists (siblings)

Not bad for the basics, here is an example of what was compatible at that stage, and the [commit](https://github.com/alecsgone/jsx-files/commit/e20f3ae964b3af5e20d6c7e1a8b4d94934436868) :

```
function Headline() {  
  return (  
    <h1 className="headline">Inital Line  
      <br />  
      new line  
    </h1>  
  )  
}function Main() {  
  return (  
    <div>  
      <Headline />  
      <p>Lorem ipsum</p>  
      <ul>  
        <li><a href="">anchor</a></li>  
        <li>2</li>  
        <li><a href="">anchor2</a> More</li>  
      </ul>  
    </div>  
  )  
}const app = document.querySelector('.app')  
app.appendChild(Main())
```

Let’s enumerate what we are missing, at least for an alpha version the top things that were a “must implement”:

* `Array.map( item => <tag>{item}</tag>)`
* Refs to implement event listeners or anything that needs access to the `HTMLNodeElement`
* Fragments (the current react component had them and I didn’t feel like re-writing into divs)

### A decent implementation (alpha)

Starting with map because is the one most commonly used, checking if the arg3 is an array we should be able to append the result of those functions on a document fragment and append later to the root, just as e.g. in the case of multiple LI the root will be UL/OL, ok that’s clear, now, siblings are extra arguments on the dom function not just an array as the last argument, I’m glad that we know by first hand what the first 2 arguments are and also thanks to babel we can just `fn(arg1, arg2, …arg3){}` and arg3 will always be an array even with one item, so we already have a function for that let’s just re-use it. [commit](https://github.com/alecsgone/jsx-files/commit/1ec5ad125cbcd4fc4c3ed30d7d9302a45048235f)

### 2 More features to go

Refs and Fragments were the only things missing so the ref was as easy as asking if one of the props on the second argument is named ref and pass a callback to the same node. [commit](https://github.com/alecsgone/jsx-files/commit/4ccbb319e01a8a79c85d8d58b3c6241c92e39646)  
At this point a had a rough idea of how React worked and it was a nice exercise, only missing fragments, the missing feature for so many versions of React, initially I created a function to export and be able to use it at that point I didn’t know what the function should look like I just returned the word Fragment for logging purposes, funny thing that was all, after I tried to log that word I realize that if the function returns [fragment](https://github.com/alecsgone/jsx-files/commit/5c011ba221760f468baa1b609eef2a8d9773dfb5) I should only return the children 😋 (still doesn’t work for the root app but who exports fragments as main functions? I hope not a lot of people 😉)  
With this basic, less than 50 lines here’s a full example of what you can accomplish.

```
import dom, { Fragment } from 'jsx-render'function Headline() {  
  return (  
    <Fragment>  
      <h1 className="headline">Hello this in an h1  
        <br />  
        new line  
      </h1>  
      <h2>Second Headline</h2>  
    </Fragment>  
  )  
}function Main() {  
  return (  
    <div>  
      <Headline />  
      <p>Lorem ipsum</p>  
      <ul>  
        <li><a href="">anchor</a></li>  
        <li>More</li>  
      </ul>  
      <ol> {items.map(item => <li>{item}</li>)} </ol>  
      <button ref={node => {   
        node.addEventListener('click', console.log)   
      }}>  
        Click Me!  
      </button>  
    </div>  
  )  
}const app = document.querySelector('.app')  
app.appendChild(Main())
```

### Conclusions / Tips / Gotchas / Q&A

* JSX beautifully gives you the possibility to implement your own pragma fn and is not that complicated.
* The migration from the React component was just a copy-paste because the component was stateless, only one click function to open a modal but a toggle of open/closed class doesn’t hurt anybody, so far so good.
* “if you implement events like that, what about the zombies?” — Well for how the company is structured right now the components will be used on static and very simple pages, there’s no story with SPA and because of that, it doesn’t really bother me that much.
* When the interactions are really simple as a click to toggle, you don’t need to react/redux, sometimes a 1-hour reimplementation can save you 30kb per load.
* How to implement Fragments blows my mind.

### Other approaches

After additional research, I also found a library that transpile to JSX but instead of creating a fn() per component to execute at runtime, it transforms every component directly into document.createElement, There are a few small missing features nothing to be worried about unless you need SVG support which we will talk/implement later.

### Notes

The example repo uses lerna in case you feel like giving it a try. [jsx-files/blueprint](https://github.com/alecsgone/jsx-files/tree/master/packages/blueprint)
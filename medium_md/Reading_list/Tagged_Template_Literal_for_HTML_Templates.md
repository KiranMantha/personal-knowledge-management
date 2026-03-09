---
title: "Tagged Template Literal for HTML Templates"
url: https://medium.com/p/4820cf5538f9
---

# Tagged Template Literal for HTML Templates

[Original](https://medium.com/p/4820cf5538f9)

# Tagged Template Literal for HTML Templates

[![TruckJS](https://miro.medium.com/v2/resize:fill:64:64/1*dhIGFUxu3BPh-qLtcYDohQ.jpeg)](/@trukrs?source=post_page---byline--4820cf5538f9---------------------------------------)

[TruckJS](/@trukrs?source=post_page---byline--4820cf5538f9---------------------------------------)

11 min read

·

Aug 7, 2017

--

2

Listen

Share

More

When tag template literals were first announced, my initial reaction was that they were an over-engineered solution for a problem that didn’t exist. We already had string concatenation. Creating a function that could run any kind of JavaScript while calculated the final HTML to return was easy. Yeah, string concatenation was usually hard to follow, but there was so much power in being able to write whatever JavaScript you might need.

In contrast template literals felt like a straightjacket. They only had variable interpolation and minimum logic support through the JavaScript ternary operator. Fast forward to today and I absolute love template literals and cannot stand using the addition operator to do string concatenation. What changed? I started experimenting with tagged template literals. These little wonders let you create your own DSL for handling the production of any kind of markup you can image. With the right tagged template literal you can say goodbye to Moustache, Backbone and other template engines. Oh, and Babel can transpile your tagged template literal results down to ES5 string concatenation for old-timey browsers.

## Tagging a Template Literal

A tagged template literal is really just a function that takes a template literal as its argument. Surprisingly, tagged template literals do not look like functions when you use them. Below is an example of one:

```
html`<div class='item'>${item}</div>`
```

As you can see, a tagged template literal looks just like a template literal, except for the name at the start, right before the first back tick. For this to work you need to define a tagged template literal. Fortunately, the definition is a normal JavaScript function. This function will take one argument — a template literal. Internally you’ll have access to it as a raw string. You can find out more about the general ways of manipulating a tagged template literal’s arguments at [Mozilla](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Template_literals). For now, we’re going to look at how to create a tagged template literal for HTML template production.

## Make it Function

We’ll start by creating a function that takes an argument, which will be a template literal:

```
function html(literal) {  
  // Do stuff here  
}
```

We can then use our function like this:

```
html`<div>${stuff}</div>`
```

Actually, we need to do some processing in our function before it can return anything, so let’s see how to do that. Template literals expose their internal structure through the `raw` property. We can therefore access it like this:

```
function html(literals, ...vars) {  
  let raw = literals.raw  
}
```

The first part of the `raw` property is an array of all the string portions of the template literal, the rest parameter `...vars` captures all the variables used in that template literal.

We’ll need a few more variables to make this work: `result`, `i`, `len`, `str` and `variable`:

```
function html(literals, ...vars) {  
  let raw = literals.raw   
  result,  
  i,  
  len,  
  str,  
  variable  
}
```

From these variables you can see that we are going to do some looping and then return the result as `result`.

## Concatenation

So although the purpose of using a tagged template literal is to avoid string concatenation, internally in our tag function we will have to do a some concatenation. The irony, right? The good part is that it isn’t a lot, it isn’t hard to understand, and we only have to do it here. Once this is done, we won’t need to use string concatenation again for our template needs. First we are going to to use a `while` loop:

```
function html(literals, ...vars) {  
  let raw = literals.raw   
  result,  
  i = 1,  
  len = arguments.length,  
  str,  
  variable   
  while(i < len) {   
    // Do stuff here  
    i++  
  }  
}
```

So, where it says `// Do stuff here` is where we will have to take all the raw pieces of a template literal and concatenate them together as a string which we can return. The first thing we want to get is the string part of our template literal. This will probable constitute an opening HTML tag, although technically there might not be anything more than a variable to interpolate. Regardless, we need to examine the string array and grab the pieces.

```
function html(literals, ...vars) {  
  let raw = literals.raw   
  result,  
  i = 1,  
  len = arguments.length,  
  str,  
  variable   
  while(i < len) {   
    str = raw[i =1]  
    // Do stuff here  
    i++  
  }  
}
```

## Variables

The next thing we want to do is get all the variables that were used in the template literal. As we mentioned earlier, the rest parameter `...args` will capture all the variables used in the template literal. Since this is an array, we’ll need to reduce the `i` value by 1 when accessing the `args` array:

```
function html(literals, ...vars) {  
  let raw = literals.raw   
  result,  
  i = 1,  
  len = arguments.length,  
  str,  
  variable   
  while(i < len) {   
    str = raw[i =1]  
    variable = vars[i -1]  
    // Do stuff here  
    i++  
  }  
}
```

## Put it Together

Now we just need to combine our strings with our variables to get the final result:

```
function html(literals, ...vars) {  
  let raw = literals.raw   
  result,  
  i = 1,  
  len = arguments.length,  
  str,  
  variable   
  while(i < len) {   
    str = raw[i =1]  
    variable = vars[i -1]  
    result += str + variable  
    // Do stuff here  
    i++  
  }  
}
```

There’s still one final step, we need to grap the very last string value and close the whole template off:

```
function html(literals, ...vars) {  
  let raw = literals.raw,  
  result = '',  
  i = 1,  
  len = arguments.length,  
  str,  
  variable  
    
  while (i < len) {  
    str = raw[i - 1]      
    variable = vars[i -1]  
    result += str + variable  
    i++  
  }  
  result += raw[raw.length - 1]  return result  
}
```

## Make it Functional

So, we have a tagged template literal that can take a template and data and return a string. The problem is, the data needs to be existent at the time this is called or we’ll get an error about undefined variables. To get around this “feature” of template literals and tagged template literals, we can use our tagged template literal in a function. This will have as its argument the data that the template literal will consume. The data can be primitive types — strings, numbers, booleans — or complex types like an object, an array of primitive types or an array of objects.

I usually call my template function `render`, but you can call it whatever you want:

```
function render(data) => html`<div>${data}</div>`
```

## How to Render

We are going to create our render function. We want it to be able to handle different types of data — strings, numbers, objects and array. Most template engines have special syntax for array: ng-for, v-for, each{}, etc. We don’t want to have to bother. Just pass data to the render function and it should know how to process it. So, we want to check if the data is a primitive type, an object or an array:

```
function render(data, template) {  
  if (!template) return  
  if (typeof data === 'string') {  
    // Handle primitive type:  
    return template(data)  
  } else if (typeof data === 'object' && !Array.isArray(data)) {  
    // Handle object:  
    return template(data)  
  } else if (Array.isArray(data)) {  
    // Handle array:  
    return data.map(item => template(item)).join('')  
  }  
}
```

With the above render function we can handle strings, numbers, objects and arrays. This function expects to arguments: the data to use and a template. The template will be defined using the tagged template literal we defined earlier: `html`. Let’s look at some examples of using `html` with `render`.

## Template with String Data

```
const name = 'John Doe'  
const nameTemplate = (name) => html`<p>${name}</p>`  
const nameResult = render(name, nameTemplate)
```

The value of `nameResult` will be `<p>John Doe</p>`.

## Template with Object Data

Now let’s try a template that consumes an object:

```
const person = {  
  firstName: 'Joe',  
  lastName: 'Bodoni',  
  job: 'Mechanic',  
  age: 26  
}const personTemplate = (person) => html`  
  <p>Name: ${person.firstName} ${person.lastName}</p>  
  <p>Age: ${person.age}</p>  
  <p>Job: ${person.job}</p>`const obj = render(person, personTemplate)
```

The value of `obj` will be:

```
<p>Name: Joe Bodoni</p>  
<p>Age: 26</p>  
<p>Job: Mechanic</p>
```

## Template with Array

Now let’s see what happens when we pass our `render` function an array:

```
const people = [  
  {  
    firstName: 'Joe',  
    lastName: 'Bodoni'  
  },  
  {  
    firstName: 'Ellen',  
    lastName: 'Vanderbilt'  
  },  
  {  
    firstName: 'Sam',  
    lastName: 'Anderson'  
  }  
]const peopleTemplate = (person) => html`  
  <li>  
    ${person.firstName} ${person.lastName}  
  </li>`const listTemplate = render(people, peopleTemplate)
```

The value of `listTemplate` will be:

```
<li>Joe Bodoni</li>  
<li>Ellen Vanderbilt</li>  
<li>Sam Anderson</li>
```

By checking the data before rendering the template, we remove a big headache about worrying if the data is an object or array. Define your template to expect the properties you want. If the data is an object or array, it will render just fine. You never have to worry. You don’t have to think about it.

## Template to Nodes

So far we’ve got a render function that gives use back markup representing the HTML we would like to create. Now we need a way to turn the string of markup that the render function returns into actual nodes that can be inserted into the DOM. We could just use `innerHTML` to insert our string template into the DOM. But we want more flexibility that that. We want to be able to prepend, append, insert before and insert after.

There are several ways we could accomplish this, using `insertAdjacentHTML`, `createElement`, etc. We’re going to go with `createDocumentFragment` for a couple of reasons. First, when you insert a document fragment into the DOM, only its children get inserted. This means your fragment can have a bunch of siblings, such a list items, and when you insert the fragment into an unordered list, only the fragment children get inserted. This reasults in very efficient update of the DOM which better performance for layout and paint operactions.

Using create element, we would have to create an unordered list in memory, then loop over its children to append them one by one to the DOM. This is not very efficient as each append will cause a layout update and paint.

## createElement

Actually, we will use `innerHTML`, but in memory to create our nodes. Then we’ll append the resulting node to a document fragment and return it for insertion in the document.

```
function createElement(markup) {  
  const temp = document.createElement('div')  
  temp.innerHTML = markup  
  const frag = document.createDocumentFragment()  // Use childNodes to allow creating element nodes or text nodes:  
  const children = Array.prototype.slice.apply(temp.childNodes)  
  children.map(el => frag.appendChild(el))  
  return frag  
}
```

Notice how we use `childNodes`. This enables the function to create siblings that are element nodes or text nodes for mixed content. Because this is happening in memory, the processing is very fast. Now that we can create a document fragment, we need a way to insert it into the DOM. As I mentioned earlier, we want to be able to prepend, append, insert before and insert after.

## insert(target, fragment, position)

In order to insert a document fragement we first need to now into what we are inserting it. This is covered by the `target` parameter. We want to be able to use an actual DOM node or a selector, so we’ll need to test that value. Next we need to provide the document fragement to insert, and finally we can provide an optional position. If no position is provided, we will just append the fragment to the target. Otherwise we will insert the fragment based on the provided position. Based on these requirements, here is our insert function:

```
function insert(target, fragment, position) {  
  if (!node) return  
  let el  
  // Turn selector into fragment:  
  if (typeof target === 'string') {  
    el = document.querySelector(target)  
  } else if (target.nodeName) {  
    el = target  
  }  
  if (!position || position === 'append') {  
    el.appendChild(fragment)  
  } else if (position === 'prepend') {  
    el.insertBefore(fragment, el.firstChild)  
  } else if (position === 'before') {  
    el.parentNode.insertBefore(fragment, el)  
  } else if (position === 'after') {  
    el.parentNode.insertBefore(fragment, el.nextElementSibling)  
  }  
}
```

Of course, you don’t really need this function. But then, you don’t really need any utility fuction. However, that is not always the most practical way to write code. Abstractions exist to save us time by requiring less typing and less code to accomplish complex task. It also gives us one point to search for failures and one place to update how it works.

## Example of Template & Insertion

Let’s put all of this into some examples. We’ll start with a primitive type, then an object, and then an array of objects.

## Example of Primitive Type

We’ll make a simple template that inserts a username in a paragraph into a `div` in the document:

```
const name = 'John Smith'// Create markup from data and template:  
const nameTemplate = (name) => html`<p>${name}<p>`// Convert string markup into document fragment:  
const result = render(name, nameTemplate)  
const fragment = createElement(result)// Insert document fragment into DOM:  
insert('#userName', fragment)
```

Here’s the Codepen example:

## Example of Object

Now let’s see how to create a template that can render an object of data. To access the object’s properties, we use dot notation. Simple.

```
// Define object:  
const person = {  
  firstName: 'Joe',  
  lastName: 'Bodoni',  
  job: 'Mechanic',  
  age: 26  
}// Define template function:  
const personTemplate = (person) => html`  
  <p>Name: ${person.firstName} ${person.lastName}</p>  
  <p>Age: ${person.age}</p>  
  <p>Job: ${person.job}</p>`// Get result of render function:  
const obj = render(person, personTemplate)  
const fragment = createElement(obj)// Insert the document fragment into DOM:  
insert('#object', fragment)
```

Here’s the Codepen example:

## Example of Array

And finally, we are going to create a template that can output and array of objects:

```
const people = [  
  {  
    firstName: 'Joe',  
    lastName: 'Bodoni'  
  },  
  {  
    firstName: 'Ellen',  
    lastName: 'Vanderbilt'  
  },  
  {  
    firstName: 'Sam',  
    lastName: 'Anderson'  
  }  
]// Define template for array:  
const peopleTemplate = (person) => html`  
  <li>  
    ${person.firstName} ${person.lastName}  
  </li>`// Get document fragment of list items:  
const listTemplate = render(people, peopleTemplate)  
const fragment = createElement(listTemplate)// Insert document fragment into DOM:  
insert('#list', fragment)
```

Here’s the Codepen example:

## Updating the DOM

To recap everything, we can now create a template using a tagged template literal, we can convert its result into nodes and finally insert them in the DOM. We’re basically done. Just one last thing. We will implement a very crude way to update the DOM after the initial insertion of a template. This is not production updates. This is just to illustrate dynamically updating the DOM with our template code. Libraries and frameworks for production-ready projects use data diffing or virtual dom to calculate changes and update the DOM. This article is not about that. So, without further ado, here’s our *yes-I-wrote-this-but-it-does-work-and-is-only-for-show* function. It takes two arguments: the element to update and the document fragment to insert:

```
function updateElement(el, node) {  
  el.textContent = ''  
  el.appendChild(node)  
}
```

And here is how you could use this God-aweful function to actually update the DOM with your glorious tagged template literal:

Updating an object template result:

Updating an array template result:

## Security

As you may have noticed, this tagged template literal just renders the data. Seems simple. However, if the data comes from a third party, it might be compromised with script injection code. You can prevent this by sanitizing your data before passing it to your tagged template literal.

## Sanitation

The following function will escape questionable tags to prevent executable code being injected into the document.

```
function sanitize(data) {  
  const tagsToReplace = {  
    '&': '&amp;',  
    '<': '&lt;',  
    '>': '&gt;',  
    '(': '%28',  
    ')': '%29',  
  }  
  let str = JSON.stringify(data)  const replaceTag = function(tag) {  
    return tagsToReplace[tag] || tag  
  }  
    
  const safe_tags_replace = function(str) {  
    return str.replace(/[&<>\(\)]/g, replaceTag)  
  }  
  str = safe_tags_replace(str)  
  return JSON.parse(str)  
}
```

You would use this like this:

```
// Define template function:  
const personTemplate = (person) => html`  
  <p>Name: ${ sanitize(person.firstName) } ${ sanitize(person.lastName) }</p>  
  <p>Age: ${ sanitize(person.age) }</p>  
  <p>Job: ${ sanitize(person.job) }</p>`
```

This is article was about how to use tagged template literals for templating purposes. In our next article we’ll take these principles and use them to create a simple component architecture.
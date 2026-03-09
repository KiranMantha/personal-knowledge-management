---
title: "Write your Virtual DOM 2: Props & Events"
url: https://medium.com/p/a957608f5c76
---

# Write your Virtual DOM 2: Props & Events

[Original](https://medium.com/p/a957608f5c76)

# Write your Virtual DOM 2: Props & Events

[![deathmood](https://miro.medium.com/v2/resize:fill:64:64/1*GHAdR82a2YqtegoRlG-nIA.png)](/@deathmood?source=post_page---byline--a957608f5c76---------------------------------------)

[deathmood](/@deathmood?source=post_page---byline--a957608f5c76---------------------------------------)

8 min read

·

Jun 6, 2016

--

22

Listen

Share

More

![]()

Hi there!

I’m so happy to continue this topic and to share with you all the next things that eventually will allow us to move from the ‘baby’ Virtual DOM implementation to smth we can use in real projects.

Today we’ll talk mainly about setting/diffing attributes (props) and handling events. Ok, let’s go ;)

> It is the second article in series. If you’re new here be sure to read [introduction](/@deathmood/how-to-write-your-own-virtual-dom-ee74acc13060).

## Dealing with Babel

Before starting with props we need to fix one small gap in our previous implementation. When we have just node without attributes (props) like this:

```
<div></div>
```

Babel, when transpiling this will set ***props*** property of element to ‘null’, because there is no attributes. Thus we’ll have:

```
{ type: ‘’, props: null, children: [] }
```

It is better to set it to ***empty object*** by default — then we’ll not have errors while iterating properties (you’ll see it later). In order to fix that, we will modify our ***h(…)*** function like this:

```
function h(type, props, …children) {  
  return { type, props: props || {}, children };  
}
```

## Setting props

Setting props is really simple — you’ll see. Remember our DOM representation? There we store props like plain JS object, so for this markup:

```
<ul className=”list” style=”list-style: none;”></ul>
```

We’ll have such in-memory representation:

```
{   
  type: ‘ul’,   
  props: { className: ‘list’, style: ’list-style: none;’ }   
  children: []  
}
```

Thus each field in ***props*** object is ***attribute name***, and value of this field is ***attribute value***. So we only need to set this things on real DOM node. Let’s write a function-wrapper around ***setAttribute(…)*** method:

```
function setProp($target, name, value) {  
  $target.setAttribute(name, value);  
}
```

Well now that we know how to set one attribute (prop) — we can set them all, just iterating through all fields of ***props*** object:

```
function setProps($target, props) {  
  Object.keys(props).forEach(name => {  
    setProp($target, name, props[name]);  
  });  
}
```

Now remember ***createElement(…)*** function? We’ll just ***setProps(..)*** there immediately after real DOM node creation:

```
function createElement(node) {  
  if (typeof node === ‘string’) {  
    return document.createTextNode(node);  
  }  
  const $el = document.createElement(node.type);  
  setProps($el, node.props);  
  node.children  
    .map(createElement)  
    .forEach($el.appendChild.bind($el));  
  return $el;  
}
```

But this is not the end. We’ve forgotten some small things. First, ‘class’ is reserved word in JS so we’ll not use it as property name. We’ll use ‘className’:

```
<nav className=”navbar light”>  
  <ul></ul>  
</nav>
```

But there is no ‘className’ attribute in real DOM, so we should handle this in our ***setProp(…)*** function.

Another thing is that I found it to be more convenient to set boolean DOM attributes (e.g. checked, disabled) with boolean value like here:

```
<input type=”checkbox” checked={false} />
```

In this sample I expect that ‘checked’ attribute won’t be set on real DOM element. But in reality it will, ’cause as you know existence of this property is enough for it to be set. So we need to fix that. Notice that we’re not only setting attribute, but also setting corresponding boolean property on element reference:

```
function setBooleanProp($target, name, value) {  
  if (value) {  
    $target.setAttribute(name, value);  
    $target[name] = true;  
  } else {  
    $target[name] = false;  
  }  
}
```

Ok. And the last thing to say here is custom properties. I mean, that it is our own implementation, so in future we might want to have properties that have different role and should not be displayed in DOM. So we’ll write a function to check if this property is custom or not. For now it will be empty, ’cause we do not have any custom properties yet:

```
function isCustomProp(name) {  
  return false;  
}
```

And here is our completed ***setProp(..)*** function that fixes all the problems above:

```
function setProp($target, name, value) {  
  if (isCustomProp(name)) {  
    return;  
  } else if (name === ‘className’) {  
    $target.setAttribute(‘class’, value);  
  } else if (typeof value === ‘boolean’) {  
    setBooleanProp($target, name, value);  
  } else {  
    $target.setAttribute(name, value);  
  }  
}
```

Now let’s test that in JSFiddle:

## Diffing props

Ok, now that we can create elements with props, it’s time to think of how to diff them. Well, eventually it comes to either ***setting*** property or ***removing*** it. We have already written functions that are able to ***set props***, now let’s write functions that can ***remove*** them. Actually it is very straightforward process and I won’t even comment it:

```
function removeBooleanProp($target, name) {  
  $target.removeAttribute(name);  
  $target[name] = false;  
}function removeProp($target, name, value) {  
  if (isCustomProp(name)) {  
    return;  
  } else if (name === ‘className’) {  
    $target.removeAttribute(‘class’);  
  } else if (typeof value === ‘boolean’) {  
    removeBooleanProp($target, name);  
  } else {  
    $target.removeAttribute(name);  
  }  
}
```

Now let’s write a function ***updateProp*** that will compare two properties — old and new and modify real DOM node according to result of that comparation. Actually we have to handle next cases:

* There is no property with such name on a ***new node*** — thus we need to remove it

![]()

* There is no property with such name on ***old node*** — thus we need to set it

![]()

* Property with such name exists both on a ***new*** and ***old*** nodes — then we need to compare their ***values*** — if they are not equal we need to set that property again with value of the ***new node***

Press enter or click to view image in full size

![]()

* In other cases property hasn’t changed and we do not need to do anything

Ok. Here is the function that does exactly the same to one prop:

```
function updateProp($target, name, newVal, oldVal) {  
  if (!newVal) {  
    removeProp($target, name, oldVal);  
  } else if (!oldVal || newVal !== oldVal) {  
    setProp($target, name, newVal);  
  }  
}
```

Isn’t that was simple? But node can have more than one property — so let’s write a function that will be able to iterate through all props and call ***updateProp(…)*** function for each pair:

```
function updateProps($target, newProps, oldProps = {}) {  
  const props = Object.assign({}, newProps, oldProps);  
  Object.keys(props).forEach(name => {  
    updateProp($target, name, newProps[name], oldProps[name]);  
  });  
}
```

Notice here we are creating compound object, that contains both props of new and old node. Thus, while iterating through props we might have some `undefined`s but that is ok — our function can handle it.

The last thing is to put that function in our ***updateElement(…)*** function (remember it from our previous journey?). Where should we put it? Well probably if node hasn’t changed and we are going to diff its children we might want to check its properties before. So we put that in the last `if` clause right before diffing child nodes:

```
function updateElement($parent, newNode, oldNode, index = 0) {  
  ...  } else if (newNode.type) {  
    updateProps(  
      $parent.childNodes[index],  
      newNode.props,  
      oldNode.props  
    );  
   
    ...  
  }  
}
```

And this is it. Go forward and test it:

## Events

Of course to have a normal dynamic app we need to know how handle events. Well at this point we could already ***querySelector(…)*** our nodes by e. g. class and then ***addEventListener(…)*** to them. But it is not interesting. Actually I would like to have smth like in React:

```
<button onClick={() => alert(‘hi!’)}></button>
```

Yeah, this looks cool. Well, as you see we are using ***props*** here to declare an event listener. And our property name starts with `on` prefix:

```
function isEventProp(name) {  
  return /^on/.test(name);  
}
```

To extract ***event name*** from the ***prop name*** we’ll write next function (it just removes `on` prefix):

```
function extractEventName(name) {  
  return name.slice(2).toLowerCase();  
}
```

It seems, that if we are declaring our events in ***props*** object, then we should handle them in our ***setProps(..)/updateProps(…)*** functions. But think again about it. How can you really ***diff functions***? How?

You can’t compare them with equal signs. Well, you can use ***toString()*** method and compare code of the functions. But here we’ve go some problems. There are some functions with native code inside so we can’t diff them in such way:

![]()

Of course we could handle that with event bubbling — we could write our own event manager that will be attached to `body`or to root element and will handle all events of inner elements. Thus we could re-add event listeners on each update and that will not be so expensive.

But will not try to do that here. It adds more problems and in reality our event listeners are not changing so often. So let’s set our event listeners only ***once*** atelement creation.

So we do not want our ***setProps(…)*** function to set this events props on real DOM node. We want to handle adding event listeners ourselves. Ho to do this? Remember our function for checking for custom props? Now it won’t be empty:

```
function isCustomProp(name) {  
  return isEventProp(name);  
}
```

Adding event listeners when we know a real DOM node and have ***props*** object is also very straightforward:

```
function addEventListeners($target, props) {  
  Object.keys(props).forEach(name => {  
    if (isEventProp(name)) {  
      $target.addEventListener(  
        extractEventName(name),  
        props[name]  
      );  
    }  
  });  
}
```

Let’s put that in our ***createElement*** function:

```
function createElement(node) {  
  if (typeof node === ‘string’) {  
    return document.createTextNode(node);  
  }  
  const $el = document.createElement(node.type);  
  setProps($el, node.props);  
  addEventListeners($el, node.props);  
  node.children  
    .map(createElement)  
    .forEach($el.appendChild.bind($el));  
  return $el;  
}
```

## Re-adding events

What if you really need to re-add event listener? Let’s keep it simple. There is one very simple solution. But unfortunately it harms performance. We will introduce one more custom property called `forceUpdate`. Remeber, how we check if node changed? We will modify this function:

```
function changed(node1, node2) {  
  return typeof node1 !== typeof node2 ||  
         typeof node1 === ‘string’ && node1 !== node2 ||  
         node1.type !== node2.type ||  
         node.props.forceUpdate;  
}
```

So if `forceUpdate` is true the node will be entirely recreated and thus new event listeners will be added. We should handle it also here, ’cause we do not want this prop to be set on a real DOM node:

```
function isCustomProp(name) {  
  return isEventProp(name) || name === ‘forceUpdate’;  
}
```

And that’s pretty much all. Yeah, this solution is bad for performance. But it is simple :))

Go ahead and test it:

## Conclusion

And that’s it :)) Hope that it was interesting for you. If you know a simple way to diff event listeners it would be great if you share your ideas in comments.

In the next article we are going to write a custom component system for our Virtual DOM :))
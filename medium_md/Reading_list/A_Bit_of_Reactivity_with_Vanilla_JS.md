---
title: "A Bit of Reactivity with Vanilla JS"
url: https://medium.com/p/bde8f1a40479
---

# A Bit of Reactivity with Vanilla JS

[Original](https://medium.com/p/bde8f1a40479)

Member-only story

# A Bit of Reactivity with Vanilla JS

## Is reactive programming difficult with simple standard tools?

[![Giorgio Di Falco](https://miro.medium.com/v2/resize:fill:64:64/1*i4LcT6xUTYkq05IuZHlzpA.png)](https://medium.com/@giorgio.difalco?source=post_page---byline--bde8f1a40479---------------------------------------)

[Giorgio Di Falco](https://medium.com/@giorgio.difalco?source=post_page---byline--bde8f1a40479---------------------------------------)

8 min read

·

Apr 3, 2023

--

2

Listen

Share

More

![]()

A few days ago, I read an interesting article by [Michele Rullo](https://medium.com/@Mikepicker) on how to create a responsive web page using pure JavaScript:

[## Unravel Reactivity in 16 lines of Vanilla JS

### You are a frontend engineer.

medium.com](https://medium.com/@Mikepicker/unravel-reactivity-in-16-lines-of-vanilla-js-af13b185a733?source=post_page-----bde8f1a40479---------------------------------------)

His example draws attention to two aspects of reactive programming:

1. “marking” HTML elements with custom attributes that declare the relationship between elements and data
2. using Proxies to “add” reactive behaviors to standard objects

However, Michele’s example is all too simple, so I wondered if and how to exploit the same ideas (proxies and custom attributes) in a situation a little closer to the needs of a realistic Web application.

Doing this is also an opportunity to learn more about the nature and value of the solutions proposed by the most popular JavaScript frameworks (React, Angular, Vue, etc.). Are they Rube Goldberg machinery, *over-engineered or overly complicated devices designed to perform a simple task,* or do they have a raison d’être and are a better solution than rough homemade implementations?

## My case study

The case study I chose is very traditional: a web page displays a list of items as an HTML table. The elements come from an array of JavaScript objects. I want to get every manipulation of the array reflected, in a reactive way, on the visual part, with a piece of code as simple as possible.

My exercise is a variation of what I proposed in a recent [article](https://medium.com/javascript-in-plain-english/7-1-javascript-frameworks-compared-a58f8f16239a) where I compare 8 different JavaScript frameworks with the help of ChatGPT. Again, I use the product list returned by the public API [*https://dummyjson.com/products*](https://dummyjson.com/products). This time, however, the code is the result of my hands. The web page is pictured below:

Press enter or click to view image in full size

![Web page for the experiment]()

The page contains a table of products, formatted with *bootstrap* and equipped with some buttons used for the experiment, which I will talk about later. If you’re in a hurry, the full HTML and JavaScript code is available on [github](https://gist.github.com/geomago/56cac7d102f0a67cf204e3099c82394c).

## Filling the table

The first problem to solve is to create the table from the data. In these cases, the best way is not to directly generate HTML elements from JavaScript but to use an HTML template to transform the array of products into a sequence of table rows.

In the various frameworks available, a problem of this type is solved in several different ways, as shown in the code fragments below:

```
<!-- REACT -->  
{products.map((product) => (  
  <tr key={product.id}>  
    <td>{product.id}</td>  
    <td>{product.title}</td>  
    <td>{product.description}</td>  
    <td>{product.price}</td>  
    <td>  
      <img  
        src={product.thumbnail}  
        alt={product.title}  
        style={{ maxWidth: 100 }}  
      />  
    </td>  
  </tr>  
))}  
  
<!-- ANGULAR -->  
<tr *ngFor="let product of products">  
  <td>{{product.id}}</td>  
  <td>{{product.title}}</td>  
  <td>{{product.description}}</td>  
  <td>{{product.price}}</td>  
  <td><img [src]="product.thumbnail" [style.width.px]="100"></td>  
</tr>  
  
<!-- VUE -->  
<tr v-for="product in products" :key="product.id">  
  <td>{{ product.id }}</td>  
  <td>{{ product.title }}</td>  
  <td>{{ product.description }}</td>  
  <td>{{ product.price }}</td>  
  <td><img :src="product.thumbnail" :style="{ maxWidth: '100px' }"></td>  
</tr>  
  
<!-- SVELTE -->  
{#each products as product}  
  <tr>  
    <td>{product.id}</td>  
    <td>{product.title}</td>  
    <td>{product.description}</td>  
    <td>${product.price.toFixed(2)}</td>  
    <td class="thumbnail">  
      <img src={product.thumbnail} alt="Thumbnail"/>  
    </td>  
  </tr>  
{/each}  
  
<!-- SOLID -->  
{products.map((product) => (  
  <tr>  
    <td>{product.id}</td>  
    <td>{product.title}</td>  
    <td>{product.description}</td>  
    <td>${product.price.toFixed(2)}</td>  
    <td>  
      <img  
        src={product.thumbnail}  
        alt={product.title}  
        style="max-width: 100px"  
      />  
    </td>  
  </tr>  
))}  
  
<!-- ALPINE -->  
<template x-for="product in products" :key="product.id">  
    <tr>  
        <td x-text="product.id"></td>  
        <td x-text="product.title"></td>  
        <td x-text="product.description"></td>  
        <td x-text="product.price"></td>  
        <td><img :src="product.thumbnail" alt="thumbnail"></td>  
    </tr>  
</template>
```

As you can see, the proposed solutions always include a type of placeholders (e.g. *{product.title}* ) to specify where values must go, plus custom attributes (e.g. *v-for, \*ngFor )* to define in a more or less declarative way the link between the data (products) and the rows of the table.

In my experimentation, I want to achieve the same results using only pure HTML and JavaScript. Specifically, I decided to

1. add only standard [data-\*](https://developer.mozilla.org/en-US/docs/Learn/HTML/Howto/Use_data_attributes) attributes  
2. use standard HTML [templates](https://developer.mozilla.org/en-US/docs/Web/Web_Components/Using_templates_and_slots)  
3. omit everything redundant

Here is my HTML fragment for the table composition:

```
<tbody>  
  <template id="product-table-row">  
    <tr data-field="index:data">  
      <td data-field="id" class="text-right"></td>  
      <td data-field="title"></td>  
      <td data-field="description"></td>  
      <td class="text-right">  
        <span data-field="price"></span>  
        <button data-field="index:data" class="btn btn-light plus">+</button>  
      </td>  
      <td><img data-field="thumbnail:src"></td>  
      <td>  
        <button data-field="index:data" class="btn btn-danger delete">Delete</button>  
      </td>  
    </tr>  
  </template>  
</tbody>
```

First, note that I haven’t specified any explicit loop to generate the rows because there is no need: the template will be replicated as many times as there are occurrences of the array to which I will apply it.

Second, I didn’t use placeholders but rather added data-\* attributes to establish the link between elements and data.

Let’s start by seeing the code for loading the data and generating the rows:

```
{  
  let rowTemplate = document.getElementById('product-table-row');   
  let trow = rowTemplate.content;        // row template  
  let tbody = rowTemplate.parentElement; // container (tbody)  
  let products; // products array  
  
  fetch("https://dummyjson.com/products")  
    .then(response => response.json())  
    .then(data => {  
      products = data.products;  
      renderArray(products, trow, tbody); // create the table  
  });  
  
  let renderArray = (arr, trow, container) => {  
    arr.forEach((item, index) => { // loop over items  
      let newRow = trow.cloneNode(true); // create an empty row from template  
      applyData(newRow, item, index);    // apply data to HTML elements in the template  
      container.appendChild(newRow);     // append row to container  
    });  
  }  
}
```

“*renderArray*” is a general function which receives an array of objects, an HTML fragment and a container. It produces as many copies of the model as there are objects in the array and adds them to the container.

Each row is formatted by calling the “*applyData*” generic function, which is responsible for injecting object’s properties into an HTML fragment, marked with appropriate data-\* attributes:

```
// Generic function to apply data to HTML elements  
let applyData = (element, object, index) => {  
  element.querySelectorAll('[data-field]').forEach((item) => {  
    object.index = parseInt(index);  
    let [field, target] = item.dataset.field.split(':');  
    let value = object[field];  
    if (target===undefined) {  
      item.innerHTML = value;   
    } else {  
      item.setAttribute(target, value);  
    }  
  });  
}
```

I use one custom attribute (*data-field*), according to a convention. It may have one two forms:

```
data-field="name"  
  
data-field="name:attr"
```

The given *name* is the name of one of the object’s properties, whose value is to be injected. In the first case, it means that the value replaces the *innerText* of the element. In the second case, it replaces the indicated attribute (see for example *data-field=”thumbnail:src”* used for the *img* tag).

Note the *index at* the third argument of the function: it tracks the originating index of the item in the array, and I’ll use it in the button handlers.

This is how the generated HTML for one row looks like:

```
<tr data-field="index:data-index" data-index="7">  
  <td data-field="id" class="text-right">8</td>  
  <td data-field="title">Microsoft Surface Laptop 4</td>  
  <td data-field="description">Style and speed. Stand out on HD video calls backed by Studio Mics. Capture ideas on the vibrant touchscreen.</td>  
  <td class="text-right">  
    <span data-field="price">1499</span>  
    <button data-field="index:data-index" class="btn btn-light plus" data-index="7">+</button>  
  </td>  
  <td><img data-field="thumbnail:src" src="https://i.dummyjson.com/data/products/8/thumbnail.jpg"></td>  
  <td>  
    <button data-field="index:data-index" class="btn btn-danger delete" data-index="7">Delete</button>  
  </td>  
</tr>
```

Transforming the product array into an HTML table is done. Now let’s see how to synchronize the products array with its visual representation.

## Making it reactive

The next goal is to find an easy way for the HTML table to adapt to transformations performed on the data. In particular, I want to be able to propagate three types of change from data to HTML:

1. cancellation of a product
2. reordering of the product list
3. modification of properties of a product

For this purpose, I use a [Proxy](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Proxy) object that wraps the array of products to intercept the operations of assignment and deletion of the products. The creation of the *products* array changes from

```
products = data.products;
```

to

```
// Wrap the product array with a proxy  
products = new Proxy(data.products, {  
    
  set: (target, property, value, receiver) => {  
    if (property == "length") {  
      Reflect.set(target, property, value, receiver);  
      return true; // Reflect.set return false, but must be done  
    } else {  
      var row = tbody.querySelector(`tr[data-index="${property}"]`);  
      if (!row) return; // no provision for push  
      applyData(row, value, property); // apply data to HTML elements in the row  
      return Reflect.set(target, property, value, receiver); // allow standard continuation  
    }  
  },  
  
  deleteProperty: (target, property) => {  
    tbody.querySelector(`tr[data-index="${property}"]`)?.remove();  
    return Reflect.deleteProperty(target, property); // allow standard continuation  
  }  
});
```

Two methods are defined:

**set**: enters when a property is changed. As this object is an array, its properties are the *indexes* and the *length* property. Any operation that changes the content of an array’s item or changes the array length results in a call to this function. My implementation, does nothing if the property name is *length*, but re-render the row if the property is an *index.* In both cases, it ends up by calling *Reflect.set* to ensure that the system completes its default actions.

**deleteProperty**: enters when an item is removed from the array, for example, with a *delete products[x]* statement, but also as a consequence of a *products.splice* or a *products.shift.* The only action needed in my case study is to remove the corresponding table row, identified via the *data-index* attribute.

To test these cases, I provided a “Sort” button to sort the whole array based on the product title and a “Delete” button on each line, which removes the corresponding item using a *products.splice*. This is the simple code behind the Sort and Delete buttons:

```
// Sort by title  
document.getElementById('sort').addEventListener('click', () => {  
  products.sort((a, b) => {  
    return a.title.localeCompare(b.title)  
  });  
});  
  
// Add listeners to all delete buttons  
document.querySelectorAll('tbody button.btn-danger').forEach((item) => {  
  item.addEventListener('click', deleteRow);  
});  
  
// Delete a row  
let deleteRow = (event) => {  
  var btn = event.target;  
  products.splice(btn.dataset.index, 1);   
}
```

You can try both loading the page from this [***gist***](https://gist.github.com/geomago/56cac7d102f0a67cf204e3099c82394c).

As for the last item on my agenda, “changing a product’s properties”, the problem is that a change to a product’s property doesn’t trigger any methods in my Proxy because it’s not a change to a property of the array of products.

The little ‘+’ button on each row (which has the effect of increasing each price by 1) allowed me to test this situation as well. There are at least two ways to make the displayed price react to the change of the price property on the single product, as shown in the code below:

```
// Create listener for plus1 buttons  
document.querySelectorAll('tbody button.plus').forEach((item) => {  
  item.addEventListener('click', pricePlusOne);  
});  
  
// Add 1 to price  
let pricePlusOne = () => {  
  var index = event.target.dataset.index;  
  products[index].price++; // increment price  
  // first method: force rendering by reassigning item  
  products[index] = products[index];  
  
  // second method: direct change of the HTML element  
  //tbody.querySelector(`tr[data-index="${index}"] [data-field=price]`).innerText = products[index].price;  
}
```

The first method, more general, is to force a call to the Proxy’s ***set*** method:

```
products[index] = products[index];
```

Fortunately, a dummy assignment is enough to get the result. This way, we ensure that the row is updated with any possible consequences of the change made.

The second method is to change the HTML elements linked to the affected data-field (see the last line of the previous code), but this is a less general solution.

## Conclusions

This exercise demonstrates how we can introduce reactivity on a web page using only three standard tools (template, proxy and *data-\** attributes), with a few general-purpose functions (renderArray, applyData, two methods in a minimal Proxy ).

That doesn’t mean you should trash the “official” JavaScript frameworks, as they can certainly provide more scalable and sophisticated solutions. But I hope it will help those who want to apply similar technical solutions without feeling forced to introduce a new framework into their toolkit.

And now, get to work and have fun!

You can also be interested in:

[## Five reasons not to adopt any JavaScript framework

### After applying several cutting-edge javascript frameworks, I found good reasons to stop relying on them

javascript.plainenglish.io](/five-reasons-not-to-adopt-any-javascript-framework-7e815f1073d1?source=post_page-----bde8f1a40479---------------------------------------)

[## Transforming JS Widgets into Web Components

### A software engineering exercise showing the benefits of Web Components

javascript.plainenglish.io](/transforming-js-widgets-into-web-components-1bde419bf706?source=post_page-----bde8f1a40479---------------------------------------)

*More content at* [***PlainEnglish.io***](https://plainenglish.io/)*.*

*Sign up for our* [***free weekly newsletter***](http://newsletter.plainenglish.io/)*. Follow us on* [***Twitter***](https://twitter.com/inPlainEngHQ), [***LinkedIn***](https://www.linkedin.com/company/inplainenglish/)*,* [***YouTube***](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw)*, and* [***Discord***](https://discord.gg/GtDtUAvyhW)***.***

***Interested in scaling your software startup****? Check out* [***Circuit***](https://circuit.ooo/?utm=publication-post-cta)*.*
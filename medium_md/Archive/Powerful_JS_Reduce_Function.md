---
title: "Powerful JS Reduce Function"
url: https://medium.com/p/58cf47edcb8
---

# Powerful JS Reduce Function

[Original](https://medium.com/p/58cf47edcb8)

# Powerful JS Reduce Function

## You can use it to solve any data related problem

[![José Manuel Aguirre](https://miro.medium.com/v2/resize:fill:64:64/1*p0mCrDKI_pqIj0Nbkov9Qw.jpeg)](https://medium.com/@jmaguirrei?source=post_page---byline--58cf47edcb8---------------------------------------)

[José Manuel Aguirre](https://medium.com/@jmaguirrei?source=post_page---byline--58cf47edcb8---------------------------------------)

6 min read

·

Sep 23, 2019

--

5

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D58cf47edcb8&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fpowerful-js-reduce-function-58cf47edcb8&source=---header_actions--58cf47edcb8---------------------post_audio_button------------------)

Share

With ES6 Javascript and beyond, now you can *map*, *filter*, *reduce*, *sort*, *flatten* and much more over an array. It’s really pretty straight forward to think, succinct an elegant.

But sometimes, the big unknown of this list is *reduce*.

> You may not be aware yet of the power of this method, let’s take a look.

Maybe you imagine that the only way to “reduce” an array is turning it into something “smaller”, like a number, or a string. For example:

* If I have the array *[ 1, 2, 3 ]* I can reduce it by summing its terms, so **1 + 2 + 3 = 6**, or by multiplying them, so **1 \* 2 \* 3 = 6**, or by simply concatenate the numbers as characters, so the string **“123”**.

But, in reality reduce is very powerful and **can accomplish any data transformation**. You can go from *Array* to *Array*, *Array* to *Number*, *Array* to *Object*, *Object* to *Array*, or really anything you can imagine.

> So, I am going to argue that the name “**reduce**” is not making it justice. The name should be “**transform**” and then, in your mind, you are always sure that this function can be used in a lot of more contexts.

So, we are going to be looking some code examples now, let’s get into them!

### Example Set 1: Sum, Sum-Product and Max

The “traditional way” of thinking about reduce is represented by this examples. You are actually reducing an array into a number in each of this examples:

Press enter or click to view image in full size

![]()

And the console says:

![]()

So, just a brief explanation of each example:

* **Sum**: Start with 0, take each element and sum it to the accumulated value.
* **SumProduct**: Start with 0, take each pair (number and factor) and sum number \* factor into the accumulated value.
* **MaxNumber**: Start with nothing and return the first element, if nothing is accumulated, otherwise return the number if it’s bigger that the accumulated or the accumulated value if not.

### Example Set 2: Map, Filter, Filter & Map and FlatMap

Now, we are going one step further and actually implementing the classic map, filter, filter and then map (the other order is also possible) and flatMap functions. All of the are really a subset of reduce (“aka transform”).

![]()

And the console says:

Press enter or click to view image in full size

![]()

A brief explanation of each example:

* **Map**: Start with an empty array, take an array and a function and return the value accumulated plus the current element with the function applied to it.
* **Filter**: Start with an empty array, evaluate the function on the current element and if **false**, just return the accumulated value (so, skip this element) and otherwise return the value accumulated plus the current element.
* **FilterMap**: Take an array, a function to use as filter and a function to map, and combine the two former processes.
* **FlatMap**: Start with an empty array, take an array and a function and if the element itself is an array, spread the result over the accumulated value, otherwise, just return the value accumulated plus the current element with the function applied to it.

### Example Set 3: Unique, Sort and Reverse

This are also very useful functions that can be implemented with reduce. The big advantage over native functions provided by the *Array.Prototype*, is that you can combine more than one transformation in one step, if you wish… But really, the purpose of this examples is just show to you more power of the reduce function:

![]()

And the console says:

![]()

A brief explanation of each example:

* **Unique**: Start with an empty array, take an element and check if it’s already in the accumulated value. If present, just return the accumulated value (so skip it) otherwise return the accumulated value plus the element.
* **Sort**: Start with an empty array and separate the accumulated value into 2 sets: The set of element “less or equal than the current value” and the set of elements “greater than the current value”. So, after that, just return both sets with the current element “in the middle”.
* **Reverse**: With ES6 it’s pretty straight forward. Just return the value and append the accumulated value, so the last element of each iteration will be always at first position of the array.

### Example Set 4: Object into Array and Array into Object

If the synonym of reduce “transform” was not clear, from this point is really obvious. Sometimes you need to convert an Array into an Object or viceversa. What function can you use? Yes! Reduce!

Press enter or click to view image in full size

![]()

And the console says:

![]()

A brief explanation of each example:

* **Object To Array**: Start with an empty array and iterate over the Object keys (which is also an array). For each key, take also the value (*object[key]*) and return the accumulated value plus the *object { key: value }*. Maybe the example does not look very useful but it is useful if you imagine you are rendering a list with React and it’s convenient to have the object información as an array.
* **Array to Object**: Start with an empty object and iterate over the array to return an object with the *id* field as the object first level field, and the rest of fields as its content. This is sometimes useful when you need to group more that one array that has information about an entity (represented by the id) and return everything in a single object for further processing.

So, reduce function can be viewed more like a process, in a more traditional way: INPUT => PROCESS => OUTPUT

Press enter or click to view image in full size

![]()

### Bonus 1: Reduce actually as Augment!

Given that you don’t need to have single number as a result, or the same primitive, or even the same number of elements of the input, you can use ***reduce*** to actually add new elements to your input data.

## Get José Manuel Aguirre’s stories in your inbox

Join Medium for free to get updates from this writer.

Subscribe

Subscribe

Remember me for faster sign in

This is a real world example (simplified) where you have a list of elements that are categorized in a certain way and you want to present them but inserting some title indicating the category.

For example:

Press enter or click to view image in full size

![]()

And the Console says:

![]()

So, you are “producing” a new list by combining to different data primitives. And, of course, there is no limit. It can be an arbitrary number of entities that can be combined into a single list that is ready to be passed to the DOM for rendering.

### Bonus 2: Using reduce to process a promise chain (in sequence)

Another use of reduce I found very useful is to ensure sequentiality. When you are processing a promise chain, typically you are going to need the result of a previous promise to use as input for the next promise, and so on.

Reduce to the rescue!

![]()

And the Console says:

Press enter or click to view image in full size

![]()

And we can stop here.

All examples are in this [JS Fiddle](https://jsfiddle.net/jmaguirrei/yhmvap5o/82/)

I hope now you have more ideas to use ***reduce*** to produce readable and elegant code in your projects!

Cheers from Chile [🇨🇱](https://emojipedia.org/flag-for-chile/)!!
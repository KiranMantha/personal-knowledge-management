---
title: "Call By Value/Call By Reference In JavaScript"
url: https://medium.com/p/c5738600d9cd
---

# Call By Value/Call By Reference In JavaScript

[Original](https://medium.com/p/c5738600d9cd)

[![]()](http://www.track.datadriveninvestor.com/1B9E)

![]()

# Call By Value/Call By Reference In JavaScript

[![Abhimanyu Chauhan](https://miro.medium.com/v2/resize:fill:64:64/1*KXAAsiwm-ESRwez8IwgNkQ.jpeg)](/@abhimanyuchauhan-61309?source=post_page---byline--c5738600d9cd---------------------------------------)

[Abhimanyu Chauhan](/@abhimanyuchauhan-61309?source=post_page---byline--c5738600d9cd---------------------------------------)

5 min read

·

Jun 11, 2019

--

2

Listen

Share

More

So I have been writing about JavaScript for some time now, I also help a few of my friends learn JavaScript as they want to get into front end development. This is one of the personal favorite topics, but I was a bit surprised to find how many times, people get it wrong.

The problem with JS is that it doesn’t follow the general pattern like other languages. For e.g. in C#, the ***ref*** keyword is used to define a method with one of the parameters, which follows a *call by reference*.

```
public void useCallByRef(ref int val)
```

Before we dive into the main topic, let’s look at the different data-types JavaScript provides to us.

[## Best Coding Languages to Learn in 2019 - Data Driven Investor

### During my years as an undergrad, I skipped many night-outs to pick up Java hoping it would one day help me get ahead in…

www.datadriveninvestor.com](https://www.datadriveninvestor.com/2019/02/21/best-coding-languages-to-learn-in-2019/?source=post_page-----c5738600d9cd---------------------------------------)

> **Data Types**

There are **7 data types** in total, divided into two subgroups, *primitive* and *non-primitive* data types.

```
Primitive       Non-Primitive  
Number          Arrays  
String          Objects  
Boolean  
Undefined  
Null
```

***Note:*** *TypeOf Null and Arrays is Object.*

*Array* is treated as an Object with a special property **length** and constructor name property as “Array”**.**

![]()

***Note****: Knowing the data types, will help better understand how they are treated by the JavaScript compiler.*

> **Call by value**

When a variable is passed as a parameter to a function, if any changes are made to the parameter, the original variable will remain unaffected. This is known as **call by value** and this is true for all values having a *primitive data type.*

Let’s look at an example:

![]()

The output for the above example is 20,10. So, why didn’t the value for *original* update at line 3?

It’s actually easy, think of it as when we pass *original* to the *updateOriginal* function, we pass the value directly and not the **reference** **to the value(memory address allocated)**. Any changes made to the value does not update the actual reference of the *original value*.

> **Call by reference**

When a variable’s *reference*(address) and not its value is passed to a function’s parameter, any changes made to the parameter will update the original variable reference. This is known as **call by reference** and this is true for all values having a *non-primitive data type*.

Let’s look at an example:

![]()

The output for the above example is 20. So, why did the *value* in ***myObj*** update in line 3?

Think about an object pointing to a *memory address* for e.g. 1000 and each property of that object pointing to a value.

```
myObj -->1000 (memory address location)
```

So now when we pass this object as a parameter to a function(*updateValue*), the parameter points to the same reference.

```
objRef -->1000
```

When the values of the properties are updated, they are reflected throughout the object’s scope, as objects are references. So how can we access the properties and operate on them without updating the object itself?

The solution is easier than you think, create a copy of the object and operate on it. This is one of the basics of immutable style of programming.

```
let myObj = {  
    value:10  
}  
function updateValue(objRef){  
//creates a new object reference and assigns objRef properties to //the object  
    let copy = Object.assign({},objRef);   
    console.log(copy.value);  
    copy.value = 20;  
    console.log(copy.value);  
}  
updateValue(myObj);  
console.log(myObj.value);
```

The same can happen while working with arrays, as they are also treated as Objects in JavaScript:

```
let myArray =[1,2,3];function addToArray(arrayRef,value){  
    arrayRef.push(value);  
}  
console.log(myArray);  
addToArray(myArray,4);  
console.log(myArray);
```

The output is [1,2,3], [1,2,3,4], because the *arrayRef* will point to the *myArray* reference.

So the best way to operate on arrays without causing any side effects is by creating a copy of the array. We can use the higher order function **map**, as it returns a new array(object reference)

```
let myArray =[1,2,3];function addToArray(arrayRef,value){  
    //returns a new array  
    let newArray = arrayRef.map(val=>val);  
    newArray.push(value);  
    console.log(newArray);  
}  
addToArray(myArray,4);  
console.log(myArray);
```

The output is [1,2,3,4], [1,2,3].

There is another case where one can get confused and that is when we are working with an array of objects.

```
let myArray =[{a:1},{b:2},{c:3}];function addToArray(arrayRef,value){  
    var newArray = arrayRef.map(val=>val);  
    newArray.push(value);  
    console.log(newArray);  
}  
addToArray(myArray,{d:4});  
console.log(myArray);
```

So the output is as expected newArray is [{a:1},{b:2},{c:3},{d:4}] and myArray is [{a:1},{b:2},{c:3}].

But what if we try to update the value of {a:1} to {a:2} in newArray.

```
let myArray =[{a:1},{b:2},{c:3}];function addToArray(arrayRef,value){  
    var newArray = arrayRef.map(val=>val);  
    newArray.push(value);  
    newArray[0].a = 10;  
    console.log(newArray);  
}  
addToArray(myArray,{d:4});  
console.log(myArray);
```

**\*NOTE: Before you look at the output, please think it over.**

The output is:

![]()

So why did the value update, even when we created a new list?

The answer is simpler than you think, as we know Objects are references, so when we push an object to an array, we push its reference, not value. So any changes made to the object will directly reflect in all the occurrences. In our case {a:1} was updated in *newArray* to {a:10}, this change is also reflected in *myArray*.

**Note**: *Please try to fix the above code snippet, and I would love to see your responses.*

So creating copies or new references should be followed while working with variables which are a type of Object. Update the main object at the end of a method when it is actually required. This can help avoid bugs, which are generally hard to find and this can even help in pinpointing bugs.
---
title: "Catching memory leaks with Chrome DevTools"
url: https://medium.com/p/57b03acb6bb9
---

# Catching memory leaks with Chrome DevTools

[Original](https://medium.com/p/57b03acb6bb9)

# Catching memory leaks with Chrome DevTools

[![Aayush Arora](https://miro.medium.com/v2/resize:fill:64:64/1*EfSi6ZKpz7_P5V-_nZ6kHw.png)](/@angularboy?source=post_page---byline--57b03acb6bb9---------------------------------------)

[Aayush Arora](/@angularboy?source=post_page---byline--57b03acb6bb9---------------------------------------)

5 min read

·

Jun 1, 2019

--

1

Listen

Share

More

![]()

*When allocated memory is not returned back to the operating system or the memory pool, we refer to it as a memory leak*. In this scenario, the memory is not utilized by any application and is needlessly occupied. This results in low performance, high latency, and frequent crashes.

## Understanding memory leaks

If you are familiar with low-level languages like C, you must have used `malloc()` and `free()`. In contrast, JavaScript automatically allocates memory when objects are created and frees it when they are not used anymore.

Well, because it is automatically managed, we as developers are always under the false impression that we don’t need to worry about memory management in browsers. If a site is using more and more memory, that means nobody is collecting it and there is a memory leak.

## Garbage collectors

If garbage collectors (GCs) were perfect, then memory leaks wouldn’t be an issue. The problem is that their algorithms are not smart enough to detect the memory leaks; thus, human intervention is required.

Garbage collectors execute the process of finding memory that is no longer in use by the program and releasing it back to the OS for future reallocation. The method is effective, but still memory leaks happen. The method is not capable of detecting every leak, such as ***leaked references.***

There are two specific algorithms that browsers use:

## 1. Mark and sweep

During mark and sweep, the GC initializes all the mark bits as 0. Whenever we create an object, the mark bit is set to 1. The mark bit of every reachable object is set to 1. Finally, the GC garbage-collects all the objects whose mark bits are set to 0.

## 2. Reference count algorithm

In this algorithm, the algorithm checks if the object is no longer needed. Reference count algorithms are the most basic GC algorithms. *If an object has zero references pointing towards it, the GC collects it.*

Though these algorithms are available, they are not perfect, and therefore, we need some tools to detect whether memory leaks.

## Why is there a memory leak?

Many things can cause memory leaks, and we will cover them one by one.

### Accidental global variables

```
function getWork() {  
  this.work = “I am Memory leak”;  
}// The this here refers to window object and hence this variable will be created in the window.getWork();
```

As global variables are not collected by a GC, if this string becomes too large, it can cause a memory leak. A similar example of accidental globals would be declaring variables without using `let` and `var` keywords.

### Detached DOM nodes

Detaching DOM nodes is a crucial problem. Detached nodes still exist in memory due to their global references.

```
var node = document.createElement(‘a’);  
node.id = 'id1';  
document.body.appendChild(node);var main = {  
   Id: document.getElementById(‘id1’)  
}function removeElement(){  
   document.body.removeChild(document.getElementById(‘id1’));  
}// The ‘this’ here refers to window object and hence this variable will be created in the window.removeElement();
```

In the example above, the `removeChild` function removed the DOM node from the tree, but the reference Id in the global main object still remains in the memory and is not garbage-collected.

### Closures

Closures maintain the scope of the outer function variables for the inner function even outside the scope of outer functions.

```
function getScore(x) {  
   function score(y) {  
      return x + y;  
    }  
   return score;  
}// The this here refers to window object and hence this variable will be created in the window.var initial = getScore(2);  
var final = initial(3);
```

The function `score` here, which is the inner function, has a global reference called `initial`. This initial reference is never going to be garbage collected.

[## Visit Aayush Arora on MentorCruise

### Aayush Arora is an Engineering & Data mentor who provides personalized mentorship in Web, Software Developer, Web…

mentorcruise.com](https://mentorcruise.com/mentor/AayushArora/?source=post_page-----57b03acb6bb9---------------------------------------)

## Tools to identify memory leaks

### Comparisons for snapshot

Accidental Global Variables Memory leaks can be detected with the profiling easily. Let’s take an example of a code snippet that will cause memory leak because of the global variable.

```
var x = []  
var bool = false;function grow(){  
  x.push(new Array(100000).join(‘a’));  
  if(bool){  
    setTimeout(grow, 1000);  
  }  
}function start(){  
  grow();  
  bool = true;  
}function stop(){  
  bool = false;  
}
```

To check this code, we can take the heap snapshots by going to the *Profile Panel in Developer Tools.*

Press enter or click to view image in full size

![]()

Here, the *yellow color of the window object* is actually depicting the nodes that have *direct references from the JS code*. We need to fix the code here such that we can **get rid of yellow markers**.

Press enter or click to view image in full size

![]()

The option here is to make the array local within the function so that the garbage collector can collect it or to explicitly delete the global variable. You can find the corrected code as:

```
var bool = false;function grow(){  
  var x = [];  
  x.push(new Array(100000).join(‘a’));  
    
  if(bool){  
   setTimeout(grow, 1000);  
  }  
}function start(){  
  grow();  
  bool = true;  
}function stop(){  
  bool = false;  
}
```

### **Allocation profiler**

The Allocation Timeline is another tool that can help you track down memory leaks in your JS heap. To record the timeline, go to your profile panel and click start for the same code which was given above.  
When we click the `Start` button as shown in the image and profile that using allocation profiler, we can see it generating the blue lines as shown in the image.

Press enter or click to view image in full size

![]()

The `blue bars` represent new memory allocation, which can be a *memory leak*. You can go into the details by zooming any one of those blue bars. The details here are representing long strings which are pushed into the array and never garbage collected.

## Conclusion

Garbage collectors are necessary but insufficient. As such, human intervention with the right tools and knowledge is required to prevent memory leaks.

If you are aware of the above common patterns in which memory leaks occur, you will be able to quickly inspect them with the Chrome DevTools.

[## Visit Aayush Arora on MentorCruise

### Aayush Arora is an Engineering & Data mentor who provides personalized mentorship in Web, Software Developer, Web…

mentorcruise.com](https://mentorcruise.com/mentor/AayushArora/?source=post_page-----57b03acb6bb9---------------------------------------)

If you liked the article, please clap your heart out. Tip — **Your 50 claps will make my day!**

Want to know more about me? If you’d like to get updates, follow me on [Twitter](https://twitter.com/angularboy) and [Medium](/@angularboy). If anything isn’t clear or you want to point out something, please comment down below.
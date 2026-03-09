---
title: "10 Python Concepts That Took Me Years to Understand — Until I Saw These Examples"
url: https://medium.com/p/8ee670212c33
---

# 10 Python Concepts That Took Me Years to Understand — Until I Saw These Examples

[Original](https://medium.com/p/8ee670212c33)

Press enter or click to view image in full size

![]()

Member-only story

Featured

## The Hardest Lessons in Python Are the Ones Nobody Tells You Early

# 10 Python Concepts That Took Me Years to Understand — Until I Saw These Examples

## Sometimes one example can do more than a hundred explanations. Here are the ones that finally made things click for me.

[![Aashish Kumar](https://miro.medium.com/v2/resize:fill:64:64/1*DDAIkjJaxeJUyV2MZxwwlw.jpeg)](/@aashishkumar_77032?source=post_page---byline--8ee670212c33---------------------------------------)

[Aashish Kumar](/@aashishkumar_77032?source=post_page---byline--8ee670212c33---------------------------------------)

4 min read

·

Oct 19, 2025

--

24

Listen

Share

More

When I first began with Python, I assumed I had it down after a year. Simple syntax, welcoming community, unlimited tutorials — did I really need anything else? But the longer I went, the further I realized I was lacking in some basic fundamentals.

The difficult part? These weren’t exotic, glamorous topics like metaclasses or crafting Python compilers. They were basic fundamentals I’d gotten wrong or forgotten for decades. And every time I learned them properly, a stumbling block in my head just disappeared.

So, in this article, I’d be happy to share the 10 Python concepts I waited for years to understand, and the simple examples which made sense at last. If you are an intermediate-level Python developer, you will be definitely nodding once and thinking to yourself: “Wow, I should have known it earlier.”

Let’s begin.

## 1. Mutable vs Immutable Objects

This is the classic Python gotcha. I couldn’t for the life of me figure why my lists were magically changing within functions.

```
def add_item(items, value):  
    items.append(value)  
    return items  
  
my_list = [1, 2, 3]  
add_item(my_list, 4)  
print(my_list)  # [1, 2, 3, 4] - modified in place!
```

The key:

> ***Immutable types(int, float, str, tuple)*** *→ changes create a new object.*
>
> ***Mutable types (list, dict, set)*** *→ changes modify the original object.*

After I grasped this disparity, debugging was considerably easier.

## 2.Default Mutable Arguments

This one I’ve remembered for years. Mutable default arguments produce “weird” behavior.

```
def add_to_list(value, items=[]):  
    items.append(value)  
    return items  
  
print(add_to_list(1))  # [1]  
print(add_to_list(2))  # [1, 2] - not a fresh list!
```

Fix:

```
def add_to_list(value, items=None):  
    if items is None:  
        items = []  
    items.append(value)  
    return items
```

The explanation: default arguments are evaluated at function definition time, not each time it’s invoked.

## 3. Python’s Pass-By-Object-Reference

I used to argue forever whether Python was “pass by reference” or “pass by value.” Reality: it’s pass-by-object-reference.

> *Variables are nothing but tags for things.*
>
> *Arguments of functions are new names for the same things.*

```
def modify(num):  
    num += 1  
    print("Inside:", num)  
  
x = 5  
modify(x)  
print("Outside:", x)  # Still 5
```

Pass-by-value is true for immutable values, but pass-by-reference is true for mutable objects. It’s this subtlety I had trouble remembering for so long.

## 4. is vs ==

I once referred to them interchangeably — until it bit me.

```
a = [1, 2]  
b = [1, 2]  
print(a == b) # True (values are equal)  
print(a is b) # False (different object)
```

> `==` *→ compares values.*
>
> `is` *→ compares object identity.*

This becomes relevant when you are using `None`. Always use `is None`, not `== None`.

## 5. Iterators and Generators

I wrote in Python for decades before I ever actually understood iterators. It’s all about the `__next__` and `__iter__` functions.

```
my_iter = iter([1, 2, 3])  
print(next(my_iter)) #1  
print(next(my_iter)) # 2
```

Generators simplify this:

```
def countdown(n):  
  while n > 0:  
    n n -= 1  
  for i in countdown(3):  
    print(i)
```

It was a surprise to realize why generators do not retain all in memory.

## 6. List Comprehensions vs Generator Expressions

I assumed they were the same initially. They aren’t.

```
# List comprehension: builds the full list in RAM  
 squares = [x*x for x in range(5)]  
  
# Generator expression: lazy, one value at a time  
squares_gen = (x*x for x in range(5))
```

Memory is of utmost significance while processing large data.

## 7. Context Managers (with Statement)

I once penned:

```
f = open("data.txt")  
data = f.read()  
f.close()
```

Until I was taught this was risky. Something would go wrong and the file wouldn’t ever close. Context managers come along:

```
with open("data.txt") as f:  
    data = f.read()
```

The good thing is that with guarantees of cleanup, even on error. And yes, you can make your own context managers using \_\_enter\_\_ and \_\_exit\_\_.

## 8. The Power of \*args and \*\*kwargs

I would avoid those because they looked threatening. But they’re just dynamic argument unpackings.

```
def demo(a, *args, **kwargs):  
    print("a:", a)  
    print("args:", args)  
    print("kwargs:", kwargs)  
  
demo(1, 2, 3, x=4, y=5)
```

Output:

```
a: 1  
args: (2, 3)  
kwargs: {'x': 4, 'y': 5}
```

Once I embraced this, writing reusable functions became easier.

## 9. Decorators

I plagiarized designers for so long without ever grasping them. Until this example resonated with me:

```
def log(func):  
    def wrapper(*args, **kwargs):  
        print(f"Calling {func.__name__}")  
        return func(*args, **kwargs)  
    return wrapper  
  
@log  
def greet(name):  
    print(f"Hello, {name}")  
  
greet("Python")
```

Decorators are mere functions that take a function and output a function. If you comprehend this, your perception of decorators as “magic” goes away.

## 10. The \_\_name\_\_ == “\_\_main\_\_”

I thought this sentence was boilerplate until I recognized its purpose:

```
def main():  
    print("Running as script!")  
  
if __name__ == "__main__":  
    main()
```

It enables you to execute your file as a module and a script. Therefore, any serious project with Python has it.

## Conclusion

These ten concepts may seem obvious once you’ve read them, but I promise you — they did not seem obvious to me at first. Each of them represents a “**lightbulb moment**” from my experience with Python, in which suddenly things made sense on a deeper level.

If you find you’re still having trouble with some of these, don’t fret — it’s normal. The key thing is to keep playing with examples until it clicks for you. Because in programming, a single good example can revolutionize the way you write code for life.

Python fosters curiosity. The more you find its idiosyncrasies to explore, the\_more your code becomes beautiful. Don’t memorize the\_syntax\_by rote- experiment, break it, and learn from it.
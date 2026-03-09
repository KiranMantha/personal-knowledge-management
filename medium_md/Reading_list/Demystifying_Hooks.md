---
title: "Demystifying Hooks"
url: https://medium.com/p/f55ad885609f
---

# Demystifying Hooks

[Original](https://medium.com/p/f55ad885609f)

# Demystifying Hooks

[![Andrea Giammarchi](https://miro.medium.com/v2/resize:fill:64:64/1*54OyE6rg-MdELwb9mW56Xw.png)](/?source=post_page---byline--f55ad885609f---------------------------------------)

[Andrea Giammarchi](/?source=post_page---byline--f55ad885609f---------------------------------------)

10 min read

·

Nov 7, 2019

--

Listen

Share

More

![]()

While many could see [React Hooks](https://reactjs.org/docs/hooks-reference.html) some sort of sorcery, the concept behind is pretty simple, and I’d like to explain in few lines of code how do these work.

## In a nutshell …

This is the simplest representation of a hook I can think about:

```
const hooked = fn => function hook() {  
  /* setup hook details */  
  try { return fn.apply(null, arguments); }  
  finally { /* rollback hook details */ }  
};
```

The `hooked` constant can now be used to wrap any callback, so that when it’s invoked, the passed callback will have all the necessary details to run any of the provided APIs, such as `useState`, `useRef`, and others.

The instrumentation is needed so that the API can eventually re-invoke the hooked function at any point in time, as example via `setState(value)`.

Since the invocation is synchronous, each hook can setup itself as long as it will put back previous details, if any.

### The hooked(fn) utility

Let’s see the basic `hooked` utility in all its details:

```
let curr = null;  
const current = () => curr;  
const hooked = fn => {  
  const stack = [];  
  return function hook() {  
    const prev = curr;  
    const after = [];  
    let i = 0;  
    curr = {  
      hook, arguments,  
      stack, get index() { return i++; },  
      after  
    };  
    try { return fn.apply(null, arguments); }  
    finally {  
      curr = prev;  
      after.forEach(fn => fn());  
    }  
  };  
};
```

Those few lines of code prepare the function execution in a way that any utility could grab the running hook via `current()` , and use all the carried information with it:

* the function `hook` that is running, including its `arguments`
* the hook own `stack` and an incremental `index` to store values in it
* a reference to eventually store callbacks to invoke *after* the `hook` has run

### The stack

It is fundamental to understand that every hooked function needs a stack to memoize all the possible values needed by any provided API.

This also means that all the various APIs, such as `useState`, `useRef`, or others, cannot be defined conditionally, as example via ternary operator, as these might mix up with each other with both execution order and assigned values from the *stack*.

```
// this is *wrong*  
const [value, update] = condition ?  
        useState(0) :  
        useRef([0, () => {}]);
```

Beside forbidden conditional hooks, asynchronous hooks are also a bad idea, as the current running hook, by the time the asynchronous callback is invoked, might be different, or even `null`.

## The useState(value) hook

Let’s see how the `hooked` utility can help defining this first API:

```
const useState = value => {  
  const {hook, arguments, stack, index} = current();  
  if (stack.length <= index)  
    stack[index] = value;  
  return [stack[index], value => {  
    stack[index] = value;  
    hook.apply(null, arguments);  
  }];  
};
```

Each new `hooked` function will use its own *stack* while executing. Such *stack* is needed, so that one function can have multiple `useState(value)` in its body.

Each entry of the *stack* will contain the value initially assigned, or its updated value, reassigned when `setState(...)`, the callback returned as second value, is invoked passing the new value … here an example:

```
const counter = hooked(() => {  
  const [first, setFirst] = useState(0);  
  const [second, setSecond] = useState(1);  
  console.log(first, second);  
  return {  
    first: () => setFirst(first + 1),  
    second: () => setSecond(second + 1)  
  };  
});const count = counter();  
count.first();  
count.second();
```

As you can [see in this code-pen](https://codepen.io/WebReflection/pen/oNNdgay?editors=0011) we already have a perfectly working `useState` utility, capable of returning as many different states, and update callbacks, as needed, thanks to the *stack*.

**However**, since the callback is re-invoked each time an update occurs, not only the console output will show the sequence `0 1` , `1 1` , and `1 2` , since the current `useState` invokes the *hook* per each update, but we could run `count.first()` and `count.second()` forever, without ever seeing the new values passed along … and why is that?

### What you see is not always what you get…

The returned object points at two callbacks created only the first time the hooked *counter* is invoked, but any other invoke, through either `setFirst(...)` or `setSecond(...)` updates, won’t be able to update the initial reference, and it will create instead a new object that nothing could consume, with two methods nobody can reach or use.

To dig a bit more, in terms of amount of GC operations, *hooks* create a quite consistent amount of “*trash*”, either via objects or callbacks, and it’s only thanks to JavaScript raw performance, when it comes to runtime objects creation and GC execution, that we can simply ignore this fact, as performance will never be super optimal but “*good enough*” anyway.

## The useRef(value) hook

To circumvent the fact the returned object is different per each hook invocation, we could define a `useRef` utility:

```
const useRef = value => {  
  const {stack, index} = current();  
  return index < stack.length ?  
          stack[index] :  
          (stack[index] = {current: value});  
};
```

Similarly to `useState`, the `useRef` hook uses the *stack*, so that more than a `useRef` call can be found in any hooked callback.

The *stack* entry is a reference object with a `current` property, pointing at the related *value*, if any, set the first time only the callback executes.

From that time on, such reference object will always be the same, so that our counter can now look like the this:

```
const counter = hooked(() => {  
  const [first, setFirst] = useState(0);  
  const [second, setSecond] = useState(1);  
  console.log(first, second);  
  const {current: count} = useRef({});  
  count.first = () => setFirst(first + 1);  
  count.second = () => setSecond(second + 1);  
  return count;  
});
```

As you can [test live in this pen](https://codepen.io/WebReflection/pen/yLLjNNb?editors=0011), whenever we invoke `count.first()` or `count.second()`, the new values are respectively updated.

“*But … will the empty* `{}` *always be created?*”

Yes, but as previously mentioned, it will always be easily trashed by the Garbage Collector, or even ignored if the JS engine is smart enough.

## Avoiding unnecessary invokes

Any hooked function could use many states updates at once, and yet with the current logic such function will be executed per each singular one.

Using the *counter* example, we can see undesired logs between two consecutive updates: one for the *first* value, and one for the *second* one.

Ideally, when multiple states are updated at once, what we want to read is just the first invoke, with `0` and `1`, and the last one, with `1` and `2`. We have no interest in reading, or moving the whole logic, to log `1` and `1` between the first update and the second, but there’s no way to tell the hook to ignore such update, as these could also be fully independent, or triggered at distance in different times.

An easy way to avoid undesired hook calls, is to defer all invokes at once, making the update asynchronous, but optimal in terms of performance.

### Meet reraf

Born to solve this, and similar, use cases, the [reraf](https://github.com/WebReflection/reraf#readme) utility is capable of rescheduling, either via `requestAnimationFrame`, where available, falling back to `setTimeout`, one, two, or hundreds call to the same function, granting that only the last one will be executed.

This is kinda perfect for hooks, so that we can do a bit of refactoring, introducing reraf, and reuse such utility for other APIs too, such as `useEffect`.

```
import reraf from 'https://unpkg.com/reraf?module';  
const updates = new WeakMap;  
const useState = value => {  
  const {hook, arguments, stack, index} = current();  
  if (stack.length <= index) {  
    stack[index] = value;  
    if (!updates.has(hook))  
      updates.set(hook, reraf());  
  }  
  return [stack[index], value => {  
    stack[index] = value;  
    updates.get(hook)(hook, null, arguments);  
  }];  
};
```

After this change, we can [test live in this pen](https://codepen.io/WebReflection/pen/XWWqaYM?editors=0011) that the console output is indeed `0` and `1`, followed asynchronously by `1` and `2`.

If we look closer though, we cannot anymore invoke `current.first()` many times in a row and expect synchronous increments, for the simple reason the method will still point at the first callback until the asynchronous operation happens, …and this is fine, as invoking repeatedly the same `setState(value)` doesn’t really have many real-world applications, while undesired executions are heavier and for no gain.

## The useReducer(reducer, value[, init]) hook

The reducer allows more complex state changes at once already, but it’s still about states, so that we can use the same utility we have already.

```
const useReducer = (reducer, value, init) => {  
  const [state, setState] = useState(init ? init(value) : value);  
  return [state, value => {  
    setState(reducer(state, value));  
  }];  
};
```

## The useMemo(fn[, guards]) hook

This one is more similar to `useRef`, but it’s based on a callback to be invoked either the first time, or only when `guards` conditions would require so.

```
const useMemo = (fn, guards) => {  
  const {stack, index} = current();  
  if (  
    !guards ||  
    stack.length <= index ||  
    guards.some(different, stack[index].values)  
  )  
    stack[index] = {current: fn(), values: guards};  
  return stack[index].current;  
};
```

If either no `guards` is passed, or one of its values differs from the previous hook invocation, the result of the invocation of the callback is stored in the stack, together with the new guards. The outcome of the invocation will also be returned, and at this point we have everything we need to implement the next utility too.

## The useCallback(fn[, guards]) hook

```
const useCallback = (fn, guards) => useMemo(() => fn, guards);
```

Well, I don’t think there’s much to say in here, isn’t it? 😉

## The useContext(context) hook

Differently from any other utility described so far, the peculiarity of this one is that many hooks can use the same context to react to changes, whenever these occur.

This makes the usage of the stack meaningless, ’cause such stack is associated only to a single hooked function, so we need to create our own stack, adding every hook that is using the shared context.

```
const hooks = new WeakMap;  
const useContext = context => {  
  const {hook, args} = current();  
  const stack = hooks.get(context);  
  const info = {hook, args};  
  if (!stack.some(update, info))  
    stack.push(info);  
  return context.value;  
};  
function update({hook}) {  
  return hook === this.hook;  
}
```

That is pretty much it: we check if our stack already contains a specific hook, and if that’s not the case, we add such hook, and its arguments, to the stack.

… but how is the stack populated, and how are hooks notified once the context changes? … and what is the *context* anyway?

### The createContext(value) utility

While in *React* a context can be represented as a node that provides some value, in this post it’s simply an object with a value, and a `provide(newValue)` method.

```
const createContext = value => {  
  const context = {value, provide};  
  hooks.set(context, []);  
  return context;  
};const invoke = ({hook, args}) => { hook.apply(null, args); };function provide(value) {  
  if (this.value !== value) {  
    this.value = value;  
    hooks.get(this).forEach(invoke);  
  }  
}
```

At this point, it’s clear that passing a non-context value to the previous `useContext(context)` utility would throw an error, ’cause no stack has been possibly attached to such object, but of course if the context was previously created, the WeakMap will return its stack, and every time `context.provide(newValue)` is invoked, every hook registered in such stack will be invoked, and the new value returned per each `useContext`.

## The useEffect(fn[, guards]) hook

The last utility of this list is one that triggers the `fn` *after* the hook executed, either synchronously, via **createLayoutEffect(fn[, guards])**, or asynchronously, via *reraf*.

The logic involved is slightly more convoluted than before:

* the `fn` could return a callback to cleanup previous effects
* the *stack* details, per each effect, should not be exposed … but …
* there must be a way to cleanup all effects that were previously scheduled, simulating `componentDidUnmount` or, in DOM words, a disconnected element from the live tree.

Accordingly, we can use both the usual *stack* and its *index*, but also a *WeakMap*, to associate both a single *reraf* function, and any cleanup operation, directly to the running hook, so that third parts libraries can drop, or cleanup, all remaining effects at any time.

```
const effects = new WeakMap;  
const stop = () => {};const createEffect = sync => (effect, guards) => {  
  const {hook, stack, index, after} = current();  
  if (index < stack.length) {  
    const info = stack[index];  
    const {clean, invoke, update, values} = info;  
    if (!guards || guards.some(different, values)) {  
      info.values = guards;  
      if (clean) {  
        info.clean = null;  
        clean();  
      }  
      if (sync)  
        after.push(invoke);  
      else  
        update(invoke);  
    }  
  }  
  else {  
    const invoke = () => { info.clean = effect(); };  
    if (!effects.has(hook))  
      effects.set(hook, {stack: [], update: reraf()});  
    const details = effects.get(hook);  
    const info = {  
      clean: null,  
      invoke,  
      stop,  
      update: details.update,  
      values: guards  
    };  
    stack[index] = info;  
    details.stack.push(info);  
    if (sync)  
      after.push(invoke);  
    else  
      info.stop = details.update(invoke);  
  }  
};const useEffect = createEffect(false);  
const useLayoutEffect = createEffect(true);
```

The logic is basically the following one:

* first time the `useEffect` is called, we store in the stack some info regarding the effect, such as the function to invoke after, or asynchronously, one able to stop the effect, if not happened already, values to guard against per each invocation, and a *clean* property to carry eventual returned callback to clean up the effect.
* every other time, we ensure the previous cleanup is performed, and we reschedule the update, either after the hook executes, or asynchronously.

### The dropEffect(hook) utility

The only missing bit, is a function able to cleanup all remaining effects, in case the hook won’t be executed ever again, or its related DOM node has been removed from the tree.

```
const dropEffect = hook => {  
  if (effects.has(hook))  
    effects.get(hook).stack.forEach(info => {  
      const {clean, stop} = info;  
      stop();  
      if (clean) {  
        info.clean = null;  
        clean();  
      }  
    });  
};
```

The *stop()* could be a no-op, and if there’s any clean operation left, the related info is also cleaned up, and the callback invoked to execute such cleanup once.

## And That’s All Folks 🎉

I’ve tried to cover basically everything [**augmentor**](https://github.com/WebReflection/augmentor#readme) library offers, using also most of its real code, hoping you followed this journey, also understanding how hooks work internally, and how to use related utilities for your project.

Its dependent [**dom-augmentor**](https://github.com/WebReflection/dom-augmentor#readme) also provides all it takes to invoke `dropEffect(hook)` when some node is removed from the DOM, which is handy for 3rd parts libraries such as [neverland](https://github.com/WebReflection/neverland#readme), or even [heresy](https://github.com/WebReflection/heresy#readme) (where hoooks are not in yet, but will be soon).

So, you have all the primitives you need to play around or create the next library, with an overhead of less than 1K, which is the current *augmentor* size.

Enjoy hooks, and feel free to ask me more either here or in [twitter](https://twitter.com/WebReflection) 👋

## Compatibility

If you are wondering which browser is compatible with *augmentor*, or the code in this post, the answer is IE11 or greater, once transpiled, or any other engine compatible with ES6/ES2016.
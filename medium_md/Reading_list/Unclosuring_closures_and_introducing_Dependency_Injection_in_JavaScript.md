---
title: "Unclosuring closures and introducing Dependency Injection in JavaScript"
url: https://medium.com/p/3b6673d21862
---

# Unclosuring closures and introducing Dependency Injection in JavaScript

[Original](https://medium.com/p/3b6673d21862)

# Unclosuring closures and introducing Dependency Injection in JavaScript

[![Vladislav Ihost](https://miro.medium.com/v2/resize:fill:64:64/1*msws1FU1ysbcQpaOgML31A.jpeg)](/@vladihost?source=post_page---byline--3b6673d21862---------------------------------------)

[Vladislav Ihost](/@vladihost?source=post_page---byline--3b6673d21862---------------------------------------)

5 min read

·

Feb 18, 2019

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

In this article we will consider how to write the clear and easy-to-test code in functional style, using Dependency Injection programming pattern. We also achieve 100% unit test coverage as a bonus.

## Terminology

The author of the article will have in mind precisely this interpretation of the following terms, understanding that this is not the ultimate truth and that other interpretations are possible.

- **Dependency Injection**  
This is a programming pattern that assumes that external dependencies for functions and object factories come from outside in the form of arguments to these functions. Dependency injection is an alternative to using dependencies from the global context.

- **Pure function**  
This is a function whose result depends only on its arguments. Also, the function should not have side effects.  
Immediately I want to make a remark that the functions of side effects considered by us do not have, but they can still have functions that came to us through Dependency Injection. So the purity of the functions in the article is conditional.

- **Unit test**  
The test for the function that checks that all branches inside this function work exactly as the author of the code intended. In this case, instead of calling any other functions, the call of mocks is used.

## Practice

Let’s see live example — counters factory. Counter increments with every tick, and can be stopped via `cancel` function invocation. When tick occurred, `onTick` callback is invoked.

```
const createCounter = ({ ticks, onTick }) => {  
  const state = {  
    currentTick: 1,  
    timer: null,  
    canceled: false  
  }  const cancel = () => {  
    if (state.canceled) {  
      throw new Error(‘“Counter” already canceled’)  
    }  
    clearInterval(state.timer)  
  }  const onInterval = () => {  
    onTick(state.currentTick++)  
    if (state.currentTick > ticks) {  
      cancel()  
    }  
  }  state.timer = setInterval(onInterval, 200)  const instance = {  
    cancel  
  }  return instance  
}export default createCounter
```

We see human-readable, understandable code. But there is one catch — you can’t write normal unit tests to it. Let’s see what’s stopping you?

1) internal functions `cancel` and `onInterval` can’t be accessed from the unit test to be tested independently

2) function `onInterval` can’t be tested independently from `cancel` since the first function has direct reference to the second function

3) external dependencies are used in functions `setInterval` and `clearInterval`

4) function `createCounter` can’t be independently tested since the existence of direct references

Let’s solve 1-st and 2-nd problems by extracting `cancel` and `onInterval` functions from closure and break down direct references via introducing additional object — `pool`.

```
// index.js  
export const cancel = pool => {  
  if (pool.state.canceled) {  
    throw new Error(‘“Counter” already canceled’)  
  }  
  clearInterval(pool.state.timer)  
}export const onInterval = pool => {  
  pool.config.onTick(pool.state.currentTick++)  
  if (pool.state.currentTick > pool.config.ticks) {  
    pool.cancel()  
  }  
}const createCounter = config => {  
  const pool = {  
    config,  
    state: {  
      currentTick: 1,  
      timer: null,  
      canceled: false  
    }  
  }  pool.cancel = cancel.bind(null, pool)  
  pool.onInterval = onInterval.bind(null, pool)  pool.state.timer = setInterval(pool.onInterval, 200)  const instance = {  
    cancel: pool.cancel  
  }  return instance  
}export default createCounter
```

Let’s solve the 3-rd problem. By using Dependency Injection pattern, external dependencies `setInterval` and `clearInterval` can also be moved in object `pool`.

```
// index.js  
export const cancel = pool => {  
  const { clearInterval } = pool  
  if (pool.state.canceled) {  
    throw new Error(‘“Counter” already canceled’)  
  }  
  clearInterval(pool.state.timer)  
}export const onInterval = pool => {  
  pool.config.onTick(pool.state.currentTick++)  
  if (pool.state.currentTick > pool.config.ticks) {  
    pool.cancel()  
  }  
}const createCounter = (dependencies, config) => {  
  const pool = {  
    ...dependencies,  
    config,  
    state: {  
      currentTick: 1,  
      timer: null,  
      canceled: false  
    }  
  }  
  pool.cancel = cancel.bind(null, pool)  
  pool.onInterval = onInterval.bind(null, pool)  const { setInterval } = pool  pool.state.timer = setInterval(pool.onInterval, 200)  const instance = {  
    cancel: pool.cancel  
  }  return instance  
}export default createCounter.bind(null, {  
  setInterval,  
  clearInterval  
})
```

Now, almost everything is fine, but there is still a 4-th problem. In the last step, we will apply Dependency Injection to each of our functions and break the remaining references between them through the `pool` object. At the same time, we will split one large file into many files so that later it would be easier to write unit tests.

```
// index.js  
import { createCounter } from ‘./create-counter’  
import { cancel } from ‘./cancel’  
import { onInterval } from ‘./on-interval’export default createCounter.bind(null, {  
  cancel,  
  onInterval,  
  setInterval,  
  clearInterval  
})  
// create-counter.js  
export const createCounter = (dependencies, config) => {  
  const pool = {  
    ...dependencies,  
    config,  
    state: {  
      currentTick: 1,  
      timer: null,  
      canceled: false  
    }  
  }  pool.cancel = dependencies.cancel.bind(null, pool)  
  pool.onInterval = dependencies.onInterval.bind(null, pool)  const { setInterval } = pool  pool.state.timer = setInterval(pool.onInterval, 200)  const instance = {  
    cancel: pool.cancel  
  }  return instance  
}  
// on-interval.js  
export const onInterval = pool => {  
  pool.config.onTick(pool.state.currentTick++)  
  if (pool.state.currentTick > pool.config.ticks) {  
    pool.cancel()  
  }  
}  
// cancel.js  
export const cancel = pool => {  
  const { clearInterval } = pool  if (pool.state.canceled) {  
    throw new Error(‘“Counter” already canceled’)  
  }  
  clearInterval(pool.state.timer)  
}
```

## Conclusion

What is the conclusion? A bunch of files each containing one clean function. The simplicity and clarity of the code have slightly deteriorated, but this is more than offset by the 100% coverage picture in unit tests.

Press enter or click to view image in full size

![]()

Also I want to note that we don’t need to do any manipulations with `require` and to mock the Node.js file system to write unit tests.

## Unit tests

```
// cancel.test.js  
import { cancel } from ‘../src/cancel’describe(‘method “cancel”’, () => {  
  test(‘should stop the counter’, () => {  
    const state = {  
      canceled: false,  
      timer: 42  
    }  
    const clearInterval = jest.fn()  
    const pool = {  
      state,  
      clearInterval  
    }    cancel(pool)    expect(clearInterval).toHaveBeenCalledWith(pool.state.timer)  
  })  test(‘should throw error: “Counter” already canceled’, () => {  
    const state = {  
      canceled: true,  
      timer: 42  
    }  
    const clearInterval = jest.fn()  
    const pool = {  
      state,  
      clearInterval  
    }    expect(() => cancel(pool)).toThrow(‘“Counter” already canceled’)    expect(clearInterval).not.toHaveBeenCalled()  
  })  
})  
// create-counter.test.js  
import { createCounter } from ‘../src/create-counter’describe(‘method “createCounter”’, () => {  
  test(‘should create a counter’, () => {  
    const boundCancel = jest.fn()  
    const boundOnInterval = jest.fn()  
    const timer = 42  
    const cancel = {  
      bind: jest.fn().mockReturnValue(boundCancel)  
    }  
    const onInterval = {  
      bind: jest.fn().mockReturnValue(boundOnInterval)  
    }  
    const setInterval = jest.fn().mockReturnValue(timer)    const dependencies = {  
      cancel,  
      onInterval,  
      setInterval  
    }  
    const config = { ticks: 42 }    const counter = createCounter(dependencies, config)    expect(cancel.bind).toHaveBeenCalled()  
    expect(onInterval.bind).toHaveBeenCalled()  
    expect(setInterval).toHaveBeenCalledWith(  
      boundOnInterval,  
      200  
    )  
    expect(counter).toHaveProperty(‘cancel’)  
  })  
})  
// on-interval.test.js  
import { onInterval } from ‘../src/on-interval’describe(‘method “onInterval”’, () => {  
  test(‘should call “onTick”’, () => {  
    const onTick = jest.fn()  
    const cancel = jest.fn()  
    const state = {  
      currentTick: 1  
    }  
    const config = {  
      ticks: 5,  
      onTick  
    }  
    const pool = {  
      onTick,  
      cancel,  
      state,  
      config  
    }    onInterval(pool)    expect(onTick).toHaveBeenCalledWith(1)  
    expect(pool.state.currentTick).toEqual(2)  
    expect(cancel).not.toHaveBeenCalled()  
  })   test(‘should call “onTick” and “cancel”’, () => {  
    const onTick = jest.fn()  
    const cancel = jest.fn()  
    const state = {  
      currentTick: 5  
    }  
    const config = {  
      ticks: 5,  
      onTick  
    }  
    const pool = {  
      onTick,  
      cancel,  
      state,  
      config  
    }    onInterval(pool)    expect(onTick).toHaveBeenCalledWith(5)  
    expect(pool.state.currentTick).toEqual(6)  
    expect(cancel).toHaveBeenCalledWith()  
  })  
})
```

> **Only by unclosuring all functions to the end, we gain freedom.**
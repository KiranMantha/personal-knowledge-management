---
title: "Event-Driven React with the Observer Pattern: A Clean Alternative to Prop Drilling"
url: https://medium.com/p/a472aae7a74d
---

# Event-Driven React with the Observer Pattern: A Clean Alternative to Prop Drilling

[Original](https://medium.com/p/a472aae7a74d)

# Event-Driven React with the Observer Pattern: A Clean Alternative to Prop Drilling

[![Frontend Highlights](https://miro.medium.com/v2/resize:fill:64:64/1*ISIQMnQqz3UzRTGB0_d4jw.jpeg)](/@ignatovich.dm?source=post_page---byline--a472aae7a74d---------------------------------------)

[Frontend Highlights](/@ignatovich.dm?source=post_page---byline--a472aae7a74d---------------------------------------)

6 min read

·

Jan 30, 2025

--

31

Listen

Share

More

In modern React development, managing state and communication between components can become a challenge, especially as applications grow in complexity. While tools like Redux and Context API have become popular solutions, they often introduce additional boilerplate and complexity. What if there was a simpler, more elegant way to handle component communication without relying on these tools? Enter **event-driven React with the Observer Pattern**.

## The Problem: Prop Drilling and State Management Overhead

In React, **prop drilling** occurs when you need to pass data or callbacks through multiple layers of components to reach a deeply nested child. This can make your code harder to maintain and more error-prone. While solutions like Redux and Context API exist to centralize state management, they come with their own trade-offs:

* **Redux** requires a significant amount of boilerplate code and can feel overkill for smaller applications.
* **Context API** is simpler but can still lead to unnecessary re-renders if not used carefully.

You may that there are a lot of alternatives for Redux, e.g. Zustand, but all they are external libs and we try to avoid props drilling by without any help :))

What if we could achieve component communication in a more decoupled way, without relying on these tools?

## The Observer Pattern: A Lightweight Solution

The **Observer Pattern** is a design pattern where an object (the subject) maintains a list of its dependents (observers) and notifies them of state changes. This pattern is perfect for creating an **event bus** — a central communication channel where components can publish and subscribe to events.

By using an event bus, components can communicate directly without needing to pass props or rely on a global state management library. This approach promotes loose coupling and makes your code more modular and maintainable.

Press enter or click to view image in full size

![]()

Let’s draw a schematic diagram

```
+--------------------+  
|    Event Bus       |  
|--------------------|  
| - on(event, cb)    |  
| - off(event, cb)   |  
| - emit(event, data)|  
+--------------------+  
         ^   ^  
         |   |  
         |   |  
+---------+  +-----------------+  
|  Button  |  | MessageDisplay |  
|----------|  |----------------|  
| - emit() |  | - on()         |  
+---------+  +-----------------+
```

Here’s we have:

**Subject (Event Bus)**: there, we have methods like `on()`, `off()`, and `emit()`.

**Observers (Components)**: boxes are representing a React component (`Button`, `MessageDisplay`). Button will emit an event

**Event Flow (Arrows)**: from the `Button` component to the **Event Bus** (e.g., `emit('buttonClicked')`) and from the **Event Bus** to the `MessageDisplay` component (e.g., `on('buttonClicked')`).

## Implementing an Event Bus in React

Let’s create a simple event bus using the Observer Pattern. Here’s how it works:

### 1. Create the Event Bus

First, we’ll define a simple event bus class:

```
class EventBus {  
  constructor() {  
    this.listeners = {};  
  }  
  
  on(event, callback) {  
    if (!this.listeners[event]) {  
      this.listeners[event] = [];  
    }  
    this.listeners[event].push(callback);  
  }  
  
  off(event, callback) {  
    if (this.listeners[event]) {  
      this.listeners[event] = this.listeners[event].filter(  
        (listener) => listener !== callback  
      );  
    }  
  }  
  
  emit(event, data) {  
    if (this.listeners[event]) {  
      this.listeners[event].forEach((listener) => listener(data));  
    }  
  }  
}  
  
const eventBus = new EventBus();  
export default eventBus;
```

This `EventBus` class allows components to subscribe to events (`on`), unsubscribe from events (`off`), and emit events (`emit`).

### 2. Using the Event Bus in Components

Now that we have our event bus, let’s see how we can use it in React components.

### Publishing Events

A component can publish an event using the `emit` method:

```
import React from 'react';  
import eventBus from './eventBus';  
  
const Button = () => {  
  const handleClick = () => {  
    eventBus.emit('buttonClicked', { message: 'Button was clicked!' });  
  };  
  
  return <button onClick={handleClick}>Click Me</button>;  
};  
  
export default Button;
```

### Subscribing to Events

Another component can subscribe to the event using the `on` method:

```
import React, { useEffect, useState } from 'react';  
import eventBus from './eventBus';  
  
const MessageDisplay = () => {  
  const [message, setMessage] = useState('');  
  
  useEffect(() => {  
    const handleButtonClick = (data) => {  
      setMessage(data.message);  
    };  
  
    eventBus.on('buttonClicked', handleButtonClick);  
  
    return () => {  
      eventBus.off('buttonClicked', handleButtonClick);  
    };  
  }, []);  
  
  return <div>{message}</div>;  
};  
  
export default MessageDisplay;
```

In this example, when the button is clicked, the `MessageDisplay` component updates its state to show the message emitted by the `Button` component.

Press enter or click to view image in full size

![]()

## Testing the Event Bus

The event bus is the core of our architecture, so we need to verify that it works as expected. We’ll write unit tests for the `EventBus` class to ensure it can handle subscriptions, unsubscriptions, and event emissions correctly.

Example Test Suite for `EventBus`

```
import EventBus from './eventBus';  
  
describe('EventBus', () => {  
  let eventBus;  
  
  beforeEach(() => {  
    eventBus = new EventBus();  
  });  
  
  it('should subscribe to an event and call the listener when the event is emitted', () => {  
    const listener = jest.fn();  
    eventBus.on('testEvent', listener);  
  
    eventBus.emit('testEvent', { message: 'Hello, world!' });  
  
    expect(listener).toHaveBeenCalledWith({ message: 'Hello, world!' });  
  });  
  
  it('should unsubscribe from an event and not call the listener', () => {  
    const listener = jest.fn();  
    eventBus.on('testEvent', listener);  
    eventBus.off('testEvent', listener);  
  
    eventBus.emit('testEvent', { message: 'Hello, world!' });  
  
    expect(listener).not.toHaveBeenCalled();  
  });  
  
  it('should handle multiple listeners for the same event', () => {  
    const listener1 = jest.fn();  
    const listener2 = jest.fn();  
    eventBus.on('testEvent', listener1);  
    eventBus.on('testEvent', listener2);  
  
    eventBus.emit('testEvent', { message: 'Hello, world!' });  
  
    expect(listener1).toHaveBeenCalledWith({ message: 'Hello, world!' });  
    expect(listener2).toHaveBeenCalledWith({ message: 'Hello, world!' });  
  });  
  
  it('should not throw an error when emitting an event with no listeners', () => {  
    expect(() => {  
      eventBus.emit('testEvent', { message: 'Hello, world!' });  
    }).not.toThrow();  
  });  
});
```

## Testing Components That Use the Event Bus

To test components that publish or subscribe to events, we’ll use **React Testing Library** and **Jest**. The goal is to ensure that components interact with the event bus correctly.

### Example: Testing the `Button` Component

The `Button` component publishes an event when clicked. We’ll test that the event is emitted correctly

```
import React from 'react';  
import { render, fireEvent } from '@testing-library/react';  
import Button from './Button';  
import eventBus from './eventBus';  
  
jest.mock('./eventBus'); // Mock the event bus  
  
describe('Button', () => {  
  it('should emit an event when clicked', () => {  
    const { getByText } = render(<Button />);  
    const button = getByText('Click Me');  
  
    fireEvent.click(button);  
  
    expect(eventBus.emit).toHaveBeenCalledWith('buttonClicked', {  
      message: 'Button was clicked!',  
    });  
  });  
});
```

### Example: Testing the `MessageDisplay` Component

The `MessageDisplay` component subscribes to an event and updates its state when the event is emitted. We’ll test that the component reacts correctly to the event.

```
import React from 'react';  
import { render, act } from '@testing-library/react';  
import MessageDisplay from './MessageDisplay';  
import eventBus from './eventBus';  
  
jest.mock('./eventBus'); // Mock the event bus  
  
describe('MessageDisplay', () => {  
  it('should update the message when an event is received', () => {  
    const { getByText } = render(<MessageDisplay />);  
  
    // Simulate the event being emitted  
    act(() => {  
      eventBus.listeners['buttonClicked'][0]({ message: 'Button was clicked!' });  
    });  
  
    expect(getByText('Button was clicked!')).toBeInTheDocument();  
  });  
  
  it('should clean up the event listener on unmount', () => {  
    const { unmount } = render(<MessageDisplay />);  
  
    unmount();  
  
    expect(eventBus.off).toHaveBeenCalledWith(  
      'buttonClicked',  
      expect.any(Function)  
    );  
  });  
});
```

## Key Testing Strategies

1. **Mock the Event Bus**: Use `jest.mock` to mock the event bus and control its behavior in tests.
2. **Test Event Emission**: Verify that components emit the correct events with the right data.
3. **Test Event Subscription**: Ensure that components react to events as expected.
4. **Test Cleanup**: Check that event listeners are properly removed when components unmount to avoid memory leaks.

## Tools for Testing

* **Jest**: For unit testing and mocking.
* **React Testing Library**: For testing React components in a way that simulates user interactions.
* **Mock Functions**: Use `jest.fn()` to mock event listeners and verify their behavior.

## Benefits of Using an Event Bus

1. **Decoupled Components**: Components no longer need to know about each other. They communicate through the event bus, promoting separation of concerns.
2. **No Prop Drilling**: You can avoid passing props through multiple layers of components.
3. **Lightweight**: Unlike Redux or Context, an event bus is simple to implement and doesn’t require additional dependencies.
4. **Scalable**: As your application grows, you can add more events and listeners without significantly increasing complexity.

## When to Use an Event Bus

While an event bus is a powerful tool, it’s not a one-size-fits-all solution. Here are some scenarios where it shines:

* **Small to Medium Applications**: For smaller apps, an event bus can be a simpler alternative to Redux or Context.
* **Cross-Component Communication**: When components need to communicate across different parts of the component tree.
* **Decoupled Logic**: When you want to keep your components independent and reusable.

However, for larger applications with complex state management needs, Redux or Context might still be the better choice.

## Conclusion

The Observer Pattern and event-driven architecture offer a clean and elegant way to handle component communication in React. By using an event bus, you can eliminate prop drilling, reduce boilerplate, and keep your components decoupled and maintainable.

While it’s not a replacement for every state management scenario, it’s a valuable tool to have in your React toolkit. Give it a try in your next project and see how it simplifies your code!

If you enjoy what I do, please support me on [Ko-fi](https://ko-fi.com/dm110416)!
---
title: "Effector: powerful and fast 5kb state manager"
url: https://medium.com/p/6ee2e72e8e0b
---

# Effector: powerful and fast 5kb state manager

[Original](https://medium.com/p/6ee2e72e8e0b)

# Effector: powerful and fast 5kb state manager

[![Do Async](https://miro.medium.com/v2/resize:fill:64:64/2*VL6bn351mM8Axgkd_AS8dw.jpeg)](https://medium.com/@doasync?source=post_page---byline--6ee2e72e8e0b---------------------------------------)

[Do Async](https://medium.com/@doasync?source=post_page---byline--6ee2e72e8e0b---------------------------------------)

2 min read

·

Apr 25, 2019

--

3

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D6ee2e72e8e0b&operation=register&redirect=https%3A%2F%2Fcodeburst.io%2Feffector-state-manager-6ee2e72e8e0b&source=---header_actions--6ee2e72e8e0b---------------------post_audio_button------------------)

Share

![]()

Effector is a state manager for any JavaScript app (React/Vue/Node.js). It allows you to manage data in complex applications without the risk of inflating the monolithic central store.

### Key features

* multiple stores
* computed values (no need for memoization)
* side-effect management (async actions)
* statically typed (TypeScript/Flow/Reason)
* framework agnostic
* less boilerplate by design
* relatively small size
* optimized for speed

### Simple example

Counter app using React + hooks

👆 [Try it](https://share.effector.dev/epAix7Ae)

### Principles

* Application stores should be as light as possible — the idea of adding a store for specific needs should not be frightening or damaging to the developer.
* Application stores should be freely combined — application data can be statically distributed, showing how it will be converted in runtime.
* Autonomy from controversial concepts — no decorators, no need to use classes or proxies — this is not required to control the state of the application and therefore the library uses only functions and simple JavaScript objects.
* Predictability and clarity of API — a small number of basic principles are reused in different cases, reducing the user’s workload and increasing recognition. For example, if you know how .watch works for events, you already know how .watch works for stores.
* The application is built from simple elements — space and way to take any required business logic out of the view, maximizing the simplicity of the components.

**GitHub** ★**:** <https://github.com/zerobias/effector>

## Core concepts

```
import {createEvent, createStore, createEffect} from 'effector'
```

### Event

Event — is something that happens. Trigger it with some arguments to do some action.

### Store

Store — an object that holds the state. There can be multiple stores.

### Effect

Effect is a container for an async function. It triggers its done/fail events.

### combine

You can combine many stores into a single computed one.

## Codesandbox

## API Reference

<https://effector.now.sh/docs/api/effector/effector>

…

Modern state management libraries solve some problems, but they have problems themselves to a greater or lesser degree, because of which the developer sometimes has to strain more than he could.

Effector is an integrated approach to solving a problem, an attempt to do everything at once. And the attempt is quite successful.
---
title: "I Replaced 400ms Of JavaScript With 12ms Of Rust In Angular"
url: https://medium.com/p/0fee51546a5e
---

# I Replaced 400ms Of JavaScript With 12ms Of Rust In Angular

[Original](https://medium.com/p/0fee51546a5e)

Member-only story

# I Replaced 400ms Of JavaScript With 12ms Of Rust In Angular

[![Ark Protocol](https://miro.medium.com/v2/resize:fill:64:64/1*5Af7Za2-Mu7q8X3FpdM1Kg.jpeg)](/@ArkProtocol1?source=post_page---byline--0fee51546a5e---------------------------------------)

[Ark Protocol](/@ArkProtocol1?source=post_page---byline--0fee51546a5e---------------------------------------)

6 min read

·

Jan 4, 2026

--

4

Listen

Share

More

The input box lagged behind my finger.

Press enter or click to view image in full size

![]()

One character.  
One tiny pause.  
And my stomach dropped.

The page did not crash.  
It did not throw an error.  
It just hesitated.

That hesitation is louder than any exception. It tells the user that your app is weak. It tells your teammate that your performance story is imaginary. It tells you, in the most personal way possible, that the system is doing work in the wrong place.

I watched the cursor blink late.  
I watched the typed letters arrive in a small burst, like the browser was catching up on life.  
I watched a perfectly healthy backend get blamed for a front-end crime.

And the worst part was this: the code looked fine.

In review, it read like clean Angular.  
In production, it felt like I was dragging the UI through wet cement.

## The Kind Of Slowness That Feels Like You

Backend latency has a shape. You can explain it. You can graph it. You can put it in a ticket.

Front-end latency is different. It feels personal. The user does not think, the app is slow. The user thinks, this app is broken.

Input lag is the most humiliating version of slow because it attacks the one thing you cannot fake: control.

When the UI misses a keystroke, the user starts typing harder.  
When the UI delays a click, the user clicks twice.  
When the UI stutters, the user stops trusting every number it shows.

I had built a data-heavy Angular screen: a large table, filters, ranking, sorting, and a search box that had to feel instant. The product requirement was simple: type, and see results update immediately.

The dataset was not a toy. The table often held tens of thousands of rows. Each row had a numeric score, an identifier, and a few small fields used for filtering. Nothing exotic.

Still, the UI lagged. Not always. Only when it mattered.

The quiet truth was sitting there, waiting for me: the main thread was overloaded.

## The Profiling Moment That Changed My Mind

I stopped guessing and opened the Performance panel.

I recorded a single interaction: type one character into the search box and wait for the results to update.

The flame chart was not subtle. The browser was begging for mercy.

The top offender was a ranking function. A simple, innocent-looking loop that scored rows, sorted them, and returned the top results.

There was no single bug. There was no dramatic red warning. There was just a thick block of compute on the main thread. The kind of compute that steals time from rendering and input handling.

On my machine, that one function consumed roughly 400ms in the worst moments.

Four hundred milliseconds is not slow in a batch job.  
Four hundred milliseconds is catastrophic when it sits between the user and their own keystrokes.

I did what many Angular developers do next.

I tried to tune the framework.

I adjusted change detection. I reduced bindings. I tightened templates. I added trackBy. I avoided re-creating arrays. I simplified pipes. I did the usual dance where performance work turns into a hunt for cleverness.

Some of it helped. The app looked faster in empty cases.

Then I typed quickly again.

The input lag returned like it owned the place.

That was the moment the problem became clear.

This was not Angular being slow.  
This was me placing heavy compute in the wrong runtime.

## The Mistake That Made The Problem Invisible In Review

The code looked clean because JavaScript can hide cost behind readability.

A map.  
A filter.  
A sort.

You can write something elegant that quietly explodes at scale, especially when the work repeats more often than you think. Angular can call your logic more times than your intuition expects, and the user can trigger it with normal behavior.

The operation itself was not complex. It was just expensive at the wrong moment.

I needed the hot loop to leave JavaScript.

Not because JavaScript is bad.  
Because the browser is strict about what the main thread is allowed to do.

If the UI needs to feel instant, the main thread must stay light. That is the deal.

So I moved the ranking core into Rust and compiled it to WebAssembly.

## The Architecture, Drawn The Way I Explained It To Myself

```
User Input  
   |  
   v  
Angular Component  
   |  
   v  
Angular Service  
   |  
   v  
Typed Arrays (Flat Data)  
   |  
   v  
WASM Module (Rust Hot Loop)  
   |  
   v  
Sorted Ids Back To Angular  
   |  
   v  
Render Stays Smooth
```

I did not change the whole app.  
I did not rewrite Angular.  
I did not start a framework debate.

I moved one hot loop into a runtime that is built for tight compute.

## The First WASM Version Was Slower

This is the part I wish someone had warned me about.

My first version was not fast in the real app. It was fast in isolation, then disappointing when integrated.

The reason was simple and painful: I passed objects.

I moved compute into WebAssembly, then paid the bill in conversion. I was packaging data like a human-friendly message instead of an efficient memory layout.

It was a classic self-own.

WebAssembly wants flat numeric data.  
The boundary should be boring.

So I switched to typed arrays.

I stopped shipping objects across the boundary.  
I stopped serializing.  
I stopped pretending that convenience is free.

I also made initialization a one-time event. If you initialize the WASM module repeatedly, you trade one performance problem for another.

After those changes, the numbers finally matched the promise.

## The Code That Stayed Small On Purpose

I kept the interface simple: ids and scores go in, sorted ids come out.

Angular side:

```
import init, { rank } from "./pkg/ranker";  
  
let ready = false;  
export async function rankRows(ids: Uint32Array, scores: Float32Array) {  
  if (!ready) { await init(); ready = true; }  
  return rank(ids, scores);  
}
```

Rust side:

```
use wasm_bindgen::prelude::*;  
  
#[wasm_bindgen]  
pub fn rank(ids: Vec<u32>, scores: Vec<f32>) -> Vec<u32> {  
    let mut pairs: Vec<(u32, f32)> = ids.into_iter()  
        .zip(scores.into_iter())  
        .collect();  
    pairs.sort_by(|a, b| b.1.partial_cmp(&a.1).unwrap());  
    pairs.into_iter().map(|p| p.0).collect()  
}
```

No fancy abstractions.  
No clever generics.  
No performance theater.

A tight loop.  
Flat data.  
Predictable work.

## The Benchmark That Ended The Argument

I measured the operation the only way that mattered: inside the user interaction.

Same dataset.  
Same UI action.  
Multiple runs.  
I looked at the median and also the worst spikes because that is what users feel.

The dataset in this test was 25,000 rows, each with one score. The user action was typing into the search box to re-rank and update visible results.

```
| Path               | Compute Time           | What The User Felt                          |  
| ------------------ | ---------------------- | ------------------------------------------- |  
| JavaScript Ranking | ~400ms (worst moments) | Sticky input, delayed cursor, double clicks |  
| Rust In WASM       | ~12ms                  | Clean typing, instant response, stable UI   |
```

The 12ms number matters, but the emotional impact matters more: the UI stopped arguing with the user.

The cursor stayed honest.  
The screen stopped feeling fragile.  
The app started feeling like it respected the user’s hands.

## The Real Lesson Was Not Rust

Rust was the tool.

The lesson was placement.

If your UI feels slow, you might not have a rendering problem. You might have a compute placement problem. When heavy work sits on the main thread, no amount of template cleanup will save you.

This experience rewired how I think about performance in Angular.

I stopped asking, how do I make Angular faster.  
I started asking, what work deserves to stay in JavaScript.

Because once you see input lag as a symptom of misplaced compute, you never unsee it.

And once you fix it, you gain something that no micro-optimization gives you.

You gain trust.
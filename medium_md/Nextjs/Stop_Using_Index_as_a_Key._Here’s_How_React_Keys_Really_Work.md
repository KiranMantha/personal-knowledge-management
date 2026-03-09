---
title: "Stop Using Index as a Key. Here’s How React Keys Really Work"
url: https://medium.com/p/07423f3d9b33
---

# Stop Using Index as a Key. Here’s How React Keys Really Work

[Original](https://medium.com/p/07423f3d9b33)

Member-only story

# Stop Using Index as a Key. Here’s How React Keys Really Work

## **The secret behind those weird UI bugs you only see after clicking around**

[![Sanjeevani Bhandari](https://miro.medium.com/v2/resize:fill:64:64/1*Sj1DOUmlNi9JaXsD5oKm1w.jpeg)](https://medium.com/@sanjeevanibhandari3?source=post_page---byline--07423f3d9b33---------------------------------------)

[Sanjeevani Bhandari](https://medium.com/@sanjeevanibhandari3?source=post_page---byline--07423f3d9b33---------------------------------------)

4 min read

·

Jan 8, 2026

--

3

Listen

Share

More

*You add a new item to a list.*

Suddenly, the wrong row updates.  
Input values jump.  
Animations glitch for half a second and then fix themselves.

***You stare at the code. Everything looks right.***

Then someone says, “*Did you check the keys?*”

That moment is a React rite of passage.

Press enter or click to view image in full size

![]()

## The uncomfortable truth about React keys

Most of us learn about keys like this:

> *“***Keys help React identify which items have changed.***”*

Cool.  
Vague.  
Not very useful.

So we do the obvious thing:

Press enter or click to view image in full size

![]()

React stops complaining.  
We move on.

**Until it doesn’t work.**

## What React is actually trying to do

React is obsessed with *efficiency*.

When a list changes, React does not want to re-render everything.

> It wants to figure out what stayed the same,
>
> what moved, and what changed.

**Keys are how React tracks identity.**

**Not position.  
Not order.  
Identity.**

If React knows that “*this item is the same one as before,*” it can reuse the component and its state.

If it doesn’t, it guesses.

And React is very confident when it guesses.

## Why using index as a key breaks things

Indexes feel safe because they are stable… until they aren’t.

Imagine this list:

```
['Apple', 'Banana', 'Cherry']
```

Rendered like this:

```
items.map((item, index) => (  
  <input key={index} defaultValue={item} />  
))
```

Now insert “Orange” at the top.

The ***indexes*** shift.

React thinks:

* *Apple became Banana*
* *Banana became Cherry*
* *Cherry became… something else*

> The inputs keep their internal state, but now that state is attached to the wrong item.

That’s when you see:

* wrong values
* wrong focus
* wrong animations
* bugs that disappear on refresh

***React did exactly what you told it to do.***

## A better mental model for keys !!!

Think of keys like name tags at a conference.

> If everyone wears a name tag, you can move people around and still know who’s who.

* If people are identified only by where they’re sitting, chaos follows the moment someone stands up.

Keys are name tags.

**Indexes are seat numbers.**

## What makes a good key

A good key is:

* Stable across renders
* Unique among siblings
* Tied to the data, not the UI

*Most of the time, this means an ID from your data.*

Press enter or click to view image in full size

![]()

This tells React, “**This thing is the same thing as before, even if its position changes.**”

> React relaxes. Your UI behaves.

## Why keys affect state, not just rendering

This part surprises people.

> Keys don’t just affect how React renders.  
> They affect component state.

> React uses keys to decide whether a component instance should be reused or recreated.

*Change the key, and React throws the old component away.*

This is why this works:

```
<Form key={userId} />
```

* Switch users.  
  Form resets.  
  No manual cleanup needed.

You didn’t reset state explicitly.  
You told React, “*This is a different thing now.*”

That’s power.

## When keys actually don’t matter much

Here’s the nuance nobody tells you.

Keys matter most when:

* Lists change order
* Items are inserted or removed
* Components hold internal state

*If your list:*

* Never changes
* Never reorders
* Is purely presentational

Then using index as a key won’t explode anything.

*This is fine:*

```
['Mon', 'Tue', 'Wed'].map((day, index) => (  
  <span key={index}>{day}</span>  
))
```

Static list.  
No state.  
No reordering.

React won’t punish you for this.

*The problem is copying that pattern everywhere without thinking.*

## When using index is actually dangerous

Use index as a key and you are likely to regret it if:

* The list can be filtered
* Items can be sorted
* Items can be added or removed
* Child components store state
* Inputs are involved
* Animations are involved

Basically, if the list behaves like real data, index is a trap.

Press enter or click to view image in full size

![]()

## Keys and performance myths

Keys do not magically make React faster.

They make React more correct.

Bad keys can cause:

* unnecessary re-renders
* state mismatches
* subtle bugs that look like performance issues

***Good keys help React avoid unnecessary work, but correctness is the real win.***

Performance comes second.

## One subtle mistake even experienced devs make

Using keys that change over time.

```
key={Math.random()}
```

or

```
key={Date.now()}
```

*This forces React to remount everything on every render.*

**State resets.  
Effects rerun.  
Performance tanks.**

> If your key changes every render, it is not a key.
>
> It is a reset button.

*Keys are not a React rule to silence warnings.*

They are a contract.

You are telling React: “**This thing is the same thing as before.**”

If that statement is true, your UI stays predictable.  
If it’s false, React will confidently do the wrong thing.

Most React bugs around lists are not React bugs. They are identity bugs.

**And once you see keys as identity, not syntax, everything clicks.**

***Thanks for reading. If this felt familiar, feel free to follow. And if you’ve ever been burned by keys in a weird way, drop it in the comments.***
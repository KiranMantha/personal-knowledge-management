---
title: "The Power of the Observer Pattern in JavaScript"
url: https://medium.com/p/4f4e0b908d5e
---

# The Power of the Observer Pattern in JavaScript

[Original](https://medium.com/p/4f4e0b908d5e)

Member-only story

# The Power of the Observer Pattern in JavaScript

## Build a DMV ticket-calling system

[![jsmanifest](https://miro.medium.com/v2/resize:fill:64:64/2*hMSDnIbezH2uXPYk7tV2hA.jpeg)](/@jsmanifest?source=post_page---byline--4f4e0b908d5e---------------------------------------)

[jsmanifest](/@jsmanifest?source=post_page---byline--4f4e0b908d5e---------------------------------------)

6 min read

·

Oct 6, 2019

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

In this post, we will be going over the observer patternand implementing it with JavaScript so that, hopefully, you can attain a better understanding of it, especially if you were having trouble understanding the concept.

The observer pattern remains one of the best practices for designing decoupled systems and should be an important tool for any JavaScript developer.

The observer pattern is a design pattern in which subjects (which are simply just *objects* with methods) maintain a list of observers who are *registered* to be notified of upcoming messages.

When they receive a notification event about something on the subject they are attached to, they can use these opportunities to do something useful, depending on what was received from them.

The pattern is most useful in situations when you need multiple objects to get notified simultaneously at the same time of recent changes to state. Thus, the power of this pattern comes to light when you need multiple objects to maintain consistency throughout your app, as opposed to having tightly coupled classes.

With that said, it’s even possible to have several objects that aren’t directly related to each other to stay consistent at the same time.

Observers can remove themselves after they were attached, so there’s even some flexibility on opting in and out for one observer and the next, and vice versa.

When you have all of this functionality combined, you can build dynamic relationships between subjects and observers that make up robust functionality.

## The Concept

When an observer is concerned about a subject’s state and wants to opt in to observeupcoming state updates to it, they can register or attach themselves to them to receive upcoming information.

Then, when something changes, those observers will be able to get notified about it, including the updates thereafter. This is done when the subject sends notification messages to its attached observer(s), using a broadcasting method.

Each of these notification messages can contain useful data to one or more observers that receive them. The way that notifies that messages are sent usually invokes a `notify` method to loop through its list of observers and inside each loop it would invoke an observer’s `update` method.

When the observer no longer wishes to be associated with the subject, they can be detached.

Here is a short and precise table with all of the common participants that make up this pattern:

Now, let’s go ahead and see how this might look like in code.

The first thing we are going to do is to begin creating the subject that will hold an interface for managing its observers. To do that, we are actually going to define the constructor on a separate function called `ObserversList`:

And then we attach this interface directly on a property of a subject:

```
function Subject() {  
  this.observers = new ObserversList()  
}
```

We could have defined the prototyped methods directly on the subject, but the reason we don’t is because the subjects are usually going to be arbitrary instances of something in a real-world use case that just needs to inherit the observer interface, and then possibly extending its functionality or creating wrappers around them.

Now, we will go ahead and define the `Observer`:

```
function Observer() {  
  this.update = function() {}  
}
```

When different objects inherit the `Observer`, what usually happens is that they overwrite the `update` (or an updater) function that is interested in data that they were looking for.

This is because, when the subject invokes its `notifyAll` method, the observer’s updater function is used on each loop.

You can see this in action:

## Real-World Example

Let’s now move on to a real-world example.

Pretend that we are operating a [DMV](https://www.dmv.ca.gov/) in the location `Alhambra`. We're going to implement the ticket-calling system, using the observer pattern.

In a typical ticket-calling system at the DMV, people are usually given a ticket number when they are placed into the waiting list and they’d wait until their number is called.

Right before they were given their ticket number, the DMV checks if there is already a booth available before handing it to them. If there are no booths available, that’s when they get placed onto the waiting list with their assigned ticket number.

When a person completes their session at the booth, let’s pretend that they’re done for the day. This is when their ticket number is no longer in use and can be re-used again later.

In our example, we’ll be marking the ticket numbers as immediately available to assign to someone else that will get placed onto the waiting list.

The first thing we need to do is to define the `DMV` constructor:

In our example, the `DMV` is the `subject` because it's going to manage a list of people and ticket numbers.

We set a `maxTicketsToProcess` parameter because, without it, the waiting list will always be empty because we won't have a way to know when it's appropriate to place a person onto the waiting list.

When `maxTicketsToProcess` is reached, we would start placing people onto the waiting list with a ticket number if there are still tickets in `this.ticketsFree`.

Now, when we look at the `DMV` constructor, it's assigning `this.waitingList` with a `WaitingList` instance. That `WaitingList` is basically the `ObserversList` as it provides a nearly identical interface to manage its list of people:

`broadcastNext` is the equivalent of our `notifyAll` method from the `ObserversList` example. Instead of calling `.update`, however, we call `.notifyTicket` which is defined on the `person` instance (which we will see in a bit).

We provide an `accept` callback function as the second argument because this will simulate the real-life scenario when a person looks at their ticket number, realizes that their assigned number is being called and walks up to their booth.

Let’s define a `Person` constructor to instantiate for each person:

```
function Person(name) {  
  this.name = name  
}
```

You might have realized that the method `notifyTicket` is missing, as we used it here:

```
person.notifyTicket(ticketNum, function accept() {
```

This is fine, because we don’t want to mix in a waiting list’s interface with a generic `People` one.

So, we’re going to create a `WaitingListPerson` constructor that will contain its own interface specifically for people on the waiting list as we know that these functionalities won’t be of any use after the person is taken out of it. So, we keep things organized and simple.

The way we are going to extend instances of `Person` is through a utility called `extend`:

```
function extend(target, extensions) {  
  for (let ext in extensions) {  
    target[ext] = extensions[ext]  
  }  
}
```

And here is the definition for `WaitingListPerson`:

Great! The last thing we are going to do is to finally implement the methods to `DMV` so that it will actually be able to add/remove people, manage ticket numbers, etc.

Now we have a sufficient DMV ticketing system, backed by the observer pattern!

Let’s see this in use:

Press enter or click to view image in full size

![]()

So now we’ve seen how far the observer pattern can take your app. We’ve taken advantage of it to build a functional DMV ticket calling system. Give yourselves a pat on the back!

And that is the end of this post! I hope you found this valuable and look out for more in the future.

Want to keep in touch? Subscribe to my [newsletter](https://app.getresponse.com/site2/javascript-newsletter?u=zpBtw&webforms_id=SM2hz).
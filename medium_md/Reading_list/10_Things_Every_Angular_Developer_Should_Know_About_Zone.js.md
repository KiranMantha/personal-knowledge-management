---
title: "10 Things Every Angular Developer Should Know About Zone.js"
url: https://medium.com/p/573d89bbb890
---

# 10 Things Every Angular Developer Should Know About Zone.js

[Original](https://medium.com/p/573d89bbb890)

Member-only story

# 10 Things Every Angular Developer Should Know About Zone.js

## Every developer should know the basics about Zone.js

[![Matthias Junker](https://miro.medium.com/v2/resize:fill:64:64/0*M8vt1xlOEoaFhq9x.jpg)](/@matt_junker?source=post_page---byline--573d89bbb890---------------------------------------)

[Matthias Junker](/@matt_junker?source=post_page---byline--573d89bbb890---------------------------------------)

6 min read

·

Oct 8, 2019

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

## 1. Why Should I Care About Zone.js?

Angular introduced [Zone.js](https://github.com/angular/zone.js/) to handle change detection. This allows Angular to decide when the UI has to be refreshed. Usually, you don’t have to care about any of this, because Zone.js just works.

However, if something goes wrong with Zone.js it can be very frustrating to analyze and understand. This is why every developer should know some basics about Zone.js.

## 2. In a Nutshell: How Does Zone.js Work?

Zone.js patches all common async APIs like `setTimeout`, `setInterval`, the promise API, etc. to keep track of all async operations.

Here are the basic concepts you should understand:

### **Zone**

Zone is a mechanism for intercepting and keeping track of asynchronous work.

### **Tasks**

For each async operation, Zone.js creates a task. A task is run in one zone.

### **NgZone**

By default, in an Angular app every task runs in the “Angular” Zone, which is called `NgZone`. There is only one Angular Zone and change detection is triggered exclusively for async operations which run in the `NgZone`.

### **Root Zone/Forks**

Zone.js zones are hierarchical which means you always start with a top-level Zone — the “root” Zone. New Zones can be created by forking the root Zone. NgZone is also a fork of the root Zone.

### **ZoneSpecs**

When forking a Zone, a new Zone will be created based on a `ZoneSpec`. A `ZoneSpec` can just include a name for the new child Zone, or can include various Hook methods which can be used to intercept certain Zone/task events.

There are more concepts and if you want to learn more about how Zone.js works, you can find more information here:

[## Understanding Zones

### Join our upcoming public training! Get a ticket → At NG-Conf 2014, Brian gave an excellent talk on zones and how they…

blog.thoughtram.io](https://blog.thoughtram.io/angular/2016/01/22/understanding-zones.html?source=post_page-----573d89bbb890---------------------------------------)

## 3. You Don’t Have to Use Zone.js With Angular (but You Probably Should)

Zone.js can easily be deactivated during bootstrapping of an Angular application by passing a `noop` Zone. However, you give up change detection, which means you have to decide yourself when the UI has to be refreshed (e.g. via `ChangeDetectorRef.detectChanges()`).

In general, this is not recommended because you give up the convenience of automatic change detection, however, for custom elements (Angular elements) this might make sense.

More details about how to disable Zone.js can be found at [Software Architect](https://www.softwarearchitekt.at/aktuelles/angular-elements-part-iii/).

## 4. Automagic Change Detection Is Fine, but What If I Want Control?

There might be cases where you run into problems because change detection is triggered too often which might lead to performance problems.

If you still want the benefits of Zone.js, but want to control what triggers change detection and what doesn’t, you can still do that.

By injecting the `NgZone`, you get an API for deciding if an async operation runs in or outside of the `NgZone`. The method `runOutsideAngular` can be used to run code outside `NgZone` so change detection is not triggered.

Here’s an example:

```
constructor(private ngZone: NgZone) {  this.ngZone.runOutsideAngular(() => {  
    // this will not trigger change detection  
    setInterval(() => doSomething(), 100)  
  });  
}
```

## 5. How Does Zone.js Affect Protractor Tests?

A Zone is stable once no async operations are running anymore. A “healthy” Zone starts stable, then some tasks are run which means the Zone becomes “unstable” and, at some point, tasks complete which means the Zone becomes stable again.

What does this have to do with protractor? If you use `browser.waitForAngular` in your E2E tests then protractor checks the `NgZone` to determine if the test can continue.

So, after every command you send to the browser, Protractor will wait until the zone becomes stable, and only continue then. If you’re using, for example, `setInterval` with a short interval time this will mean that the `NgZone` will never stabilize and your test will freeze and timeout.

These kinds of problems can be solved by running long-running or repeatedly running tasks outside of the Angular Zone.

## 6. How Does RxJS Work With Zone.js?

By default, Zone.js and [RxJS](https://rxjs-dev.firebaseapp.com/) might not behave as you expect. For example, you might wrap your observable code in a function and pass it to `NgZone.runOutsideAngular`, and still end up with a task that runs inside the `NgZone`.

When using RxJS, you should always import the patch from Zone.js which gives a more reasonable behavior. At construction time of a subscription, operator, or observable it will remember the current zone and will always run in the remembered zone, independently of where you subscribe.

You can import the patch like this right after you import Zone.js (typically in `polyfill.ts`):

```
import ‘zone.js/dist/zone-patch-rxjs’;
```

A good example of how this works can be found in the [documentation](https://github.com/angular/zone.js/blob/master/NON-STANDARD-APIS.md).

## 7. How to Exclude Certain Events From Zone.js

If, for some reason, you don’t want change detection for certain event types ( `Scroll-Events`, …) you can blacklist these globally.

However, remember that you will have to trigger change detection manually in these cases. An example of how to do this can be found in the documentation under `BlackListEvents`.

## 8. How Can I Analyze Problems With Zone.js?

When debugging Zone.js issues for the first time, it can be a daunting task.

Zones don’t offer an API for inspecting scheduled/currently running tasks. Also, sometimes it can be hard to figure out where a task actually originates from, because in the stack trace you can only see Zone-related entries.

Luckily, Zone.js provides some tools which can help to understand what is going on.

Zone.js includes some Zone specs that can be used to construct Zones from which we can fork a Zone we want to investigate. There are two `ZoneSpecs` which are very useful:

* `TaskTrackingZoneSpec`:Can be used to track all current tasks and offers an API to inspect them.
* `LongStackTrace`:Remembers for each task all the stack traces of all predecessor tasks. So, you basically have one big stack trace over all asynchronous steps that led to the creation of the task you want to inspect.

Here’s a short snippet on how these can be used to inspect the Angular Zone:

```
// increase stack trace length (optional)  
Error.stackTraceLimit = 100;  
const longStackTraceZoneSpec = Zone.longStackTraceZoneSpec;// increase stack trace limit (optional)  
longStackTraceZoneSpec.longStackTraceLimit = 1000;Zone.current  
.fork(new Zone.TaskTrackingZoneSpec())  
.fork(longStackTraceZoneSpec)  
.run(() => {  
   // NgZone forks currentZone, which is here longStackTraceZone  
   const ngZone = new NgZone({enableLongStackTrace: true});  
   platformBrowserDynamic()  
      .bootstrapModule(AppModule, {ngZone: ngZone});  
});
```

You can then access, for example, tasks of type `macroTask` like this:

```
let macroTasks = Zone.current  
 // get the TaskTrackingZone via it's name  
 .get(‘TaskTrackingZone’)  
 .getTasksFor(‘macroTask')
```

## 9. What Are Micro and Macro Tasks?

When debugging Zones, you will see that there are different types of tasks: micro and macro. In general, it’s best to start looking at the macro tasks first, because most problems are related to macro tasks.

But what is the difference between theses types>

In short, micro tasks are scheduled immediately after the current task (in the current VM turn), and macro tasks are only scheduled in the next VM turn. A detailed explanation can be found in this excellent article by 

[Jake Archibald](/u/f87cd234b9d9?source=post_page---user_mention--573d89bbb890---------------------------------------)

:

[## Tasks, microtasks, queues and schedules

### When I told my colleague Matt Gaunt I was thinking of writing a piece on microtask queueing and execution within the…

jakearchibald.com](https://jakearchibald.com/2015/tasks-microtasks-queues-and-schedules/?source=post_page-----573d89bbb890---------------------------------------)

## 10. How Does Zone.js Work With Ng-Upgrade?

When you’re migrating from an Angular.js app to a hybrid app using `ng-upgrade`, this can lead to hard-to-debug problems.

The first thing you will notice when using `ng-upgrade` is that all async operations also are executed in the `NgZone`. This makes sense because Zone.js automatically patches all async APIs.

You might notice, in some cases, that performance is getting worse. This might be an indicator to look at what’s happening between Zone.js and the digest cycles from Angular.js.

Whenever all micro tasks are done in the NgZone, `ng-upgrade` triggers a `$digest` on the `rootScope`.

If a digest triggers any async code like a `setTimeout`, this will create another task in the `NgZone`. Once this is done `$digest` will be triggered again and again.
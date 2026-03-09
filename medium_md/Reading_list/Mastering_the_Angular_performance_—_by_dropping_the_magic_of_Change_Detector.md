---
title: "Mastering the Angular performance — by dropping the magic of Change Detector"
url: https://medium.com/p/2b605b444b04
---

# Mastering the Angular performance — by dropping the magic of Change Detector

[Original](https://medium.com/p/2b605b444b04)

# Mastering the Angular performance — by dropping the magic of Change Detector

[![Jack Tomaszewski](https://miro.medium.com/v2/resize:fill:64:64/1*rTHmzhomGgoB_cqQhX2Pag.png)](https://jtomaszewski.medium.com/?source=post_page---byline--2b605b444b04---------------------------------------)

[Jack Tomaszewski](https://jtomaszewski.medium.com/?source=post_page---byline--2b605b444b04---------------------------------------)

6 min read

·

May 17, 2018

--

7

Listen

Share

More

**In big Angular 2+ applications, that consist of hundreds of components being rendered at the same time, you cannot rely solely on Angular Change Detection mechanism *magically* refreshing your view.** If your end-user has to wait 50ms every time he types a letter in a text input, because your framework has to trigger template binding checks for each of your currently living components in the app, then something has gone wrong.

**Luckily, there’s** `ChangeDetectionStrategy.OnPush` **.** A new feature introduced in version 2 of this framework, allows us to skip checks for the given component (and thus, all its’ nested children), if its’ `@Input()` bindings haven’t been changed.

Then, even if we trigger Change Detection every time something happens in our app (for example, a user types something in a text input), it will be way less painful, because Angular will recheck only a small subset of our component tree.

For example let’s say we’re on a typical search results page like below:

Press enter or click to view image in full size

![]()

1. On the left we have filters. We want them to be updated and rechecked only if any of the filters has been changed.
2. In the middle top we have search query input. We want it to be updated and rechecked only if search query has been is changed.
3. Below it we have the search results. We want it to be updated and rechecked only if any of the results or the pagination data has been changed.

If I do it the Redux-way, that is I keep the state of all the page in one object AND I will keep all the actions logic in the page component, then this is how its’ html template would look like:

In this way we have everything what we wanted. Our page component tree is split into 3 subtrees. **Even if we recheck the page component’s bindings every time the** `state` **is changed, it won’t do much more than it**, because in fact it will be rechecking bindings only for this component and for one of its’ nested subtrees, like `my-search-page-query-filters` — because in most of the cases, a change that happens influences only one of the subtrees.

If we divide our application evenly into components that have children components (that have further children components), then a well designed app should resemble a balanced tree like the left one in below:

![]()

**Even if our app has about *n = 1000* living components and a change happens somewhere deep in the tree, it’ll end up rechecking no more than ~10 of them, because the depth of tree is equal to *d = log n.***

(You can see it in our demo at <https://stackblitz.com/edit/angular-qyybtn> .)

### Cutting down the change detection tree even more — by detaching its’ root from the Change Detector

**Sometimes though we don’t want the component tree to be rechecked from its’ top root.** For example, let’s say that deep down in the `my-search-page-results` component we have a `my-search-page-result-inline-form` that lets us edit rows in-place. We had decided that the temporary state of the form is unimportant to us from the page’s component perspective, and we’ll keep it as a internal state of `my-search-page-result-inline-form` component.

When anything in the `my-search-page-result-inline-form` is being changed, only this component (and prospectively its’ children) should be updated. There’s no need to recheck the `my-search-page` on each key input that happens somewhere deep down in an inline form.

So, to implement it, it should be enough to keep the state locally in the component and after any change just call `ChangeDetectorRef#detectChanges()`, right? **Unfortunately, it is not. Whenever Angular receives a new event in the component (f.e. through** `(click)="handleClick($event)”`**), besides just calling the event listener, it apparently also calls** `ChangeDetectorRef#markForCheck()` **for that component, making the Angular recheck all its’ ancestors**… Which is not what we intended.

**We discovered it only after setting up a demo and debugging the change detection mechanism ourselves.** (You can see it here: <https://stackblitz.com/edit/angular-qyybtn> .) Neither the documentation or any of the publicly available articles about Angular Change Detection mentioned such behaviour (and we had read them a lot, believe me), so it was quite a surprise to us.

**There’s a workaround though**: if at least one of the component’s ancestors is detached from the Change Detector through `ChangeDetectorRef#detach()`, then it will function properly as we wanted: an internal change in a nested OnPush component will check only that given component and its’ children, nothing more.

We showcased it in [our demo](https://stackblitz.com/edit/angular-qyybtn) and compared the performance of component written in both ChangeDetectionStrategy.Default/OnPush with and without `ChangeDetectorRef#detach()`. The result clearly shows that detaching the tree from Change Detector helps a lot, because:

1. When using `ChangeDetectionStrategy.Default`, it is suuuper slow — because all subscribed events trigger Change Detection checks for all the living components in the app),
2. When using `ChangeDetectionStrategy.OnPush`, it is kind of okay — because all subscribed events trigger Change Detection checks only for the component where the event happened and its’ all ancestors,
3. When using `ChangeDetectionStrategy.OnPush` with the detached ancestor, it is even faster — because if a change happens deep down in a tree, it rechecks only the given component where the event happened, nothing more.

The only disadvantage of the approach with `ChangeDetectionStrategy.OnPush` is that **from then on you have to manually inform Angular about any changes to the internal state of the component**. **To me, that’s actually an advantage,** because it forces you to use `@Input()` more often or to explicitly inform Angular about any external changes happening to your components.

(In [Recruitee](https://jobs.recruitee.com/) we even went as far as to implement a React-like `this.setState({{...})` function, that updates the component state and calls `ChangeDetectorRef#detectChanges()`. We’re using it in all parts of our app, whenever a component has a local state that impacts its’ view.)

The approach with using `ChangeDetectionStrategy.OnPush` has also another big advantage: **If you do it everywhere in your app, you can disable the NgZone for free!** When your app is manually informing Angular about all the internal changes to your app components (either by changing their `@Input()` values or by calling `ChangeDetectorRef#detectChanges()`), then there’s no reason to have NgZone anymore. **Which means less magic, better performance, and much clearer error stack traces ;)**

### TL;DR

1. **Always use** `ChangeDetectionStrategy.OnPush` **.**
2. **Try to divide your component tree as much as you can**, so you won’t be rechecking everything whenever anything small happens.
3. **Try detaching your top components from the Change Detector.** You’ll have to explicitly inform Angular about any external changes to your components, either by updating `@Input()` values for their children or by calling `ChangeDetectorRef#detectChanges()`. In exchange you’ll get much better performance and complete control over Change Detection mechanism. It might also improve your components code readability.

We’re doing it in [Recruitee](https://recruitee.com/admin) since December 2017 and we have already rewrote most of our existing components, so that instead of relying on the magic of NgZone and Change Detection, they just call `this.cdRef.detectChanges()` whenever something is changed in their internal state. We’re already seeing huge gains in performance. Also, the code seems to be more readable, since now we exactly know when each of the components will be changed and how.

**What do you think?** Would you do a similar “sacrifice”, if you cared about performance and scalability of your Angular application? Feel free to comment.

—

P.S. I’m currently looking for a job! 🙂 If you’re in need of a full-stack web dev or a tech lead, check out my [portfolio](https://jtom.me/portfolio) / [CV](https://jtom.me/cv/ideal.html) and [message me](https://jtom.me/contact). Happy to relocate if needed.
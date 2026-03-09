---
title: "RxJS | Create Observables from event sources directly"
url: https://medium.com/p/2b7c96170e17
---

# RxJS | Create Observables from event sources directly

[Original](https://medium.com/p/2b7c96170e17)

# RxJS | Create Custom Observables from event sources directly

[![Simar Paul Singh](https://miro.medium.com/v2/resize:fill:64:64/1*yAH5Ot82WG0pmz7ZlfcSwQ.jpeg)](/@simars?source=post_page---byline--2b7c96170e17---------------------------------------)

[Simar Paul Singh](/@simars?source=post_page---byline--2b7c96170e17---------------------------------------)

3 min read

·

Oct 26, 2018

--

Listen

Share

More

**RxJs** simplifies working with event streams. In **Angular**, we get notified of almost all events and changes by *subscribing* to **RxJs** `Observable(s)` Ex ([*ActvatedRoute#params*](https://angular.io/api/router/ActivatedRoute#params) , [*HttpClient*](https://angular.io/guide/http)*#get)*.

We seldom create our own `Observable(s)` from an actual *event source.* Unless, you consider emitting known values, with of and from as we usually do in our tests.

```
import { Observable, of, from } from 'rxjs';Observable<String> one = of('1');  
Observable<String> oneTwoThree = from(['1','2', '3']);
```

**RxJs** provides us handy utility *function* `from(...) : Observable<T>` to create `Observable(s)` from well known event sources, (Ex. a native *dom-event)*.

Here is an example of`fromEvent(input[click]):Observable`*,* implementing a text-input search-box, which can notify us of changing text.

```
import {AfterViewInit, Component, ElementRef, EventEmitter, OnDestroy, OnInit, Output, ViewChild} from '@angular/core';  
import {fromEvent, Observable, Subscription} from 'rxjs';  
import {debounceTime, distinctUntilChanged, map, startWith, tap} from 'rxjs/operators';@Component({  
  selector: 'search-box',  
  template: `  
    <div>  
      <input placeholder="search" #searchInput autocomplete="off"/>  
    </div>  
`  
})  
export class SearchBoxComponent implements AfterViewInit, OnDestroy {@Output('onSearch')   
onSearch = new EventEmitter<string>();@ViewChild('searchInput')   
input: ElementRef;private subscription: Subscription;ngAfterViewInit(): void {  
 const terms$ = fromEvent<any>(this.input.nativeElement, 'keyup')  
      .pipe(  
        map(event => event.target.value),  
        startWith(''),  
        debounceTime(400),  
        distinctUntilChanged()  
      );  
   this.subscription = term$  
      .subscribe(  
        criterion => {  
          this.onSearch.emit(criterion);  
        }  
      );}ngOnDestroy() {  
    this.subscription.unsubscribe();  
  }}
```

## Custom Observable(s)

Sometimes source of your event(s) is not well known, and likely **RxJs** wouldn’t have any stock functions to create `Observable(s)` of it.

RxJs provides a mechanism to create our own Observable(s).

***Observable.create(function(observer) {***

*// create or listen to an event-source (ex promises)*

*// decide when to call observer.(next|error|complete)*

***})***

For example, Let us try creating our own `Observable` the works like Angular’s `Http.get` using the **browser’s native** `fetch`-api

```
import {Observable} from 'rxjs';  
  
  
export function createHttp$(url:string) {  
  return Observable.create(observer => {  
  
    const controller = new AbortController();  
    const signal = controller.signal;  
  
    fetch(url, {signal})  
      .then(response => {  
         if (response.ok) {  
           return response.json();  
         }  
         else {  
           observer.error(`Failed HTTP : response.status`);  
         }  
      })  
      .then(body => {  
         observer.next(body);  
         observer.complete();  
      })  
      .catch(err => {  
         observer.error(err);  
       //observable which immediately errors out  
      });  
  
   return () => controller.abort()  
   // this return function? executed on unsubscribe  
  });  
}
```

This is how we can use it

```
const http$ = createHttp$('/some/url');  
http$.subscribe({      
 next: (value: any) => console.log(`next ${value}`),      
 complete: () => console.log(`complete`)};  
);
```

Everything in the above code-snippet is straightforward besides the *function* returned by `Observable.create(…)` which is the one ***that’s called when you unsubscribe to the observable created*** created by `createHttp$(...)`.

Browser’s `fetch(…)` API gives us way to cancel ongoing requests by sending an abort signal. Therefore we send the abort signal when the subscriber unsubscribes from on Observable before it completes. This will cancel long running *http-get-request* to which no one now is subscribing.

```
const url = '/some/entity';  
const http$ = this.activatedRoute.params.pipe(  
 switchMap( id => createHttp$(`${url}/${id}`))  
).subscribe({      
  next: (value: any) => console.log(`next ${value}`),      
  complete: () => console.log(`complete`)};  
);
```

In the example above, we listen to changing URL parameters emitted from `Router’s` from `activatedRoute.params` and issue corresponding *http* requests with newly emitted param value `{id}` using `Observables(s)` created by calling`` createHttp$(`${url}/${id}`)) ``

However since we are using `switchMap(…)` to emit new `createHttp$(…)` `Observales`, the previously emitted `Observable` is first *unsubscribed* (cancelled) before a new one is created and emitted by `switchMap(…)`.

Since `Observable(s)` created from `createHttp$(...)` implements and returns function for cancellation, if *http* request inside was still on going in the `Observable` being *unsubscribed*, it will get *aborted* before new `createHttp$(...)` `Observable` is created and emitted by `switchMap` with in which a new *http* request gets issued.
---
title: "Mastering Concurrent/Multiple API Requests with RxJS: A Deep Dive into resource/rxResource and RxJS…"
url: https://medium.com/p/da53e544b0d8
---

# Mastering Concurrent/Multiple API Requests with RxJS: A Deep Dive into resource/rxResource and RxJS…

[Original](https://medium.com/p/da53e544b0d8)

# Mastering Concurrent/Multiple API Requests with RxJS: A Deep Dive into resource/rxResource and RxJS Operators

[![Muhammad Awais](https://miro.medium.com/v2/resize:fill:64:64/1*NnDOVXdGrdEWBXXK6o9BXA.jpeg)](https://medium.com/@awaisshaikh94?source=post_page---byline--da53e544b0d8---------------------------------------)

[Muhammad Awais](https://medium.com/@awaisshaikh94?source=post_page---byline--da53e544b0d8---------------------------------------)

6 min read

·

Feb 3, 2025

--

2

Listen

Share

More

In modern Angular applications, handling multiple API requests efficiently is crucial for optimizing performance and ensuring a smooth user experience. There are various ways to achieve this using RxJS operators, depending on the use case. This article explores different approaches to managing multiple HTTP requests effectively using [angular v.19 resource & rxResource API](https://medium.com/javascript-in-plain-english/angular-v19-seamless-api-integration-using-experimental-resource-rxresource-api-ec5ff0656719)

Press enter or click to view image in full size

![]()

## Older Approach — with RxJS Operators only

In previous approaches to handling multiple API requests in Angular, developers often relied on using RxJS operators along with direct subscriptions. While this method was widely used, it had its drawbacks, such as the risk of nested subscriptions and difficulty in managing complex asynchronous flows. In this article, we will revisit the older way of handling multiple API requests, where developers primarily used `subscribe()` with RxJS operators to manage concurrency.

### 1. Using Nested Subscriptions (Not Recommended)

A common but inefficient approach is using nested subscriptions. This method often leads to callback hell and makes the code difficult to maintain.

```
this.http.get('https://jsonplaceholder.typicode.com/users/1')  
  .subscribe(user => {  
    this.http.get(`https://jsonplaceholder.typicode.com/posts?userId=${user.id}`)  
      .subscribe(posts => {  
        console.log(user, posts);  
      });  
  });
```

**Why avoid this?**

* Leads to deeply nested structures
* Harder to debug and maintain
* Not scalable for multiple requests

### 2. Using `mergeMap` (Better Approach)

The `mergeMap` operator flattens nested observables, making the code cleaner and more readable.

```
this.http.get('https://jsonplaceholder.typicode.com/users/1')  
  .pipe(  
    mergeMap(user =>  
      this.http.get(`https://jsonplaceholder.typicode.com/posts?userId=${user.id}`).pipe(  
        map(posts => ({ user, posts }))  
      )  
    )  
  )  
  .subscribe(data => console.log(data));
```

* Removes nested subscriptions
* Improves readability
* Maintains a functional programming approach

### 3. Using `forkJoin` (When Requests Are Independent)

If multiple API calls are independent but need to be executed simultaneously, `forkJoin` is an excellent choice. It waits for all requests to complete before returning the combined result.

```
forkJoin({  
  user: this.http.get('https://jsonplaceholder.typicode.com/users/1'),  
  posts: this.http.get('https://jsonplaceholder.typicode.com/posts?userId=1')  
})  
.subscribe(data => console.log(data));
```

* Executes all requests in parallel
* Returns results only when all requests complete
* Handles independent requests efficiently

If any request fails, the entire `forkJoin` will fail. To handle errors gracefully, wrap each request with `catchError`.

```
forkJoin({  
  user: this.http.get('https://jsonplaceholder.typicode.com/users/1').pipe(catchError(() => of(null))),  
  posts: this.http.get('https://jsonplaceholder.typicode.com/posts?userId=1').pipe(catchError(() => of([])))  
})  
.subscribe(data => console.log(data));
```

### 4. Using `combineLatest` (When Values Change Dynamically)

`combineLatest` is useful when multiple observables emit values over time, and you need to react to the latest values from all sources.

```
combineLatest([  
  this.http.get('https://jsonplaceholder.typicode.com/users/1'),  
  this.http.get('https://jsonplaceholder.typicode.com/posts?userId=1')  
])  
.subscribe(([user, posts]) => console.log(user, posts));
```

* Handling real-time data streams
* Combining multiple observables where values change frequently

### 5. Using `concatMap` (For Sequential API Calls)

When API calls need to be executed in sequence (e.g., fetching a user first, then their related posts), `concatMap` ensures each request completes before starting the next one.

```
this.http.get('https://jsonplaceholder.typicode.com/users/1')  
  .pipe(  
    concatMap(user => this.http.get(`https://jsonplaceholder.typicode.com/posts?userId=${user.id}`)),  
  )  
  .subscribe(posts => console.log(posts));
```

* Ensures requests are executed sequentially
* Prevents race conditions

### 6. Using `switchMap` (Cancelling Previous Requests)

When dealing with real-time data (e.g., search queries), `switchMap` cancels the previous request before initiating a new one. This prevents outdated responses from overriding the latest data.

```
fromEvent(inputElement, 'keyup').pipe(  
  debounceTime(300),  
  switchMap(() => this.http.get('https://jsonplaceholder.typicode.com/posts'))  
)  
.subscribe(posts => console.log(posts));
```

* Live search functionality
* Avoiding unnecessary API calls

### Key Takeaways:

Choosing the right approach depends on the use case:

* **Use** `mergeMap` when nesting multiple requests.
* **Use** `forkJoin` for independent parallel API calls.
* **Use** `combineLatest` for real-time updates.
* **Use** `concatMap` for sequential requests.
* **Use** `switchMap` to prevent unnecessary requests.

By leveraging RxJS operators effectively, Angular applications can handle multiple API requests efficiently while improving performance and maintainability.

## Modern Approach — Angular v.19 (resource(), rxResource() & RxJS operators)

With the **new Angular** `resource` **API** (`rxResource` from `@angular/core/rxjs-interop`), we can efficiently manage API requests using reactive signals. Here’s how we can achieve **parallel API requests, sequential requests, caching, and error handling** using this modern approach.

Press enter or click to view image in full size

![]()

### 1. Parallel API Requests (Fetching Multiple APIs Simultaneously)

We can use **multiple** `rxResource` **instances** to fetch data from different endpoints in parallel and combine them using `combineLatest`.

```
import { Component, signal, computed } from '@angular/core';  
import { rxResource } from "@angular/core/rxjs-interop";  
import { HttpClient } from '@angular/common/http';  
import { Observable, combineLatest } from 'rxjs';  
  
@Component({  
  selector: 'app-user-resource',  
  templateUrl: './user-resource.component.html',  
  styleUrls: ['./user-resource.component.css']  
})  
export class UserResourceComponent {  
  limit = signal(10);  
    
  // User Resource  
  userResource = rxResource({  
    loader: (limit: number): Observable<User[]> => {  
      return this.http.get<User[]>(`https://api.example.com/users?_limit=${limit}`);  
    }  
  });  
  
  // Orders Resource  
  orderResource = rxResource({  
    loader: (limit: number): Observable<Order[]> => {  
      return this.http.get<Order[]>(`https://api.example.com/orders?_limit=${limit}`);  
    }  
  });  
  
  // Combining Both Resources  
  combinedResource = computed(() =>  
    combineLatest([this.userResource(this.limit()), this.orderResource(this.limit())])  
  );  
  
  constructor(private http: HttpClient) {}  
  
  updateLimit(newLimit: number) {  
    this.limit.set(newLimit);  
  }  
}
```

* `userResource` and `orderResource` fetch users and orders independently.
* `combineLatest` merges the results, updating when either changes.
* `computed()` ensures reactivity so both resources reload when `limit` changes.

### 2. Sequential API Requests (Fetching Orders After Users)

To fetch orders **after** getting user details:

```
import { switchMap } from 'rxjs';  
  
userWithOrders = rxResource({  
  loader: (userId: number) =>   
    this.userResource(userId).pipe(  
      switchMap(user => this.orderResource(user.orderId)) // Fetch orders after user  
    )  
});
```

* Uses `switchMap` to **chain** requests (fetch order after getting the user).
* Ensures **requests are sequential** and avoid unnecessary API calls.

### 3. Error Handling in `rxResource`

To handle errors inside the new `resource` API:

```
import { catchError, of } from 'rxjs';  
  
userResource = rxResource({  
  loader: (limit: number) =>   
    this.http.get<User[]>(`https://api.example.com/users?_limit=${limit}`).pipe(  
      catchError(error => {  
        console.error('Failed to fetch users', error);  
        return of([]); // Return empty array on failure  
      })  
    )  
});
```

* Catches errors gracefully.
* Prevents app crashes and provides a **fallback value**.

### 4. Caching API Responses (Avoiding Unnecessary Calls)

If you **don’t** want to reload the API on every call, you can **cache responses** using `shareReplay`.

```
import { shareReplay } from 'rxjs';  
  
cachedUserResource = rxResource({  
  loader: (limit: number) =>   
    this.http.get<User[]>(`https://api.example.com/users?_limit=${limit}`).pipe(  
      shareReplay(1) // Cache last successful response  
    )  
});
```

* Prevents **unnecessary API calls**.
* Uses **RxJS caching** with `shareReplay(1)`.

## Enhancing API Calls with `forkJoin` and `mergeMap`

We’ll integrate these strategies using Angular’s **new** `rxResource` **API**.

### 1. `forkJoin` (Parallel API Calls that Complete Together)

* **Use case:** Fetch multiple API requests **in parallel** but proceed **only when all are done**.

```
import { forkJoin } from 'rxjs';  
  
combinedResource = rxResource({  
  loader: (limit: number) =>  
    forkJoin({  
      users: this.http.get<User[]>(`https://api.example.com/users?_limit=${limit}`),  
      orders: this.http.get<Order[]>(`https://api.example.com/orders?_limit=${limit}`)  
    })  
});
```

* Ensures both requests complete **before proceeding**.
* Good for **batch data loading** (e.g., users & their orders at once).

### 2. `mergeMap` (Execute API Calls One After Another, Non-Cancelable)

* **Use case:** Fetch **users first**, then **fetch orders for each user** (non-cancelable).

```
import { mergeMap } from 'rxjs';  
  
userWithOrders = rxResource({  
  loader: (limit: number) =>  
    this.http.get<User[]>(`https://api.example.com/users?_limit=${limit}`).pipe(  
      mergeMap(users => this.http.get<Order[]>(`https://api.example.com/orders?userId=${users[0].id}`))  
    )  
});
```

## Final Optimized Version (Including Everything)

Here’s a **full implementation** integrating all strategies:

```
import { Component, signal, computed } from '@angular/core';  
import { rxResource } from "@angular/core/rxjs-interop";  
import { HttpClient } from '@angular/common/http';  
import { Observable, combineLatest, forkJoin } from 'rxjs';  
import { mergeMap, switchMap, catchError, shareReplay, of } from 'rxjs/operators';  
  
@Component({  
  selector: 'app-user-resource',  
  templateUrl: './user-resource.component.html',  
  styleUrls: ['./user-resource.component.css']  
})  
export class UserResourceComponent {  
  limit = signal(10);  
  
  // Fetch Users with Error Handling & Caching  
  userResource = rxResource({  
    loader: (limit: number): Observable<User[]> =>   
      this.http.get<User[]>(`https://api.example.com/users?_limit=${limit}`).pipe(  
        catchError(error => {  
          console.error('Failed to fetch users', error);  
          return of([]); // Handle error gracefully  
        }),  
        shareReplay(1) // Cache response  
      )  
  });  
  
  // Fetch Orders (for Parallel Fetching)  
  orderResource = rxResource({  
    loader: (limit: number): Observable<Order[]> =>  
      this.http.get<Order[]>(`https://api.example.com/orders?_limit=${limit}`).pipe(shareReplay(1))  
  });  
  
  // Parallel Fetching with combineLatest  
  combinedParallelResource = computed(() =>  
    combineLatest([this.userResource(this.limit()), this.orderResource(this.limit())])  
  );  
  
  // Parallel Fetching with forkJoin (Only When Both Are Done)  
  combinedForkJoinResource = rxResource({  
    loader: (limit: number) =>  
      forkJoin({  
        users: this.userResource(limit),  
        orders: this.orderResource(limit)  
      })  
  });  
  
  // Sequential Requests with mergeMap (Users → Orders)  
  userWithOrders = rxResource({  
    loader: (limit: number) =>  
      this.userResource(limit).pipe(  
        mergeMap(users => this.http.get<Order[]>(`https://api.example.com/orders?userId=${users[0]?.id}`))  
      )  
  });  
  
  constructor(private http: HttpClient) {}  
  
  updateLimit(newLimit: number) {  
    this.limit.set(newLimit);  
  }  
}
```

## Key Takeaways:

Using `rxResource` makes API management in Angular much easier with RxJS-powered streams. It integrates well with Angular services and provides a modern approach to handling HTTP calls efficiently.

Press enter or click to view image in full size

![]()

## Thank you for being a part of the community

*Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
* [**Check out CoFeed, the smart way to stay up-to-date with the latest in tech**](https://cofeed.app/) **🧪**
* [**Start your own free AI-powered blog on Differ**](https://differ.blog/) 🚀
* [**Join our content creators community on Discord**](https://discord.gg/in-plain-english-709094664682340443) 🧑🏻‍💻
* For more content, visit [**plainenglish.io**](https://plainenglish.io/) + [**stackademic.com**](https://stackademic.com/)
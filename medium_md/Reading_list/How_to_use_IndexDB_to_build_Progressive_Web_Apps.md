---
title: "How to use IndexDB to build Progressive Web Apps"
url: https://medium.com/p/dcbcd6cc2076
---

# How to use IndexDB to build Progressive Web Apps

[Original](https://medium.com/p/dcbcd6cc2076)

Member-only story

## JavaScript

# How to use IndexedDB to build Progressive Web Apps

[![Uday Hiwarale](https://miro.medium.com/v2/resize:fill:64:64/1*B4PQwnTacbDmtJgKYY7CzA.jpeg)](/@thatisuday?source=post_page---byline--dcbcd6cc2076---------------------------------------)

[Uday Hiwarale](/@thatisuday?source=post_page---byline--dcbcd6cc2076---------------------------------------)

12 min read

·

Apr 4, 2018

--

11

Listen

Share

More

Press enter or click to view image in full size

![]()

In this [previous post](https://itnext.io/service-workers-your-first-step-towards-progressive-web-apps-pwa-e4e11d1a2e85), I talked about implementation of IndexedDB inside Service Workers. If you don’t understand that part, please read that article to clear up some concepts about service workers.

## Getting started

Single page applications (SPAs) demand data to be loaded from a web service. This data then gets injected into the DOM by the controller. Angular, React and other front-end libraries follow the same approach.

You can cache static web pages and assets, but that won’t be enough. You also need to store some data for online viewing. When a web app makes an HTTP request for some data and the user doesn’t have internet connectivity, we can serve this data from the local database cache.

**IndexedDB** is an alternative to the Web SQL (deprecated) database. It is a key-value pair NoSQL database and supports large scale storage (**up to 20%–50% of hard drive capacity**). It supports many data types like number, string, JSON, blob, and so on.

IndexedDB adheres to a same-origin policy. That means any other applications running on different origins cannot access the data of other origins. It is event (DOM) driven, transactional (**atomic operations**) and its API is mostly asynchronous. It is supported in all major browsers and available for future release in those which don’t currently support it. So it makes a good fit to store offline data for our application.

> There is new version of IndexedDB labeled as **IndexedDB 2.0** which you can take a look at as well. It isn’t supported in all browsers, though.

Press enter or click to view image in full size

![]()

I am going to use only few functionalities of IndexedDB and my explanation won’t cover the full API. You should visit its official documentation on the Mozilla Development Network [here](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Basic_Concepts_Behind_IndexedDB) and [here](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB).

## An intro to IndexedDB

A typical IndexedDB database consists of multiple **object stores**. They are like MySQL tables or MongoDB collections. Each store can contain multiple objects (**like rows in a MySQL table**).

The **object store** persistently holds records, which are key-value pairs. Records within an object store are sorted according to the keys in ascending order. Every object store must have a name that is unique within its database.

When a database is first created, its version is the integer 1. Each database has one version at a time — a database can’t exist in multiple versions at once.

An operation is performed by opening a database. A given database can have multiple connections at the same time. Data read or write operations must happen in transaction, which is an atomic set of data-access and data-modification operations on a particular database. It is how you interact with the data in a database. In fact, any reading or changing of data in the database must happen in a transaction.

A key in the object store can be one of these types: **string**, **date**, **float**, **a binary blob,** or an **array**. Each entry in the object store has a value, which could include anything that can be expressed in JavaScript, including a **boolean**, **number**, **string**, **date**, **object**, **array**, **regexp**, **undefined** and **null**.

The following are the basic steps for doing something in IndexedDB.

1. Open a database.
2. Create an object store in the database.
3. Start a transaction and make a request to do some database operation, like adding or retrieving data.
4. Wait for the operation to complete by listening for the right kind of DOM event.
5. Do something with the results (which can be found on the request object).

The API for IndexedDB is available in the **global scope** of **window** or **service worker**. Hence you can check support for IndexedDB using `window.indexedDB` or `self.IndexedDB`.

```
if(self.IndexedDB){  
    console.log('IndexedDB is supported');  
}
```

First, we open a database using `.open(dbName, versionInt)` method. This sends an open request to the IndexedDB database and returns the request object. This method accepts the database name and version number of the database.

If the database doesn’t exist, **then it will be created**. If the database exists but the version number is higher, **then the database is upgraded** with the new version **without keeping a copy of the older version**.

```
var request = self.IndexedDB.open('EXAMPLE_DB', 1);
```

As we discussed, IndexedDB operations are event-driven. Therefore, we need to use event listeners on `request` to get some response. The `open` method triggers three events viz. `success`, `error` and `upgradeneeded`. You can listen to these events on `request` object like below.

```
var request = self.IndexedDB.open('EXAMPLE_DB', 1);  
var db;request.onsuccess = function(event) {  
    console.log('[onsuccess]', request.result);  
    db = event.target.result; // === request.result  
};request.onerror = function(event) {  
    console.log('[onerror]', request.error);  
};
```

You can also use `event.target` to get the `request` object. The `result` property on the `request` object is the **database reference object** which needs to be stored for further use.

The IndexedDB API is designed to minimize the need for error handling, so you’re not likely to see many error events. All errors on database operations can be handled by the above `onerror` event handler when it’s placed **as the error events bubble**.

You can run the above code in the browser and look up for the database in Chrome Developers Tools, inside the **Application > IndexedDB** tab. Since we don’t have any data in our database now, it is shown empty.

Press enter or click to view image in full size

![]()

`onupgradeneeded` event is triggered when we are trying to create a new database or trying to upgrade the database with a new version. This is a great place to create the object store.

```
request.onupgradeneeded = function(event) {  
    // create object store from db or event.target.result  
};
```

The object store can be created using the `createObjectStore` method on the database object. The syntax for the `createObjectStore` method is as follows.

```
db.createObjectStore(storeName, options);
```

Store name (`storeName`) must be unique. The `options` object can have two properties. `options.keyPath` is a field name in the data (**AKA object or entry**) being stored (**if data is a JavaScript object**). The value of that key will be the key for the object. If we don’t have `keyPath` in the data, then we have to provide the key manually or by using a key-generator, which can auto increment the key value when a new entry is added to the store.

Let’s create a sample object store for our database.

```
request.onupgradeneeded = function(event) {  
    var db = event.target.result;  
    var store = db.createObjectStore('products', {keyPath: 'id'});  
};
```

With the above code, we are creating a `products` **object store** to store JavaScript objects. These objects will have a key `id` which will be the **key used by the object store to locate objects**.

Try to execute the above code in conjugation with the previous code and check the database again from Chrome Developer Tools.

> First delete the old database from developer tools.

Press enter or click to view image in full size

![]()

If you want IndexedDB to generate auto incremented integer keys *(1, 2, 3,…)* whenever a new object entry is added to the store, then set `options.autoIncrement` to `true`. You can mix it with the `keyPath` option as well, and IndexedDB will behave as per the table shown below.

Press enter or click to view image in full size

![]()

One great feature about IndexedDB is **Indexes**. If you’ve come from a MySQL background, then you know how they work. In brief, indexes help a database organize tables, and they store data more efficiently and put constraints on them. One such constraint is the **unique constraint,** which restricts data operations from inserting duplicate entries based on any `keyPath`.

```
store.createIndex(indexName, keyPath, options);
```

In the above case, `indexName` is the name of the index which can be anything, while `keyPath` is any key on the **object** which should be used to check for duplicate entries. `options` is an optional object which contains an extra configuration of an index being created. A unique index is created by using `{unique: true}` in `options` object.

In our previous example, we can disallow adding products to the **products store** if a product in the store with a matching `id` already exists.

```
request.onupgradeneeded = function(event) {  
    var db = event.target.result;  
    var store = db.createObjectStore('products', {keyPath: 'id'});// create unique index on keyPath === 'id'  
    store.createIndex('products_id_unqiue, 'id', {unique: true});  
};
```

Once `onupgradeneeded` event handler **exits successfully,** a`success` event is triggered. In the `success` event handler, we are going to add some products to the products store.

To insert or do any operations on database, we need to get the **transaction** object from the database. That can be done by using the `transaction` method in the database with one of the following signatures.

```
var transaction = db.transaction(storeName, mode);  
var transaction = db.transaction(storeNamesArray, mode);
```

In the above syntax, the first parameter is the name of the object store or the array of names of the object stores. If you specify the array of store names, then you get permission to perform database operations on multiple stores.

The second `mode` parameter is optional. `mode` can be either **readonly**, **readwrite**, or **versionchange**. By default, **readyonly** is the default mode. While doing read only operations, you should use **readonly** mode for performance benefits.

To perform an operation in any store, we need to get the **object store** from the transaction with the below syntax.

```
var objectStore = transaction.objectStore(storeName);
```

**As per MDN**, transactions can receive DOM events of three different types: `error`, `abort`, and `complete`. If you don’t handle an error event or if you call `abort()` on the transaction, then the transaction is rolled back and an `abort` event is triggered on the transaction. Otherwise, after all pending requests have completed, you’ll get a `complete` event. If you make a transaction and return to the event loop without using it then the transaction will become **inactive**. The only way to keep the transaction active is to make a request on it.

> Read more about transactions on MDN at <https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB>

`objectStore` is an instance of `IDBObjectStore` interface which provides methods like **get**, **add**, **clear**, **count**, **put**, **delete** etc.

For now, we are going to use `add` method to put some data in products object store whose transaction we have already acquired.

```
var request = self.IndexedDB.open('EXAMPLE_DB', 1);request.onsuccess = function(event) {  
    // some sample products data  
    var products = [  
        {id: 1, name: 'Red Men T-Shirt', price: '$3.99'},  
        {id: 2, name: 'Pink Women Shorts', price: '$5.99'},  
        {id: 3, name: 'Nike white Shoes', price: '$300'}  
    ];// get database from event  
    var db = event.target.result;// create transaction from database  
    var transaction = db.transaction('products', 'readwrite');// add success event handleer for transaction  
    // you should also add onerror, onabort event handlers  
    transaction.onsuccess = function(event) {  
        console.log('[Transaction] ALL DONE!');  
    };// get store from transaction  
    // returns IDBObjectStore instance  
    var productsStore = transaction.objectStore('products');// put products data in productsStore  
    products.forEach(function(product){  
        var db_op_req = productsStore.add(product); // IDBRequest  
    });  
};
```

Please read comments in above program. I have dropped out `onerror` and `onupgradeneeded` event handlers just for the sake of simplicity. In above program, in `onsuccess` event handler which would be ideal place to perform database operations when database is opened successfully, we are adding some sample products data to products object store.

As we know, we have added **unique index** on object store with keyPath `id`, any duplicate document insertion with same `id` will cause transaction to fail and error for that should be handled in `transaction.onerror` event handler (*else it will bubble up to error handler of database*). A transaction is all or nothing type database operation. That means, until all operations on transaction is completed, it won’t perform actual database operation. It will instead modify a copy of database and update the difference to database once transaction is completed.

Any operations done on object store, like `productStore.add` will return `IDBRequest` object, which will trigger events like `success` and `error`, for individual database operations. Hence they should be handled by `onsucess` and `onerror` event handler like below.

```
var db_op_req = productsStore.add(product);db_op_req.onsuccess = function(event) {  
    console.log(event.target.result == product.id); // true  
};db_op_req.onerror = function(event) {  
    // handle error  
};
```

You should again check the database in Chrome Developer Tools, which should appear like below.

Press enter or click to view image in full size

![]()

So far, we understood how to work with IndexedDB. Now let’s do some **CRUD** operations. Following are the methods using which we can perform these operations.

* `objectStore.add(data)`  
  *This creates new object in object store from provided* `data`*.*
* `objectStore.get(key)`  
  *Returns an object with specified* `key`*.*
* `objectStore.getAll()`  
  *Returns all objects in the store. You can also pass optional parameter, read here* [*https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAll*](https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAll)
* `objectStore.count(key?)`  
  *Returns the total number of objects that match the provided* `key` *or IDBKeyRange. If no arguments are provided, it returns the total number of objects in the store.*
* `objectStore.getAllKeys()`  
  *Returns keys of all objects present in the store. You can also pass optional parameter, read here* [*https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAllKeys*](https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore/getAllKeys)
* `objectStore.put(data, key?)`  
  *This updates existing objects in an object store when the transaction’s mode is* ***readwrite****. key is not needed when* `keyPath` *is provided in object store. If object with key doesn’t exist, then it will create new object from data.*
* `objectStore.delete(key)`  
  *Deletes the object with provided* `key`*.*
* `objectStore.clear()`  
  *Deletes all objects in object store.*

To know more about these methods and more of such methods, follow <https://developer.mozilla.org/en-US/docs/Web/API/IDBObjectStore> document on MDN.

> `close` method on IDBDatabase interfaces closes the database connection. Connection to database is not closed until all transactions are completed. If we call close method on database, no new transactions can be created. Although, this method is not available in service workers.

Let’s use some of the above methods in one transaction. This will help us get familiar with IndexedDB queries.

If you run above script in console of your browser, you will see following output log.

![]()

You can also check updates done by the script in database.

Press enter or click to view image in full size

![]()

This was fun, isn’t it. We learned so much about IndexedDB and now can get to do some serious stuff with this. There are more concepts in IndexedDB like cursors, database migration, database versioning etc. which you can read on Mozilla documentation ([*https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB\_API/Using\_IndexedDB*](https://developer.mozilla.org/en-US/docs/Web/API/IndexedDB_API/Using_IndexedDB)), but that is pretty advanced stuff. With this knowledge, we can move ahead to the service worker and start implementing IndexedDB there.

Storing database for offline use is a not a big task but using it right is a tough game. You need a good application design to implement it well. These are the basic steps you should follow to make your application available offline.

* Cache static files in `install` event handler of service worker.
* In `activate` event handler of service, remove old cached files. This also makes a good place to initialize IndexedDB database, better than using the service worker’s `install` event handler, since the old service worker will still be in control at that point, and there could be conflicts if a new database is mixed with an old service worker. Create IndexedDB database with proper version and using fetch API (*to pull data from web service*) to add entries to the database for offline use. Use `keyPath` as URL endpoint that you would like to use for offline access. Make sure these URLs falls under service worker’s scope. Example of such URL will be `/offline-api/users`.
* Whether online or offline, your app will use cached files. But API requests for data will still propagate to the network because you commonly will be using separate origin for data, like `https://api.example.com/users`[.](https://api.example.com/users.)
* In your main program, when you make request for data like `https://api.example.com/users` which returns in 404 error or some other error because of bad internet connection, retry the request with modified URL like `https://example.com/offline-api/users`. This will go through service worker.
* Inside service worker’s `fetch` event handler, if a request starts with `/offline-api`, then fetch data from database with `key` equal to the path of the request. Set proper header on the response like `application/json` and return response back to the browser. You can use **Response** constructor for that.

Using above method, you can achieve full offline access for your application. I am not going to demonstrate above application design because I am going to write another blog on **Progress Web Apps** where I will create a sample app with everything we have learned so far.

I guess that’s it for now in Offline Database Storage. You should check official Mozilla documentation for IndexedDB in case we missed something.

Unlike Cache API, IndexedDB API is event driven and not promise based. This makes writing and maintaining JavaScript code little bit harder. Hence, you can work with some indexeddb wrapper libraries which allow to you write promise based code without sacrificing much. These libraries provide you great API to write long IndexedDB code in few lines.

* [localForage](https://github.com/localForage/localForage) (~8KB, promises, good legacy browser support)
* [IDB-keyval](https://www.npmjs.com/package/idb-keyval) (500 byte alternative to localForage, for modern browsers)
* [IDB-promised](https://www.npmjs.com/package/idb) (~2k, same IndexedDB API, but with promises)
* [Dexie](http://dexie.org/) (~16KB, promises, complex queries, secondary indices)
* [PouchDB](https://pouchdb.com/) (~45KB (supports [custom builds](https://pouchdb.com/2016/06/06/introducing-pouchdb-custom-builds.html)), synchronization)
* [Lovefield](https://github.com/google/lovefield) (relational)
* [LokiJS](http://lokijs.org/#/) (in-memory)
* [ydn-db](https://github.com/yathit/ydn-db) (dexie-like, works with WebSQL)

Press enter or click to view image in full size

![]()

![]()
---
title: "Searching in Your IndexedDB Database"
url: https://medium.com/p/d7cbf202a17
---

# Searching in Your IndexedDB Database

[Original](https://medium.com/p/d7cbf202a17)

![]()

# Searching in Your IndexedDB Database

[![Ryan Dabler](https://miro.medium.com/v2/resize:fill:64:64/1*Gl9TPR7M5Mud_vmBX1P7Nw.jpeg)](https://medium.com/@ryan.dabler?source=post_page---byline--d7cbf202a17---------------------------------------)

[Ryan Dabler](https://medium.com/@ryan.dabler?source=post_page---byline--d7cbf202a17---------------------------------------)

7 min read

·

Oct 4, 2018

--

2

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dd7cbf202a17&operation=register&redirect=https%3A%2F%2Fitnext.io%2Fsearching-in-your-indexeddb-database-d7cbf202a17&source=---header_actions--d7cbf202a17---------------------post_audio_button------------------)

Share

*This is a continuation of my* [*previous article*](/getting-started-with-persistent-offline-storage-with-indexeddb-1af66727246c) *on getting started with IndexedDB. Read that article to get familiar with the basics of IndexedDB if you aren’t familiar with it.*

IndexedDB is a great document storage database to persist data offline with native functionality for all the basic CRUD operations. The next (maybe more) important step in working with any database is how do we find data in it? We’ve seen with IndexedDB how to retrieve data when we know the key path we used to create it. But what about when we want to search for documents that contain certain text or meet certain conditions?

Well, the answer is…not as easy as it is to do CRUD.

The unfortunate problem with IndexedDB is that it has no native search functionality. After working with other NoSQL databases like Mongo, this is a little disappointing because finding documents is so *easy* using their API. In order to do any kind of searching we will have to implement it ourselves using the basic building blocks we have available to us.

This leads us to a discussion of the *cursor*.

## What the heck is a cursor?

A cursor, simply put, is a pointer that iterates over all the documents in a given data store or index, and on each iteration exposes the data for the document that is currently being “pointed” at. It also contains a few pieces of additional metadata as well as a couple methods.

You can read the full specs of a cursor [on MDN,](https://developer.mozilla.org/en-US/docs/Web/API/IDBCursor) but for our purposes we are interested in the following properties and methods:

* `primaryKey`: the key path defined an object in the store
* `value`: the document itself
* `continue()`: a directive to move to the next document
* `delete()`: a directive to delete the current document
* `update()`: a directive to update the current document

Some of these (and especially those that I left out from MDN) will be more or less important depending on what your use case is, but I want to show a couple of the most important techniques because, even though IndexedDB is a little clunky, the cursor is a powerful tool.

## Getting a cursor on our database

We will use the database from my prior article ([code here](https://gist.github.com/ryandabler/41c458871cb6b64f599fb182ba88daba)) throughout the rest of the article as well as the data set from [this Gist](https://gist.github.com/ryandabler/3a0b2999e9e96045689de7ea0a7d5a3b) to seed our database so we have something to search over.

So, now that we have data in our database, let’s open up a cursor.

```
const request = window.indexedDB.open('database', 1);request.onsuccess = () => {  
    const db = request.result;  
    const transaction = db.transaction(['invoices'], 'readonly');  
    const invoiceStore = transaction.objectStore('invoices');  
    const getCursorRequest = invoiceStore.openCursor();    getCursorRequest.onsuccess = e => {  
        // Cursor logic here  
    }  
}
```

Remember that IndexedDB is event-based so all our requests trigger `onsuccess` events that we need to listen for and implement our application logic in. In the code above, if the database successfully opens, we go through the typical IndexedDB chain of initiating a transaction and pulling off an object store. Once we have the store, it’s simply a matter of opening a cursor on it.

But, because opening a cursor is a request, we must handle its `onsuccess` to implement our cursor logic. So let’s just go and print out the objects in the invoice store:

```
const request = window.indexedDB.open('database', 1);request.onsuccess = () => {  
    const db = request.result;  
    const transaction = db.transaction(['invoices'], 'readonly');  
    const invoiceStore = transaction.objectStore('invoices');  
    const getCursorRequest = invoiceStore.openCursor();    getCursorRequest.onsuccess = e => {  
        const cursor = e.target.result;  
        if (cursor) {  
            console.log(cursor.value);  
            cursor.continue();  
        } else {  
            console.log('Exhausted all documents');  
        }  
    }  
}
```

There are a couple important things to note about what is going on:

* We get the actual cursor off the `onsuccess` event.
* We have access to the document in our object store that the cursor is pointing to through the `value` property, as you can verify from the console log.
* We call the `continue()` method on the cursor to move to the next item in the database.
* We need to check if the cursor actually exists. This is important because when we have iterated onto the last item, and `cursor.continue()` is called, we end up with a `null` value indicating we have traversed every document in the store and we are done. In the case above, we print that we’ve exhausted all our documents and simply exit the event handler.

This is a fairly boring example, so let’s do something interesting with cursors.

## Selectively modifying documents in our database

### `update()`

Let’s suppose that our vendor GE merged with Proctor & Gamble to become a new entity P&GE. To keep our database in sync with this merger, we want to update all our invoices to reflect the new name.

We are going to want to open a cursor on our invoice store, check whether the vendor’s name is GE, and update to P&GE if so.

```
const request = window.indexedDB.open("database", 1);request.onsuccess = () => {  
    const db = request.result;  
    const transaction = db.transaction(['invoices'], 'readwrite');  
    const invStore = transaction.objectStore('invoices');  
    const cursorRequest = invStore.openCursor();    cursorRequest.onsuccess = e => {  
        const cursor = e.target.result;  
        if (cursor) {  
            if (cursor.value.vendor === 'GE') {  
                const invoice = cursor.value;  
                invoice.vendor = 'P&GE';  
                const updateRequest = cursor.update(invoice);  
            }  
            cursor.continue();  
        }  
    }  
};
```

In our example above as the cursor iterates over the store, we check the document’s `vendor` property to see if it matches. If so, we create a new invoice document from the cursor’s `value` key, update the field we want, and pass that new document into the `update()` method on the cursor.

Calling `update()` actually returns a transaction request, so we could have put an `onsuccess` handler on `updateRequest` if we wanted to do any further actions (print to the console, call another function to update application state, etc.). We unnecessarily assigned the request to a variable to show that something is there if we ever choose to use it.

## Getting cursors off indexes

Our example above can be done a slightly different way that is actually more efficient than iterating over the whole store. Remember that indexes exist to group together documents whose values for a particular key are all equal. So, up above, we could have opened a cursor on an index targeting that specific value.

```
const request = window.indexedDB.open("database", 1);request.onsuccess = () => {  
    const db = request.result;  
    const transaction = db.transaction(['invoices'], 'readwrite');  
    const invStore = transaction.objectStore('invoices');  
    const vendorIndex = invStore.index('VendorIndex');  
    const keyRng = IDBKeyRange.only('GE');  
    const cursorRequest = vendorIndex.openCursor(keyRng);    cursorRequest.onsuccess = e => {  
        const cursor = e.target.result;  
        if (cursor) {  
            const invoice = cursor.value;  
            invoice.vendor = 'P&GE';  
            const updateRequest = cursor.update(invoice);  
  
            cursor.continue();  
        }  
    }  
};
```

As you can see, we made a number of small changes:

* We opened a cursor off the previously defined vendor index on our invoices store
* We passed in an optional `IDBKeyRange` parameter when opening the cursor to target just the vendor we wanted. Note two things: (1) Had we not passed this parameter in, we would have iterated over the entire object store with the documents lexicographically sorted by the value of the index (whereas a cursor opened on an object store is sorted by value of its key path). There are many possible ways to define a key range; the full list is available at [MDN](https://developer.mozilla.org/en-US/docs/Web/API/IDBKeyRange). (2) We can also use key ranges when we define a cursor on an object store.
* We no longer had to check the vendor name on each iteration of the cursor, because we were guaranteed to have only the documents that we wanted to change.

## Having multiple cursors open at the same time

One nice thing about cursors is that you can have many open simultaneously. In fact, you can open an unlimited number if you wanted (and had the memory to store that many).

So, let’s suppose that our vendor Frigidaire went out of business and we no longer have to pay our invoices to them. The way our database is structured means that we need to go through our invoice store (selectively choosing only Frigidaire invoices), and for each invoice in that store delete it and all its line items in the invoice items store.

```
const request = window.indexedDB.open("database", 1);request.onsuccess = () => {  
    const db = request.result;  
    const transaction = db.transaction(  
        ['invoices', 'invoice-items'],  
        'readwrite'  
    );  
    const invStore = transaction.objectStore('invoices');  
    const invItemStore = transaction.objectStore('invoice-items');    // Get invoice cursor  
    const invoiceCursorRequest = invStore.index('VendorIndex')  
        .openCursor(IDBKeyRange.only('Frigidaire'));    invoiceCursorRequest.onsuccess = e => {  
        const invCursor = e.target.result;  
        if (invCursor) {  
            // Get invoice item cursor  
            const invItemCursorRequest = invItemStore  
                .index('InvoiceIndex')  
                .openCursor(  
                    IDBKeyRange.only(invCursor.value.invoiceId)  
                );            invItemCursorRequest.onsuccess = e => {  
                const invItemCursor = e.target.result;  
                if (invItemCursor) {  
                    invItemCursor.delete();  
                    invItemCursor.continue();  
                }  
            }  
            invCursor.delete();  
            invCursor.continue();  
        }  
    }  
};
```

In this example, we have our invoice item cursor nested inside the `onsuccess` handler of the outer invoice cursor, and each calls its `delete()` method, which initiates a delete transaction (just like our `update()` call above) to delete the underlying document. We abbreviated the code by not assigning the `delete()` operation to a variable, as we don’t need to worry about any success/error handling for the operation.

## Conclusion

This is essentially using cursors and IndexedDB. There are so many more use cases than we covered here — such as calculating aggregate data on our documents — but understanding the concepts covered here will allow you to implement all the same functionality you would expect out of a database system. I’ll leave [this Gist](https://gist.github.com/ryandabler/28d7b7932415e1e4b23ddb56d80bd0c9) as a working example of all the things we did with our database.
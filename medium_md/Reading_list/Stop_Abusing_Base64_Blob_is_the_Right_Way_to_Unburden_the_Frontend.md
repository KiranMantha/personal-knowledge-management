---
title: "Stop Abusing Base64: Blob is the Right Way to Unburden the Frontend"
url: https://medium.com/p/f1f1009a7544
---

# Stop Abusing Base64: Blob is the Right Way to Unburden the Frontend

[Original](https://medium.com/p/f1f1009a7544)

Member-only story

# Stop Abusing Base64: Blob is the Right Way to Unburden the Frontend

[![Oliver Foster](https://miro.medium.com/v2/resize:fill:64:64/1*ggy9mwK4Uj54EJL52gtC0A.png)](https://medium.com/@haiou-a?source=post_page---byline--f1f1009a7544---------------------------------------)

[Oliver Foster](https://medium.com/@haiou-a?source=post_page---byline--f1f1009a7544---------------------------------------)

4 min read

·

Dec 6, 2025

--

6

Listen

Share

More

Press enter or click to view image in full size

![]()

> My article is open to everyone; non-member readers can click this [link](https://medium.com/@haiou-a/stop-abusing-base64-blob-is-the-right-way-to-unburden-the-frontend-f1f1009a7544?sk=65b54f6b457a491b93dd5f247ac3bcb7) to read the full text.

## I. What is a Blob?

**Blob (Binary Large Object)** is an immutable, file-like raw data container provided by the browser.

It can store any type of binary or text data, such as images, audio, PDFs, or even a piece of plain text.

Compared to the `File` object, `Blob` is more low-level; in fact, `File` inherits from `Blob` and simply adds metadata like `name` and `lastModified`.

The biggest feature of a Blob is that it is **purely client-side with zero network interaction**:

once data enters a Blob, it lives in memory and can be previewed, downloaded, or further processed without needing to be uploaded to a server.

## II. Constructing a Blob: One Line of Code

```
const blob = new Blob(parts, options);
```

**Parameters:**

* **parts**: An array where elements can be `String`, `ArrayBuffer`, `TypedArray`, `Blob`, etc.
* **options**: An optional object. Common fields include:
* `type`: MIME type (default is `application/octet-stream`).
* `endings`: Whether to convert newline characters (rarely used).

**Example: Dynamically generate a Markdown file for the user to download**

```
const content = '# Hello Blob\n> Generated dynamically by the browser';  
const blob = new Blob([content], { type: 'text/markdown' });  
const url = URL.createObjectURL(blob);  
​  
const a = document.createElement('a');  
a.href = url;  
a.download = 'hello.md';  
a.click();  
​  
// Release memory immediately after use  
URL.revokeObjectURL(url);
```

Press enter or click to view image in full size

![]()

## III. Blob URL: Giving Memory Data a “Temporary Address”

### **1. Generation Method**

```
const url = URL.createObjectURL(blob);  
// Return value example:  
// blob:https://localhost:3000/550e8400-e29b-41d4-a716-446655440000
```

### **2. Lifecycle**

* **Scope:** Valid only within the current document and current session. It becomes invalid upon page refresh, `close()`, or manual calls to `revokeObjectURL()`.
* **Performance Trap:** Failure to actively release it will cause **memory leaks**, especially in Single Page Applications (SPAs) or scenarios involving mass image previews.

**Best Practice Wrapper:**

```
function createTempURL(blob) {  
  const url = URL.createObjectURL(blob);  
  // Auto-revoke to prevent forgetting  
  requestIdleCallback(() => URL.revokeObjectURL(url));  
  return url;  
}
```

## IV. Blob vs. Base64 vs. ArrayBuffer: How to Choose?

Press enter or click to view image in full size

![]()

## V. High-Frequency Real-World Scenarios

**1. Local Image/Video Preview (Zero Upload)**

```
<input type="file" accept="image/*" id="uploader">  
<img id="preview" style="max-width: 100%">  
​  
<script>  
uploader.onchange = e => {  
  const file = e.target.files[0];  
  if (!file) return;  
  const url = URL.createObjectURL(file);  
  preview.src = url;  
  preview.onload = () => URL.revokeObjectURL(url); // Release immediately after loading  
};  
</script>
```

**2. Export Canvas Drawing to PNG and Download**

```
canvas.toBlob(blob => {  
  const url = URL.createObjectURL(blob);  
  const a = document.createElement('a');  
  a.href = url;  
  a.download = 'snapshot.png';  
  a.click();  
  URL.revokeObjectURL(url);  
}, 'image/png');
```

**3. Fetch Remote Image → Blob → Local Preview (Requires CORS)**

```
fetch('https://i.imgur.com/xxx.png', { mode: 'cors' })  
  .then(r => r.blob())  
  .then(blob => {  
    const url = URL.createObjectURL(blob);  
    document.querySelector('img').src = url;  
  });
```

*Note: If the image does not display, 99% of the time it is because the server did not return the* `Access-Control-Allow-Origin` *header.*

## VI. Pitfalls and Performance Tips

* **Memory Spikes:** Always ensure you `revokeObjectURL` at the appropriate time after every `createObjectURL`.
* **CORS Failures:** Ensure the server has CORS enabled; add `{credentials: 'include'}` to the fetch request if Cookies are needed.
* **Mobile Lag with Large Videos:** Avoid reading the entire file at once; use `blob.slice(start, end)` to read in segments.
* **Legacy Browser Compatibility:** Native support requires IE10+; for lower versions, introduce the `Blob.js` polyfill library.

Press enter or click to view image in full size

![]()

## VII. Extension: The Dream Combination of Blob and Stream

When files are huge (GB level), reading everything into memory is unrealistic. You can leverage `ReadableStream` to convert a Blob into a stream, enabling progressive uploading:

```
const stream = blob.stream(); // Returns a ReadableStream  
await fetch('/upload', {  
  method: 'POST',  
  body: stream,  
  headers: { 'Content-Type': blob.type }  
});
```

Chrome 85+, Edge 85+, and Firefox already support `blob.stream()`, allowing for "read-while-uploading" functionality with extremely low memory usage.

## VIII. Summary: Remember These “Three Sentences”

1. **Blob** = The browser-side binary data warehouse; `File` is just a superset of it.
2. **Blob URL** = A temporary pointer to memory; it must be manually or automatically released after use.
3. For any requirement involving **“local preview, zero upload, or dynamic generation for download,”** prioritize the **Blob + Blob URL** combination.

Using Blob well can improve user experience (instant previews) and reduce server load (no intermediate transfers), making it an essential skill for every frontend engineer.
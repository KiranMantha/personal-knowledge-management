---
title: "Uploading Massive Files Without Breaking Your App: A Guide to Streaming & Chunking in JavaScript"
url: https://medium.com/p/d1185252bb46
---

# Uploading Massive Files Without Breaking Your App: A Guide to Streaming & Chunking in JavaScript

[Original](https://medium.com/p/d1185252bb46)

Member-only story

# Uploading Massive Files Without Breaking Your App: A Guide to Streaming & Chunking in JavaScript

[![Jitin Kayyala](https://miro.medium.com/v2/resize:fill:64:64/1*ClfDPH29hfFSjjiTLKJnqA.png)](https://medium.com/@kjitin?source=post_page---byline--d1185252bb46---------------------------------------)

[Jitin Kayyala](https://medium.com/@kjitin?source=post_page---byline--d1185252bb46---------------------------------------)

10 min read

·

Jan 15, 2026

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

Ever had a user try to upload a 1GB file to your web app and watch the browser just… freeze? Their tab becomes unresponsive. The UI locks up. If they’re on a flaky connection, the entire upload fails and they lose progress.

The solution isn’t hard — it’s chunking and streaming. Instead of trying to load that massive file into memory all at once, you break it into bite-sized pieces, upload them one at a time, and reassemble them on the server. Your browser stays responsive. The user can see real-time progress. And if a chunk fails? No problem — just retry that one piece.

This post will walk you through everything you need to know about handling large file uploads gracefully in JavaScript.

## The Problem: Why Your Browser Is Choking

Modern files are big. Video files, database backups, media libraries, scientific datasets — they regularly hit gigabytes. If you try to load a 5GB file into memory and upload it in one shot:

* Memory explosion: The browser allocates RAM to store the entire file. On a machine with limited RAM, this causes the browser to crash or hang.
* Timeout risk: Large uploads take time. If the network hiccups or the server takes a moment to respond, the entire request times out and fails.
* No progress feedback: The user sits there staring at a frozen UI with no idea what’s happening.
* Retry nightmare: If something fails halfway through, the whole thing starts over from zero. You lose the work you’ve already done.

Chunking solves all of this.

## What Is Chunking

Chunking is the practice of dividing a large file into smaller pieces (chunks) and uploading them separately. Instead of one monolithic request, you make multiple smaller requests, each handling a portion of the file.

The flow looks like this:

1. User selects a large file
2. JavaScript divides it into chunks (e.g., 5MB each)
3. Upload chunk 1 → Upload chunk 2 → Upload chunk 3 → … (one at a time or in parallel)
4. Server stores each chunk temporarily
5. Once all chunks arrive, the server reassembles them into the original file

Benefits:

* ✅ Memory efficient: Only one chunk is in memory at a time
* ✅ Resumable uploads: Track which chunks succeeded; retry only the failed ones
* ✅ Real progress feedback: Show the user exactly how far along they are
* ✅ Cancellable: Stop midway and resume later (with proper server support)
* ✅ Parallelizable: Upload multiple chunks simultaneously for faster throughput

## The Simple Approach: Chunking a File

Let’s start with the basics. Here’s how to divide a file into chunks using JavaScript’s Blob API:

```
// Configuration  
const CHUNK_SIZE = 1024 * 1024; // 1MB chunks  
  
function chunkFile(file) {  
  const chunks = [];  
  let offset = 0;  
  
  while (offset < file.size) {  
    // Slice the file at the current offset  
    const chunk = file.slice(offset, offset + CHUNK_SIZE);  
    chunks.push(chunk);  
    offset += CHUNK_SIZE;  
  }  
  
  return chunks;  
}  
  
// Usage  
const fileInput = document.getElementById('fileInput');  
fileInput.addEventListener('change', (event) => {  
  const file = event.target.files;  
  const chunks = chunkFile(file);  
  console.log(`File divided into ${chunks.length} chunks`);  
});
```

What’s happening here?

* `file.slice(start, end)` returns a Blob object representing that portion of the file
* We loop through the file, slicing it into pieces of `CHUNK_SIZE`
* Each chunk is a Blob, which we can upload just like a regular file

The beauty of the Blob API is that it doesn’t load the entire file into memory. The `slice()` method is a zero-copy operation—it just creates a reference to that portion of the file on disk.

## Uploading Chunks: One at a Time

Now that we have chunks, let’s upload them. Here’s a robust implementation that uploads chunks sequentially and tracks progress:

```
class FileUploader {  
  constructor(file, chunkSize = 1024 * 1024) {  
    this.file = file;  
    this.chunkSize = chunkSize;  
    this.chunks = [];  
    this.uploadedChunks = new Set();  
    this.totalChunks = 0;  
    this.divideIntoChunks();  
  }  
  
  divideIntoChunks() {  
    let offset = 0;  
    this.totalChunks = Math.ceil(this.file.size / this.chunkSize);  
  
    while (offset < this.file.size) {  
      const chunk = this.file.slice(offset, offset + this.chunkSize);  
      this.chunks.push(chunk);  
      offset += this.chunkSize;  
    }  
  }  
  
  async uploadChunk(chunkIndex) {  
    const chunk = this.chunks[chunkIndex];  
    const formData = new FormData();  
    formData.append('chunk', chunk);  
    formData.append('chunkIndex', chunkIndex);  
    formData.append('totalChunks', this.totalChunks);  
    formData.append('fileName', this.file.name);  
    formData.append('fileSize', this.file.size);  
  
    try {  
      const response = await fetch('/api/upload-chunk', {  
        method: 'POST',  
        body: formData,  
      });  
  
      if (!response.ok) {  
        throw new Error(`Chunk ${chunkIndex} upload failed with status ${response.status}`);  
      }  
  
      this.uploadedChunks.add(chunkIndex);  
      this.logProgress();  
      return true;  
    } catch (error) {  
      console.error(`Failed to upload chunk ${chunkIndex}:`, error);  
      return false;  
    }  
  }  
  
  async uploadSequentially(onProgress) {  
    for (let i = 0; i < this.totalChunks; i++) {  
      const success = await this.uploadChunk(i);  
      if (!success) {  
        console.error(`Upload failed at chunk ${i}`);  
        return false;  
      }  
      if (onProgress) {  
        onProgress(this.uploadedChunks.size, this.totalChunks);  
      }  
    }  
    return true;  
  }  
  
  logProgress() {  
    const percentage = ((this.uploadedChunks.size / this.totalChunks) * 100).toFixed(2);  
    console.log(`Progress: ${this.uploadedChunks.size}/${this.totalChunks} chunks (${percentage}%)`);  
  }  
}  
  
// Usage  
const fileInput = document.getElementById('fileInput');  
fileInput.addEventListener('change', async (event) => {  
  const file = event.target.files;  
  const uploader = new FileUploader(file);  
  
  const success = await uploader.uploadSequentially((uploaded, total) => {  
    const percentage = ((uploaded / total) * 100).toFixed(2);  
    document.getElementById('progressBar').textContent = `${percentage}%`;  
    document.getElementById('uploadStatus').textContent = `Uploading: ${uploaded}/${total}`;  
  });  
  
  if (success) {  
    console.log('✅ Upload complete!');  
  } else {  
    console.log('❌ Upload failed');  
  }  
});
```

Key features:

* Sequential upload: Each chunk waits for the previous one to finish
* FormData: Sends the chunk along with metadata (chunk index, total chunks, file name)
* Progress tracking: A `Set` keeps track of successfully uploaded chunks
* Error handling: Catches upload failures and reports which chunk failed
* Callback: `onProgress` lets the UI update in real-time

## Parallel Uploading: Go Faster

Sequential uploads are safe and simple, but they can be slow. If you want faster throughput, you can upload multiple chunks in parallel:

```
class FastFileUploader extends FileUploader {  
  async uploadInParallel(concurrency = 3, onProgress) {  
    const queue = Array.from({ length: this.totalChunks }, (_, i) => i);  
    const inProgress = new Set();  
    const failed = [];  
  
    while (queue.length > 0 || inProgress.size > 0) {  
      // Fill the queue up to the concurrency limit  
      while (inProgress.size < concurrency && queue.length > 0) {  
        const chunkIndex = queue.shift();  
        const uploadPromise = this.uploadChunk(chunkIndex).then((success) => {  
          inProgress.delete(uploadPromise);  
          if (!success) {  
            failed.push(chunkIndex);  
          }  
          if (onProgress) {  
            onProgress(this.uploadedChunks.size, this.totalChunks);  
          }  
        });  
        inProgress.add(uploadPromise);  
      }  
  
      // Wait for at least one to finish  
      if (inProgress.size > 0) {  
        await Promise.race(Array.from(inProgress));  
      }  
    }  
  
    if (failed.length > 0) {  
      console.error(`Failed chunks: ${failed.join(', ')}`);  
      return false;  
    }  
  
    return true;  
  }  
}  
  
// Usage  
const uploader = new FastFileUploader(file);  
await uploader.uploadInParallel(4, (uploaded, total) => {  
  const percentage = ((uploaded / total) * 100).toFixed(2);  
  document.getElementById('progressBar').textContent = `${percentage}%`;  
});
```

What changed?

* `uploadInParallel(concurrency)` uploads up to `concurrency` chunks at the same time
* The queue keeps track of pending uploads
* `Promise.race()` waits for one upload to finish, then starts the next
* This approach balances speed with server load

Pro tip: A concurrency of 3–4 is usually optimal. Too many parallel uploads can overwhelm the server or hit browser connection limits.

## Resumable Uploads: Never Lose Progress

What if the network drops halfway through? With proper bookkeeping, you can resume from where you left off:

```
class ResumableFileUploader extends FileUploader {  
  constructor(file, chunkSize = 1024 * 1024, storageKey = 'upload-progress') {  
    super(file, chunkSize);  
    this.storageKey = storageKey;  
    this.loadProgress();  
  }  
  
  saveProgress() {  
    const progress = {  
      fileName: this.file.name,  
      fileSize: this.file.size,  
      uploadedChunks: Array.from(this.uploadedChunks),  
      timestamp: Date.now(),  
    };  
    localStorage.setItem(this.storageKey, JSON.stringify(progress));  
  }  
  
  loadProgress() {  
    const saved = localStorage.getItem(this.storageKey);  
    if (saved) {  
      const progress = JSON.parse(saved);  
      // Only restore if it's the same file  
      if (progress.fileName === this.file.name && progress.fileSize === this.file.size) {  
        this.uploadedChunks = new Set(progress.uploadedChunks);  
        console.log(`Resumed upload: ${this.uploadedChunks.size}/${this.totalChunks} chunks already uploaded`);  
      }  
    }  
  }  
  
  async uploadSequentially(onProgress) {  
    for (let i = 0; i < this.totalChunks; i++) {  
      // Skip already uploaded chunks  
      if (this.uploadedChunks.has(i)) {  
        console.log(`Chunk ${i} already uploaded, skipping`);  
        continue;  
      }  
  
      const success = await this.uploadChunk(i);  
      if (!success) {  
        this.saveProgress(); // Save before giving up  
        return false;  
      }  
  
      this.saveProgress(); // Save after each successful chunk  
      if (onProgress) {  
        onProgress(this.uploadedChunks.size, this.totalChunks);  
      }  
    }  
  
    // Clear progress when complete  
    localStorage.removeItem(this.storageKey);  
    return true;  
  }  
}  
  
// Usage: User can refresh the page and resume  
const fileInput = document.getElementById('fileInput');  
fileInput.addEventListener('change', async (event) => {  
  const file = event.target.files;  
  const uploader = new ResumableFileUploader(file);  
  
  const success = await uploader.uploadSequentially((uploaded, total) => {  
    document.getElementById('progressBar').textContent = `${uploaded}/${total}`;  
  });  
  
  if (success) {  
    console.log('✅ Upload complete and saved!');  
  }  
});
```

What’s new?

* localStorage: Saves which chunks have been uploaded
* loadProgress(): On page refresh, restores the upload state
* Resumable: Upload continues from where it left off, not from the beginning
* Cleanup: Removes the saved progress once upload is complete

This approach means users can close the browser, go to lunch, and come back — their upload progress is still there.

## The Server Side: Handling Chunks

Your JavaScript is only half the battle. The server needs to accept, store, and reassemble chunks. Here’s a simple Node.js/Express example:

```
const express = require('express');  
const multer = require('multer');  
const fs = require('fs');  
const path = require('path');  
  
const app = express();  
const upload = multer({ dest: './uploads/chunks' });  
  
app.post('/api/upload-chunk', upload.single('chunk'), (req, res) => {  
  const { chunkIndex, totalChunks, fileName, fileSize } = req.body;  
  const chunk = req.file;  
  
  if (!chunk) {  
    return res.status(400).json({ error: 'No chunk provided' });  
  }  
  
  // Move the chunk to a directory named after the file  
  const uploadDir = path.join('./uploads/in-progress', fileName);  
  if (!fs.existsSync(uploadDir)) {  
    fs.mkdirSync(uploadDir, { recursive: true });  
  }  
  
  const chunkPath = path.join(uploadDir, `chunk-${chunkIndex}`);  
  fs.renameSync(chunk.path, chunkPath);  
  
  console.log(`Received chunk ${chunkIndex}/${totalChunks} for file ${fileName}`);  
  
  // Check if all chunks have been received  
  const chunks = fs.readdirSync(uploadDir);  
  if (chunks.length === parseInt(totalChunks)) {  
    // All chunks received, reassemble the file  
    reassembleFile(fileName, uploadDir);  
    res.json({ message: 'Upload complete', status: 'complete' });  
  } else {  
    res.json({ message: 'Chunk received', status: 'pending' });  
  }  
});  
  
function reassembleFile(fileName, uploadDir) {  
  const outputPath = path.join('./uploads/completed', fileName);  
    
  if (!fs.existsSync('./uploads/completed')) {  
    fs.mkdirSync('./uploads/completed', { recursive: true });  
  }  
  
  const writeStream = fs.createWriteStream(outputPath);  
  
  // Get all chunk files and sort by index  
  const chunks = fs.readdirSync(uploadDir)  
    .sort((a, b) => {  
      const indexA = parseInt(a.split('-'));  
      const indexB = parseInt(b.split('-'));  
      return indexA - indexB;  
    });  
  
  chunks.forEach((chunk, index) => {  
    const chunkPath = path.join(uploadDir, chunk);  
    const data = fs.readFileSync(chunkPath);  
    writeStream.write(data);  
    fs.unlinkSync(chunkPath); // Delete chunk after writing  
  });  
  
  writeStream.end(() => {  
    fs.rmdirSync(uploadDir); // Remove now-empty directory  
    console.log(`File ${fileName} reassembled successfully`);  
  });  
}  
  
app.listen(3000, () => {  
  console.log('Server running on port 3000');  
});
```

How it works:

1. Each chunk arrives at `/api/upload-chunk`
2. Server stores it in a directory named after the file
3. Once all chunks are received, the server reassembles them in order
4. Original chunk files are deleted to free up space

## Full Frontend Example: HTML + CSS + JS

Let’s tie it all together with a complete, usable file uploader UI:

```
<!DOCTYPE html>  
<html lang="en">  
<head>  
  <meta charset="UTF-8">  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">  
  <title>Chunked File Uploader</title>  
  <style>  
    body {  
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;  
      max-width: 600px;  
      margin: 50px auto;  
      padding: 20px;  
      background: #f5f5f5;  
    }  
  
    .uploader {  
      background: white;  
      padding: 30px;  
      border-radius: 8px;  
      box-shadow: 0 2px 8px rgba(0,0,0,0.1);  
    }  
  
    h1 {  
      font-size: 24px;  
      margin-bottom: 20px;  
      color: #333;  
    }  
  
    .file-input-wrapper {  
      position: relative;  
      margin-bottom: 20px;  
    }  
  
    input[type="file"] {  
      display: none;  
    }  
  
    .file-button {  
      display: inline-block;  
      padding: 12px 20px;  
      background: #2563eb;  
      color: white;  
      border-radius: 6px;  
      cursor: pointer;  
      font-weight: 500;  
      transition: background 0.3s;  
    }  
  
    .file-button:hover {  
      background: #1d4ed8;  
    }  
  
    .file-name {  
      margin-top: 10px;  
      color: #666;  
      font-size: 14px;  
    }  
  
    .progress-container {  
      display: none;  
      margin-top: 20px;  
    }  
  
    .progress-container.active {  
      display: block;  
    }  
  
    .progress-bar-bg {  
      width: 100%;  
      height: 20px;  
      background: #e0e0e0;  
      border-radius: 4px;  
      overflow: hidden;  
      margin-bottom: 10px;  
    }  
  
    .progress-bar {  
      height: 100%;  
      background: linear-gradient(90deg, #2563eb, #60a5fa);  
      width: 0%;  
      transition: width 0.3s ease;  
      display: flex;  
      align-items: center;  
      justify-content: center;  
      color: white;  
      font-size: 12px;  
      font-weight: bold;  
    }  
  
    .progress-text {  
      display: flex;  
      justify-content: space-between;  
      font-size: 14px;  
      color: #666;  
    }  
  
    .status {  
      margin-top: 20px;  
      padding: 12px;  
      border-radius: 4px;  
      display: none;  
    }  
  
    .status.active {  
      display: block;  
    }  
  
    .status.success {  
      background: #dcfce7;  
      color: #166534;  
      border: 1px solid #86efac;  
    }  
  
    .status.error {  
      background: #fee2e2;  
      color: #991b1b;  
      border: 1px solid #fca5a5;  
    }  
  
    .status.info {  
      background: #dbeafe;  
      color: #0c4a6e;  
      border: 1px solid #7dd3fc;  
    }  
  </style>  
</head>  
<body>  
  <div class="uploader">  
    <h1>📁 Upload Large Files</h1>  
      
    <div class="file-input-wrapper">  
      <label for="fileInput" class="file-button">  
        Choose File  
      </label>  
      <input type="file" id="fileInput">  
      <div class="file-name" id="fileName"></div>  
    </div>  
  
    <div class="progress-container" id="progressContainer">  
      <div class="progress-bar-bg">  
        <div class="progress-bar" id="progressBar" style="width: 0%;">0%</div>  
      </div>  
      <div class="progress-text">  
        <span id="uploadStatus">Ready</span>  
        <span id="uploadSpeed">0 MB/s</span>  
      </div>  
    </div>  
  
    <div class="status" id="statusMessage"></div>  
  </div>  
  
  <script>  
    class ResumableFileUploader {  
      constructor(file, chunkSize = 1024 * 1024) {  
        this.file = file;  
        this.chunkSize = chunkSize;  
        this.chunks = [];  
        this.uploadedChunks = new Set();  
        this.totalChunks = 0;  
        this.startTime = 0;  
        this.divideIntoChunks();  
      }  
  
      divideIntoChunks() {  
        let offset = 0;  
        this.totalChunks = Math.ceil(this.file.size / this.chunkSize);  
  
        while (offset < this.file.size) {  
          const chunk = this.file.slice(offset, offset + this.chunkSize);  
          this.chunks.push(chunk);  
          offset += this.chunkSize;  
        }  
      }  
  
      async uploadChunk(chunkIndex) {  
        const chunk = this.chunks[chunkIndex];  
        const formData = new FormData();  
        formData.append('chunk', chunk);  
        formData.append('chunkIndex', chunkIndex);  
        formData.append('totalChunks', this.totalChunks);  
        formData.append('fileName', this.file.name);  
        formData.append('fileSize', this.file.size);  
  
        try {  
          const response = await fetch('/api/upload-chunk', {  
            method: 'POST',  
            body: formData,  
          });  
  
          if (!response.ok) {  
            throw new Error(`Chunk ${chunkIndex} failed`);  
          }  
  
          this.uploadedChunks.add(chunkIndex);  
          return true;  
        } catch (error) {  
          console.error(`Chunk ${chunkIndex} error:`, error);  
          return false;  
        }  
      }  
  
      async uploadSequentially(onProgress) {  
        this.startTime = Date.now();  
  
        for (let i = 0; i < this.totalChunks; i++) {  
          if (this.uploadedChunks.has(i)) continue;  
  
          const success = await this.uploadChunk(i);  
          if (!success) return false;  
  
          const uploaded = this.uploadedChunks.size;  
          const totalBytes = uploaded * this.chunkSize;  
          const elapsedSeconds = (Date.now() - this.startTime) / 1000;  
          const speed = (totalBytes / 1024 / 1024 / elapsedSeconds).toFixed(2);  
  
          if (onProgress) {  
            onProgress(uploaded, this.totalChunks, speed);  
          }  
        }  
  
        return true;  
      }  
    }  
  
    const fileInput = document.getElementById('fileInput');  
    const fileNameDisplay = document.getElementById('fileName');  
    const progressContainer = document.getElementById('progressContainer');  
    const progressBar = document.getElementById('progressBar');  
    const uploadStatus = document.getElementById('uploadStatus');  
    const uploadSpeed = document.getElementById('uploadSpeed');  
    const statusMessage = document.getElementById('statusMessage');  
  
    fileInput.addEventListener('change', async (event) => {  
      const file = event.target.files;  
      if (!file) return;  
  
      fileNameDisplay.textContent = `Selected: ${file.name} (${(file.size / 1024 / 1024).toFixed(2)} MB)`;  
      progressContainer.classList.add('active');  
      statusMessage.classList.remove('active');  
  
      const uploader = new ResumableFileUploader(file);  
  
      const success = await uploader.uploadSequentially((uploaded, total, speed) => {  
        const percentage = ((uploaded / total) * 100).toFixed(0);  
        progressBar.style.width = percentage + '%';  
        progressBar.textContent = percentage + '%';  
        uploadStatus.textContent = `${uploaded}/${total} chunks`;  
        uploadSpeed.textContent = `${speed} MB/s`;  
      });  
  
      statusMessage.classList.add('active');  
      if (success) {  
        statusMessage.classList.add('success');  
        statusMessage.textContent = '✅ Upload complete! File received on server.';  
      } else {  
        statusMessage.classList.add('error');  
        statusMessage.textContent = '❌ Upload failed. Please try again.';  
      }  
    });  
  </script>  
</body>  
</html>
```

## Final Thoughts

Chunking and streaming transform the file upload experience from frustrating to delightful. Your users get:

* Peace of mind: Real-time progress feedback
* Resilience: Uploads that survive network hiccups
* Control: The ability to pause and resume

Your app stays responsive, your memory usage stays low, and you handle files of virtually any size.

**Finally, if the article was helpful, please clap 👏and follow, Thank you!**
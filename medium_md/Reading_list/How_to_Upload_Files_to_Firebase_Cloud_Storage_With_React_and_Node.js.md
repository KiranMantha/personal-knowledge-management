---
title: "How to Upload Files to Firebase Cloud Storage With React and Node.js"
url: https://medium.com/p/e87d80aeded1
---

# How to Upload Files to Firebase Cloud Storage With React and Node.js

[Original](https://medium.com/p/e87d80aeded1)

Member-only story

# How to Upload Files to Firebase Cloud Storage With React and Node.js

## A step-by-step guide to building a file uploader for your app

[![Claire Chabas](https://miro.medium.com/v2/resize:fill:64:64/1*TyEpx4eCIckEcTQsXsRVKg.png)](/@clairechabas?source=post_page---byline--e87d80aeded1---------------------------------------)

[Claire Chabas](/@clairechabas?source=post_page---byline--e87d80aeded1---------------------------------------)

8 min read

·

May 17, 2020

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

I’ve come to work on several projects that required the implementation of a file uploader and always found it was not that easy.

Handing a file format opens different questions: “What exactly is a file? What are we sending through the wire? How do we handle such a format to store it and make it available to users?”

I recently built one using Firebase Cloud Storage as the file storing space and thought I would have enjoyed a post walking me through understanding how it all works and how to set it up correctly.

So, here it is, I hope it will answer those questions for you and I provide the repo for the full project if you need a boilerplate for your next project.

Prerequisites: This post assumes that you are already familiar with building a Node.js API with Express and a front end with React. We’ll only focus on the file upload part here.

## Setting Up Firebase Cloud Storage

First, you need a Firebase account with an active project and a storage bucket opened:

1. Connect to or create a [Firebase](https://firebase.google.com) account.
2. Create a new project.
3. Give your project a name.
4. Activate or don’t activate Google Analytics, it’s up to you.
5. In the left side menu, click on “Storage”, and then on “Start”.
6. Rules: A modal opens showing the default rules for read and write access for your bucket. We want to keep authentication for write access. Regarding read access, it depends on your needs. Here we’ll update the rules to make our images publicly readable from their public URL.

```
rules_version = '2';  
service firebase.storage {  
  match /b/{bucket}/o {  
    match /{allPaths=**} {  
      allow read;  
      allow write: if request.auth != null;  
    }  
  }  
}
```

More about Storage security rules [in the docs](https://firebase.google.com/docs/storage/security/start?authuser=0#sample-rules).

7. Location: Choose wisely, you can’t change this later. I live in Paris so I chose `europe-west3` which is located in Frankfurt, Germany. You can find the full locations list along with more information about selecting the data location for your project on [this Firebase page](https://firebase.google.com/docs/projects/locations?authuser=0).

Now you have your default bucket ready to use. In [Firebase’s free tier](https://firebase.google.com/pricing), you can have one and store up to 5 GB. If you need multiple buckets and more space, you’ll need to upgrade your plan accordingly.

Now that we have our storage bucket, we need to generate a private key that our API will use to connect safely to our bucket.

1. In the left side menu, click on the settings wheel at the top.
2. Select the “Service accounts” tab.
3. At the bottom of the page click on the “Generate new private key” button. This will generate a JSON file containing your Firebase account credentials.

You’ll get a warning saying that this private key should be kept confidential and in a safe place, so make sure that wherever you put this file you do *not* commit it to your remote repo.

As you’ll see in the next step, we’ll create an `api/` folder for our server. I’ll store this file inside this folder within a `services/` folder. Then I’ll add all JSON files form this folder to my `.gitignore`:

```
/api/services/*.json
```

Now we’re ready for the next step, building the upload API.

For security reasons, we want to handle the authenticated calls from our server, not from the browser where our environment variables containing our sensitive credentials could be accessed more easily.

## API: Node.js + Express.js + Multer

To provide you with a fully functional repo, I’ve included the API in the same project folder.

However, this is not ideal since having all your eggs in the same basket never is. So, keep in mind that in real life, you’ll either use a serverless function or have the upload API run with the rest of your back end.

### Setting up the Express server

1. We install the necessary dependencies:

```
$ npm i express body-parser cors dotenv
```

2. At the root of the project, we create an `api/` folder and within it an `index.js` file in which we set up the Express server:

Now we want both our front end and our API to run simultaneously while still having a single command to run. For this, inside our `package.json` file, we update our `start` script as such:

```
"scripts": {       
    "start": "(cd api && node index.js) & react-scripts start",       
    ...   
}
```

By the way, if you want to read more about how to run multiple commands simultaneously, I found [this article](https://itnext.io/4-solutions-to-run-multiple-node-js-or-npm-commands-simultaneously-9edaa6215a93) useful.

### Adding the upload endpoint

We create an `/api/upload` endpoint that is able to receive POST requests. We’ll use [Multer](https://www.npmjs.com/package/multer), which is a Node.js middleware that allows us to handle `multipart/form-data`:

```
$ npm i multer
```

Multer adds a `file` (or `files` if you send multiples files) to the `request` object, which contains the file(s) uploaded. It also adds a `body` object to `request`, which contains any other text field you’d want to add to your request.

So, thanks to Multer, we’ll be able to access our uploaded file via `req.file` and our remaining data from `req.body`.

In `index.js`, we create a Multer instance:

```
const multer = require('multer');
```

To send our file to Firebase, we’ll need to make a `Buffer` object out of it. We’ll do that using the memory storage engine provided by Multer:

When using memory storage, our `req.file` will contain a field called `buffer` that contains the entire file.

Here’s the starter code for this endpoint:

We’re halfway there. Now all that is left is connecting to Firebase Cloud Storage and processing our files as the service needs to upload it properly.

### Connecting to Firebase Cloud Storage

1. First, we need to add the `@google-cloud/storage` dependency to connect to Firebase Cloud Storage:

```
$ npm i @google-cloud/storage
```

2. Going on, we’ll need three environment variables. This is where the `dotenv` module we installed at the beginning comes into play. It loads environment variables from a `.env` file into `process.env`.

Create a `.env` file at the root of your project and add two environment variables inside it:

* `GCLOUD_PROJECT_ID`: This is your Firebase project ID. You can find it in your Firebase account > Settings > General settings.
* `GCLOUD_APPLICATION_CREDENTIALS`: Remember the private key you stored somewhere at the beginning? This is where we need it. You need to indicate the path to your private key JSON file here. So, it could be something like `/api/services/myprivatekey.json`.
* `GCLOUD_STORAGE_BUCKET_URL`: Finally, you need the URL of your storage bucket which is `[YOUR_GCLOUD_PROJECT_ID].appspot.com`. If you’re not sure, you can see it in your Firebase account > Storage > Files tab (which is the default one) > Just above the stored files list on the left, you have a URL like `gs://you-project-id.appspot.com`. This is it.

Finally, make sure you add your new `.env` file to your `.gitignore`.

3. Now we can initiate a `Storage` instance with our Firebase credentials:

```
const { Storage } = require('@google-cloud/storage');const storage = new Storage({  
    projectId: process.env.GCLOUD_PROJECT_ID,  
    keyFilename: process.env.GCLOUD_APPLICATION_CREDENTIALS,  
});
```

4. And create a `bucket`, which is a container for objects (files), which we associate to our Firebase storage bucket. We’ll use it below in our endpoint to process our file.

```
const bucket =  
    storage.bucket(process.env.GCLOUD_STORAGE_BUCKET_URL);
```

5. Next, we continue inside our `app.post('api/upload')` endpoint. After checking that we do have an existing `req.file`. If you log it, you’ll see it contains the following:

```
{  
  fieldname: 'image',  
  originalname: 'Medium Post Cover 3.png',  
  encoding: '7bit',  
  mimetype: 'image/png',  
  buffer: <Buffer 89 50 4e 47 0d 0a 1a 0a 00 00 00 0d 49 48 44 52 00 00 0b 22 00 00 07 6c 08 06 00 00 00 e9 93 d9 14 00 00 00 04 67 41 4d 41 00 00 b1 8f 0b fc 61 05 00 ... 1834232 more bytes>,  
  size: 1834282  
}
```

Firebase uses `Blobs` (Binary Large Objects), which is a data type that can store binary data in a database.

So, we create a new blob in our bucket with the `file()` method, passing it our file name as reference:

```
const blob = bucket.file(req.file.originalname);
```

Then we initiate a *writable stream*. FreeCodeCamp wrote [an awesome guide about Node.js streams](https://www.freecodecamp.org/news/node-js-streams-everything-you-need-to-know-c9141306be93/) in which they answer all the questions you might have about them (and I had a lot).

*Streams* are a collection of data (like arrays or strings) that might not be available all at once. They allow us to work with large amounts of data (like images or videos) that we need to process one chunk at a time.

And a *writable stream* is one type of stream that is an abstraction for a *destination* to which data can be written, so basically, we use a writable stream when we want to write data, which is what we want here.

```
const blobStream = blob.createWriteStream({  
    metadata: {  
        contentType: req.file.mimetype,  
    },  
});
```

**Important**: You need to pass the file mimetype as metadata to `createWriteStream()` otherwise your file won’t be stored in the proper format and won’t be readable.

This returns a `WriteStream` object on which we can check for events. On the `finish` event, we assemble the public URL of our newly stored file and send it in the response for the user to either display the file on the front or store the location string in a database.

Note that we use `encodeURI` on the `blob.name` to cover cases where the file name had whitespaces or other characters needing to be encoded.

```
// If there's an error  
blobStream.on('error', (err) => next(err));// If all is good and done  
blobStream.on('finish', () => {    // Assemble the file public URL  
    const publicUrl =  
`https://firebasestorage.googleapis.com/v0/b/${bucket.name}/o/${encodeURI(blob.name)}?alt=media`;    // Return the file name and its public URL  
    // for you to store in your own database  
    res.status(200).send({   
        fileName: req.file.originalname,  
        fileLocation: publicUrl  
    });  
});// When there is no more data to be consumed from the stream the end event gets emitted  
blobStream.end(req.file.buffer);
```

And there we have it! Our API is ready for use. Here is the gist with the full `index.js` file:

All that’s left is a simple front end with a form handling a file input. We’ll use React for this.

## The Upload Handler on the Front End

Since we assume here that you know how to set up a React app and use Hooks, I’m only going to focus on the form submit handler which calls our upload endpoint. But I provide the full project repo at the end of this post.

We need a `FormData` object:

```
let fileData = new FormData();
```

We set the `image` field on our `FormData` object and add the selected file and its name. Two notes here:

First, the field name must be the same as the one we expect in our API : `app.post('/api/upload', uploader.single(<FIELD_NAME>), …)`.

Second, note that we append the file name with the current timestamp using `Date.now()`. This ensures that the file has a unique name in storage which prevents potential later overrides.

On the one hand, this lets the user upload the same file several times, which you may or may not want. On the other hand, it prevents a potential issue if you need to set up auth to read images.

Indeed, Firebase then generates an access token for each file and if the user uploads the same picture, it will replace the previous one and renew the access token, which will cause your image using the previous token somewhere to break.

```
fileData.set('image', selectedFile, `${Date.now()}-${selectedFile.name}`  
);
```

Finally, I’m using `axios` for the API call:

And we put all of it inside a try/catch:

And that’s all there is to it really!

## Conclusion

You can check the complete React component with loading and error handling (I kept it simple with only one main `App` component) in the full project repo:

[## clairechabas/file-uploader-firebase-storage-react-node

### To use this file uploader you need the following: Set up a Firebase account > activate Cloud Storage > generate a…

github.com](https://github.com/clairechabas/file-uploader-firebase-storage-react-node?source=post_page-----e87d80aeded1---------------------------------------)

I hope this article was helpful. If you have any questions or improvement recommendations, I’ll be happy to read about it in the comments.

Happy coding.
---
title: "Enable Brotli Compression in Webpack with Fallback to Gzip"
url: https://medium.com/p/397a57cf9fc6
---

# Enable Brotli Compression in Webpack with Fallback to Gzip

[Original](https://medium.com/p/397a57cf9fc6)

# Enable Brotli Compression in Webpack with Fallback to Gzip

## Why should I care, what exactly and how to use.

[![Vikas Singh](https://miro.medium.com/v2/resize:fill:64:64/1*gJsLM1QWmppyTl6ZtVa3Tw.jpeg)](https://vikas-singh707.medium.com/?source=post_page---byline--397a57cf9fc6---------------------------------------)

[Vikas Singh](https://vikas-singh707.medium.com/?source=post_page---byline--397a57cf9fc6---------------------------------------)

3 min read

·

Dec 6, 2018

--

3

Listen

Share

More

Press enter or click to view image in full size

![]()

Customer Centricity is essential in today’s world. Most of the companies are now adapting customer first strategy to increase engagement, thus business. And providing a super fast web experience is one of the best ways to improve user experience and decrease bounce rate.

According to a [Google](https://developers.google.com/web/fundamentals/performance/why-performance-matters/) study, it was found that sites loading within 5 seconds had 70% longer sessions, 35% lower bounce rates, and 25% higher ad viewability than sites taking nearly four times longer at 19 seconds. Yes, every second matters! And we at [Groww](https://groww.in) saved around 1.8 seconds by using Brotli compression over gzip compression for our Javascript files.

### It’s important but what the hell is Brotli Compression?

Just for the sake of completion, let’s see for a sec what is Brotli Compression.

> Brotli is a generic-purpose lossless compression algorithm that compresses data using a combination of a modern variant of the LZ77 algorithm, Huffman coding, and 2nd order context modeling, with a compression ratio comparable to the best currently available general-purpose compression methods. It is similar in speed with deflate but offers more dense compression.

*All the developers out there working to get that performance boost in their React Project already knows the power of shipping less js code.* ***Code splitting*** *comes into play here.* ***Enabling Brotli compression*** *further helps to reduce the number of packets you send to the client and thus gives performance boost especially on 3G and 4G network.*

### **Why we need the fallback to Gzip?**

Because not all browsers support Brotli compression yet. But all support Gzip.

Press enter or click to view image in full size

![]()

![]()

### **Let’s get started**

*Goal: We will enable Brotli compression in Webpack with fallback support to Gzip.*

There are 2 significant steps in this process.

1. Generate Brotli and Gzip compressed version of files.
2. Send correct version of the file when requested based on the request headers.

For the first step, we will use “[*compression-webpack-plugin*](https://www.npmjs.com/package/compression-webpack-plugin)*”* and “[*brotli-webpack-plugin*](https://www.npmjs.com/package/brotli-webpack-plugin)*” to generate required files.*

```
const CompressionPlugin = require(‘compression-webpack-plugin’);  
const BrotliPlugin = require(‘brotli-webpack-plugin’);  
module.exports = {  
plugins: [  
 new CompressionPlugin({  
 asset: ‘[path].gz[query]’,  
 algorithm: ‘gzip’,  
 test: /\.js$|\.css$|\.html$/,  
 threshold: 10240,  
 minRatio: 0.7  
 }),  
 new BrotliPlugin({  
 asset: ‘[path].br[query]’,  
 test: /\.js$|\.css$|\.html$/,  
 threshold: 10240,  
 minRatio: 0.7  
 })  
]  
}
```

![]()![]()

Next step is to serve right file based on accept-encoding header. We will use [express-static-gzip](https://www.npmjs.com/package/express-static-gzip) for handling this part for us.

```
import expressStaticGzip from "express-static-gzip";app.use('/build/client', expressStaticGzip('build/client' {  
   enableBrotli: true,  
   orderPreference: ['br', 'gz'],  
   setHeaders: function (res, path) {  
      res.setHeader("Cache-Control", "public, max-age=31536000");  
   }  
}));
```

That’s it. Those few lines enables the Brotli compression with fallback to the Gzip compression for all the static resources of your website.

Press enter or click to view image in full size

![]()

So, in just a few lines of code, we have given a boost to our Webpack powered website. There are various other things that one can do to improve the performance which I will discuss in my next blog.

> If you enjoyed this story, please click the 👏 button and share to help others find it! Feel free to leave a comment below.
>
> The Groww Engineering publishes technical stuff, latest technologies and better ways to tackle common programming problems. You can subscribe to get them [here](https://medium.com/groww-engineering).
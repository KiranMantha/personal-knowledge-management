---
title: "AEM Dispatcher — Turn Fear into Confidence"
url: https://medium.com/p/c2d36ab666a8
---

# AEM Dispatcher — Turn Fear into Confidence

[Original](https://medium.com/p/c2d36ab666a8)

Member-only story

# AEM Dispatcher — Turn Fear into Confidence

[![SravanKumar](https://miro.medium.com/v2/resize:fill:64:64/1*gqCmfCq9aYW1A99Yo-BgYw.jpeg)](/@uchihamadara_?source=post_page---byline--c2d36ab666a8---------------------------------------)

[SravanKumar](/@uchihamadara_?source=post_page---byline--c2d36ab666a8---------------------------------------)

4 min read

·

Jan 10, 2025

--

Listen

Share

More

Are you thinking there is one more article on the dispatcher to read? Absolutely no, I have found many great articles and resources to understand the dispatcher. But I have never found a blog which gives the information about how a request is being handled in the dispatcher in a flow from start to end. This article is about such an effort to understand the request journey in the dispatcher.

As someone said AEM Dispatcher is often seen as a complex and daunting part. I feel it shouldn’t be in that way work on the daunting topic until it becomes our confidence. Now let’s get into it.

**First Request**  
As an internet user I want to open a webpage, which is built in AEM configured with the Dispatcher. Now opening of a webpage implies that I am requesting something. This request will have some parameters in their headers. A sample request header is as follows.

```
method : GET  
path : www.example.com/in-en  
scheme : https  
accept : text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7  
accept-encoding : gzip, deflate, br  
cache-control : no-cache  
connection : keep-alive  
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

It will reach the DISPATCHER, as it is a first time request by the user, so there will be no cache to serve.

**1.Client   
 ↓  
2.HTTP Request with Headers  
 ↓  
3.Dispatcher (Caching + Filtering)  
 ↓  
4.AEM Publish (if not cached)  
 ↓  
5.AEM Publish Resolves Request  
 ↓  
6.Dispatcher Caches Response  
 ↓  
7.HTTP Response with Headers  
 ↓  
8.Client (Browser)**

If you observe there is a parameter **cache-control: no-cache,** the request will not be served from cache even if it is available in the cache. The request is served from the AEM Publisher. The header response from the publisher might look like

```
HTTP/1.1 200 OK  
Content-Type: text/html;charset=UTF-8  
Content-Length: 3456  
Cache-Control: max-age=3600  
Last-Modified: Fri, 10 Jan 2025 10:00:00 GMT  
ETag: "12345abcd"  
Date: Fri, 10 Jan 2025 10:01:00 GMT  
X-Dispatcher: MISS
```

The response body is cached in the Dispatcher to serve for future requests.

A beautiful article that helps us to understand the technical concept of Configuring Dispatcher : [Demystifying the Fear of AEM Dispatcher — Part 1](/@bhargava.shalki/demystifying-the-fear-of-aem-dispatcher-part-1-07fcdf06cdb4).**[**If you have read the above article or if had an idea on dispatcher then by now you all know the entry point to our Dispatcher module is httpd.conf (*the main Apache HTTP server configuration file)* where we include all the configurations and at the end we all will be referred to dispatcher.any file and eventually you will reach opening a farm file( this is where we have all things to do and understand.)**]**

## Visiting the Dispatcher with second request

The first section you see in the **farm** is **/clientheader** section which helps in allowing the request header properties forwarded to the Publish server. Take an instance of adding custom-authorization header to access the publisher server. Dispatcher won’t consider any other headers other then that of mentioned in the clientheader section. Take a look at [Demystifying the Fear of AEM Dispatcher — Part 2](/@bhargava.shalki/demystifying-the-fear-of-aem-dispatcher-part-2-7b4ecb21056f).

The second section in the **farm** you see is **/virtualhosts** this section helps us in defining the which virtualhosts should have the mentioned configurations that are present in this farm file. Apache server will maintain a list of virtualhosts and their respective domains.

Take two domains **exampleone.com** and **exampletwo.com** whichare present in two different files **farmOnefile** and **farmTwofile** respectively.

If a request comes to **example.com** then the Apache server matches this request to the appropriate virtual hosts and then invoke the Dispatcher **farmOnefile** configurations. This is how we configure different dispatcher configurations to different domains. Have a quick look at this [Demystifying the Fear of AEM Dispatcher — Part 3](/@bhargava.shalki/demystifying-the-fear-of-aem-dispatcher-part-3-6310a8d25e24).

then you come to **render** section, this will help the Dispatcher to connect with available Publisher servers. When a publisher is busy and unable to respond to the dispatcher’s request then the dispatcher will request other servers mentioned here in this render section.

## **The Interesting part starts from this section**

Filter Section [Demystifying the Fear of AEM Dispatcher — Part 4](/@bhargava.shalki/demystifying-the-fear-of-aem-dispatcher-part-4-9b581bd30b40)

```
method : GET  
path : www.example.com/in-en/home.html  
scheme : https  
accept : text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7  
accept-encoding : gzip, deflate, br  
connection : keep-alive  
user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
```

if you see the request we have **GET** method to the path **www.example.com/in-en/home.html** this filter section is where we filter out requests based on what the user is requesting for.

As the request is a content page then it is allowed by a filter rule which is in the form   
**/001 { /type “allow” /method “GET” /path “/content/example-site/\*” }**

Vanity Url Section [Demystifying the Fear of AEM Dispatcher](/@bhargava.shalki/demystifying-the-fear-of-aem-dispatcher-part-5-d18902abfa04#id_token=eyJhbGciOiJSUzI1NiIsImtpZCI6Ijg5Y2UzNTk4YzQ3M2FmMWJkYTRiZmY5NWU2Yzg3MzY0NTAyMDZmYmEiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIyMTYyOTYwMzU4MzQtazFrNnFlMDYwczJ0cDJhMmphbTRsamRjbXMwMHN0dGcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIyMTYyOTYwMzU4MzQtazFrNnFlMDYwczJ0cDJhMmphbTRsamRjbXMwMHN0dGcuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMTc0MzI0NTQwMzMwMjAzODA0NDUiLCJlbWFpbCI6InNyYXZhbmt1bWFycGZAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsIm5iZiI6MTczNjUwNjQ5MywibmFtZSI6InNyYXZhbiBrdW1hciIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NMcFBla3pMcFRYMWY0V2RpUVQ2Q1hnd2tFcXRNNXV4dkZUZkJabVViQ0RUYnhHNnB0eD1zOTYtYyIsImdpdmVuX25hbWUiOiJzcmF2YW4iLCJmYW1pbHlfbmFtZSI6Imt1bWFyIiwiaWF0IjoxNzM2NTA2NzkzLCJleHAiOjE3MzY1MTAzOTMsImp0aSI6IjQ1ZTEwODIxYjMwYTlkZWJkNjllM2FjODM2Zjg2Yjc2ZDJmNWI4ZTgifQ.ny6o_mw2G4aFdSLZv9E2IZRmfTzPEjFnfF_bRJ9WI8tHJPcvMQXCkw7X3fTLcPYkn8o1GHJfJqo7vpb-tLdt9M_DXY0gwnfjToWPlRcc_BxU0u8AMua0p2bb7doArhvIoTmF855hg0fJ4POa6Q_Wbg37qK288l8QcY0_Gioc-PDYjzRVJIswKBCS5VvpwYQ8W9YWkCQjfsNrunfB7JjZd_tsEgLNiXvfPuuBvVX1Q3w33f9vX5seNjBqEFMQpXtspLXPiF4kYkSO10gx741q6KSbEVlpM6nAqJrYha16IakDtqGsgrFE2LaijOVAFG9DyBiMMKXyT-gVSJGZu5YLcg)

Vanity URLs and Rewrite Rules are simple concept of redirecting to some other path. **in-en/home.html** when had a rewrite rule on this url to **us-en/home-page** then the requested content is served from **us-en/home-page** path.

CACHE SECTION [Demystifying the Fear of AEM Dispatcher — Part 6](/@bhargava.shalki/demystifying-the-fear-of-aem-dispatcher-part-6-15950eed593b)

As this is our second request the dispatcher will now validate the cache rules, generally everything will be cached except the tokens and any other dynamic things. The response from the first request which will have cache-control of max-age=2592000 (30days) of that particular request will be valid

```
Cache-Control: max-age=2592000
```

Now the dispatcher and browser will know that this particular resource is valid for 30 days after that they need to rerequest the resource again.

The request served from cache is faster when compared to involving the AEM Publisher in the process.
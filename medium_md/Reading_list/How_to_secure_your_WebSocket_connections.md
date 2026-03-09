---
title: "How to secure your WebSocket connections"
url: https://medium.com/p/d0be0996c556
---

# How to secure your WebSocket connections

[Original](https://medium.com/p/d0be0996c556)

# How to secure your WebSocket connections

[![Mehul Mohan](https://miro.medium.com/v2/resize:fill:64:64/0*bCTl1wh-XL6s5HxZ.)](/@mehulmpt?source=post_page---byline--d0be0996c556---------------------------------------)

[Mehul Mohan](/@mehulmpt?source=post_page---byline--d0be0996c556---------------------------------------)

6 min read

·

Nov 12, 2018

--

3

Listen

Share

More

![]()

The Web is growing at a massive rate. More and more web apps are dynamic, immersive and do not require the end user to refresh. There is emerging support for low latency communication technologies like websockets. Websockets allow us to achieve real-time communication among different clients connected to a server.

A lot of people are unaware of how to secure their websockets against some very common attacks. Let us see what they are and what should you do to protect your websockets.

## #0: Enable CORS

WebSocket doesn’t come with CORS inbuilt. That being said, it means that any website can connect to any other website’s websocket connection and communicate without any restriction! I’m not going into reasons why this is the way it is, but a quick fix to this is to verify `Origin` header on the websocket handshake.

Sure, Origin header can be faked by an attacker, but it doesn’t matter, because to exploit it, attacker needs to fake the Origin header on victim’s browser, and modern browsers do not allow normal javascript sitting in web browsers to change Origin header.

Moreover, if you’re actually authenticating users using, preferably, cookies, then this is not really a problem for you (more on this on point #4)

## #1: Implement rate limiting

Rate limiting is important. Without it, clients can knowingly or unknowingly perform a DoS attack on your server. DoS stands for Denial of Service. DoS means a single client is keeping the server so busy that the server is unable to handle other clients.

In most of the cases it is a deliberate attempt by an attacker to bring down a server. Sometimes poor frontend implementations can also lead to DoS by normal clients.

We’re gonna make use of the leaky bucket algorithm (which apparently is a very common algorithm for networks to implement) for implementing rate limiting on our websockets.

The idea is that you have a bucket which has a fixed size hole at its floor. You start putting water in it and the water goes out through the hole at the bottom. Now, if your rate of putting water into the bucket is larger than the rate of flowing out of the hole for a long time, at some point, the bucket will become full and start leaking. That’s all.

Let’s now understand how it relates to our websocket:

1. Water is the websocket traffic sent by the user.
2. Water passes down the hole. This means the server successfully processed that particular websocket request.
3. Water which is still in the bucket and has not overflowed is basically pending traffic. The server will process this traffic later on. This could also be bursty traffic flow (i.e. too much traffic for a very small time is okay as long as bucket doesn’t leak)
4. Water which is overflowing is the traffic discarded by the server (too much traffic coming from a single user)

The point here is, you have to check your websocket activity and determine these numbers. You’re going to assign a bucket to every user. We decide how big the bucket should be (traffic which a single user could send over a fixed period) depending on how large your hole is (how much time on average does your server need to process a single websocket request, say saving a message sent by a user into a database).

This is a trimmed down implementation I’m using at [codedamn](https://codedamn.com) for implementing leaky bucket algorithm for the websockets. It is in NodeJS but the concept remains same.

```
if(this.limitCounter >= Socket.limit) {if(this.burstCounter >= Socket.burst) {   return 'Bucket is leaking'}++this.burstCounterreturn setTimeout(() => {this.verify(callingMethod, ...args)setTimeout(_ => --this.burstCounter, Socket.burstTime)}, Socket.burstDelay)}++this.limitCounter
```

So what’s happening here? Basically, if the limit is crossed as well as the burst limit (which are constants set), the websocket connection drops. Otherwise, after a particular delay, we’re gonna reset the burst counter. This leaves space again for another burst.

## #2: Restrict payload size

This should be implemented as a feature within your server-side websocket library. If not, its time to change it to a better one! You should limit the maximum length of the message that could be sent over your websocket. Theoretically there is no limit. Of course, getting a huge payload is very likely to hang that particular socket instance and eat up more system resources than required.

For example, if you’re using WS library for Node for creating websockets on server, you can use the [maxPayload option](https://github.com/websockets/ws/blob/master/doc/ws.md#new-websocketserveroptions-callback) to specify the maximum payload size in bytes. If the payload size is bigger than that, the library will natively drop the connection.

Do not try to implement this on your own by determining message length. We don’t want to read the whole message into the system RAM first. If it is even 1 byte greater than our set limit, drop it. That could be only implemented by the library (which handles messages as a stream of bytes rather than fixed strings).

## #3: Create a solid communication protocol

Because now you’re on a duplex connection, you could be sending anything to the server. The server could send any text back to client. You would need to have a way for effective communication between both.

You can’t send raw messages if you want to scale the messaging aspect of your website. I prefer using JSON, but there are other optimized ways to set up a communication. However, considering JSON, here’s what a basic messaging schema would look like for a generic site:

```
Client to Server (or vice versa):   
{ status: "ok"|"error", event: EVENT_NAME, data: <any arbitrary data> }
```

Now it’s easier for you on the server to check for valid events and format. Drop the connection immediately and log the IP address of the user if the message format differs. There’s no way the format would change unless someone is manually tingling with your websocket connection. If you’re on node, I recommend using the [Joi library](https://github.com/hapijs/joi) for further validation of incoming data from user.

## #4: Authenticate users before WS connection establishes

If you’re using websockets for authenticated users, it is a pretty good idea to only allow authenticated users to establish a successful websocket connection. Don’t allow anyone to establish a connection and then wait for them to authenticate over the websocket itself. First of all, establishing a websocket connection is a bit expensive anyway. So you don’t want unauthorized people hopping on your websockets and hogging connections which could be used by other people.

To do this, when you’re establishing a connection on frontend, pass some authentication data to websocket. It could be a header like X-Auth-Token: <some token assigned to this client on login>. By default, cookies would be passed anyway.

Again, it really comes down to the library you’re using on the server for implementing websockets. But if you’re on Node and using WS, there’s this [verifyClient](https://github.com/websockets/ws/blob/master/doc/ws.md#new-websocketserveroptions-callback) function which gets you access to info object passed to a websocket connection. (Just like you have access to req object for HTTP requests.)

## #5: Use SSL over websockets

This is a no-brainer, but still needs to be said. Use wss:// instead of ws://. This adds a security layer over your communication. Use a server like Nginx for reverse proxying websockets and enable SSL over them. Setting up Nginx would be a whole another tutorial. I’ll leave the directive you need to use for Nginx for those folks who are familiar with it. [More info here](http://nginx.org/en/docs/http/websocket.html).

```
location /your-websocket-location/ {  
    proxy_pass ​http://127.0.0.1:1337;  
    proxy_http_version 1.1;  
    proxy_set_header Upgrade $http_upgrade;  
    proxy_set_header Connection "Upgrade";  
}
```

Here it is assumed your websocket server is listening on port 1337 and your users connect to your websocket in this fashion:

```
const ws = new WebSocket('wss://yoursite.com/your-websocket-location')
```

## Questions?

Have any questions or suggestions? Ask away!
---
title: "Enforcing a single web socket connection per user with Node.js, Socket.IO, and Redis"
url: https://medium.com/p/65f9eb57f66a
---

# Enforcing a single web socket connection per user with Node.js, Socket.IO, and Redis

[Original](https://medium.com/p/65f9eb57f66a)

# Enforcing a single web socket connection per user with Node.js, Socket.IO, and Redis

[![Mario Tacke](https://miro.medium.com/v2/resize:fill:64:64/1*OmrK_iNMdfOTiTqJEqaAqQ.jpeg)](/@mariotacke?source=post_page---byline--65f9eb57f66a---------------------------------------)

[Mario Tacke](/@mariotacke?source=post_page---byline--65f9eb57f66a---------------------------------------)

7 min read

·

Jul 30, 2018

--

11

Listen

Share

More

Press enter or click to view image in full size

![]()

Recently, I have been working on a real-time multi-player browser game and ran into the “single-session” problem. Essentially, I wanted to prevent a user from connecting more than once via web sockets. This is important because being logged on to the same account multiple times could create unfair scenarios and makes the server logic more complex. Since web socket connections are long lived, I needed to find a way to prevent this.

### Wish list

* A user can only be connected once, no matter how many browser tabs they have open. A user can be identified via their authentication token.
* The system must work in a clustered environment. Individual server nodes should be able to go down without affecting the rest of the system.
* Authorization tokens should not be passed via query parameters, instead via a dedicated authentication event after the connection is established.

For this project we will use Node.js, Socket.IO, and Redis.

## Humble Beginnings

Let’s set up our project and get this show on the road. You can check out the full GitHub [repo here](https://github.com/mariotacke/blog-single-user-websocket). First, we will set up our Socket.IO server to accept connections from the front-end.

By default, the server will listen on port 9000 and echo the connection status of each client to the console. Socket.IO provides a built-in mechanism to generate a unique socket id which we will use to identify our client’s socket connection.

Next, we create a sample page to connect to our server. This page consists of a status display, an input box for our secret token (we will use it for authentication down the road) and buttons to connect and disconnect.

Also, we need to set up some very rudimentary logic to perform the connect/disconnect and hook up our status and token inputs.

This is everything you need to set up a basic web socket client and server. At this moment, we can connect, disconnect, and log the connection status to the user. And all of this in vanilla JavaScript too! 🍻 Next up: authenticating users.

## Authentication

Letting users connect without knowing who they are is of little use to us. Let’s add basic token authentication to the connection. We assume that the connection uses SSL/TLS once deployed. Never use an unencrypted connection. Ever. 😶

At this point we have a few options: a) append a user’s token to the query string when they are connecting, or b) let any user connect and require them to send an authentication message after they connect. The Web Socket protocol specification ([RFC 6455](https://tools.ietf.org/html/rfc6455#section-10.5)) does not prescribe a particular way for authentication and it does not allow for custom headers, and since query parameters could be logged by the server, I chose option b) for this example.

We will implement the authentication with `socketio-auth` by 

[Facundo Olano](/u/f89b781338d4?source=post_page---user_mention--65f9eb57f66a---------------------------------------)

, an Auth module for Socket.IO which allows us to prompt the client for a token **after** they connect. Should the user not provide it within a certain amount of time, we will close the connection from the server.

We hook up `socketAuth` by passing it our `io` instance and configurations options in the form of three events: `authenticate`, `postAuthenticate`, and `disconnect`. First, our `authenticate` event is triggered after a client connected and emits a subsequent `authentication` event with a user token payload. Should the client not send this authentication event within a configurable amount of time, `socketio-auth` will terminate the connection.

Once the user has sent their token, we verify it against our known users in a database. For example purposes, I created an async `verifyUser` method that mimics a real database or cache lookup. If the user is found, it will be returned, otherwise the promise is rejected with reason `USER_NOT_FOUND`.

If all goes well, we invoke the callback and mark the socket as authenticated or return `UNAUTHORIZED` if the token is invalid.

We have to adapt our front-end code to send us the user’s token upon connection. We modify our `connect` function as follows:

We added two things: `socket.emit('authentication', { token })` to tell the server who we are and an event listener `socket.on('unauthorized')` to react to rejections from our server.

Now we have a system in place that let’s us authenticate users and optionally kick them out should they not provide us a token after they initially connect.

This however still does not prevent a user from connecting twice with the same token. Open a separate window and try it out. To force a single session, our server has to smarten up. 💡

## Preventing Multiple Connections

Making sure that a user is only connected once is simple enough on a single server since all connections sit in memory. We can simply iterate through all connected clients and compare their ids with the new client. This approach breaks down when we talk about clusters however. There is no easy way to determine if a particular user is connected or not without issuing a query across all nodes. With many users connecting, this creates a bottleneck. Surely there has to be a better way.

Enter distributed locks with Redis.

We will use Redis to lock and unlock resources, in our case: user sessions. Distributed locks are hard and you can read all about them [here](https://redis.io/topics/distlock). For our use case, we will implement a resource lock on a single Redis node. Let’s get started.

The first thing we will do is connect Socket.IO to Redis to enable pub/sub across multiple Socket.IO servers. We will use the `socket.io-redis` adapter provided by Socket.IO.

This Redis server is used for its pub/sub functionality to coordinate events across multiple Socket.IO instances such as new sockets joining, exchanging messages, or disconnects. In our example, we will reuse the same server for our resource locks, though it could use a different Redis server as well.

Let’s create our Redis client as a separate module and promisify the methods so we can use `async` / `await` .

Let’s talk theory for a moment. What is it *exactly* we are trying to achieve? We want to prevent users from having more than one concurrent web socket connection to us at any given time. For an online game this is important because we want to avoid users using their account for multiple games at the same time. Also, if we can guarantee that only a single user session per user exists, our server logic is simplified.

To make this work, we must keep track of each connection, acquire a lock, and terminate other connections should the same user try to connect again. To acquire a lock, we use Redis’ `SET` method with `NX` and an expiration (more on the expiration later). `NX` will make sure that we only set the key if it does not already exist. If it does, the command returns `null` . We can use this setup to determine if a session already exists and abort if it does.

We modify our `authenticate` function as follows:

Once we have verified that a user has a valid token, we attempt to acquire a lock for their session (line 6). If Redis can `SET` the key, it means that it did not previously exist. We also added `EX 30` to the command to auto-expire the lock after 30 seconds. This is important because our server or Redis might crash and we don’t want to lock out our users forever. The reason I chose 30 seconds is because Socket.IO has a default ping of 25 seconds, that is, every 25 seconds it will probe connected users to see if they are still connected. In the next section, we will make use of this to renew the lock.

To renew the lock, we’re going to hook into the `packet` event of our socket connection to intercept `ping` packages. These are received every 25 seconds by default. If a package is not received by then, Socket.IO will terminate the connection.

We’re using the `postAuthenticate` event to register our `packet` event handler. Our handler then checks if the socket is authenticated via `socket.auth` and if the packet is of type `ping`. To renew the lock, we will again use Redis’ `SET` command, this time with `XX` instead of `NX`. `XX` states that it will only be set if it already exists. We use this mechanism to refresh the expiration time on the key every 25 seconds.

We can now authenticate users, acquire a lock per user id, and prevent multiple sessions from being created. Our locks will remain in effect as long as the clients report back to our servers every 25 seconds.

Yet, there is one use case we have overlooked: if a user closes their browser with an active connection and attempts to reconnect, they will erroneously receive an `ALREADY_LOGGED_IN` message. This is because the previous lock is still in effect. To properly release the lock when a user intentionally leaves our site, we must remove the lock from Redis upon disconnect.

In our `disconnect` event, we check whether or not the socket was authenticated and then remove the lock from Redis via the `DEL` command. This cleans up the user session lock and prepares it for the next connection.

That’s all there is to it! To see our connection flow in action, open two browser windows and click Connect in each of them with the same token; you will receive a status of `Disconnected: ALREADY_LOGGED_IN` on the latter. Exactly what we wanted. Time to sit back and relax. 😅

## Conclusion

In this article I described a way to authenticate web socket connections and prevent multiple user sessions through the use of Node.js, Socket.IO, and Redis. This mechanism is stateless and works in a clustered server environment.

To get even better session control and fail over, I suggest delving deeper into distributed locks with Redis and reading about the redlock algorithm.

Thank you for taking the time to read through my article. If you enjoyed it, please hit the Clap button a few times 👏! If this article was helpful to you, feel free to share it!

For more from me, be sure to follow me on [Twitter](https://twitter.com/MarioTacke), here on [Medium](/@mariotacke), or check out my [website](https://www.mariotacke.io)!

### References

* [Distributed locks with Redis](https://redis.io/topics/distlock)
* [Sample project repository](https://github.com/mariotacke/blog-single-user-websocket)
* [socket.io-redis repository](https://github.com/socketio/socket.io-redis)
* [socketio-auth repository](https://github.com/facundoolano/socketio-auth)
* [RFC 6455](https://tools.ietf.org/html/rfc6455#section-10.5)
* Redis [SET](https://redis.io/commands/set) and [DEL](https://redis.io/commands/del) commands
---
title: "Switching from ws to socket.io"
url: https://medium.com/p/d66343ca900d
---

# Switching from ws to socket.io

[Original](https://medium.com/p/d66343ca900d)

# Switching from ws to socket.io

[![Tosh Velaga](https://miro.medium.com/v2/resize:fill:64:64/1*KlQUEdLUxZGginDLHDsDgg.jpeg)](/@toshvelaga?source=post_page---byline--d66343ca900d---------------------------------------)

[Tosh Velaga](/@toshvelaga?source=post_page---byline--d66343ca900d---------------------------------------)

3 min read

·

Feb 14, 2022

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

I originally built my SaaS application using [ws](https://www.npmjs.com/package/ws) on my Node server and the native websockets implementation on my React frontend. I did this because I had prior experience working with the native implementation at a startup and so I thought it would be faster to go with what I was most comfortable with. The native implementation worked great, the problem though is that like literally every example I could find online uses socket.io. The reality is socket.io is still enormously popular and practically every open source webRTC project online uses socket.io. Instead of building everything from scratch I decided to build off this excellent [open source repo](https://github.com/0x5eba/Video-Meeting), which uses socket.io in order to speed up development time. Additionally socket.io has several advantages such as great docs, a large community, [heartbeats](https://stackoverflow.com/questions/7061362/advantage-disadvantage-of-using-socketio-heartbeats) to check if the connection is still intact, and built in methods that can speed up development if you need to create rooms and [send messages](https://socket.io/docs/v3/broadcasting-events/) to the connected clients.

Porting my app over wasn’t too difficult, the only issue I encountered was that once again my app worked locally, but didn’t work in production. I had to do some configuring to get it to work in production, which involved editing my Nginx configuration.

On the server side it was super simple to set up. Here is my new socket setup on the server:

```
OLD WS INITIALIZATION   
const wss = new WebSocket.Server({ port: WS_PORT }, () => {  
  console.log(`Listening on PORT ${WS_PORT} for websockets`)  
})NEW SOCKET.IO INITIALIZATION  
const io = new Server(WS_PORT, {  
/* options */  
cors: {  
  origin: '*',  
  },  
})
```

On the client side here is my main logic which takes place in a useEffect hook. One thing that is unique about socket.io is that it first establishes a connection through HTTP long polling and then upgrades to a websocket connection. From the [docs](https://socket.io/docs/v3/how-it-works/) here is how it works in a little more detail. So I couldn’t actually get it to work like this, so I added an option to ONLY use websockets and not use any HTTP long polling. Thats why you see **{transports: [‘websocket’]}** in the code.

Press enter or click to view image in full size

![]()

The last thing I had to do was change my Nginx configuration since I am running my server on AWS EC2. Here is my updated Nginx server block.

Overall switching from ws to socket io is fairly easy. Socket.io obviously adds more overhead, but it has amazing docs and community support. Additionally socket.io is easier to scale horizontally than vanilla websockets and has some built it methods that make broadcasting messages to every connected client simpler. That being said there are [obvious drawbacks](https://dzone.com/articles/socketio-the-good-the-bad-and-the-ugly). For a more detailed comparison check out this excellent [blog post](https://itnext.io/differences-between-websockets-and-socket-io-a9e5fa29d3dc). As for my project I hope that using socket.io continues to speed up development. Hope you found this article helpful. If so give it a clap :)
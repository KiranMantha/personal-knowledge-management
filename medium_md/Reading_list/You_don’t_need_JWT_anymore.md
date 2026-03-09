---
title: "You don’t need JWT anymore"
url: https://medium.com/p/974aa6196976
---

# You don’t need JWT anymore

[Original](https://medium.com/p/974aa6196976)

# You don’t need JWT anymore

[![Miroslaw Shpak](https://miro.medium.com/v2/resize:fill:64:64/1*PaAGo9HckwLGRjpj4RmRWg.jpeg)](/@bytesbay?source=post_page---byline--974aa6196976---------------------------------------)

[Miroslaw Shpak](/@bytesbay?source=post_page---byline--974aa6196976---------------------------------------)

3 min read

·

Oct 2, 2021

--

87

Listen

Share

More

A simpler way to authenticate users with web3 using signed messages

Press enter or click to view image in full size

![]()

It’s no secret that the Ethereum login will soon become a user standard and passwords will no longer be needed. Nevertheless, dApp development is still a fairly young direction and many standards for their development are still set.

Now all developers continue to write dApps with old practices, instinctively using the same JWT for authentication. I propose a slightly different approach.

I myself started developing dApps using JWT. From the first project, I felt that authentication always becomes tricky and that there must be something redundant in the process. After a couple of projects, I realized that the JWT itself is redundant. Let me explain why.

Press enter or click to view image in full size

![]()

This diagram shows how I did authentication on my first few projects. Here the scheme almost wholly repeats the standard procedure with JWT, the only thing is that instead of a login and password, the user sends a signature.

Why do we need to get JWT? After all, even without it, you can reliably identify the user by taking the address from his signature.

Here’s how to simplify it:

Press enter or click to view image in full size

![]()

The user still generates a signature, but already with an **Expire-date** inside, so that if an attacker gets the signature, it won’t be useful for long (the same as with the JWT). Further, the signature is placed in the standard Authorization header and processed on the server by taking the user’s address and finding the user in the database. That’s all. And you do not need to constantly update the encryption keys for the JWT on the server, so in general, a lot of responsibility falls off the server.

To simplify this flow even more, I made the [web3-token](https://github.com/bytesbay/web3-token) module. To install it, use the command:

```
$ npm i web3-token
```

This module can be used both on the server and on the client.

Let’s look at an example, starting with the client-side.

After calling the **.sign** method, you will see something similar to this (if you are using MetaMask).

Press enter or click to view image in full size

![]()

As you can see, the message is completely transparent for the user since they must see what they are signing. So instead of using JSON structure for better readability, I decided to use the same structure as for HTTP headers.

In the body of the message, we see the version of the token and the **expire date** itself.

Next, here’s what the backend (Node.js) does with this token:

It’s pretty simple, just one line, and the module takes over all cryptography. We magically obtain the user’s address from the signature and find them in the database using this address. Then , for example , you may grant this user an NFT by his address.

The result is a very convenient stateless user authentication method, ideal for hybrid dApps. The only drawback is that it is hard to test in Postman 😀

I would really like something like a standard to come out of this, but until then, I am open to criticism (or possibly questions/suggestions) via telegram [@bytesbay](http://twitter.com/bytesbay) or mail [miroslaw.shpak@gmail.com](mailto:miroslaw.shpak@gmail.com). I am also currently preparing a series of articles on real-time blockchain game development with NFT, so stay tuned.

Web3 is just around the corner.

There is still a war going on in Ukraine and at this moment the support of each and everyone is really important. Every dollar **strongly** brings Ukraine closer to victory 🇺🇦. [How can you help](https://aid.prytulafoundation.org/en/)
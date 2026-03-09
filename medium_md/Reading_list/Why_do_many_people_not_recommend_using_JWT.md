---
title: "Why do many people not recommend using JWT?"
url: https://medium.com/p/9147b2c899f8
---

# Why do many people not recommend using JWT?

[Original](https://medium.com/p/9147b2c899f8)

Member-only story

# Why do many people not recommend using JWT?

[![Oliver Foster](https://miro.medium.com/v2/resize:fill:64:64/1*ggy9mwK4Uj54EJL52gtC0A.png)](https://medium.com/@haiou-a?source=post_page---byline--9147b2c899f8---------------------------------------)

[Oliver Foster](https://medium.com/@haiou-a?source=post_page---byline--9147b2c899f8---------------------------------------)

5 min read

·

Sep 16, 2024

--

75

Listen

Share

More

Press enter or click to view image in full size

![]()

> My article is open to everyone; non-member readers can click this [link](https://medium.com/@haiou-a/why-do-many-people-not-recommend-using-jwt-9147b2c899f8?sk=c497651e1aef92eeba8dd18490303113) to read the full text.

If you often look at online tutorials for building projects, you’ll notice that many of them use JWT.

But is it really safe?

Why do so many people advise against using it? This article will provide you with a comprehensive understanding of JWT and its pros and cons.

## What is JWT?

Here is the official website: [JSON Web Tokens — jwt.io](https://jwt.io/)

This is what JWT is.

Press enter or click to view image in full size

![]()

JWT stands for `JSON Web Token`.

If you’re not familiar with JWT, don’t worry! They’re not that complicated!

You can think of JWT as a piece of JSON data that you can verify to confirm that **the data** comes from someone you trust.

Of course, we won’t go into how it’s implemented here, but if you’re interested, you can look into it yourself.

Now, let’s talk about its process:

1. When you log in to a website, the website generates a **JWT** and sends it to you.
2. The JWT acts like a package that contains some **identity information** about you, such as your username, roles, permissions, etc.
3. Then, **you carry this JWT with you every time you communicate with the website**.
4. Whenever you access a page that requires authentication, **you present this JWT to the website**.
5. When the website receives the JWT, it verifies its signature to ensure that it was issued by the website and checks the information within it to confirm your identity and permissions.
6. If everything checks out, you’re allowed to continue accessing the protected page.

![]()

## Why is JWT considered bad?

First, when we use JWT, it’s typically for tasks like:

* User registration on a website
* User login on a website
* User clicks and performs actions
* The website uses the user’s information to create, update, or delete data

These tasks often involve database operations such as:

* Recording the actions a user is performing
* Adding some user data to the database
* Checking the user’s permissions to see if they can perform certain actions

Now, let’s go over some of its drawbacks step by step.

## Size

This is an undeniable issue.

For example, if we need to store a user ID like “xiaou”:

* If stored in a cookie, the total size would only be 5 bytes.
* If we store the ID in a JWT, its size increases by about 51 times.

Press enter or click to view image in full size

![]()

This undoubtedly increases our bandwidth burden.

## Redundant Signatures

One of JWT’s main selling points is its encrypted signature.

Since JWTs are signed, the recipient can verify whether the JWT is valid and trustworthy.

However, for the past 20 years, almost every web framework has offered the benefits of encrypted signatures while using regular session cookies.

In fact, most web frameworks automatically sign (and even encrypt!) your cookies for you.

This means you get the same benefits as JWT signatures without needing to use JWT itself.

In practice, in most web authentication cases, JWT data is stored in session cookies, meaning you now have two layers of signatures: one on the cookie itself and one on the JWT.

## Token Revocation Issue

Since tokens remain valid until they expire, the server has no simple way to revoke them.

Here are some use cases where this can become dangerous.

**Logging out doesn’t actually log you out!**

Imagine you tweet something on Twitter and then log out. You might think you’ve been logged out from the server, but that’s not the case.

Since JWTs are self-contained, they remain valid until they expire, which could be 5 minutes, 30 minutes, or any duration set as part of the token.

So, if someone obtains this token during that time, they can continue accessing your account until it expires.

**Stale Data**

Imagine a user is an administrator but is downgraded to a regular user with fewer privileges. Again, this won’t take effect immediately, and the user will continue to have admin privileges until the token expires.

**JWTs are often not encrypted**

This means that anyone who can perform a man-in-the-middle attack and sniff the JWT will have your authentication credentials. This becomes easier because the attack only needs to intercept the connection between the server and the client.

## Security Issues

As for whether JWT is secure, we can refer to this article:

[JWT (JSON Web Token) (in)security — research.securitum.com](https://research.securitum.com/jwt-json-web-token-security/)

## Conclusion

In summary, JWTs are suitable as **one-time authorization tokens** for transmitting claims between two entities.

However, JWTs are not suitable as a **long-term, persistent data storage mechanism**, especially for **managing user sessions**.

Using JWTs for session management can introduce a series of serious security and implementation issues.

Instead, traditional session mechanisms like session cookies, along with their well-established implementations, are more appropriate for storing long-term, persistent data.

That said, if you’re using JWT for your own development and learning purposes, without considering security or performance, then it’s perfectly fine.

However, once you’re dealing with a production environment, you need to avoid these potential issues.

## Stackademic 🎓

Thank you for reading until the end. Before you go:

* Please consider **clapping** and **following** the writer! 👏
* Follow us [**X**](https://twitter.com/stackademichq) | [**LinkedIn**](https://www.linkedin.com/company/stackademic) | [**YouTube**](https://www.youtube.com/c/stackademic) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443)
* Visit our other platforms: [**In Plain English**](https://plainenglish.io/) | [**CoFeed**](https://cofeed.app/) | [**Differ**](https://differ.blog/)
* More content at [**Stackademic.com**](https://stackademic.com/)
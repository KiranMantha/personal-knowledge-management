---
title: "Where Should You Store JSON Web Tokens (JWT)?"
url: https://medium.com/p/4f76abcd4577
---

# Where Should You Store JSON Web Tokens (JWT)?

[Original](https://medium.com/p/4f76abcd4577)

# Where Should You Store **JSON Web Tokens** (**JWT**)?

[![Naveen DA](https://miro.medium.com/v2/resize:fill:64:64/1*M5RzDcyh7z_OkignP1UNUg.jpeg)](https://naveenda.medium.com/?source=post_page---byline--4f76abcd4577---------------------------------------)

[Naveen DA](https://naveenda.medium.com/?source=post_page---byline--4f76abcd4577---------------------------------------)

4 min read

·

Jul 6, 2021

--

19

Listen

Share

More

Press enter or click to view image in full size

![]()

I have been designing and developing web applications for more than 7 years.

Through these years, I have been seen a lot of authentication mechanisms, some of them are RESTful and others are not. The RESTful services mostly used JSON Web Token (JWT) as an authentication token.

Whenever I implemented JWT-based authentication, I asked myself this question, “**Where do we store the JWT?”**

*Edit:* This article is focusing only on browser implementation.

Let’s answer the big question.

We have three options available for storing the data on the client side and each of those has its own advantages and disadvantages. And the options are:

1. Cookie
2. localStorage
3. Session Storage

### **Cookie**

![]()

If you set the JWT on cookie, the browser will automatically send the token along with the URL for the Same Site Request. But it is vulnerable to the [CSRF](https://en.wikipedia.org/wiki/Cross-site_request_forgery).

We can protect the site against `CSRF` by setting a cookie with `SameSite=strict`

*Edit 1:* I̶n̶ ̶g̶e̶n̶e̶r̶a̶l̶ ̶p̶e̶o̶p̶l̶e̶ ̶m̶i̶g̶h̶t̶ ̶t̶h̶i̶n̶k̶,̶ ̶X̶S̶S̶ ̶c̶a̶n̶ ̶b̶e̶ ̶d̶e̶f̶e̶a̶t̶e̶d̶ ̶i̶f̶ ̶w̶e̶ ̶s̶e̶t̶ ̶t̶h̶e̶ ̶h̶t̶t̶p̶O̶n̶l̶y̶ ̶f̶l̶a̶g̶,̶ ̶b̶u̶t̶ ̶i̶t̶ ̶i̶s̶ ̶p̶o̶s̶s̶i̶b̶l̶e̶ ̶t̶o̶ ̶a̶t̶t̶a̶c̶k̶ ̶b̶y̶ ̶u̶s̶i̶n̶g̶ ̶X̶S̶T̶ ̶”̶s̶u̶b̶s̶e̶t̶”̶ ̶(̶k̶i̶n̶d̶a̶)̶ ̶o̶f̶ ̶X̶S̶S̶.̶

*Edit 2:* We can easily defect the XSS by setting `httpOnly` flag.

**Pros:**

1. The browser will automatically send the token to the server.
2. The same token is available to multiple tabs of your application instance.

**Con:**

1. Vulnerable to XSS.
2. You need to attach the token in the header if you use a protocol like [OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6750).

**localStorage**

![]()

The localStorage doesn’t send the data automatically along with the URL. So you need to implement the system for the auth token for every URL. But the best part is that this method is not vulnerable to CSRF.

**Pros**

1. Not vulnerable to CSRF.
2. The same token is available to multiple tabs of your application instance.

**Con**

1. Vulnerable to XSS.
2. You need to implement a mechanism for the sent the token.

**Session Storage**

![]()

Session Storage is pretty much the same as Local Storage, except the token will accessible only one tab, once the tab is closed the session got destroyed. So it **not** useful for the feature like **remember me.** But this can be used in the multi-login feature like Tab A is in a different login and Tab B is in different login.

**Pros:**

1. Not Vulnerable to CSRF.
2. Easy to implement Multiple logins in one browser.

**Con:**

1. Vulnerable to XSS.
2. Once the tab is closed, the session data got destroyed.

You might notice that all the 3 methods have the same con — “**Vulnerable to XSS”.** Yes, all these methods are vulnerable to XSS. Please do care about XSS and always follows the [best practices](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html) for XSS protection.

### **Conclusion**

Both localStorage and SessionStorage are not protected by the XSS by default.

However, the Cookie provides a bunch of security options like `SameSite` ,” `HttpOnly` , etc. So it is good to go with Cookie.

***“Store Your JWT on Cookie with Some Secure Flag.”***

### Sidenote:

If you use Express, [these packages](https://medium.com/hackernoon/express-js-important-npm-packages-related-to-security-2393466e18d5) might help to improve your application security.

Also, check out my recent articles

1. [Deep Dive Into Tree-Shaking](/deep-dive-into-tree-shaking-ba2e648b8dcb)(How to reduce your bundle size)
2. [5 useEffect Infinite Loop Patterns](/5-useeffect-infinite-loop-patterns-2dc9d45a253f)

I found these articles are useful to me, maybe these can be useful to you.

[## Why JWTs Suck as Session Tokens

### JSON Web Tokens (JWTs) are so hot right now. They're all the rage in web development: With all these amazing things…

scotch.io](https://scotch.io/bar-talk/why-jwts-suck-as-session-tokens?source=post_page-----4f76abcd4577---------------------------------------)

[## Token Storage

### Securing SPAs that make API calls come with their own set of concerns. You'll need to ensure that tokens and other…

auth0.com](https://auth0.com/docs/security/data-security/token-storage?source=post_page-----4f76abcd4577---------------------------------------#don-t-store-tokens-in-local-storage)

[## Is it safe to store a JWT in localStorage with ReactJS?

### In most of the modern single-page applications, we indeed have to store the token somewhere on the client-side (most…

stackoverflow.com](https://stackoverflow.com/questions/44133536/is-it-safe-to-store-a-jwt-in-localstorage-with-reactjs?source=post_page-----4f76abcd4577---------------------------------------)

*More content at* [***plainenglish.io***](http://plainenglish.io/)
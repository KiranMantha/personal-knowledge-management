---
title: "JWT Ultimate: How-To Guide With Best Practices In JavaScript"
url: https://medium.com/p/f7ba4c48dfbd
---

# JWT Ultimate: How-To Guide With Best Practices In JavaScript

[Original](https://medium.com/p/f7ba4c48dfbd)

Member-only story

# JWT: Ultimate How-To Guide With Best Practices In JavaScript

## JSON Web Token in Node.js from basics to code examples

[![Martin Novak](https://miro.medium.com/v2/resize:fill:64:64/1*R0H334cJb2-2c_XDtzkU5Q.jpeg)](/@meet-martin?source=post_page---byline--f7ba4c48dfbd---------------------------------------)

[Martin Novak](/@meet-martin?source=post_page---byline--f7ba4c48dfbd---------------------------------------)

14 min read

·

Nov 24, 2021

--

1

Listen

Share

More

Press enter or click to view image in full size

![]()

[JSON Web Token (JWT)](https://jwt.io/) is a standard [RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519) for exchanging cryptographically signed JSON data. It is probably the most popular current standard of authorization on the web, especially when it comes to microservices and distributed architecture.

As a developer, when you are asked to implement a modern web application, you may need to break it down into independent services. Independent services and distributed architecture have many advantages. One thing that you will need to think about is how your services will know that users are allowed to use them.

![]()

With stateful session management, your solution would be to create a user session that is shared among all parts of the system. But with a growing distributed system, sharing a session can be quite challenging.

The alternative to stateful session management is passing a stateless JSON Web Token which will represent an access token or an identity token. It will hold claims that allow your services to authorize their users and it will use the magic of cryptography to ensure that the token is authentic and has not been tampered with.

![]()

This way your services don’t need to share a stateful session, they only need to trust the token that they are given.

## Standard Sessions

If you have been around for a while like me, you know that the standard approach on the web has been the use of session and session-based cookies.

Users would sign in with their credentials and the server would give them back a cookie with their session ID. That cookie is then sent by the user with every request to authorize the user.

Nowadays that process is so automated that you barely need to write any code to support it and browsers know to automatically send the session cookie with every request themselves. it is super convenient.

Press enter or click to view image in full size

![]()

The above diagram should feel fairly familiar and simple and it is what websites have been doing for a long time.

Modern web solutions are often based on multiple servers or multiple services working together. If you want to use the session for these, it means that you will need some centralized storage for your sessions available to all pieces of your architecture that require authorized access.

For a simple website, it is far easier to implement standard session management which is well supported by libraries on the server, and cookie management in the browser.

JWT is much harder to implement and requires an experienced team to make a well architectured secure solution even when using products like [Auth0](https://auth0.com/).

I would not consider classic session management dead. I would even always recommend its use until you can justify the need for JWT based on the distributed architecture of your solution.

But because JWT is a challenging and exciting topic, let's dive into its intricacies and learn about its advantages.

## What is JWT?

JWT is simply a signed JSON intended to be shared between two parties. The signature is used to verify the authenticity of the token to make sure that none of the JSON data were tampered with. The data of the token themselves are not encrypted.

The method of authenticating users does not change with JWT. You can still use a user name and password (although you should use something more secure like two-factor authentication or DID Auth). The difference is only in how you manage the user authorization (how you let your service know that the user has permission to do something).

On the server, you verify the token signature and get access to the JSON data directly which is much simpler for distributed architectures.

In your web application frontend, your code needs to manage how the token is stored in the browser (cookie, session storage, or local storage) and how it is passed with requests to the server (as authorization bearer header).

Press enter or click to view image in full size

![]()

If you compare the diagrams for session-based authorization and JWT, you will notice that the principle is very similar. The main reason for using JWT is for the client-server communication to remain stateless.

JWT gained popularity because statelessness made it easier to design independent services without having to deal with shared session management. However, there are solutions for managing sessions with each cloud provider whether it’s [Amazon Web Service](https://aws.amazon.com/caching/session-management/), [Microsoft Azure](https://azure.microsoft.com/es-es/blog/using-sql-azure-for-session-state/), or [Google Cloud](https://cloud.google.com/go/getting-started/session-handling-with-firestore). On your own servers, you can for example use [Redis](https://redis.com/solutions/use-cases/session-management/) as a shared cache for session storage.

JWT is generally considered to be a more secure solution than common session management. However, I would consider this highly debatable. Both approaches have their own strong and weak points and you have to make compromises to account for user convenience.

## jsonwebtoken library for Node.js with axios

Node.js has a great library from auth0 guys for JWT: [jsonwebtoken](https://www.npmjs.com/package/jsonwebtoken), which is directly featured on the [JWT webpage](https://jwt.io/).

To create a token you can just call:

This basic call will encrypt the JSON data using a secret key which you would usually store as an environment variable. Without other arguments, this is a synchronous call that will use symmetric encryption HS256 (HMAC with SHA-256).

The generated token might look like this:

```
eyJhbGciOfJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkaWWiOiJka…afyMH0.WrIEBW5LNLjfGWqIA4XKsyIiuWzbIIpNadfZVkmA6hPs
```

The token is just Base64 code which decode would look like this:

```
{"alg":"HS256","typ":"JWT"}{"id":"fo:%sk@lr"}�k��c~¶.�S��K�`ѱ
```

The random characters that you see at the end are the signature that allows you to verify the authenticity of the token but the data and claims that you add are not encrypted unless you encrypt them, as you can see.

Return this token to the frontend application as part of the server response.

The frontend app then needs to add the token in a header to every request that requires authorization. This is how such a call might look with [axios](https://www.npmjs.com/package/axios) library:

Notice the authorization header, that is where we add the token.

Server-side we then verify the token and access its secrets:

That is all the magic that there is to it. With this information, you should be able to make a working solution.

However, there are also a few considerations for your implementation that you should think about.

Full `jsonwebtoken` implementation with HS512 would look like this:

## jose library example in Node.js

A better Node.js library for JWT is [jose](https://www.npmjs.com/package/jose).

It is a bit more complicated to use but it supports the use of JWK, or JWE, as well as signing with EdDSA, so I would recommend it to you as an option.

This is an example of using the library with EdDSA and importing PEM private and public keys (also notice how short the EdDSA keys are even though offer better protection):

## What to store in the JWT token?

JWT in our scenario represents an identity token and it should hold claims about the subject (user). That means that the token holds the user identifier, like: `{ "sub": "awWF#$512" }`.

Depending on your application the token can also hold capability claims that for example indicate that the subject can access certain services of your system.

You can of course store other information in the cookie including the user’s e-mail and so on. However, think about what information your services really need about the user and what you store in the token, given that the information is not encrypted. The user identifier (subject claim) is usually sufficient.

If you use JWT as an identity token, then the most important claim is the subject, because you can use it to identify the user in your services.

If you use JWT as an access token, you use a claim that the holder of this token is authorized to use some part of a system. You can do that using the audience claim which can be a single uri or string record or it can be an array of these. Service consuming the token can then verify that it is among the audience listen in the JWT.

There is a number of other information recommended to store in the payload defined by the JWT RFC 7519. These optional claims include:

* **iss**: issuer string or URI,  
  for example: `"iss": "https://didauth.meet-martin.com"`
* **sub**: subject identifier string or URI,  
  for example: `"sub": "OCfs425k"`
* **aud**: audience string or URI, or an array of these,  
  for example: `"aud": "https://api.meet-martin.com"`
* **exp**, expiration time after which the token is not valid by NumericDate,  
  for example: `"exp": "1630983721"`
* **nbf**, not before identifies NumericDate before which the token cannot be accepted,  
  for example: `"nbf": "1630983612"`
* **iat**, issue at contains NumbericDate of when the token was issued,  
  for example: `"iat": "163983612"`
* **jti**, JWT, holds a unique identifier of the JWT as a case sensitive string,  
  for example: `"jti": "fsg1R34"`

Keep in mind that none of these claims are encrypted unless you provide additional encryption yourself. If you need to transfer sensitive data, have a look at the JWE standard.

Base 64 decoded token looks like this:

```
{"alg":"ES512","typ":"JWT"}{"iss":"https://domain.tld","sub":"martin@mail.tld","aud":"https://domain.tld","exp":1630986887,"nbf":1630983287,"jti":"asfasgsadg","iat":1630983287}☺ɱ��%�§�∟x��8�k��c~¶.�S��K�`ѱ���♣��►C∟�8����ϖ↔C�x�����<����c♫♥���q/W�  
� �♂t�↑V�0�☼�4��  
�hG��Z��‼u�     �oU▬Q[L�hʒ‼�(♀�H
```

## Where to store the JWT token in the browser?

You have three options here really. You either use cookies, web storage, or in memory. The most commonly used option seems to be local storage.

### JWT in a cookie

Cookies have the advantage that they are automatically sent together with each request so you don’t need to deal with the authorization header.

Cookies are still open to Cross-Site Request Forgery (CSRF)attacks because of which you should also implement CSRF tokens. CSRF token is a random string sent as a cookie with each request and it is different for each request.

You should also use `httpOnly` flag to make the cookie available only server-side. A cookie with the `HttpOnly` attribute is inaccessible to the JavaScript `document.cookie` API; it is sent only to the server.

A cookie with the `Secure` attribute is sent to the server only with an encrypted request over the HTTPS protocol (however, on localhost only, you can still use HTTP).

This is an example implementation for Express in Nodej.js:

In Express you can use [csurf middleware](https://www.npmjs.com/package/csurf) that takes care of the CSRF token for you. The [express-session](https://www.npmjs.com/package/express-session) uses cookies which are `httpOnly` by default but you need to make them `secure` by a parameter as you can see in the code.

### JWT in web storage: Local storage vs session storage

The difference between these two is that local storage is more permanent. Session storage is cleared when the user closes the website window. Local storage data have to be explicitly deleted.

Unlike cookies, local storage is sandboxed to a specific domain and its data cannot be accessed by any other domain including sub-domains. But remember that you are still vulnerable to Cross-Site Scripting (XSS). Both cookie and web storage solutions are vulnerable to XSS.

Local storage is used the most in JWT implementations. However, session storage is the more secure option here.

With localStorage JWT is not passed with each request automatically, and you need to pass it to the server through an authorization header yourself.

### JWT in memory

The most secured solution here is to store JWT in memory of your single-page application. This means that you end up storing the token in a variable in JavaScript without additional persistence.

This comes with some limitations. You cannot implement a single-sign-on (SSO) and each tab or open window in a browser will require its own sign-in because JavaScript memory is not shared. However, the sharing issue can be worked around by the use of a refresh token.

This solution is of course still vulnerable to Cross-Site Scripting like all the other solutions.

You will need to pass the JWT with each request using an authorization header the same way as with web storage in the previous code example.

## Refresh Tokens

Your application design should include the provision of refresh tokens.

JWT represents a short-lived access token. Short-lived here means usually anything between 5 minutes to 24 hours or days depending on your application.

Refresh tokens are long-lived and represent a mechanism for silent authentication to obtain a new access token without any user action. How long is long-lived is driven by user convenience or how long you want users to remain authenticated between uses of your service. For example, if you want your user to come to your website after two weeks of not using it and still find themselves authenticated, then two weeks is your refresh token expiration date.

Your refresh token renewal strategy also depends on your expiration date.

For example, you can design your system to provide an access token with a 24-hour expiration time. You also provide a refresh token with 2 week expiration time. However, with every renewal of the access token, you also provide a new refresh token.

You may want to also store in the token the time when it was created (`iat`) so that information can be used to invalidate centrally all old tokens before their original expiration time.

Refresh token usually holds just an opaque identifier and it is stored either as an `httpOnly`, `secure` cookie or within web storage (either of which enables your website to work in multiple open tabs in case that you store your access token in memory as recommended earlier).

## How to sign out users with JWT access tokens?

The user could sign in on multiple devices which means that one user will have multiple access tokens and refresh tokens. Any of these could also be in a possession of an evil hacker.

You should store the action of signing out separately in your database and use it to invalidate all refresh tokens.

Usually, we rely on JWT expiration but the JWT and refresh token could be invalidated by their `id` (`jti`).

An easy solution is to store in your database the time of sign out and consider all JWT and refresh tokens created before that date (`iat`) as invalid.

On the side of your browser application, you should simply remove the JWT from its storage (web storage or memory).

## What encryption should you use?

The most commonly used algorithm for JWT encryption is HMAC and RSA. Other algorithms are supported as well including RSASSA-PKCS, RSASSA-PSS, and ECDSA. The default is HMAC, the most popular is RSA, and the most secure is ECDSA.

### HMAC

The most simple and least secure option is HS256 which is HMAC with SHA-256. It is a symmetric algorithm which means that one secret is used for both signing and verifying the token. An example of a secret would be: `Much$3cr3tS0S3cureVerySafe`.

In this case, the authentication service as well as all services requiring authorization will need access to the same key which potentially opens more opportunities for stealing it through some API exploit.

It is not generally recommended for production use. Nonetheless, it is easier for demo applications or code examples.

### RSA

Your other option for JWT is to use RS256 (RSA with SHA-256) which is an asymmetric encryption algorithm using private and public keys. It is also probably the most common algorithm used by web applications because a lot of developers are familiar with it even though it is not the most secure or most performant option.

A private key is used by the authentication service to produce the original token. The public key is then used by other services to verify the token. If the public key is compromised, it can be used to read the data, but it cannot be used to create other tokens. Using RSA over HMAC is recommended.

The public key can also be kept public for other third-party consumers so that by using it anyone can access the data in the token and verify that the data are really coming from you because they are signed by your private key.

You can generate your RSA public and private keys by `openssl`:

### ECDSA

When using `jsonwebtoken` node library, your best option is ES512, which is Elliptic Curve Digital Signature Algorithm ([ECDSA](https://en.wikipedia.org/wiki/Elliptic_Curve_Digital_Signature_Algorithm)) using a P-521 curve and SHA-512 hash algorithm. ECDSA is also used by bitcoin. ECDSA is another asymmetric encryption like RSA and it is considered to be the more secure option.

> Elliptic Curve Cryptography (ECC) is much harder to crack than RSA (or maybe we are just really good at breaking RSA). As a result, ECDSA can use much shorter keys than RSA along with much shorter signatures. A short Elliptic Curve (EC) key of around 256 bits provides the same security as a 3072 bit RSA key.  
> - <https://www.scottbrady91.com/JOSE/JWTs-Which-Signing-Algorithm-Should-I-Use>

The approach here is the same as with RSA. Use your private key to sign the token as part of authentication and use the public key in your services.

You can generate your ECDSA ES512 public and private keys by `openssl`:

The U.S. Department of Commerce National Institute of Standards and Technology (NIST) has included ECDSA in FIPS 186–4 Digital Signature Standard (DSS): <https://csrc.nist.gov/publications/detail/fips/186/4/final>

### EdDSA

If you use `jose` node library, you will also get access to Edwards-curve Digital Signature Algorithm ([EdDSA](https://en.wikipedia.org/wiki/EdDSA)) encryption algorithm, which is the [ultimate best option for JWT implementation](https://crypto.stackexchange.com/questions/60383/what-is-the-difference-between-ecdsa-and-eddsa). It uses SHA-512 and Curve 25519 to give the Ed25519 method.

EdDSA, as you can guess, is an asymmetric algorithm that uses public and private keys so its use is the same as with RSA or ECDSA. EdDSA has better performance and even shorter keys than ECDSA while providing better security.

You can generate your EdDSA ed25519 public and private keys by `openssl`:

The U.S. Department of Commerce National Institute of Standards and Technology (NIST) has included EdDSA in a draft of FIPS 186–5 Digital Signature Standard (DSS): <https://csrc.nist.gov/publications/detail/fips/186/5/draft>

FIPS 186–5 has been in draft since October 2019 but it is not yet a released standard in November 2021.

However, if U.S. NIST is not your concern, then EdDSA is the most secure and performant option that you can currently use for a JWT signature.

### Signature Cryptography Conclusion

In your application, try to use EdDSA. If that is not possible then use ES512. Using symmetric algorithms like HMAC should be your last option.

For a comparison of key length, running the example `openssl` codes, RSA private key is 1674 characters, es512 is 308 characters, and ed25519 is just 64 characters.

Use the private key in your authentication service and use the public key in your other services. To increase security, also think of key rotation. Generate new keys after some period of time.

Don’t ever save your encryption keys directly in code or in a code versioning system like git. You should either use a key management system or environment variables.

## Summary: Top 10 JWT Recommendations

Press enter or click to view image in full size

![]()

* Before JWT you need to also think about making your authentication process secure. Use 2 Factor Authentication for your users or decentralized identifiers. Just a user name and a password is not considered a secure solution.
* If you are building a standard frontend/backend website, use standard session management. If you are building distributed system with services, implement JWT authorization.
* Create an access token by signing the JWT using a private key of an asymmetric encryption algorithm. Use ES512 for `jsonwebtoken` NPM library and Ed25519 for `jose` NPM library.
* Use `sub` subject claim to store user ID but don’t save other user data unless necessary because everything stored in the JWT can be read directly. The data are not encrypted.
* Create a refresh token with a long-lived expiration date.
* In your frontend, store the access token in memory of your client's JavaScript application and store the refresh token in a web store.
* Send JWT access token as a bearer in HTTP header with each server request that requires authorization.
* Verify the JWT on your server using the public key (public to your services). Load user data from your database based on the user ID stored in the JWT subject.
* When the access token expires, silently authenticate the user again by using the refresh token.
* Perform the silent authentication by using a refresh token to provide both a new access token and a new refresh token.
* Sign out the user from all devices by invalidating all access tokens and request tokens connected to the user ID.

## Conclusion

When you implement your JWT logic, your solution decisions should take into account the best practice, security, and also user convenience.

Hopefully, I have included all the necessary information that you may require.
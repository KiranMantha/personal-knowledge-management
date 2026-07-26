---
title: "Building A Simple Single Sign On(SSO) Server And Solution From Scratch In Node.js."
url: https://medium.com/p/ea6ee5fdf340
---

# Building A Simple Single Sign On(SSO) Server And Solution From Scratch In Node.js.

[Original](https://medium.com/p/ea6ee5fdf340)

# Building A Simple Single Sign On(SSO) Server And Solution From Scratch In Node.js.

[![Ankur Anand](https://miro.medium.com/v2/resize:fill:64:64/1*DsmXrZxd1k-4EedPT5D3pg.jpeg)](https://medium.com/@ankur_anand?source=post_page---byline--ea6ee5fdf340---------------------------------------)

[Ankur Anand](https://medium.com/@ankur_anand?source=post_page---byline--ea6ee5fdf340---------------------------------------)

7 min read

·

Aug 28, 2018

--

11

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3Dea6ee5fdf340&operation=register&redirect=https%3A%2F%2Fcodeburst.io%2Fbuilding-a-simple-single-sign-on-sso-server-and-solution-from-scratch-in-node-js-ea6ee5fdf340&source=---header_actions--ea6ee5fdf340---------------------post_audio_button------------------)

Share

The web application uses the browser/server architecture, `HTTP` as the communication protocol. `HTTP` is a stateless protocol. Each time the browser requests, the server processes it independently and does not associate with the previous or subsequent request. But it also means that any user can access the server resources through the browser. If you want to protect some resources of the server, you must restrict the browser request; to limit the browser request, you must authenticate the browser request, respond to the legitimate request, ignore Illegal request; to authenticate a browser request, you must be aware of the browser request status. Since the `HTTP` protocol is stateless, so we let the server and browser maintain a state together, using the mechanism such as ‘Cookies’ or ‘Sessions’ or ‘JWT’.

When we have a single system the state mechanism, through the the login authentication is easy to maintain. But when a single system evolves into multiple system, how do we maintain the state of each individual system, do users have to log in one by one and then log out one by one?

The golden rule of the good users solution is that, the growing complexity of your architecture should be borne by the system rather than the user. No matter how complex the internals of the web system is, it is a unified whole for the users. That is to say, the entire application group of the user accessing the web system is the same as accessing a single system.

So how do we write the system using single-system login solution?   
Remember the Good old ‘Cookies’ solution, but then we hit domain restriction of the cookie street, until we unified the domain names of all subsystems in the web application group under a top-level domain name.

> But then,  
> Microservices ate the Cookies

People started using different technologies to build their services sometime utilizing different domains too, where key value of the cookie (JSESSIONID in Java) is different than (session in Node.js), and suddenly the session was not easier to be maintained.

And, we all started building a new login method to enable login for multi-system application groups. This is single sign-on.

## Single Sign-On(SSO)

> The basic working principle on which SSO works is you can log in to a system in a multi-system application group and be authorized in all other systems without having to log in again, including single sign-on and single sign-off.

Going forward we are going to write the same for us, for learning perspective.

> Enterprise solutions needs much more efforts than what we we are going to put😅. That’s a sole reason Enterprise solutions are in business.

**So how do we login using SSO?**

At the Heart ❤️ of SSO we have a single independent authentication server, which can accept security information such as user’s email, username and password. Other systems do not provide login access and only accept indirect authorization from the authentication server. The indirect authorization is implemented using the token.

[## ankur-anand/simple-sso

### A Simple sso principle implemented in node.js. Contribute to ankur-anand/simple-sso development by creating an account…

github.com](https://github.com/ankur-anand/simple-sso?source=post_page-----ea6ee5fdf340---------------------------------------)

I’m going to use node.js for the code, but you can use any technology the implement the basic principle of the SSO.

1. The user accesses the protected resource of system “sso-consumer”. “sso-consumer” finds that the user is not logged in, jumps to the “sso-server”, using his own address as a parameter.  
   We are going to build the express.js middleware to check the same for our request.

Press enter or click to view image in full size

![]()

**2.** The SSO authentication server finds that the user is not logged in and directs the user to the login page.

Press enter or click to view image in full size

![]()

*Extra Security Pointers:   
\** We are checking if the serviceURL that has came as query to the ‘sso-server’ has been registered to use the ‘sso-server’ or not.

```
const alloweOrigin = {  
"http://consumer.ankuranand.in:3020": true,  
"http://consumertwo.ankuranand.in:3030": true,  
"http://test.tangledvibes.com:3080": true,  
"http://blog.tangledvibes.com:3080": fasle,  
};
```

**3.** User enters username and password to submit login request.

Press enter or click to view image in full size

![]()

**4.** The SSO authentication server verifies the user information and creates a session between the user and the sso authentication server. **This is called a global session and creates an authorization token.** The authorization token is a string of random characters. It doesn’t matter how it is generated. As long as it is not repeated and not easy to forge,

**5.** The SSO authentication server takes the **authorization token** to jump to the initial request address (system “sso-consumer”).

Press enter or click to view image in full size

![]()

*Extra Security Pointers:  
\* Always consider this token as intermediate token and exchange the real data using this token.  
\* If you are using JWT as the intermediate token please avoid sharing any critical data over this JWT.*

**6**. The ‘sso-consumer’ gets the token and goes to the ‘sso-server’ authentication to check if the token is valid.The ‘SSO-SERVER’ verifies the token and return another token with user information to the “sso-consumer”. The “sso-consumer” uses this token to create a session with the user. **This session is called local session.**

Here is a brief sso-consumer middle-ware inside the “sso-consumer” application, built using the ‘express.js’

Press enter or click to view image in full size

![]()

After the request from the sso-consumer , the sso-server checks the token to find out whether the token exists and expires. The token verification succeeds.

The SSO-Server in our case we are going to return a signed JWT with user information, after successful validation.

Press enter or click to view image in full size

![]()

*Extra Security Pointers:  
\* Inside “sso-server” register each application that’s going to use the sso-server for authentication and give them some sort of verification header while making a request. This establishes a better security between consumer and “sso-server”.  
\* You can also generate different “private” and “public”* `rsa` *file for each application and let each application verify their JWT with their respective Public Key at the consumer side.*

You can also define application-level policy at the centralized place.

Press enter or click to view image in full size

![]()

After the user logs in successfully, a session is established with the “sso authentication server” and each consumer subsystem. The session established between the user and the “sso authentication server” is called a **global session**. The session established between the user and each “consumer subsystem” is called a **local session**. After the local session is established, the user can access the consumer subsystem protected resources.

Press enter or click to view image in full size

![]()

“Local session” and “Global session” both are established.

Brief look at the functions that sso-client and sso-server that we’ve implemented.

**SSO-Consumer**

1. The sso-consumer subsystem does not log in to the user request and jumps to the sso server for authentication.
2. Receive the token sent by the sso authentication server.
3. Communicate with sso-server to verify the validity of the token.
4. Receives a JWT, verifies the JWT using the public key.
5. Establish a local session

**Sso-server**

1. Verify the user’s login information.
2. Create a global session.
3. Create an authorization token.
4. Send a token with sso-client communication.
5. Verify sso-client token validity.
6. Send a JWT with the user information.

In summary, there are many options for system integration single sign-on solutions, each of which has its own advantages and adaptation environment. Building one from scratch is an iterative project that needs to analyze the characteristics of each system, including login methods, user information storage and synchronization, etc., and cannot blindly rely on the single way to solve the problem.

Similarly we can implement the “Logout”, just we need to consider these three relationship in mind while writing the “Logout” Functionality.

1. Local session exists, global session must exist.
2. Global session exists, local session does not necessarily exist.
3. Global session is destroyed, local session must be destroyed.

[## ankur-anand/simple-sso

### A Simple sso principle implemented in node.js. Contribute to ankur-anand/simple-sso development by creating an account…

github.com](https://github.com/ankur-anand/simple-sso?source=post_page-----ea6ee5fdf340---------------------------------------)

**Learned something? Clap your 👏 to help others find this article.**
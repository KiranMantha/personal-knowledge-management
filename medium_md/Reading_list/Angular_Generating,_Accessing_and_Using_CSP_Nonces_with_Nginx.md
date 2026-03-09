---
title: "Angular: Generating, Accessing and Using CSP Nonces with Nginx"
url: https://medium.com/p/14e0da87b20e
---

# Angular: Generating, Accessing and Using CSP Nonces with Nginx

[Original](https://medium.com/p/14e0da87b20e)

# Angular: Generating, Accessing and Using CSP Nonces with Nginx

[![Angular&NodeEnthusiast](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)](https://ramya-bala221190.medium.com/?source=post_page---byline--14e0da87b20e---------------------------------------)

[Angular&NodeEnthusiast](https://ramya-bala221190.medium.com/?source=post_page---byline--14e0da87b20e---------------------------------------)

7 min read

·

Jun 27, 2024

--

1

Listen

Share

More

**What is a nonce ?**

In general, **nonce** means a word or phrase that is intended for use only once. In CSP, it is a randomly generated token that we use exactly one time. This means that a unique nonce must be generated per request.

**Why do we need a nonce ?**

Using a nonce is one of the easiest ways to allow the execution of inline scripts and styles when Content Security Policy (CSP) is enforced in the application.

From your web server generate a random **base64-encoded** string of at least **128 bits of data** from a cryptographically secure random number generator to set the CSP nonce value.

**How does nonce allow inline execution of scripts and styles ?**

When you enforce CSP, inline execution of scripts and styles will be disabled because the browser doesn’t know the difference between JS code that you wrote and intend for the user to execute vs code that an attacker has injected into the page (for example via an XSS vulnerability).

So code like the following will not execute:

```
<style>  
p{ color:red;   }  
  
</style>  
  
<script>  
    console.log("I am an inline script")  
</script>
```

These inline script/style blocks are dangerous, and the **nonce at**tribute in the script/style element lets the browser know that the web-server intends on serving this script/style block if and only if the nonce attribute value in the script/style tag matches the nonce value in the **Content-Security-Policy** header.

**How can we generate a nonce in Nginx ?**

This is how my **nginx.config** looks like currently.

I have applied the Content Security Policy using the **add\_header** directive below. A very basic policy which puts a restriction that the source of the resources loaded in the application must be the application itself.

```
add_header Content-Security-Policy “default-src ‘self’; always”;
```

This is how the **index.html** looks like. We are loading an external JS file:**external.js** , an inline script and an inline style as well.

In **external.js**, we just have a single log statement.

```
console.log(“I am logging from an external JS file”);
```

I have containerized the application and deployed to nginx. Loading the application in the browser, observe the errors due to CSP violation.

Only the log statement within **external.js** has executed. The inline script has not executed. Even the inline style has not executed because the color of <h4>Secure Angular App</h4> has not changed to red.

Press enter or click to view image in full size

![]()

Lets now modify the **nginx.config** as below to generate a unique random nonce for every request and add it to the Content-Security-Policy header. We have set the nonce to **$request\_id** which is a unique request identifier generated from 16 random bytes(128 bits), in hexadecimal.

I suggest you to go for the **njs** module in nginx to generate a stronger CSP nonce. <https://github.com/nginx/njs> and <https://nginx.org/en/docs/njs/reference.html> can give you a better idea.

In the below lines of code, we have set a variable **$cspNonce** to the request ID.

```
set $cspNonce $request_id;  
sub_filter_once off;  
sub_filter_types *;  
sub_filter NGINX_CSP_NONCE $cspNonce;
```

What is **sub\_filter,sub\_filter\_once** and **sub\_filter\_types** ?

The **ngx\_http\_sub\_module** module is a filter that modifies a response by replacing one specified string by another.

sub\_filter,sub\_filter\_once and sub\_filter\_types are few of the multiple directives available under this module.

In the below line, the **sub\_filter** directive will replace the content of **NGINX\_CSP\_NONCE** variable with the value of **$cspNonce**.

```
sub_filter NGINX_CSP_NONCE $cspNonce;
```

In the below line, we want to perform this replacement of **NGINX\_CSP\_NONCE** variable with the value of **$cspNonce** not just once, but wherever the variable is encountered.

```
sub_filter_once off;
```

We pass the mime-type as value to the sub\_filter\_types directive. In the below line \* indicates that string replacement can be enabled for any mime-type.

```
sub_filter_types *;
```

Finally we are using **$cspNonce** variable in the CSP header under the **script-src** and **style-src** directives.

```
add_header Content-Security-Policy “default-src ‘self’; script-src ‘self’ ‘nonce-$cspNonce’; style-src ‘self’ ‘nonce-$cspNonce’ always”;
```

**How do we access and use the nonce in the Angular app ?**

Angular states there are 2 ways to do it:

=>Using the **ngCspNonce** attribute on the root component selector <app-root> and setting the attribute to a unique nonce for each request.

OR

=>Registering the **CSP\_NONCE** injection token with the providers of the **AppModule** and feeding this token with a runtime nonce value.

In this story, will be demonstrating only the first approach of using the ngCspNonce attribute, since **with nginx we can add nonce to both the index.html and the response headers**.

Below is the updated **index.html**.

We have added the **ngCspNonce** attribute to the root **AppComponent** selector **<app-root>** and set this attribute to a variable **NGINX\_CSP\_NONCE**. As discussed earlier, this variable will be replaced with a nonce by the **sub\_filter** directive provided by nginx before the response is sent back. We will see that shortly.

There is no change in the **nginx.config**.

Redeploying the application, observe that the inline <style> has executed and the <h4> element is now red in color.

Press enter or click to view image in full size

![]()

Observe below that NGINX\_CSP\_NONCE has been replaced by a nonce in the **ngCspNonce** attribute and a **nonce** attribute with the same nonce has been applied to the inline <style> element as well.

Press enter or click to view image in full size

![]()

Please note that the inline script has failed to execute and is still blocked by CSP. Setting the nonce using the **ngCspNonce** attribute will **only enable Angular to render the inline <style> elements**. Shortly we will discuss how we can handle inline <script> elements.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

As previously mentioned and also as the **angular.dev** documentation states: **“When serving your Angular application, the server should include a randomly-generated nonce in the HTTP header for each request”,** we are generating a different nonce for each request as you can see in the screenshots below.

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

Getting back to the inline script issue. To resolve the inline script error, we can propose 2 solutions:

1. **Get rid of inline scripts !!** So I move the contents of the script into a new file **inlineScriptMoved.js** within the **assets/js** folder. I have slightly updated the content of the script.

```
console.log(“I am an inline script moved to an external file”)
```

I reference this JS file as below in the index.html.

```
<script src=”assets/js/inlineScriptMoved.js”></script>
```

When I re-deploy the application with the changes, I no longer face any CSP violations.

Press enter or click to view image in full size

![]()

2. The 2nd solution will be to retain the inline script but **manually add the nonce attribute to the <script> element** as below.

```
<script nonce=”NGINX_CSP_NONCE”>  
console.log(“I am an inline script”)  
</script>
```

As already discussed, nginx will replace all occurrences of **NGINX\_CSP\_NONCE** with random nonce value.

So our updated **index.html** now likes below.

Redeploying the application, observe that our inline script has successfully executed.

Press enter or click to view image in full size

![]()

A nonce attribute has been set on the inline <script> element which matches the nonce in the CSP header. Thus the browser has no reason to complain :)

Press enter or click to view image in full size

![]()

Let me show you another scenario with inline styles.

In the **AppComponent**, I will add a <p> element as below with an inline style.

```
<p style=”background-color: aqua;color:blue”>I am a paragraph tag with an inline style</p>
```

When I redeploy the application, you can observe below that the style has not been applied to the <p> element and we see a CSP violation, inspite of the **ngCspNonce** attribute being used.

Press enter or click to view image in full size

![]()

In such scenarios, it would be preferred to get rid of inline styles. If you find it unavoidable, you can modify the style attribute in the <p> element as below to make it work.

```
<p [style]=”’background-color: aqua;color:blue’”>I am a paragraph tag with an inline style</p>
```

The style now applies correctly without any errors.

Press enter or click to view image in full size

![]()

## In Plain English 🚀

*Thank you for being a part of the* [***In Plain English***](https://plainenglish.io) *community! Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://twitter.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/)
* Visit our other platforms: [**CoFeed**](https://cofeed.app/) | [**Differ**](https://differ.blog/)
* More content at [**PlainEnglish.io**](https://plainenglish.io)
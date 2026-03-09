---
title: "AEM ACS Commons error page handling"
url: https://medium.com/p/a84549761260
---

# AEM ACS Commons error page handling

[Original](https://medium.com/p/a84549761260)

# AEM ACS Commons error page handling

[![Imran Khan](https://miro.medium.com/v2/resize:fill:64:64/1*qB5cH4JYH-vgBSoEJHR2IQ.jpeg)](/@toimrank?source=post_page---byline--a84549761260---------------------------------------)

[Imran Khan](/@toimrank?source=post_page---byline--a84549761260---------------------------------------)

3 min read

·

Jan 22, 2023

--

1

Listen

Share

More

ACS commons provide a capability to load page related to 404, 500, 405 etc. in case requested page didn’t get find or something went wrong on server.

Let’s try to understand the flow for error page handling using ACS commons.

browser raised a request for home.html page. AEM publish instance or dispatcher cache will return requested page if it is found.

In case page doesn’t exist on both the places either on AEM instance or dispatcher will return 404.html page with the help of ACS commons.

If something went wrong or any 500 error occurred on AEM server will return or 500.htm page with the help of ACS commons

Press enter or click to view image in full size

![]()

## Steps to implement ACS Commons error page handling:

1. install ACS commons package or include same as pom.xml dependency. Follow this [link](https://medium.com/p/c7a4cc75b867/edit) for more detail.

2. Add **errorhandler** folder inside apps folder as shown below. Add **404.jsp** and **default.jsp** file to handle error.

Press enter or click to view image in full size

![]()

3. Add below content to 404.jsp file:

```
<%@page session="false"%><%  
%><%@include file="/apps/acs-commons/components/utilities/errorpagehandler/404.jsp" %>
```

4. Add below content to 500.jsp file:

```
<%@page session="false"%><%  
%><%@include file="/apps/acs-commons/components/utilities/errorpagehandler/default.jsp" %>
```

5. Add below dependency to **filter.xml** file:  
/ui.apps/src/main/content/META-INF/vault/filter.xml

![]()

6. Add below code to inline **pom.xml** file:  
/ui.apps.structure/pom.xml

![]()

7. Add below code snippet in page component dialog xml file to author root site page to author error page.

Press enter or click to view image in full size

![]()

8. Add below OSGI configuration in code base to enable error page handling.

![]()

9. Create below hierarchy to create error pages of type CQ page inside project as shown below.

Naming convention for pages inside error page hierarchy will follow HTTP status error codes.   
**Examples:**  
**Page Not Found →** /errors/404.html  
**Internal Server Error →** /errors/500.html  
**Forbidden Error →** /errors/405.html, etc.

![]()

**Note:** Always to try to create new error page template and component to create pages related to error handling.

10. Author error page path /content/practice/us/en/errors) on root content hierarchy as /content/practice/us/en.

Press enter or click to view image in full size

![]()

11. Try to access a page in browser which doesn’t exist under **/content/practice/us/en** hierarchy will load 404 page:

Press enter or click to view image in full size

![]()

**Note:** Set`DispatcherPassError=0` in dispatcher configuration will allow erring requests to be sent back to AEM.

I hope you found out this article interesting and informative. Please share it with your friends to spread the knowledge.

You can follow me for upcoming blogs [follow](/@toimrank).  
Thank you!
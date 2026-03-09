---
title: "AEM: Fixing the “No Renderer for Extension HTML” Error in AEM After Code Deployment"
url: https://medium.com/p/09ef03f51580
---

# AEM: Fixing the “No Renderer for Extension HTML” Error in AEM After Code Deployment

[Original](https://medium.com/p/09ef03f51580)

Member-only story

# AEM: Fixing the “No Renderer for Extension HTML” Error in AEM After Code Deployment

[![Shankar Angadi](https://miro.medium.com/v2/resize:fill:64:64/0*-1pQrVD3TD58V6lb.jpg)](/@angadi.saa?source=post_page---byline--09ef03f51580---------------------------------------)

[Shankar Angadi](/@angadi.saa?source=post_page---byline--09ef03f51580---------------------------------------)

1 min read

·

Aug 30, 2024

--

7

Listen

Share

More

Non members can access from [**here**](/@angadi.saa/aem-fixing-the-no-renderer-for-extension-html-error-in-aem-after-code-deployment-09ef03f51580?sk=854914cbf4bbfcc569491421d429fd2f)

In one of our recent projects, we encountered an issue where, after **deploying** code through the pipeline, none of the pages would work. The error log showed the following message

```
org.apache.sling.servlets.get.impl.DefaultGetServlet No renderer for extension html, cannot render resource JcrNodeResource
```

Restarting the server temporarily resolved the problem, but this was not an acceptable long-term solution. After investigation, we found that the issue could be fixed by updating the `sling.properties` file.

### Solution:

1. Open the `sling.properties` file.
2. Search for the `org.osgi.framework.bootdelegation` property.
3. Modify it to include the following:

```
org.osgi.framework.bootdelegation=sun.*,com.sun.*,jdk.internal.reflect,jdk.internal.reflect.*
```

4. Save the file and restart the server.

This update prevents the error from occurring even after multiple deployments. The addition of the `jdk.internal.reflect,jdk.internal.reflect.*` packages allows for proper class loading, ensuring that the server can render the necessary resources.

By making this change, we were able to stabilize the deployment process and eliminate the need for manual restarts.
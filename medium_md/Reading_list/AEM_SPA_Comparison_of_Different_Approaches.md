---
title: "AEM SPA | Comparison of Different Approaches"
url: https://medium.com/p/fd5860fb6530
---

# AEM SPA | Comparison of Different Approaches

[Original](https://medium.com/p/fd5860fb6530)

# **AEM SPA | Comparison of Different Approaches**

[![Gourav Chakraborty](https://miro.medium.com/v2/resize:fill:64:64/1*dmbNkD5D-u45r44go_cf0g.png)](/@gourav.chakraborty?source=post_page---byline--fd5860fb6530---------------------------------------)

[Gourav Chakraborty](/@gourav.chakraborty?source=post_page---byline--fd5860fb6530---------------------------------------)

7 min read

·

Nov 28, 2023

--

Listen

Share

More

Single-page applications are becoming more and more common.

It is a contemporary method of creating a website where browsing seems like using a native application without waiting for a page to load.

AEM offers the ability to use the SPA framework to develop a SPA-compliant website.

With AEM, we may create SPA using a contemporary JS framework, such as Angular or React.

## **Levels of AEM SPA Integration**

The following are the principal three ways SPAs can be integrated with AEM.

Via Remote Editor, SPA Editor SDK, Pure Headless.

Another new approach is via Universal editor.

## **Pure Headless**

The content is managed in the AEM repository and made available via REST and GraphQL APIs in the headless model.

On a single-page app, styling, presentation, and delivery take place.

AEM can be used to manage content creation and distribution while leaving other native apps in charge of the presentation.

Pure Headless Solution can be achieved via

**1.** **Content Fragments**

Content fragments are used to create data for the single-page app. We can use different types of content fragment data types to create data models and deliver them to the app.Content fragments are type of assets which can be accessed via GraphQL and Asset Http APIs.

**2.** **GraphQL APIs**

The data is queried via the GraphQL API.

Even so, the client can access the persistent GraphQL queries on the AEM server.

By caching the queries, this feature enhances performance.

The high-level steps that must be taken to accomplish this are listed below with the diagram.

· Create a Project specific Configuration folder to hold the content fragment model.

· Define Content Fragment Model.

· Author Content Fragments.

· Create GraphQL Endpoints.

· Publish the GraphQL endpoint and Content Fragments.

· Permit data access for the Single Page App in the OSGi configuration.

· Allow the endpoints in the dispatcher.

Press enter or click to view image in full size

![]()

**Advantages**

• Emphasizes the development of reusable, cross-channel, channel-neutral content fragments.

• AEM is used as a content repository, for managing content, and for content authoring.

• AEM can be used to just manage content, enabling another platform to handle content delivery and presentation.

• Content that is reusable, presentation-neutral, and made from structured data elements (text, dates, references, etc.)

• Dissociates the presentation of content from its administration.

**Limitations/Considerations**

• AEM’s complete editing features cannot be utilized.

• Only content fragments can be used to expose content.

• AEM is solely used for content production; its display, analytics, scaling, and caching features are not utilized.

• The Presentation layer’s total reliance on third-party programmers.

## **Remote Editor**

The Single Page Application is hosted remotely, and a portion of the app can be edited in AEM.

The SPA Editor SDK framework is used. Only a few areas of the website can be authored within AEM.

The high-level steps that must be taken to accomplish this are listed below with the diagram.

Create a page using the Remote SPA Page Template.

· Configure the SPA URL in page properties.

· Create a mapping using Sling Mapping between SPA routes and AEM pages.

· Configure CORS OSGI configuration to protect AEM and allow SPA to fetch only allowed details.

Press enter or click to view image in full size

![]()

**Advantages**

• Fixed components ensure component positioning.

• The component’s creation and modification are possible outside of the development cycle.

• This strategy is appropriate for parts of the website that have been fixed but still require minor tweaking.

• Sling mappings and placeholder pages can be utilized to implement the dynamic route feature.

**Limitations/Considerations**

• Requires developers to precisely define the composition of editable content.

• It takes extra effort to set up policies.

• Teams working on AEM, and third-party applications need to be given clear guidelines and regulations around who is responsible for creating and rendering content.

## **SPA Editor SDK**

The SPA Editor JS SDK that AEM offers allows content creators to modify the content of Single Page apps inside of AEM.

On top of AEM, you may create a complete single-page application.

Behind the scenes, SPA pages communicate with Sling Models, which give content in JSON format. The react component receives the JSON and oversees presentation logic.

Here are the high-level steps with a diagram regarding how to enable SPA editor SDK with AEM.

Press enter or click to view image in full size

![]()

• Create a project with a recent AEM archetype and specify the frontend module whether “react” or “angular”.

• This archetype will add several SPA-related dependencies to package.json.

Press enter or click to view image in full size

![]()

• The default template extends spa-project-core/components/page which interacts with the page model

data-sly-use.page=”com.adobe.aem.spa.project.core.models.Page”. It provides a hierarchical model of subpages with which a single-page application can be built.

• The next step is to create different building block components for the page.

You need to create the component’s presentation part in the ui.frontend part. JSX is used to render the HTML of the component.

• The component dialog needs to be created in the ui.apps as usual under the component folder.

• The Backend model should implement ComponentExporter and override getExportedType().

• Map SPA Comment to AEM component. A 1:1 mapping should be created between SPA component and AEM component.

Press enter or click to view image in full size

![]()

8. The JSON model response is parsed by MapTo, which then sends the appropriate values as props to the SPA component.

### **Advantages**

• The Author and Publish environments share the same user experience because SPA is hosted on the AEM platform.

• Incontext editing is allowed.

• With little AEM development, the front-end developer has total control over the project.

• Simple connection with current experience cloud solutions, such as digital asset management, targeting, and analytics.

### **Limitations/Considerations**

• Additional work is needed to make the website SEO enabled, including SSR and HTML push state,

• First page load might be delayed but subsequent page loads will be quicker.

* XSS attacks are more common in SPA applications.

## Universal Editor

This is a new feature launched by Adobe to edit any content, from any implementation and any aspect.

Press enter or click to view image in full size

![]()

The universal editor supports any architecture including, server-side rendering, client-side rendering etc.

It supports any framework including Vanilla AEM, 3rd party frameworks like React, Next.js Angular etc.

It supports any hosting either inside AEM or a remote domain.

**Steps to enable Universal Editor**

First request access to the universal editor <https://experience.adobe.com/#/aem/editor>

**Add dependencies**

Before your app can be instrumented for use with the Universal Editor, it must include the following dependency.

[@adobe/universal-editor-cors](http://twitter.com/adobe/universal-editor-cors)

To activate the instrumentation, the following import must be added to your index.js.

import “[@adobe/universal-editor-cors](http://twitter.com/adobe/universal-editor-cors)”;

NOTE:- If you are not using React App add this in the document body

<script src=”https://cdn.jsdelivr.net/gh/adobe/universal-editor-cors/dist/universal-editor-embedded.js" async></script>

**Add OSGI Configurationons**

CORS and cookie settings must be done within AEM.

Following OSGI configuration must be done

com.day.crx.security.token.impl.impl.TokenAuthenticationHandler

org.apache.sling.engine.impl.SlingMainServlet

**Instrument the Page**

The universal editor requires a URN, URN identifies the correct backend system for the content in the App.

URN schema is required to map content back to the content resource.

<meta name=”urn:adobe:aue:<category>:<referenceName>” content=”<protocol>:<url>”>

<meta name=”urn:adobe:aue:system:aemconnection” content=”aem:https://localhost:4502">

<meta name=”urn:adobe:aue:<category>:<referenceName>” content=”<protocol>:<url>”>

<category> consist

System for connection endpoints

Config for defining optional configurations

<referenceName> — short name to identify the connection E.g. aemconnection

<protocol> Universal Editor Persistence Service to use. E.g. aem

<url> — Ths is the URL to the system where the changes shall be persisted. E.g. <http://localhost:4502>

The identifier urn:adobe:aue:system represents the connection for the Adobe Universal Editor.

itemid=”urn:<referenceName>:<resource>”

● <referenceName> — This is the named reference mentioned in the <meta> tag. E.g. aemconnection

● <resource> — This is a pointer to the resource in the target system. E.g. an AEM content path such as /content/page/jcr:content

<meta name=”urn:adobe:aue:system:<referenceName>” content=”<protocol>:<url>”>

```
<html>  
<head>  
<meta name="urn:adobe:aue:system:aemconnection" content="aem:https://localhost:4502">  
<meta name="urn:adobe:aue:system:fcsconnection" content="fcs:https://example.franklin.adobe.com/345fcdd">  
</head>  
<body>  
<aside>  
<ul itemscope itemid="urn:aemconnection:/content/example/list" itemtype="container">  
<li itemscope itemid="urn:aemconnection/content/example/listitem" itemtype="component">  
<p itemprop="name" itemtype="text">Jane Doe</p>  
<p itemprop="title" itemtype="text">Journalist</p>  
<img itemprop="avatar" src="https://www.adobe.com/content/dam/cc/icons/Adobe_Corporate_Horizontal_Red_HEX.svg" itemtype="image" alt="avatar"/>  
</li>  
…  
<li itemscope itemid="urn:fcsconnection:/documents/mytext" itemtype="component">  
<p itemprop="name" itemtype="text">John Smith</p>  
<p itemid="urn:aemconnection/content/example/another-source" itemprop="title" itemtype="text">Photographer</p>  
<img itemprop="avatar" src="https://www.adobe.com/content/dam/cc/icons/Adobe_Corporate_Horizontal_Red_HEX.svg" itemtype="image" alt="avatar"/>  
</li>  
</ul>  
</aside>  
</body>  
</html>
```

## Configuration Settings

config prefix in your connection URN to set service and extension endpoints if necessary.

If you would like not to use the Universal Editor Service, which is hosted by Adobe, but your own hosted version, you can set this in a meta tag.

To overwrite the default service endpoint that the Universal Editor provides, set your own service endpoint:

Meta name — urn:adobe:aue:config:service

Meta content — content=”https://adobe.com" (example)

<meta name=”urn:adobe:aue:config:service” content=”<url>”>

You can set the extension using the extension tag

If you only want to have certain extensions enabled for a page, you can set this in a meta tag. To fetch extensions, set the extension endpoints:

● Meta name: urn:adobe:aue:config:extensions

● Meta content: content=”https://adobe.com,https://anotherone.com,https://onemore.com" (example)

<meta name=”urn:adobe:aue:config:extensions” content=”<url>,<url>,<url>”>

Authoring content with a universal editor

After instrumenting the app sign into the universal editor, using Adobe ID.

After you are signed in, enter the URL of the page you want to edit in the [location bar](https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/universal-editor/authoring.html?lang=en#location-bar).

NOTE:- The Universal Editor is still in development. It currently cannot edit all content types. More you can find here <https://experienceleague.adobe.com/docs/experience-manager-cloud-service/content/universal-editor/getting-started.html?lang=en>
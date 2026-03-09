---
title: "AEM with NextJS spa component rendering"
url: https://medium.com/p/c8d788e3eb2e
---

# AEM with NextJS spa component rendering

[Original](https://medium.com/p/c8d788e3eb2e)

# AEM with NextJS spa component rendering

[![Jayant Kumar](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*XTLBC57m-qVkuXIz)](/@jaykrs?source=post_page---byline--c8d788e3eb2e---------------------------------------)

[Jayant Kumar](/@jaykrs?source=post_page---byline--c8d788e3eb2e---------------------------------------)

4 min read

·

Apr 3, 2024

--

Listen

Share

More

AEM (Adobe Experience Manager) is a comprehensive content management solution offered by Adobe. It allows users to create, manage, and deliver digital experiences across various channels such as web, mobile, and IoT devices. AEM primarily deals with managing content, assets, digital forms, and personalization features to deliver rich and engaging experiences to users.

Next.js is a popular React framework for building server-side rendered (SSR) React applications. It provides tools and features to simplify the process of building React applications with server-side rendering capabilities, enabling better performance, SEO, and faster initial page loads.

When integrating AEM with Next.js for single page application (SPA) rendering, you typically leverage AEM as a headless CMS (Content Management System) to manage your content and Next.js to render the SPA. Here’s how the integration might work:

1. **Content Management in AEM**: Content authors use the AEM interface to create and manage content. This can include web pages, images, videos, text, and other digital assets.

2. **Content Delivery via APIs**: AEM provides APIs (such as RESTful/Graph APIs) to deliver content to client applications. These APIs allow Next.js to fetch content from AEM and render it within the SPA.

3. **Integration with Next.js**: In your Next.js application, you would integrate logic to fetch content from AEM using APIs provided by AEM. This can be done using libraries like `aem-headless-client-js` , `aem-react-editable-components`, `a`em-spa-page-model-manager`provided by adobe in JavaScript.

4. **Server-side Rendering** : Next.js allows you to implement server-side rendering (SSR) or static site generation (SSG). With SSR, the server pre-renders the React components before sending them to the client, resulting in faster initial page loads and better SEO.

5. **Dynamic Content Rendering**: As users navigate through the SPA, Next.js can fetch additional content from AEM dynamically based on user interactions. This allows for a seamless and interactive user experience while still leveraging AEM’s content management capabilities.

6. **SEO Optimization**: By using server-side rendering, the initial HTML content delivered to search engine crawlers contains meaningful content, improving SEO compared to traditional client-side rendered SPAs.

Overall, integrating AEM with Next.js for SPA rendering allows you to leverage the content management capabilities of AEM while benefiting from the performance and SEO advantages of server-side rendering provided by Next.js. This approach can result in faster, more engaging, and SEO-friendly web experiences.

Now lets deep dive how we can achieve this

create an aem project via cmd prompt with admin mode

```
mvn -B org.apache.maven.plugins:maven-archetype-plugin:3.2.1:generate -D archetypeGroupId=com.adobe.aem -D archetypeArtifactId=aem-project-archetype -D archetypeVersion=41 -D aemVersion=6.5.17 -D appTitle="Remote App" -D appId="remote-app" -D groupId="com.adobe.aem.guides.remoteapp" -D frontendModule="decoupled"
```

We need to setup template to support spa component rendering for that we need to update page content.xml under \remote-app\ui.content\src\main\content\jcr\_root\content\remote-app\us\en\home

```
<?xml version="1.0" encoding="UTF-8"?>  
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0" xmlns:cq="http://www.day.com/jcr/cq/1.0" xmlns:jcr="http://www.jcp.org/jcr/1.0" xmlns:nt="http://www.jcp.org/jcr/nt/1.0"  
          jcr:primaryType="cq:Page">  
    <jcr:content  
        cq:lastModified="{Date}2018-10-04T09:50:29.650+02:00"  
        cq:lastModifiedBy="admin"  
        cq:template="/conf/remote-app/settings/wcm/templates/spa-next-remote-page"  
        jcr:primaryType="cq:PageContent"  
        jcr:title="Remote App Home Page"  
        sling:resourceType="remote-app/components/remotepagenext">  
        <root  
            jcr:primaryType="nt:unstructured"  
            sling:resourceType="wcm/foundation/components/responsivegrid">  
            <responsivegrid  
                jcr:primaryType="nt:unstructured"  
                sling:resourceType="wcm/foundation/components/responsivegrid">  
                <text  
                    jcr:primaryType="nt:unstructured"  
                    sling:resourceType="remote-app/components/text"  
                    text="&lt;p>Hello World!&lt;/p>"  
                    textIsRich="true">  
                    <cq:responsive jcr:primaryType="nt:unstructured"/>  
                </text>  
            </responsivegrid>  
        </root>  
    </jcr:content>  
</jcr:root>
```

deploy project on aem server

```
mvn clean install -PautoInstallPackage
```

then navigate to page property and under spa set nextjs rendering url , here nextjs will be running on 3000 port

Press enter or click to view image in full size

![]()

Now clone nextjs sample app provided via adobe from <https://github.com/adobe/aem-headless-app-templates> verify env.development or env.production has correct entry

these entry are self explanatory about aem running host and nextjs running host , public site and content path.

```
git clone https://github.com/adobe/aem-headless-app-templates  
cd nextjs-remotespa  
npm install  
npm start  
  
  
NEXT_PUBLIC_AEM_HOST=http://localhost:4502  
NEXT_GRAPHQL_ENDPOINT="/content/_cq_graphql/wknd-shared/endpoint.json"  
NEXT_PUBLIC_URL=http://localhost:3000  
NEXT_PUBLIC_AEM_SITE=remote-app  
NEXT_PUBLIC_AEM_PATH=/content/remote-app/us/en/home  
NEXT_PUBLIC_AEM_ROOT=/content/remote-app/us/en
```

make sure we have correct path in pages/[[…page]].jsx like

const pagePath = `/content/remote-app/us/en/

if all went well navigate <http://localhost:3000/> here page is rendering via nextjs

Press enter or click to view image in full size

![]()

Navigate to AEM and open page in editor , here we can author and update page but content rendering is picked from nextjs.

Press enter or click to view image in full size

![]()

Hope you enjoyed AEM with NextJs rendering , very soon will move on with writing custom component.

Can find github reference here <https://github.com/jaykrs/aem-nextjs-remote>
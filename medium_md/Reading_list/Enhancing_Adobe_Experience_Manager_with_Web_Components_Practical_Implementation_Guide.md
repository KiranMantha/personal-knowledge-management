---
title: "Enhancing Adobe Experience Manager with Web Components: Practical Implementation Guide"
url: https://medium.com/p/e5569164d0ec
---

# Enhancing Adobe Experience Manager with Web Components: Practical Implementation Guide

[Original](https://medium.com/p/e5569164d0ec)

# Enhancing Adobe Experience Manager with Web Components: Practical Implementation Guide

[![Sumeer](https://miro.medium.com/v2/resize:fill:64:64/0*_tryQGy2DNN7j_NA.jpg)](/?source=post_page---byline--e5569164d0ec---------------------------------------)

[Sumeer](/?source=post_page---byline--e5569164d0ec---------------------------------------)

2 min read

·

Apr 9, 2024

--

[Listen](https://medium.com/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3De5569164d0ec&operation=register&redirect=https%3A%2F%2Fsumeerbasha.medium.com%2Fenhancing-adobe-experience-manager-with-web-components-practical-implementation-guide-e5569164d0ec&source=---header_actions--e5569164d0ec---------------------post_audio_button------------------)

Share

Integrating Web Components into Adobe Experience Manager (AEM) can significantly enhance the flexibility and efficiency of your web development projects. Here, we provide a practical example with code snippets to show how you can implement a custom Web Component in AEM and utilize it within your AEM pages.

## **Creating a Custom Web Component**

First, let’s create a simple Web Component. We’ll develop a user profile card that displays a user’s name, a brief description, and a profile picture. This component will be built using the Custom Elements API and Shadow DOM for encapsulation.

**Step 1: Define the Web Component**

Here’s the JavaScript code to define a custom Web Component:

```
class UserProfile extends HTMLElement {  
    constructor() {  
        super();  
        const shadow = this.attachShadow({mode: 'open'});  
  
        const style = document.createElement('style');  
        style.textContent = `  
            .profile-card {  
                font-family: Arial, sans-serif;  
                background: #f0f0f0;  
                border: 1px solid #ccc;  
                padding: 10px;  
                width: 200px;  
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);  
            }  
            .profile-image img {  
                width: 100%;  
                height: auto;  
            }  
        `;  
  
        const container = document.createElement('div');  
        container.className = 'profile-card';  
  
        const imageDiv = document.createElement('div');  
        imageDiv.className = 'profile-image';  
        const img = document.createElement('img');  
        img.src = this.getAttribute('image');  
        imageDiv.appendChild(img);  
  
        const name = document.createElement('h2');  
        name.textContent = this.getAttribute('name');  
  
        const description = document.createElement('p');  
        description.textContent = this.getAttribute('description');  
  
        container.appendChild(imageDiv);  
        container.appendChild(name);  
        container.appendChild(description);  
  
        shadow.appendChild(style);  
        shadow.appendChild(container);  
    }  
}  
  
window.customElements.define('user-profile', UserProfile);
```

This code snippet creates a `UserProfile` class that extends `HTMLElement`. It uses the Shadow DOM to encapsulate the style and markup, preventing styles from leaking and ensuring the component’s independence from the rest of the page’s CSS.

**Step 2: Include the Component in AEM**

To use this Web Component within AEM, you need to ensure the JavaScript is loaded into the appropriate client library category associated with your AEM site’s pages. This involves creating a clientlib (client library) with the following structure:

```
/ui.apps/src/main/content/jcr_root/apps/myproject/clientlibs/user-profile  
    /css  
    /js  
        - user-profile.js  
    /resources  
    .content.xml  
    js.txt
```

.context.xml

```
<?xml version="1.0" encoding="UTF-8"?>  
<jcr:root xmlns:jcr="http://www.jcp.org/jcr/1.0"  
    jcr:primaryType="cq:ClientLibraryFolder"  
    categories="[myproject.components]"  
    jsProcessor="[default:none,min:gcc]"  
    allowProxy="{Boolean}true"/>
```

**Step 3: Create an AEM Component to Use the Web Component**

Next, create an AEM component that will use this Web Component. This component could include a dialog for authors to input the user name, description, and image URL.

/apps/myproject/components/content/userprofile/.content.xml

```
<?xml version="1.0" encoding="UTF-8"?>  
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0" xmlns:cq="http://www.day.com/jcr/cq/1.0"  
    jcr:primaryType="cq:Component"  
    jcr:title="User Profile"  
    sling:resourceSuperType="core/wcm/components/container/v1/container"  
    componentGroup="My Project"/>
```

dialog.xml

```
<?xml version="1.0" encoding="UTF-8"?>  
<jcr:root xmlns:jcr="http://www.jcp.org/jcr/1.0"  
          xmlns:nt="http://www.jcp.org/jcr/nt/1.0"  
          xmlns:cq="http://www.day.com/jcr/cq/1.0"  
          xmlns:sling="http://sling.apache.org/jcr/sling/1.0"  
          jcr:primaryType="cq:Dialog"  
          title="User Profile Settings"  
          helpPath="en/cq/current/wcm/default_components.html#Text">  
    <items jcr:primaryType="cq:WidgetCollection">  
        <name  
            jcr:primaryType="cq:Widget"  
            fieldLabel="Name"  
            name="./name"  
            allowBlank="false"  
            xtype="textfield"  
            fieldDescription="Enter the name for the user profile."/>  
        <description  
            jcr:primaryType="cq:Widget"  
            fieldLabel="Description"  
            name="./description"  
            xtype="textarea"  
            fieldDescription="Enter a short description for the user profile."/>  
        <image  
            jcr:primaryType="cq:Widget"  
            fieldLabel="Image URL"  
            name="./image"  
            xtype="pathfield"  
            rootPath="/content/dam"  
            fieldDescription="Path to the profile image."/>  
    </items>  
</jcr:root>
```

HTML File (userprofile.html) in the same directory:

```
<sly data-sly-use.clientlib="/libs/granite/sightly/templates/clientlib.html"  
     data-sly-call="${clientlib.all @ categories='myproject.components'}"></sly>  
<user-profile name="${properties.name}" description="${properties.description}" image="${properties.image}"></user-profile>
```

**Conclusion**

With these steps, you have successfully created and integrated a Web Component into AEM. This allows for the development of highly reusable, encapsulated, and efficient web components that can be seamlessly integrated into AEM’s powerful digital experience platform. The use of Web Components in AEM bridges the gap between modern web development practices and enterprise content management, enabling the delivery of cutting-edge user experiences.
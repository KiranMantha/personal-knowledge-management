---
title: "AEM 6.5 Model Annotations"
url: https://medium.com/p/a9493b6e1b28
---

# AEM 6.5 Model Annotations

[Original](https://medium.com/p/a9493b6e1b28)

Member-only story

# AEM 6.5 Model Annotations

[![Mircea Gabriel Dumitrescu](https://miro.medium.com/v2/resize:fill:64:64/1*TW-JpYR1nk7ciXTnm9yAmA.png)](/@mirceagab?source=post_page---byline--a9493b6e1b28---------------------------------------)

[Mircea Gabriel Dumitrescu](/@mirceagab?source=post_page---byline--a9493b6e1b28---------------------------------------)

10 min read

·

Aug 21, 2023

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

Adobe Experience Manager (AEM) 6.5 supports various annotations for use in Java models. These annotations are used to inject values, adapt resources, and perform other operations on Sling Models. Below are some of the commonly used annotations in AEM 6.5 for Sling Models:

[@Model](http://twitter.com/Model): Used to specify that a class is a Sling Model.

```
@Model(adaptables = Resource.class)
```

[@Inject](http://twitter.com/Inject): Used for injecting properties from the resource or its ancestors.

```
@Inject  
private String title;
```

[@Named](http://twitter.com/Named): Used in conjunction with [@Inject](http://twitter.com/Inject) to specify the property name if it’s different from the field name.

```
@Inject @Named("jcr:title")  
private String title;
```

[@Optional](http://twitter.com/Optional): Specifies that the injection is optional.

```
@Inject @Optional  
private String subtitle;
```

[@Source](http://twitter.com/Source): Specifies the injector to be used for the injection.

```
@Inject @Source("script-bindings")  
private Page currentPage;
```

[@Default](http://twitter.com/Default): Specifies a default value to use if the injection is unsuccessful.

```
@Inject @Optional @Default(values = "Untitled")  
private String title;
```

[@Via](http://twitter.com/Via): Specifies the intermediary adapter through which to run the adaptables object.

```
@Inject @Via("resource")  
private String title;
```

[@ChildResource](http://twitter.com/ChildResource): Injects a child resource.

```
@ChildResource  
private Resource image;
```

[@SlingObject](http://twitter.com/SlingObject): Injects common sling objects like ResourceResolver, Resource, SlingHttpServletRequest, etc.

```
@SlingObject  
private ResourceResolver resourceResolver;
```

[@Self](http://twitter.com/Self): Injects the adaptable itself.

```
@Self  
private SlingHttpServletRequest request;
```

[@OSGiService](http://twitter.com/OSGiService): Injects an OSGi service.

```
@OSGiService  
private MyService myService;
```

[@PostConstruct](http://twitter.com/PostConstruct): Specifies a method to be called after the object is instantiated and all dependencies are injected.

```
@PostConstruct  
protected void init() {  
  // initialization code  
}
```

[@ValueMapValue](http://twitter.com/ValueMapValue) annotation. This annotation is specifically used for injecting properties from a ValueMap. It works similarly to [@Inject](http://twitter.com/Inject), but it is a bit more expressive in terms of indicating that the value is coming directly from a ValueMap associated with a resource.

```
@Model(adaptables = Resource.class)  
public class MyModel {  
  
  @ValueMapValue  
  private String title;  
  
  @ValueMapValue(name = "jcr:description")  
  private String description;  
  
  @ValueMapValue @Optional  
  private String subtitle;  
  
  @ValueMapValue @Default(values = "N/A")  
  private String missingProperty;  
  
  // ... methods, etc.  
}
```

## Difference between Inject and ValueMapValue, commonly seen in all projects

Both [@ValueMapValue](http://twitter.com/ValueMapValue) and [@Inject](http://twitter.com/Inject) annotations are used for property injection in AEM’s Sling Models, but they serve slightly different purposes and are used in different contexts. Here’s how they differ:

[@ValueMapValue](http://twitter.com/ValueMapValue)  
Explicitness: When you use [@ValueMapValue](http://twitter.com/ValueMapValue), it’s explicit that the value is being obtained directly from a ValueMap associated with a Resource. It’s like saying, “Look up this key in the resource’s properties and inject the corresponding value.”

Limited to Resources: This annotation is primarily intended for use with resources. If you are adapting from a Resource, this is a clear way to denote property injection.

No Injector Specification: With [@ValueMapValue](http://twitter.com/ValueMapValue), you don’t specify an injector ([@Source](http://twitter.com/Source)). It’s assumed that you’re using the ValueMap injector.

Example:

```
@ValueMapValue  
private String title;
```

[@Inject](http://twitter.com/Inject)  
Flexibility: [@Inject](http://twitter.com/Inject) is more general and can be used for a variety of injection types, not just property injection. For example, you can inject OSGi services, request attributes, and other Sling objects.

Broad Applicability: While it can certainly be used to inject properties from a resource’s ValueMap, it’s also used for other types of injection. You can specify which injector to use by adding the [@Source](http://twitter.com/Source) annotation.

Injector Specification: You can specify a different injector by using the [@Source](http://twitter.com/Source) annotation. This is not possible with [@ValueMapValue](http://twitter.com/ValueMapValue).

Example:

```
@Inject  
private String title;  // This could also be from a ValueMap  
  
@Inject @Source("osgi-services")  
private MyService myService;
```

Use [@ValueMapValue](http://twitter.com/ValueMapValue) when you’re explicitly interested in pulling a value from a Resource’s ValueMap.

Use [@Inject](http://twitter.com/Inject) when you need more flexibility, or when you’re injecting something other than a simple property from a Resource.  
Both will work for injecting simple properties, so you’ll sometimes see them used interchangeably in that context. However, the semantic difference can make your code more self-explanatory, aiding in readability and maintainability.

## More about the Source Annotation

The [@Source](http://twitter.com/Source) annotation in AEM’s Sling Models specifies which injector should be used for a given field. In Sling Models, an injector is responsible for providing the actual object that gets injected into a model field. Multiple injectors can be registered within the OSGi framework, and each has its own way of obtaining or creating the objects to be injected.

The [@Source](http://twitter.com/Source) annotation allows you to explicitly choose one of these injectors for a particular injection point (field). By default, Sling Models use a prioritized list of available injectors. If you don’t specify an injector using [@Source](http://twitter.com/Source), the Sling Model will go through this list and use the first injector that can provide a non-null value. When you do specify an injector, only that particular injector is used for that field, bypassing the default order.

Here are some commonly used injectors and how you might specify them with [@Source](http://twitter.com/Source):

Value Map Injector: Injects properties from the resource’s value map.

```
@Inject @Source("valuemap")  
private String title;
```

Sling Object Injector: Injects common Sling objects like ResourceResolver, SlingHttpServletRequest, etc.

```
@Inject @Source("sling-object")  
private ResourceResolver resourceResolver;
```

Script Bindings Injector: Injects objects from the script context, useful in JSPs or HTL.

```
@Inject @Source("script-bindings")  
private Page currentPage;
```

OSGi Service Injector: Injects an OSGi service.

```
@Inject @Source("osgi-services")  
private MyService myService;
```

Request Attribute Injector: Injects an attribute from the current HTTP request.

```
@Inject @Source("request-attribute")  
private String attribute;
```

Custom Injector: If you write a custom injector, you can specify its name here.

```
@Inject @Source("my-custom-injector")  
private CustomObject customObject;
```

By specifying the source, you are making the injection more precise and easier to understand. You are explicitly indicating which injector should be responsible for populating that field, which can make your code more self-explanatory and potentially easier to debug.

Keep in mind that the actual availability of these injectors can depend on your specific setup and any custom configurations or extensions you may have added to your AEM instance.

## What are these Injectors?

In the context of Adobe Experience Manager (AEM) and Apache Sling, an injector is a component responsible for populating the fields of a Sling Model class with actual values. Essentially, it acts as a bridge that pulls data from various sources and places it into the object’s fields during the instantiation of the Sling Model. Injectors can fetch data from a variety of sources like Sling resources, OSGi services, request parameters, and more.

Here’s a simplified breakdown of what happens during the injection process:

**Identification**: When a Sling Model is adapted from a resource, Sling identifies the fields that need to be populated.

**Injector Lookup**: Sling looks for available injectors that can handle each field. Multiple injectors can be available, and they are usually checked in a certain order of precedence unless you specify a particular injector using the [@Source](http://twitter.com/Source) annotation.

**Data Retrieval**: Once an appropriate injector is found, it fetches the necessary data from the source it is designed to interact with (e.g., ValueMap for resource properties, OSGi services, HTTP request, etc.).

**Field Population**: Finally, the retrieved data is populated into the Sling Model’s field.

Here are a few examples to give you an idea of how different types of injectors work:

**Value Map Injector**  
**Source**: Properties of a Sling resource.  
**Typical Use Case**: Populating fields with content from a JCR node.  
**Example Annotation:** **@Inject or @ValueMapValue**

**Sling Object Injector**  
**Source**: Sling’s own objects like Resource, ResourceResolver, SlingHttpServletRequest, etc.  
**Typical Use Case**: Getting Sling API objects that are not directly content but part of the Sling framework.  
**Example Annotation**: **@SlingObject**

**OSGi Service Injector**  
**Source**: OSGi services registered in the OSGi service registry.  
**Typical Use Case**: Accessing custom or built-in services to perform more complex logic that’s not directly tied to content.  
**Example Annotation**: **@OSGiService**

**Request Attribute Injector**  
**Source**: HTTP request attributes.  
**Typical Use Case**: Obtaining data that has been set elsewhere in the request lifecycle.  
**Example Annotation**: **@RequestAttribute**

**Custom Injectors**  
You can also create custom injectors to handle specific use cases that the built-in injectors don’t cover. These custom injectors implement the **org.apache.sling.models.spi.Injector** interface and are registered as OSGi services.

Understanding injectors helps make sense of how data flows into your Sling Models, allowing you to work more effectively with AEM and Sling.

## What is a SlingObject exactly?

The [@SlingObject](http://twitter.com/SlingObject) annotation in AEM’s Sling Models is used to inject instances of certain key Sling API classes directly into your model class. It’s a convenient way to obtain references to objects like Resource, ResourceResolver, SlingHttpServletRequest, SlingHttpServletResponse, and other foundational Sling objects without having to adapt or create them manually.

When you annotate a field with [@SlingObject](http://twitter.com/SlingObject), the Sling Model framework automatically injects an instance of the specified Sling object, provided that the object is available in the current context.

Here’s a basic example of a Sling Model class using [@SlingObject](http://twitter.com/SlingObject):

```
@Model(adaptables = SlingHttpServletRequest.class)  
public class MyModel {  
  
    @SlingObject  
    private Resource currentResource;  
  
    @SlingObject  
    private ResourceResolver resourceResolver;  
  
    @SlingObject  
    private SlingHttpServletRequest request;  
  
    // ... other fields and methods  
}
```

In this example, the MyModel class is adapted from a SlingHttpServletRequest. It uses [@SlingObject](http://twitter.com/SlingObject) to automatically inject instances of Resource, ResourceResolver, and SlingHttpServletRequest into the fields currentResource, resourceResolver, and request, respectively.

Here’s what each object generally represents:

Resource: Represents a resource in the Sling resource tree, often mapped to a node in the JCR (Java Content Repository).

ResourceResolver: Provides methods to resolve a resource based on a given path or URI and to traverse the resource tree. It’s often used to find, create, or delete resources.

SlingHttpServletRequest: Represents the HTTP request object with additional methods to work with Sling resources. Extends the standard javax.servlet.http.HttpServletRequest.

The [@SlingObject](http://twitter.com/SlingObject) annotation makes it easier to work with these foundational objects, allowing you to focus on your business logic instead of boilerplate code to obtain them.

## A more in depth example

Let’s consider a real-life scenario where we’re building a component to display an article on an AEM site. The component would need details like the article title, author, publish date, and the article content itself.

The Sling Model for this component might look like this:

```
import org.apache.sling.api.resource.Resource;  
import org.apache.sling.api.resource.ResourceResolver;  
import org.apache.sling.api.SlingHttpServletRequest;  
import org.apache.sling.models.annotations.Default;  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.Optional;  
import org.apache.sling.models.annotations.injectorspecific.SlingObject;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
  
import javax.annotation.PostConstruct;  
  
@Model(adaptables = SlingHttpServletRequest.class)  
public class ArticleModel {  
  
    // Injecting foundational Sling objects  
    @SlingObject  
    private Resource currentResource;  
  
    @SlingObject  
    private ResourceResolver resourceResolver;  
  
    @SlingObject  
    private SlingHttpServletRequest request;  
  
    // Injecting properties from the component's resource  
    @ValueMapValue  
    private String articleTitle;  
  
    @ValueMapValue  
    @Optional  
    @Default(values = "Anonymous")  
    private String author;  
  
    @ValueMapValue  
    private String publishDate;  
  
    @ValueMapValue  
    private String articleContent;  
  
    private String imageFullPath;  
  
    // Post-construct method to perform additional logic after all injections are complete  
    @PostConstruct  
    protected void init() {  
        // Assume 'imagePath' is a relative path stored in the JCR node  
        String imagePath = currentResource.getValueMap().get("imagePath", String.class);  
        if (imagePath != null) {  
            // Generate the full path of the image using ResourceResolver  
            imageFullPath = resourceResolver.map(request, imagePath);  
        }  
    }  
  
    // Getters  
    public String getArticleTitle() {  
        return articleTitle;  
    }  
  
    public String getAuthor() {  
        return author;  
    }  
  
    public String getPublishDate() {  
        return publishDate;  
    }  
  
    public String getArticleContent() {  
        return articleContent;  
    }  
  
    public String getImageFullPath() {  
        return imageFullPath;  
    }  
  
    // Optional: Setters, though usually not required for read-only models  
}
```

In this example:

The model is adapted from SlingHttpServletRequest, which is commonly available in component rendering contexts.

I’ve used [@SlingObject](http://twitter.com/SlingObject) to inject instances of Resource, ResourceResolver, and SlingHttpServletRequest.

I’ve used [@ValueMapValue](http://twitter.com/ValueMapValue) to inject properties like articleTitle, author, publishDate, and articleContent from the JCR node that represents this component.

The [@PostConstruct](http://twitter.com/PostConstruct) annotated init() method performs additional logic after all injections are complete. Here, it’s used to generate the full path for an image based on a relative path.

I’ve provided getter methods for all the fields we want to access in the template (HTL, JSP, etc.).

This is a fairly typical use-case for a Sling Model in AEM, bringing together different types of injections and post-construction logic to represent a real-world component.

## ResourceResolver and SlingHttpServletRequest

In the context of Adobe Experience Manager (AEM) and Apache Sling, both ResourceResolver and SlingHttpServletRequest are foundational classes that offer different functionalities. Let’s dive deeper into each:

## ResourceResolver

The ResourceResolver is one of the core concepts in Sling/AEM. It’s essentially a mapping service between resource URLs and actual resources (often JCR nodes). Here’s why you might need it:

Functionality:  
1. **Resource Resolution**: Convert a URL or path into a Resource object that allows you to read or manipulate a node in the JCR.

2. **Adaptation**: Use it to adapt a Resource to another object, such as a Sling Model.

3. **Query Execution**: Run queries to search for resources.

4. **Resource Creation/Modification/Deletion**: Programmatically create, modify, or delete resources in the repository.

Typical Use Cases:  
- To fetch additional resources that are related to the current resource but not directly accessible.  
- To map resource paths, converting them to URL-friendly paths.  
- To execute queries to find resources that meet specific criteria.

Example Usage in Code:

```
Resource pageResource = resourceResolver.getResource("/content/my-site/en/home");  
Page page = pageResource.adaptTo(Page.class);
```

## SlingHttpServletRequest

The SlingHttpServletRequest class extends the standard Servlet API’s HttpServletRequest and adds functionalities specific to Sling.

Functionality:  
1. **Resource Association**: Unlike the standard servlet request, a SlingHttpServletRequest is always associated with a Resource. This resource is what the request is “targeting.”

2. **Script Resolution**: Information in the request is used by Sling to resolve which script (JSP, HTL, etc.) should be used to respond to the request.

3. **Access to Sling API**: Provides methods to easily access other Sling-related objects like ResourceResolver, SlingScript, SlingSession, etc.

Typical Use Cases:  
- When you need to access query parameters, request headers, or other HTTP-specific information.  
- When you need the resource associated with the current request.  
- When you need to find out about the current Sling processing context (current resource, selectors, suffix, etc.)

Example Usage in Code:

```
String selectorString = request.getRequestPathInfo().getSelectorString();  
Resource requestResource = request.getResource();
```

In the example Sling Model you saw earlier, ResourceResolver was used to convert a relative image path into a full path that could be used in the website’s HTML. The SlingHttpServletRequest was injected primarily to provide the context for this path conversion but could also be used for additional functionalities like accessing query parameters or headers if needed.

Both ResourceResolver and SlingHttpServletRequest are central to developing with AEM and Sling, each facilitating different kinds of operations that you’ll likely encounter regularly.

There’s much more to cover regarding these topics, but this is a good start. Good luck nerds !
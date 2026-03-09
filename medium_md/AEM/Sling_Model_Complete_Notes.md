---
title: "Sling Model Complete Notes"
url: https://medium.com/p/ccafdb171841
---

# Sling Model Complete Notes

[Original](https://medium.com/p/ccafdb171841)

# Sling Model Complete Notes

[![Naveen Rapelly](https://miro.medium.com/v2/resize:fill:64:64/1*pl3seb56A4zWFeEwnyiuzw.jpeg)](/@naveenrapelly8?source=post_page---byline--ccafdb171841---------------------------------------)

[Naveen Rapelly](/@naveenrapelly8?source=post_page---byline--ccafdb171841---------------------------------------)

12 min read

·

Mar 23, 2025

--

Listen

Share

More

Press enter or click to view image in full size

![]()

## What is the Sling Model?

* The sling Model is the restful framework created inside the AEM Architecture, which is used to map requests or resource objects.
* A Sling Model is implemented as an OSGi bundle.

## Features of Sling Models

* **Annotations-Driven**: It utilizes annotations like @Model, @Inject, and @ValueMapValue to streamline the mapping of properties in AEM components.
* **Built-in Dependency Injection**: Enables automatic injection of properties, services, and objects from the Sling context, simplifying the code
* **Versatile Adaptability**: Designed to work with a variety of adaptable objects, including Resource and SlingHttpServletRequest, to suit diverse use cases.
* **Modular Structure**: Encourages a clear separation of concerns, keeping content retrieval and business logic distinct from the component’s HTL view.

## Sling Model WorkFlow

Press enter or click to view image in full size

![]()

* You have authored a component in this page — [http://localhost:4502/content/aem-debugcode/us/en/test-page.html?wcmmode=disabl](http://localhost:4502/content/aem-debugcode/us/en/test-page.html?wcmmode=disabled)ed
* When this URL is accessed, AEM resolves it by checking the underlying CRX/DE path — /content/aem-debugcode/us/en/test-page/jcr:content/root/container/customcomponent
* AEM will check the sling:resourceType property of the custom component node to determine the corresponding component.

Press enter or click to view image in full size

![]()

* This property points to a path under /apps — /apps/aem-debugcode/components/custom-component
* Inside the resolved component folder, AEM looks for the HTL/Sightly file (e.g., customComponent.html) for renderin
* The HTL script references a Sling Model class using the data-sly-use attribute

```
<sly data-sly-use.customComponent="com.debug.code.core.models.CustomComponent">
```

* AEM binds this HTL file to the Sling Model (CustomComponent class) specified by the fully qualified Java class name (com.debug.code.core.models.CustomComponent)
* The referenced Sling Model class is instantiated and its methods are executed to provide data or logic for the HTL script.
* The returned data is then rendered as part of the final HTML output

## How Many Ways We Can Adapt the Sling Model?

we can adapt the sling model in two ways.

* Resource.class
* SlingHttpServletRequest

### Syntax

```
@Model(adaptables = {Resource.class, SlingHttpServletRequest.class}, adapters = {Button.class}, resourceType = {ButtonImpl.RESOURCE_TYPE}, defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)  
public class ButtonImpl extend Button{  
    // logic  
}
```

## Let’s Understand Common Annotation

### @Model Annotation

* This annotation defines the class as a Sling Model and must be present at the top of the class.

### adaptables.

* The adaptables attribute defines the types of objects from which a model can be adapted. There are two primary types

**Resource.class**

* Represents the data stored within the JCR (Java Content Repository). When content is treated as a resource, you can use Resource.class to adapt it and access its properties or child resources effectively.

**SlingHttpServletRequest**

* Useful when you need to access HTTP request-specific information, such as parameters, headers, or session attributes. Additionally, it allows access to WCM-specific objects like currentPage and current-design to support more dynamic use cases

### adapter

* The adapters attribute specifies the interface(s) or class(es) that this model will be adapted to.

### resourceType

* The resource type attribute specifies the resource types that this model supports.

### defaultInjectionStrategy

* The defaultInjectionStrategy attribute determines how Sling Models handle injection when a value is missing. There are two types of injection strategies
* **DefaultInjectionStrategy.OPTIONAL** If a value is unavailable for injection, it will simply be set to null instead of throwing an error.
* **DefaultInjectionStrategy.REQUIRED** Ensures that all required values are available for injection. If a value is missing, an error will be thrown

```
@Model(  
    adaptables = Resource.class,  
    adapters = CustomComponent.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)
```

## What is Annotation in the Sling Model?

Annotations in Sling Models are a way to map AEM content properties, resources, or services to Java objects. They make it easier to access and use content stored in the repository within your Java code

## Types of Annotations

## @Inject

The @Inject annotation is a generic annotation used to inject properties or objects from various contexts in Sling Models.

It does not enforce type safety for the injected dependencies, making it more flexible but less strict.

By default, fields annotated with @Inject are optional. If a value is unavailable, the field will be null unless explicitly marked as required.

This annotation is primarily used for dependency injection in Sling Models.

```
@Inject  
private String firstName;
```

## @ValueMapValue

The @ValueMapValue annotation is used to inject properties directly from a resource, making it ideal for mapping resource properties to model fields.

It supports default values, so if a property is missing in the ValueMap, the model field can still receive a default value.

If needed, the annotation automatically converts the resource property to the appropriate field type.

It provides type safety by allowing you to specify the exact type of the Java field being mapped to the JCR property.

```
@ValueMapValue  
private String firstName;
```

Press enter or click to view image in full size

![]()

## @Named

The @Named annotation is particularly useful when the field name in the model doesn’t match the property name in the source, or when you need to inject a specific value from a multi-field or a map.

For instance, if you want to fetch a property like jcr:lastModifiedBy from the JCR repository for a specific component, you can use the @Named annotation to map the property name to your model field.

* Here’s how you can use the @Named annotation

```
@ValueMapValue  
@Named("jcr:lastModifiedBy")  
private String createdBy;
```

## @default

The @Default annotation specifies a default value to be used if the injection of a property is unsuccessful.

By using a default value, you can avoid issues like NullPointerExceptions when a property is missing.

* Here’s an example of how to use the @Default annotation:

```
@ValueMapValue  
@Default(values = "Default Title Field") // Provides a default value for the title field  
private String titleField;
```

```
@ValueMapValue  
@Default(intValues = 0) // Provides a default value of 0 for the count field  
private int count;
```

## @Self

The @Self annotation in Sling Models allows you to inject the adaptable object itself directly into the model. This is helpful when you need to interact with the original resource, request, or any other adaptable object that the model is based on.

By using @Self, you gain direct access to the adaptable object, enabling you to perform additional operations or retrieve properties that may not be directly mapped to the model fields

* Here’s an example of how to use the @Self annotation

```
@Self  
private Resource resource; // Inject the adaptable object itself
```

In this example, the @Self annotation injects the Resource object into the resource field, giving the model direct access to the resource for further operations or property retrievals.

**Example 1**: Accessing the HTTP request

```
@Model(adaptables = SlingHttpServletRequest.class)  
public class RequestModel {
```

```
    @Self  
    private SlingHttpServletRequest request;    public String getRequestPath() {  
        return request.getRequestURI();  
    }  
}
```

**Example 2**: Working with a resource

```
@Model(adaptables = Resource.class)  
public class CustomModel {
```

```
    @Self  
    private Resource resource;    public boolean hasChildNodes() {  
        return resource.hasChildren();  
    }  
}
```

## @Via

The @Via annotation allows you to specify an alternative method or path to access a value. This is useful when the value you’re looking for is not directly available on the adaptable but can be accessed through another resource or object.

The @Via annotation defines an intermediary adapter that enables the model to access values via a different object or resource

**Common Use Cases for @Via**

* (Accessing a Child Resource: When the desired value is located in a child resource instead of the current resource.
* Accessing a Parent Resource: When the value can be found in a parent resource.
* Different Model: When the value is part of a different Sling Model or object.

By using @Via, you can enhance the flexibility of Sling Models and access values that may not be directly available on the adaptable object

Here’s how you can use the @Via annotation

```
JCR Structure-------------------------------------------------
```

```
/content/myproject/jcr:content  
  + myComponent  
    + buttondetails  
      - titleField: "Hello"  
      - descriptionField: "This is a descriptionField."
```

```
@Model(  
    adaptables = Resource.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class MyComponentModel {
```

```
    @ValueMapValue  
    @Via("buttondetails") // Specifies that the value should be taken from the "buttondetails" child resource  
    private String titleField;    @ValueMapValue  
    @Via("buttondetails")  
    private String descriptionField;}
```

* Here’s how you can use the @Via annotation

```
@Model(  
    adaptables = Resource.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class ParentModel {
```

```
    @ValueMapValue  
    private String titleField;    public String getTitleField() {  
        return titleField;  
    }  
}@Model(  
    adaptables = Resource.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class ChildModel {    @Self  
    @Via("parentResource") // Accessing the ParentModel through the parentResource  
    private ParentModel parentModel;    public String getTitleFromParent() {  
        return parentModel.getTitleField();  
    }  
}
```

## @PostConstruct

The @PostConstruct annotation is used to mark a method in a Sling Model that should run after the model’s dependencies are injected and the model is fully initialized.

A method annotated with @PostConstruct must have a void return type and take no arguments.

This method is typically used for any setup or initialization tasks that need to happen after the model is created.

* Here’s how you can use the @PostConstruct annotation

```
@Model(  
    adaptables = Resource.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class CustomModel {
```

```
    @ValueMapValue  
    private String titleField;    @ValueMapValue  
    private String descriptionField;    @PostConstruct  
    protected void init() {  
        if (titleField == null || titleField.isEmpty()) {  
            titleField = "Default Title Field";  
        }  
        if (descriptionField == null || descriptionField.isEmpty()) {  
            descriptionField = "Default DescriptionField";  
        }  
    }    public String getTitleField() {  
        return titleField;  
    }    public String getDescriptionField() {  
        return descriptionField;  
    }  
}
```

* This init method checks if titleField and descriptionField are null or empty, and if so, assign default values.

## @OSGiService

The @OSGiService annotation is used to inject OSGi services directly into a Sling Model. This allows you to easily access and use OSGi services within your model.

* Here’s how you can use the @OSGiService annotation

```
@Model(adaptables = SlingHttpServletRequest.class,  
        defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL )  
public class CustomConfigurationModelImpl {  
      
    @OSGiService  
    CustomConfigurationMethods customConfigurationMethods;
```

```
    public String getFirstName() {  
        return customConfigurationMethods.getFirstName();  
    }  
    public int getLastName() {  
        return customConfigurationMethods.getLastName();  
    }  
}
```

## @SlingObject

The @SlingObject annotation is used to inject common Sling objects directly into a Sling Model, providing easy access to key Sling components.

Global Objects with @SlingObject

* Resource: Represents the resource being adopted.
* ResourceResolver: Provides methods to resolve resources.
* SlingHttpServletRequest: Represents the current HTTP request.
* SlingHttpServletResponse: Represents the current HTTP response.
* SlingScriptHelper: This Provides access to various scripting utilities and services.

Here’s how you can use the @SlingObject annotation

```
@SlingObject  
private Resource resource; // Injects the current Resource
```

```
@SlingObject  
private ResourceResolver resourceResolver; // Injects the ResourceResolver@SlingObject  
private SlingScriptHelper scriptHelper; // Injects the SlingScriptHelper
```

## @ScriptVariable

* The @ScriptVariable annotation in AEM is used in Sling Models to inject values from the script context, such as the current page, resource, request, and other context-specific objects.

**Common Objects Injected with @ScriptVariable:**

* Page: Represents the current page.
* Resource: Represents the current resource.
* SlingHttpServletRequest: Represents the current HTTP request.
* SlingHttpServletResponse: Represents the current HTTP response.
* ValueMap: Represents the properties of the current resource.
* SlingScriptHelper: Provides access to various AEM services.
* ResourceResolver: Provides access to resources within the JCR.
* Here’s how you can use the @ScriptVariable annotation

```
@Model(  
    adaptables = Resource.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class CustomModel {
```

```
    @ValueMapValue  
    private String titleField;    @ScriptVariable  
    private Page currentPage;    @ScriptVariable  
    private Resource resource;    @ScriptVariable  
    private ResourceResolver resourceResolver;    @ScriptVariable  
    private SlingScriptHelper sling;    public String getTitleField() {  
        return titleField;  
    }    public Page getCurrentPage() {  
        return currentPage;  
    }    public Resource getResource() {  
        return resource;  
    }    public ResourceResolver getResourceResolver() {  
        return resourceResolver;  
    }    public SlingScriptHelper getSling() {  
        return sling;  
    }  
}
```

## @ChildResource

The @ChildResource annotation allows you to directly inject a child resource of the current resource into the model.

You can specify a path relative to the current resource to identify the child resource, making it easy to work with nested resources.

The annotation can be used to inject either a single child resource or collections of resources (e.g., lists of resources).

Here’s how you can use the @ChildResource annotation

```
JCR Structure-------------------------------------------------
```

```
/content/myProject/jcr:content  
  + myComponent  
    - titleField: "Title"  
    + detailsField  
      - subtitleField: "Sub TitleField"  
      - description: "Detailed description."  
    + items  
      + item1  
        - name: "Item 1"  
      + item2  
        - name: "Item 2"
```

```
@Model(  
    adaptables = Resource.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class CustomModel {
```

```
    @ValueMapValue  
    private String titleField;    @ChildResource(name = "detailsField")  
    private Resource detailsField; // Injects the 'detailsField' child resource    @ChildResource(name = "items")  
    private List<Resource> items; // Injects the 'items' child resources    public String getTitleField() {  
        return titleField;  
    }    public String getSubtitleField() {  
        return detailsField != null ? detailsField.getValueMap().get("subtitleField", String.class) : null;  
    }    public String getDescription() {  
        return detailsField != null ? detailsField.getValueMap().get("description", String.class) : null;  
    }    public List<Resource> getItems() {  
        return items;  
    }    public String getItemName(int index) {  
        if (items != null && items.size() > index) {  
            return items.get(index).getValueMap().get("name", String.class);  
        }  
        return null;  
    }  
}
```

@ChildResource(name = “detailsField”): Injects the detailsField child resource.

@ChildResource(name = “items”): Injects a list of child resources from the items node

## @ResourcePath

The @ResourcePath annotation is used to inject a resource based on a specified path.

This is especially useful when you need to work with resources that are not part of the current request or resource tree, allowing you to inject resources from any location within the JCR repository.

* Here’s how you can use the @ResourcePath annotation

```
JCR Structure-------------------------------------------------
```

```
/content/myProject  
  + jcr:content  
    - titleField: "Main Content"  
  + referencedContent  
    - titleField: "Referenced Content"
```

```
@Model(  
    adaptables = Resource.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class CustomModel {
```

```
    @ValueMapValue  
    private String titleField;    @ResourcePath(path = "/content/myProject/referencedContent")  
    private Resource referencedResource; // Injects the resource at the specified path    public String getTitleField() {  
        return titleField;  
    }    public String getReferencedTitle() {  
        if (referencedResource != null) {  
            ValueMap valueMap = referencedResource.getValueMap();  
            return valueMap.get("titleField", String.class);  
        }  
        return null;  
    }  
}
```

## @RequestAttribute

The @RequestAttribute annotation allows you to access request attributes directly within your model. Request attributes are data passed along with the HTTP request, and this annotation is particularly useful when you need to process or use data that is dynamically provided during the request.

Step 1: Set Up the Request Attribute

* In your servlet or any other part of your code that handles the request, you can set the request attribute
* Here’s how you can use the @RequestAttribute annotation

```
request.setAttribute("myAttribute", "This is a request attribute");
```

```
@Model(  
    adaptables = SlingHttpServletRequest.class,  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class CustomModel {
```

```
    @RequestAttribute(name = "myAttribute")  
    private String myAttribute; // Injects the request attribute    public String getMyAttribute() {  
        return myAttribute;  
    }  
}
```

## @Designate

Used for OSGi component configuration in Sling Models.

## @Activate

Used to define when an OSGi component should be activated.

## Best Practices for Writing Sling Models in AEM

> ***Note :*** *Avoid Using Both Resource and SlingHttpServletRequest Together as Adaptables in a Sling Model*

Ambiguity in Adaptation

* When a Sling Model specifies both Resource and SlingHttpServletRequest as adaptables, the framework may struggle to determine the context, leading to potential issues
* If the model is adapted from a Resource, it will look for properties within the resource.
* If adapted from SlingHttpServletRequest, it will pull in attributes, request parameters, or other injected values associated with the HTTP request.

```
@Model(adaptables = {Resource.class, SlingHttpServletRequest.class})  
public class Button {
```

```
    @ValueMapValue  
    private String property;  
}
```

* Having these two adaptables can result in inconsistent behavior, as the context for instantiating the model may not be clear.

Separation of Concerns

* **Resource**: Primarily used for accessing and working with content stored in the JCR repository, making it the best choice when you need to work with properties or children of resources.
* **SlingHttpServletRequest**: Represents the HTTP request context, providing access to request-specific data like parameters, attributes, and objects like currentPage and currentDesign.

Combining these in a single model can create confusion because it merges the content layer (JCR) with the request layer (HTTP), making it harder to maintain a clean separation of concerns.

Testing Challenges

* When both adaptables are used, unit testing becomes more complex, as you need to mock both the Resource and SlingHttpServletRequest contexts. This adds extra overhead and potential for test failures.

## Best Approach for Practices

Choose the Right Adaptable for Your Model

Use Resource When

* Your model is focused on content stored in the JCR.
* You only need to access properties or children of a resource.

```
@Model(adaptables = Resource.class)  
public class Button {  
    @ValueMapValue  
    private String title;  
}
```

Use SlingHttpServletRequest When

* Your model depends on request-specific data, such as parameters, request attributes, or objects like currentPage and currentResource.

```
@Model(adaptables = SlingHttpServletRequest.class)  
public class Button {  
@Inject  
    private Page currentPage;  
    @Inject  
    private String parameter;  
}
```

## How to Handle Both Scenarios?

* If you need to work with both Resource and SlingHttpServletRequest data, it’s a good practice to adapt your model from the SlingHttpServletRequest and retrieve the Resource within the model itself. This way, you avoid the complications of dual adaptables.

```
@Model(adaptables = SlingHttpServletRequest.class)  
public class Button {  
@Inject  
    private Resource resource;  
    @Inject  
    private String requestParam;  
    public String getTitle() {  
        return resource.getValueMap().get("title", String.class);  
    }  
    public String getRequestParam() {  
        return requestParam;  
    }  
}
```

* In this example, the resource is injected from the SlingHttpServletRequest, avoiding the complexity of adapting from multiple sources.

## Prefer Specific Annotations Over @Inject

* Although @Inject is a general-purpose annotation that can inject properties or objects from various contexts, using more specific annotations like @ValueMapValue, @ChildResource, @ScriptVariable, or @OSGiService is recommended. These annotations improve clarity, maintainability, and debugging.

## Benefits of Using Specific Annotations

* **@ValueMapValue:** Makes it clear that the property is coming from the ValueMap of the resource.
* **@OSGiService:** This indicates that the value is being injected from the OSGi service registry.

The upcoming blog will explore more about how to create a component with a sling model with real-time examples and details.

Every great discussion starts with a simple thought! If you enjoyed this article, found it useful, or have any questions, let’s talk! I’d love to hear from you.

For more updates, tips, and engaging conversations, connect with me on [**Medium**](/@naveenrapelly8), [**LinkedIn**](https://www.linkedin.com/in/naveen-rapelly/), **and** [**RealCodeWorks**](https://www.realcodeworks.com/)Let’s keep learning together! 🚀✨

Thank you 🙏 !
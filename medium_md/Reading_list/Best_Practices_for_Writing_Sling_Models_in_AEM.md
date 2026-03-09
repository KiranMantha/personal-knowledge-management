---
title: "Best Practices for Writing Sling Models in AEM"
url: https://medium.com/p/c6ff16a0fd00
---

# Best Practices for Writing Sling Models in AEM

[Original](https://medium.com/p/c6ff16a0fd00)

# Best Practices for Writing Sling Models in AEM

[![Uma Charan Gorai](https://miro.medium.com/v2/resize:fill:64:64/1*5GZRyf14G1p_APDxw8I5qQ.jpeg)](/@ucgorai?source=post_page---byline--c6ff16a0fd00---------------------------------------)

[Uma Charan Gorai](/@ucgorai?source=post_page---byline--c6ff16a0fd00---------------------------------------)

18 min read

·

Dec 1, 2024

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

A Sling Model in Adobe Experience Manager (AEM) is a framework that simplifies the development of business logic for components by enabling developers to map Java objects to JCR (Java Content Repository) nodes. It uses annotations and dependency injection to make it easier to retrieve and work with content in AEM.

Sling Models are often used to encapsulate the logic for AEM components, making the code modular, reusable, and easier to test.

## Key Features of Sling Models:

1. **Annotations-based Configuration**: Uses annotations like `@Model`, `@Inject`, `@ValueMapValue`, etc., to map properties.
2. **Dependency Injection**: Automatically injects properties, services, or objects from the Sling context.
3. **Flexibility**: Works with different adaptable objects such as `Resource` and `SlingHttpServletRequest`.
4. **Modularity**: Separates content retrieval and business logic from the component view (HTL).

## Best Practices for Writing Sling Models in AEM

> **Avoid Using Both** `Resource` **and** `SlingHttpServletRequest` **Together as Adaptables in a Sling Model**

### 1. Ambiguity in Adaptation

When a Sling Model specifies both `Resource` and `SlingHttpServletRequest` as adaptables, the framework may not have a clear context to determine how the model should be instantiated.

```
@Model(adaptables = {Resource.class, SlingHttpServletRequest.class})  
public class MyModel {  
    @ValueMapValue  
    private String property;  
}
```

* If the model is adapted from a `Resource`, it will look for properties within the `Resource`.
* If adapted from a `SlingHttpServletRequest`, it might look for attributes, request parameters, or other injected values.

This dual behavior can lead to inconsistent results depending on the context in which the model is used.

### 2. Separation of Concerns

* `Resource`: Focuses on representing and accessing content from the JCR repository.
* `SlingHttpServletRequest`: Represents the request context, including request attributes, query parameters, and additional objects like WCM-specific objects (`currentPage`, `currentDesign`, etc.).

By combining them in a single model, you blur the boundary between the content and the request context, making the model harder to understand and maintain.

### 3. Testing Complexity

When both adaptables are used, testing becomes more challenging because you need to mock both `Resource` and `SlingHttpServletRequest` contexts. This increases the complexity of unit testing and may lead to errors during integration testing.

### 4. Performance Considerations

* When adapting from `SlingHttpServletRequest`, the framework internally resolves the `Resource` from the request.
* If both are specified, the framework might perform additional overhead to handle the dual adaptable scenario, which could impact performance in large-scale deployments.

***Best Practice: Use One Adaptable per Model***

Choose the adaptable based on the specific requirements of your component or use case:

1. Use `Resource` When:

* The model is tightly coupled to content stored in the JCR.
* You only need to access properties and children of the resource.
* Example:

```
@Model(adaptables = Resource.class)  
public class ContentModel {  
    @ValueMapValue  
    private String title;  
}
```

2. Use `SlingHttpServletRequest` When:

* The model depends on request-specific data such as parameters, attributes, or context objects (e.g., `currentPage`, `currentResource`).
* Example:

```
@Model(adaptables = SlingHttpServletRequest.class)  
public class RequestModel {  
    @Inject  
    private Page currentPage;  
  
    @Inject  
    private String parameter;  
}
```

***How to Handle Both Scenarios?***

If your component requires access to both `Resource` and `SlingHttpServletRequest` data, you can adapt the model using `SlingHttpServletRequest` and internally retrieve the `Resource` as needed.

Example:

```
@Model(adaptables = SlingHttpServletRequest.class)  
public class CombinedModel {  
  
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

The `resource` field is injected from the `SlingHttpServletRequest`, avoiding the need for dual adaptables.

> **Use Specific Annotations Instead of** `@Inject` **in AEM Sling Models**

In AEM Sling Models, `@Inject` is a generic annotation that can inject properties or objects from various contexts. However, using more specific annotations like `@ValueMapValue`, `@ChildResource`, `@ScriptVariable`, or `@OSGiService` is preferred for clarity, maintainability, and debugging ease.

**Advantages of Using Specific Annotations**

### 1. Improved Readability and Clarity

**1.1** Specific annotations clearly indicate the source of the injected value. For example:

* `@ValueMapValue`: Indicates that the property comes from the `ValueMap` of the resource.
* `@OSGiService`: Shows the value is being injected from the OSGi service registry.

**1.2** Developers can understand the context and behavior of the code at a glance without additional investigation.

```
@ValueMapValue  
private String title;
```

This makes it clear that `title` is a property of the resource.

**Less Clear Example**:

```
@Inject  
private String title;
```

Here, it’s unclear whether `title` comes from the `ValueMap`, a request attribute, or another source.

### 2. Avoids Ambiguity in Injection

* `@Inject` can lead to unexpected results because it tries to resolve the value from various sources (ValueMap, request attributes, OSGi services, etc.).
* Specific annotations ensure that the value is injected from the intended source.

```
@Inject  
private String title;
```

* This might work when adapting from a `Resource` because it maps to a `ValueMap` property.
* However, when adapting from `SlingHttpServletRequest`, it might fail or inject unexpected data.

### 3. Better Debugging and Error Handling

3.1 Specific annotations provide more helpful error messages if injection fails.

For example:

* `@ValueMapValue` will indicate that the property was not found in the `ValueMap`.
* `@OSGiService` will point out that the OSGi service is missing or unavailable.

### 4. Future Proofing

* Using specific annotations ensures that your code is robust against changes in Sling Models’ default injection behavior or underlying implementation.

> **Avoiding Code Duplication in AEM Sling Models Using Abstract Classes**

When developing components in AEM, there are often common properties or functionality shared across multiple Sling Models. To avoid code duplication and promote reusability, you can use **abstract classes** in Sling Models to centralize shared logic.

**Why Use Abstract Classes in Sling Models**

* **Eliminate Redundant Code**: Shared fields, methods, and logic can be abstracted into a base class.
* **Promote DRY Principle**: (Don’t Repeat Yourself) Abstract classes ensure reusability of code across multiple models.
* **Maintain Consistency**: Shared logic remains centralized, making updates easier.
* **Enhanced Testing**: Abstract classes simplify testing by isolating common logic.

## Example Scenario: Shared Fields Across Models

Suppose you have two components:

* **Hero Component**: Displays a title, description, and an image.
* **Banner Component**: Displays a title, subtitle, and an image.

Both components share common fields like `title` and `imagePath`. Instead of duplicating these fields and their getter methods in both Sling Models, you can move them to an abstract class.

### Implementation

### Step 1: Create an Abstract Class

The abstract class will hold the common properties and their getter methods.

```
package com.example.core.models;  
  
import org.apache.sling.models.annotations.DefaultInjectionStrategy;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
  
public abstract class AbstractComponentModel {  
  
    @ValueMapValue  
    private String title;  
  
    @ValueMapValue  
    private String imagePath;  
  
    // Getter methods for common properties  
    public String getTitle() {  
        return title != null ? title : "Default Title";  
    }  
  
    public String getImagePath() {  
        return imagePath != null ? imagePath : "/content/dam/default.jpg";  
    }  
}
```

### Step 2: Extend the Abstract Class in Sling Models

Hero Model:

```
package com.example.core.models;  
  
import org.apache.sling.api.resource.Resource;  
import org.apache.sling.models.annotations.DefaultInjectionStrategy;  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
  
@Model(  
    adaptables = Resource.class,  
    resourceType = "example/components/hero",  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class HeroModel extends AbstractComponentModel {  
  
    @ValueMapValue  
    private String description;  
  
    // Getter for description  
    public String getDescription() {  
        return description != null ? description : "Default Description";  
    }  
}
```

Banner Model:

```
package com.example.core.models;  
  
import org.apache.sling.api.resource.Resource;  
import org.apache.sling.models.annotations.DefaultInjectionStrategy;  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
  
@Model(  
    adaptables = Resource.class,  
    resourceType = "example/components/banner",  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class BannerModel extends AbstractComponentModel {  
  
    @ValueMapValue  
    private String subtitle;  
  
    // Getter for subtitle  
    public String getSubtitle() {  
        return subtitle != null ? subtitle : "Default Subtitle";  
    }  
}
```

## Benefits of Using Abstract Classes in This Example

1. **Avoids Code Duplication**:

* Fields `title` and `imagePath` along with their getter methods are declared only once in the abstract class.

**2. Centralized Maintenance**:

* If the logic for `title` or `imagePath` changes (e.g., default values), it only needs to be updated in the abstract class.

**3. Improved Readability**:

* Each component-specific Sling Model focuses only on fields and logic unique to that component, making the code easier to read.

**4. Testing Simplified**:

* Tests for common functionality (`title` and `imagePath`) can be written once for the abstract class.

> **Recommended Practices Around** `@PostConstruct` **in AEM Sling Models**

The `@PostConstruct` annotation in Sling Models is used to define a method that initializes the model after all injections are complete. It is an important feature that allows for setting up derived or computed properties, performing validations, or initializing values that depend on multiple injected fields.

Here are the **recommended practices** for using `@PostConstruct` in AEM Sling Models, with a detailed explanation and example.

### 1. Purpose of `@PostConstruct`

**1.1** Use the `@PostConstruct` method to handle:

* Derived or computed properties based on injected values.
* Default values when injected properties are null.
* Validations or transformations of injected data.
* Initialization of complex objects that require logic after injections.

### 2. Keep the Method Simple

* Avoid placing complex business logic in the `@PostConstruct` method. It should focus on initializing fields required by the model.
* Delegate any heavy or reusable logic to service classes or helper methods.

### 3. Ensure Idempotence

* The `@PostConstruct` method should not cause side effects (e.g., modifying external systems or saving data).
* It should be safe to call multiple times without causing inconsistent behavior.

### 4. Avoid Over-Reliance on `@PostConstruct`

* Prefer injecting default values or using annotations like `@Default` where possible, instead of using `@PostConstruct` for simple default initialization.

**Instead of this**:

```
@PostConstruct  
protected void init() {  
    if (title == null) {  
        title = "Default Title";  
    }  
}
```

**Do this**:

```
@ValueMapValue  
@Default(values = "Default Title")  
private String title;
```

### 5. Handle Null Checks Gracefully

* Use the `@PostConstruct` method to ensure null safety for dependent logic, such as derived fields.

### 6. Log Initialization Issues

* Add logging within the `@PostConstruct` method to capture unexpected scenarios, such as missing required fields.

```
@PostConstruct  
protected void init() {  
    if (title == null) {  
        log.warn("Title is missing in the resource: {}", resource.getPath());  
    }  
}
```

### 7. Avoid Resource-Intensive Operations

* Avoid performing expensive operations like database calls, HTTP requests, or extensive data processing in the `@PostConstruct` method.

Instead, delegate these operations to an OSGi service or perform them lazily when required.

> **Sling Model Instantiation: Prefer** `modelFactory` **Over** `adaptTo()`

In AEM development, Sling Models can be instantiated using two main approaches:

1. **Using** `adaptTo()`:

* Commonly used to adapt a `Resource` or `SlingHttpServletRequest` to a Sling Model.

**2. Using** `ModelFactory`:

* A more robust and preferred method to create Sling Model instances, especially in complex use cases.

**Why Prefer** `ModelFactory` **Over** `adaptTo()`

### 1. Error Handling and Debugging

* `adaptTo()` returns `null` if the model cannot be adapted, with no indication of the cause.
* `ModelFactory` provides a more structured way to handle instantiation failures and better error messages.

### 2. Support for Advanced Use Cases

* `ModelFactory` allows for specifying custom options or custom adaptables, which `adaptTo()` does not support.

### 3. Programmatic Control

* You can create Sling Model instances programmatically with more flexibility using `ModelFactory`.

### 4. Consistent Behavior Across Contexts

* `ModelFactory` ensures consistent results, whereas `adaptTo()` behavior may vary depending on the adaptable object (e.g., `Resource` vs. `SlingHttpServletRequest`).

### Example: Using `ModelFactory` vs. `adaptTo()`

### Scenario:

You want to instantiate a model for a “Hero” component, ensuring proper error handling and supporting both `Resource` and `SlingHttpServletRequest`.

**Using** `adaptTo()` **(Traditional Approach)**

```
package com.example.core.services;  
  
import com.example.core.models.HeroModel;  
import org.apache.sling.api.resource.Resource;  
import org.apache.sling.api.scripting.SlingHttpServletRequest;  
import org.slf4j.Logger;  
import org.slf4j.LoggerFactory;  
  
public class HeroService {  
  
    private static final Logger log = LoggerFactory.getLogger(HeroService.class);  
  
    public HeroModel getHeroModel(Resource resource) {  
        if (resource == null) {  
            log.warn("Resource is null");  
            return null;  
        }  
  
        HeroModel heroModel = resource.adaptTo(HeroModel.class);  
        if (heroModel == null) {  
            log.warn("Could not adapt resource to HeroModel: {}", resource.getPath());  
        }  
  
        return heroModel;  
    }  
  
    public HeroModel getHeroModel(SlingHttpServletRequest request) {  
        if (request == null) {  
            log.warn("Request is null");  
            return null;  
        }  
  
        HeroModel heroModel = request.adaptTo(HeroModel.class);  
        if (heroModel == null) {  
            log.warn("Could not adapt request to HeroModel");  
        }  
  
        return heroModel;  
    }  
}
```

**Drawbacks**:

1. No detailed error reporting for failed adaptation.
2. The behavior of `adaptTo()` might vary depending on the adaptable type.

**Using** `ModelFactory` **(Preferred Approach)**

```
package com.example.core.services;  
  
import com.example.core.models.HeroModel;  
import org.apache.sling.api.resource.Resource;  
import org.apache.sling.models.factory.ModelFactory;  
import org.osgi.service.component.annotations.Component;  
import org.osgi.service.component.annotations.Reference;  
import org.slf4j.Logger;  
import org.slf4j.LoggerFactory;  
  
@Component(service = HeroService.class)  
public class HeroService {  
  
    private static final Logger log = LoggerFactory.getLogger(HeroService.class);  
  
    @Reference  
    private ModelFactory modelFactory;  
  
    public HeroModel getHeroModel(Resource resource) {  
        if (resource == null) {  
            log.warn("Resource is null");  
            return null;  
        }  
  
        if (!modelFactory.canCreateFromAdaptable(resource, HeroModel.class)) {  
            log.warn("Resource cannot be adapted to HeroModel: {}", resource.getPath());  
            return null;  
        }  
  
        try {  
            return modelFactory.createModel(resource, HeroModel.class);  
        } catch (Exception e) {  
            log.error("Error creating HeroModel from resource: {}", resource.getPath(), e);  
            return null;  
        }  
    }  
}
```

### Key Features of `ModelFactory` in the Example

### 1. Validation with `canCreateFromAdaptable`

* Ensures the resource can be adapted to the desired model before attempting to create it.

### 2. Exception Handling

* Catches and logs exceptions if the model creation fails.

### 3. Support for Multiple Adaptables

* The same approach works for `SlingHttpServletRequest` or other adaptables.

> **Optimize AEM Development with Core Components**

The point “Optimize AEM Development with Core Components” is highly relevant to **AEM Sling Models** for the following reasons:

### 1. Streamlined Component Development

* AEM Core Components provide pre-built, highly customizable, and extensible components that follow best practices for modern web development.
* When used with Sling Models, developers can quickly bind backend logic to these components by defining model classes annotated with `@Model`. This approach enhances maintainability and scalability while reducing boilerplate code.

### 2. Consistent and Reusable Business Logic

* Sling Models allow developers to encapsulate business logic for AEM components in Java classes, and Core Components provide a standardized structure for such logic.
* For example, when extending a Core Component (like `Teaser` or `Image`), Sling Models can be used to add or override specific features, ensuring code remains modular and reusable across projects.

### 3. Improved Performance and Optimization

* Core Components are optimized for performance and are frequently updated by Adobe to align with industry standards.
* Using Sling Models to interact with Core Components allows developers to handle data efficiently through annotations like `@Inject` or `@Optional`, ensuring optimized retrieval of content from JCR (Java Content Repository).

### 4. Ease of Frontend Integration

* Core Components support HTL (HTML Template Language), making it easier to bind data from Sling Models into front-end templates.
* Developers can map complex backend data models directly to the UI using Sling Models, ensuring a clean separation of concerns between the data layer and presentation layer.

### 5. Accelerated Development Cycles

* Leveraging Core Components reduces the need to create components from scratch, enabling developers to focus on enhancing functionality using Sling Models.
* Sling Models simplify integration by allowing dependency injection and resource mapping, leading to faster development and debugging processes.

> **Use Lombok when extending Core Components via delegation**

**“Use Lombok when extending Core Components via delegation”** is highly applicable for AEM Sling Model development, particularly when you’re enhancing or extending Core Components using delegation. Lombok is a Java library that can significantly simplify and streamline the development process, making your code more maintainable and readable. Here’s how this point relates to AEM Sling Model development, with an explanation of its benefits and practical applications:

### 1. Reduction of Boilerplate Code

* **Core Components** often need to be extended with custom models that add new functionality or delegate certain responsibilities. Writing such models manually can lead to repetitive code, especially when you need getter and setter methods, constructors, or `toString()` methods.
* **Lombok** can automatically generate these methods with annotations such as `@Getter`, `@Setter`, `@AllArgsConstructor`, `@NoArgsConstructor`, and `@ToString`. This makes the code cleaner, easier to read, and less prone to human error.

```
import lombok.Getter;  
import lombok.Setter;  
import lombok.ToString;  
import javax.annotation.PostConstruct;  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
import org.apache.sling.models.factory.ModelFactory;  
import org.osgi.service.component.annotations.Component;  
import org.osgi.service.component.annotations.Reference;  
  
@Model(adaptables = Resource.class, resourceType = "example/components/content/customtext")  
@Getter @Setter @ToString  
public class CustomTextModel {  
  
    @ValueMapValue  
    private String title;  
  
    @ValueMapValue  
    private String description;  
  
    private String formattedText;  
  
    @PostConstruct  
    protected void init() {  
        // Logic for delegating to a core component and setting formattedText  
        formattedText = (title != null) ? title.toUpperCase() : "Default Text";  
    }  
}
```

**Benefits**:

* The `@Getter`, `@Setter`, and `@ToString` annotations generate boilerplate methods automatically, keeping the model concise and focused on business logic.

### 2. Simplified Delegation Logic

* When extending a Core Component via delegation, you might need to delegate some responsibilities to the core model while adding or modifying specific properties.
* Lombok simplifies this process by generating standard code patterns, making it easier to focus on the actual delegation logic.

```
import lombok.Getter;  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
import com.adobe.cq.wcm.core.components.models.Text;  
  
@Model(adaptables = Resource.class, adapters = CustomTextModel.class, resourceType = "example/components/content/customtext")  
@Getter  
public class CustomTextModel implements Text {  
  
    @ValueMapValue  
    private String title;  
  
    @ValueMapValue  
    private String description;  
  
    @Override  
    public String getText() {  
        // Delegating to the core component's text method while adding custom logic  
        return (title != null) ? title : "Default Text";  
    }  
}
```

**Benefits**:

* Reduces the need to manually write getters and setters, letting you focus on implementing unique logic.
* Enhances readability by maintaining a clean, minimalistic code structure.

### 3. Improved Readability and Maintainability

* **Core Component Extensions** can often become complex, involving a mixture of injected values, custom methods, and delegation to existing Core Component methods.
* Lombok keeps the code base readable by automatically generating the necessary method stubs, reducing the visual clutter and making it easier for developers to follow the logic.

### 4. Avoiding Common Pitfalls

* Manually writing boilerplate code (like getters and setters) can lead to mistakes, such as accidentally omitting a method or introducing typos. Lombok minimizes such errors by generating the code at compile-time, ensuring consistency.
* In AEM development, this is particularly important when creating custom Sling Models that interact with various components and properties, as you can focus on enhancing functionality without getting bogged down by repetitive code.

### Practical Application in AEM Development:

### Scenario:

You are extending the `Text` Core Component to add additional properties such as `subtitle` and delegate core methods.

```
import lombok.Getter;  
import lombok.Setter;  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
import com.adobe.cq.wcm.core.components.models.Text;  
  
@Model(adaptables = Resource.class, adapters = CustomTextModel.class, resourceType = "example/components/content/customtext")  
@Getter @Setter  
public class CustomTextModel implements Text {  
  
    @ValueMapValue  
    private String title;  
  
    @ValueMapValue  
    private String subtitle;  
  
    @Override  
    public String getText() {  
        // Custom logic to extend the core component's text  
        return (title != null) ? title + " - " + subtitle : "Default Title";  
    }  
}
```

### How This Optimizes AEM Sling Model Development:

1. **Reduced Boilerplate**: Lombok’s annotations save development time by automatically generating code for common patterns.
2. **More Maintainable Code**: Clean and readable models that are easier to maintain and extend.
3. **Focus on Business Logic**: Allows developers to concentrate on extending functionality rather than writing repetitive code.
4. **Standardized Patterns**: Ensures that common structures, like `getters`, `setters`, and `toString()`, are consistently implemented.

> **Prefer @Optional over defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL**

In AEM development, when creating **Sling Models**, you often need to inject properties or services. AEM provides two ways to handle optional injections:

1. **Using the** `@Optional` **annotation**.
2. **Using** `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL`.

Both are valid, but **preferring** `@Optional` over `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL` can lead to more readable and flexible code. Here’s why:

**What Are These Options?**

### 1. `@Optional` Annotation

* The `@Optional` annotation can be applied to individual injection points (e.g., `@ValueMapValue` or `@Inject`). It tells AEM that this particular field or property is optional, meaning that if the value isn't present, it should not cause an error or throw an exception.
* It provides fine-grained control, allowing you to specify optional behavior for each injection point.

### 2. `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL`

* This is a class-level annotation that sets the default injection strategy for all injection points within the model. If a field or property is not explicitly marked as optional, it will default to being optional according to this strategy.

### Why Prefer `@Optional`?

1. **Fine-Grained Control**:

* `@Optional` allows you to decide which fields or properties should be treated as optional, rather than applying a global default to all injections. This ensures that you have control over the optional behavior of each specific injection, making the code more precise and readable.
* **Example**: You might want some properties to be optional while others are mandatory. Using `@Optional` on specific properties achieves this, while `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL` makes all properties optional by default.

**2. Enhanced Readability**:

* Code that explicitly marks properties with `@Optional` is more readable and self-explanatory, making it clearer which fields can be `null` or not. This improves maintainability and makes it easier for other developers to understand the code.

```
@Model(adaptables = Resource.class)  
public class CustomModel {  
  
    @ValueMapValue  
    private String requiredField; // This field is mandatory by default.  
  
    @ValueMapValue  
    @Optional  
    private String optionalField; // This field is marked as optional.  
}
```

**3. Avoiding Unintended Consequences**:

* Applying `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL` to an entire class means that all injection points are treated as optional by default. This may not be what you want, as it could lead to situations where critical fields that should be mandatory end up being treated as optional, potentially leading to `null` pointer exceptions or unexpected behavior.

**4. Explicit Over Implicit**:

* Using `@Optional` makes the optionality explicit. Developers can quickly scan the code and see which fields are optional, which is better for code clarity and avoids assumptions about the model's behavior.

**When to Use** `@Optional` **vs.** `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL`**:**

* **Use** `@Optional` when you need fine-grained control over specific injection points and want to make the optionality explicit for each field.
* **Use** `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL` if you want to apply the optionality to all injection points within the model and don't need to specify it for individual fields.

**Example: Applying** `@Optional`

```
package com.example.core.models;  
  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
import org.apache.sling.models.annotations.DefaultInjectionStrategy;  
import javax.annotation.PostConstruct;  
  
@Model(adaptables = Resource.class, defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)  
public class SampleModel {  
  
    @ValueMapValue  
    private String mandatoryField; // This field is mandatory by default.  
  
    @ValueMapValue  
    @Optional  
    private String optionalField; // Explicitly marked as optional.  
  
    @PostConstruct  
    protected void init() {  
        // Logic for initialization  
    }  
  
    public String getMandatoryField() {  
        return mandatoryField;  
    }  
  
    public String getOptionalField() {  
        return optionalField;  
    }  
}
```

### Best Practices:

* **Use** `@Optional` on fields that are not always present or are optional to improve code readability and maintainability.
* **Avoid** `defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL` unless you are confident that all properties in your Sling Model should be treated as optional, as it can lead to unintended consequences and make it harder to track mandatory vs. optional fields.

### Benefits of Using `@Optional`:

1. **Improved Clarity**: Code readers immediately know which fields can be `null`.
2. **Flexible Injection Strategy**: You can decide on a case-by-case basis which fields should be optional.
3. **Better Error Handling**: By marking specific fields as optional, you can handle `null` cases more precisely and avoid unexpected behavior.

> **Make Sling Models Secure**

Making **Sling Models secure** in Adobe Experience Manager (AEM) is essential to prevent vulnerabilities and ensure that the data and logic exposed by the models are protected. This involves implementing best practices to secure both the model’s code and the resources it interacts with. Here’s how you can make your Sling Models more secure:

### 1. Use Proper Access Controls

* **Access Control Lists (ACLs)**: Ensure that sensitive resources and data are protected by appropriate ACLs. Verify that only authorized users or service accounts have access to certain models or resources.
* **Granular Permissions**: Implement role-based access controls (RBAC) to manage who can view or edit content at the resource level.

### 2. Validate and Sanitize Input

* **Input Validation**: Always validate user inputs to prevent injection attacks and ensure that only expected data formats are accepted.
* **Sanitization**: When displaying user-generated content, ensure that you sanitize it to avoid XSS (Cross-Site Scripting) vulnerabilities.

### 3. Avoid Exposing Sensitive Data

* **Hide Sensitive Properties**: Make sure that your Sling Model does not expose sensitive data fields unless necessary. Use appropriate access control annotations to prevent certain properties from being accessible.
* **Sensitive Information**: Ensure that sensitive data, such as credentials or tokens, are not hard-coded into the Sling Model or exposed in HTTP responses.

### 4. Use @PostConstruct Carefully

* **Secure Initialization**: When using `@PostConstruct`, make sure the initialization logic does not expose or process sensitive data unnecessarily.
* **Error Handling**: Implement proper error handling within `@PostConstruct` methods to prevent unexpected data leakage or crashes.

### 5. Apply Secure Coding Practices

* **Avoid Hardcoding**: Never hard-code sensitive information (e.g., credentials or API keys) into Sling Models.
* **Use @Optional and Safe Injection**: When injecting values or dependencies, use `@Optional` or make sure fields are not exposed to null-pointer exceptions to avoid potential information leaks.
* **Avoid** `adaptTo()` **with Untrusted Data**: When adapting resources, ensure that you validate and sanitize data sources to avoid potential security risks.

### 6. Use Proper Model Adaptables

* **Secure Adaptation**: Only adapt resources or request objects that you trust and need. Do not use adaptables that could expose sensitive data or lead to unintended side effects.

### 7. Limit the Scope of @Model Annotations

* **Scoped Adaptables**: Apply the `@Model` annotation with the minimal set of adaptables required to avoid potential security risks from exposing more data than necessary.
* **Restrict Resource Types**: When defining the `resourceType` in your `@Model` annotation, ensure that it only matches trusted and necessary components.

### 8. Secure Use of Services and References

* **Reference Services Carefully**: When using `@Reference` for injecting services, ensure that only trusted services are injected, and use proper configurations to restrict access to the injected services.
* **Service Access Control**: Use AEM’s security policies to ensure that only authorized users and processes can access specific OSGi services.

### 9. Follow Secure Development Practices

* **Regular Code Reviews**: Conduct code reviews to spot potential security issues early. Peer reviews help catch vulnerabilities and enforce best practices.
* **Penetration Testing**: Regularly perform penetration tests on your AEM instance and custom Sling Models to detect vulnerabilities.
* **Update Dependencies**: Regularly update third-party libraries and dependencies used in your AEM project to ensure there are no known vulnerabilities.

### 10. Secure Data Handling in Sling Models

* **Data Encryption**: Encrypt sensitive data at rest and during transmission. Use AEM’s built-in features for encryption when necessary.
* **Avoid Excessive Data Exposure**: Do not expose all properties or methods in a Sling Model. Implement visibility controls so that only necessary data is exposed to the front end.

### 11. Secure HTL (HTML Template Language) Integration

* **Use HTL for Data Binding**: When rendering data in HTL templates, use AEM’s built-in data-binding capabilities to prevent XSS.
* **Escaping Data**: Always escape output in HTL templates to prevent data injection attacks.

**Example of a Secure Sling Model:**

```
package com.example.core.models;  
  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.DefaultInjectionStrategy;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
import javax.annotation.PostConstruct;  
import org.slf4j.Logger;  
import org.slf4j.LoggerFactory;  
  
@Model(  
    adaptables = Resource.class,  
    resourceType = "example/components/content/securetext",  
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
public class SecureTextModel {  
  
    private static final Logger LOG = LoggerFactory.getLogger(SecureTextModel.class);  
  
    @ValueMapValue  
    private String title;  
  
    @ValueMapValue  
    private String sensitiveData; // Example of sensitive data that should be handled securely.  
  
    @PostConstruct  
    protected void init() {  
        // Validate and sanitize input, log non-sensitive information for troubleshooting.  
        if (title != null && title.length() > 100) {  
            LOG.warn("Title length exceeds recommended limit.");  
        }  
  
        // Ensure sensitive data is not processed or exposed inadvertently.  
        if (sensitiveData != null) {  
            // Sanitize or mask sensitive data before use.  
            sensitiveData = "*****"; // Example of masking data.  
        }  
    }  
  
    public String getTitle() {  
        return title;  
    }  
  
    public String getSensitiveData() {  
        // Do not expose sensitive data directly; add controls as necessary.  
        return null;  
    }  
}
```

**Conclusion**

By adopting these best practices and strategies, you can create **Sling Models** that are not only optimized for performance but are also secure and maintainable. Whether it’s through using **Lombok** for concise code, employing proper annotations like `@Optional`, or ensuring secure data handling and input validation, following these guidelines will lead to more robust and secure AEM applications. Always prioritize security, keep up with updates, and maintain clear and readable code to ensure the long-term success of your projects.

[## Understanding AEM Annotations for Efficient Development

### In Adobe Experience Manager (AEM), annotations are metadata markers used to provide additional context or behavior for…

medium.com](/@ucgorai/understanding-aem-annotations-for-efficient-development-dc3aa92ecade?source=post_page-----c6ff16a0fd00---------------------------------------)
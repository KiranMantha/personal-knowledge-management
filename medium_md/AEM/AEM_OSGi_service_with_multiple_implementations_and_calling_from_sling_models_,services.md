---
title: "AEM: OSGi service with multiple implementations and calling from sling models ,services"
url: https://medium.com/p/8ed7e3ecfa92
---

# AEM: OSGi service with multiple implementations and calling from sling models ,services

[Original](https://medium.com/p/8ed7e3ecfa92)

Member-only story

# AEM: OSGi service with multiple implementations and calling from sling models ,services

[![Shankar Angadi](https://miro.medium.com/v2/resize:fill:64:64/0*-1pQrVD3TD58V6lb.jpg)](/@angadi.saa?source=post_page---byline--8ed7e3ecfa92---------------------------------------)

[Shankar Angadi](/@angadi.saa?source=post_page---byline--8ed7e3ecfa92---------------------------------------)

3 min read

·

Jun 14, 2024

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

**Creating OSGI service**

Non members can access from this [link](/@angadi.saa/aem-osgi-service-with-multiple-implementations-and-calling-from-sling-models-services-8ed7e3ecfa92?sk=a23c8986b400cec74238c86eac8a9fcb)

To create an OSGi service in AEM and manage its configuration efficiently, you can use the `@Designate` and `@ObjectClassDefinition` **(OCD)** annotations. These annotations provide a standardized way to define and manage service configurations.

**Defining the Configuration Class**

You can define the **Object Class Definition (OCD)** in a separate configuration class or within the service implementation class. The **@ObjectClassDefinition** annotation is used to declare the configuration properties.

**Linking Configuration to the OSGi Component**

Use the **@Designate** annotation to link the configuration class to the OSGi component. This tells the OSGi framework to apply the configuration defined

## Explanation

1. **@ObjectClassDefinition**: This annotation defines the configuration class (`MyServiceConfig`), which contains the configuration properties. This class provides a clear structure for managing configurations.

2. **@Designate(ocd = MyServiceConfig.class)**: This annotation links the `MyServiceConfig` class to the `MyServiceImpl` component. This tells the OSGi framework to apply the configuration defined in `MyServiceConfig` to the `MyServiceImpl` service.

3. **@Activate and @Modified**: The method annotated with `@Activate` is called when the OSGi component is activated or modified. This method reads the configuration properties and initializes the service accordingly. The `@Modified` annotation ensures that the service can handle dynamic configuration updates.

**OCD in service implementation class**

```
public interface MyService {  
    public String myServiceName();  
}
```

Service implementation class

```
@Designate(ocd= MyServiceImpl.Config.class)  
@Component(service=MyService.class)  
public class MyServiceImpl implements MyService {  
  
    @ObjectClassDefinition(name="A scheduled task",  
            description = "Simple demo for cron-job like task with properties")  
    public static @interface Config {  
  
  
        @AttributeDefinition(name = "demo service ",  
                description = "service name to show")  
        String myServiceName() default "demo service";  
    }  
  
    String myServiceName;  
    @Activate  
    protected void activate(final MyServiceImpl.Config config) {  
  
        myServiceName = config.myServiceName();  
    }  
  
    @Override  
    public String myServiceName() {  
        return myServiceName;  
    }  
}
```

**OCD as separate interface**

```
public interface CustomService {  
  
    public String domain();  
    public String path();  
}  
@ObjectClassDefinition(name = "Example custom Service configs", description = "Example of custom service configs")  
public @interface  CustomServiceConfig {  
    @AttributeDefinition(name = "define domain", description = "define domain for env", type = AttributeType.STRING)  
    String domainName() default  "localhost";  
  
    @AttributeDefinition(name = "define path", description = "define path for env", type = AttributeType.STRING)  
    String path() default  "/content";  
  
}
```

```
@Component(service = CustomService.class, immediate = true, name = "Example custom Service")  
@Designate(ocd = CustomServiceConfig.class)  
public class CustomServiceImpl implements CustomService{  
  
    String domain;  
    String path;  
    @Modified  
    @Activate  
    protected void activate(final CustomServiceConfig customServiceConfig) {  
  
        domain= customServiceConfig.domainName();  
        path= customServiceConfig.path();  
    }  
  
    @Override  
    public String domain() {  
        return domain;  
    }  
  
    @Override  
    public String path() {  
        return path;  
    }  
}
```

## **Calling osgi service from sling model and service**

**Sling model**

```
@OSGiService   
private MyService myService;
```

**Other Service**

```
@Reference   
private MyService myService;
```

## **OSGi service with multiple implementations**

Creating an OSGi service with multiple implementations and calling the respective implementation from a Sling Model or another OSGi service involves leveraging OSGi service properties and references.

In the above **MyService** will have two or more implementations as below and we need to call specific implementation from Sling Model or Service

```
@Component(service = MyService.class, immediate = true)  
public class MyServiceImplA implements MyService{  
    @Override  
    public String myServiceName() {  
        return "service A";  
    }  
}
```

```
@Component(service = MyService.class, immediate = true)  
public class MyServiceImplB implements MyService {  
    @Override  
    public String myServiceName() {  
        return "service B";  
    }  
}
```

**Invoking from sling model**

```
    @OSGiService(filter = "(component.name=com.adobe.aem.core.core.service.MyServiceImplA)")  
    MyService serviceA;  
  
    @OSGiService(filter = "(component.name=com.adobe.aem.core.core.service.MyServiceImplB)")  
    MyService serviceB;
```

Invoking from other Services

```
 @Reference(target = "(component.name=com.adobe.aem.core.saa2023.core.service.MyServiceImplA)")  
    MyService serviceA;  
  
    @Reference(target = "(component.name=com.adobe.aem.core.saa2023.core.service.MyServiceImplB)")  
    MyService serviceB;
```
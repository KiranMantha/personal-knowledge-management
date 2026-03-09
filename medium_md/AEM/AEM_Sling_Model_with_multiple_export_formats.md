---
title: "AEM: Sling Model with multiple export formats"
url: https://medium.com/p/29ba1f6b5051
---

# AEM: Sling Model with multiple export formats

[Original](https://medium.com/p/29ba1f6b5051)

Member-only story

# AEM: Sling Model with multiple export formats

[![Shankar Angadi](https://miro.medium.com/v2/resize:fill:64:64/0*-1pQrVD3TD58V6lb.jpg)](/@angadi.saa?source=post_page---byline--29ba1f6b5051---------------------------------------)

[Shankar Angadi](/@angadi.saa?source=post_page---byline--29ba1f6b5051---------------------------------------)

2 min read

·

Jun 24, 2024

--

10

Listen

Share

More

We can define multiple exporters for a Sling Model by using the `@Exporters` annotation. This is useful when you need to export the same model in different formats, such as **JSON** and **XML**.

Non members can access from this [**link**](/@angadi.saa/aem-sling-model-with-multiple-export-formats-29ba1f6b5051?sk=66351c273d195fd3a4fce08b73ecb4bd)

Create custom exporter as below

```
@Component(service = ModelExporter.class)  
public class CustomExporter implements ModelExporter {  
  
  
    public <T> T export(Object model, Class<T> clazz,  
                        Map<String, String> options)  
            throws org.apache.sling.models.factory.ExportException {  
        StringWriter sw = new StringWriter();  
        try {  
            JAXBContext jaxbContext =  
                    JAXBContext.newInstance(model.getClass());  
            Marshaller marshaller = jaxbContext.createMarshaller();  
            marshaller.marshal(model, sw);  
        } catch (JAXBException e) {  
            e.printStackTrace();  
        }  
        return (T) sw.toString();  
    }  
  
    public String getName() {  
        return "custom";  
    }  
  
    public boolean isSupported(Class Model) {  
        return true;  
    }  
}
```

Create sling model with @ Exporters and mention the required exporter as show below

```
@Model(adaptables = Resource.class, resourceType = {"project-name/components/page"}, defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL)  
@Exporters({  
        @Exporter(name = "jackson",extensions = "json"),  
        @Exporter(name = "custom",extensions = "xml",selector = "test")  
})  
  
@XmlRootElement  
public class ExportTestModel {  
  
  
    @ValueMapValue(name = "jcr:title")  
    private String title;  
    @XmlElement  
    public String getTitle()  
    {  
        return title;  
    }  
}
```

<http://localhost:4502/content/your-project/us/en/jcr:content.model.json>

![]()

<http://localhost:4502/content/your-project/us/en/jcr:content.test.xml>

Press enter or click to view image in full size

![]()
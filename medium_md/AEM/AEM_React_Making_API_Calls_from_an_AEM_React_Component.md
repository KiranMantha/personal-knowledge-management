---
title: "AEM React: Making API Calls from an AEM React Component"
url: https://medium.com/p/e13d1639b245
---

# AEM React: Making API Calls from an AEM React Component

[Original](https://medium.com/p/e13d1639b245)

Member-only story

# AEM React: Making API Calls from an AEM React Component

[![Shankar Angadi](https://miro.medium.com/v2/resize:fill:64:64/0*-1pQrVD3TD58V6lb.jpg)](/@angadi.saa?source=post_page---byline--e13d1639b245---------------------------------------)

[Shankar Angadi](/@angadi.saa?source=post_page---byline--e13d1639b245---------------------------------------)

3 min read

·

Aug 25, 2024

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

To enhance the functionality of an **AEM** React component, we can incorporate **API** calls directly within the component. This allows the component to fetch and display dynamic data, improving the user experience by providing real-time information or content updates.

## Non members can access from this [link](/@angadi.saa/aem-react-making-api-calls-from-an-aem-react-component-e13d1639b245?sk=27af73a9bbb23bbf05b4f08e3cb84024)

Create randomnumbercomponent in aem with respect to your project with some input which will display random number generated from API

```
Dialog  
<?xml version="1.0" encoding="UTF-8"?>  
<jcr:root xmlns:sling="http://sling.apache.org/jcr/sling/1.0" xmlns:granite="http://www.adobe.com/jcr/granite/1.0" xmlns:cq="http://www.day.com/jcr/cq/1.0" xmlns:jcr="http://www.jcp.org/jcr/1.0" xmlns:nt="http://www.jcp.org/jcr/nt/1.0"  
    jcr:primaryType="nt:unstructured"  
    jcr:title="RandomNumberComponent"  
    sling:resourceType="cq/gui/components/authoring/dialog"  
    helpPath="https://www.adobe.com/go/aem_cmp_navigation_v2"  
    >  
    <content  
            jcr:primaryType="nt:unstructured"  
            sling:resourceType="granite/ui/components/coral/foundation/fixedcolumns">  
        <items jcr:primaryType="nt:unstructured">  
            <column  
                    jcr:primaryType="nt:unstructured"  
                    sling:resourceType="granite/ui/components/coral/foundation/container">  
                <items jcr:primaryType="nt:unstructured">  
                    <text  
                            jcr:primaryType="nt:unstructured"  
                            sling:resourceType="granite/ui/components/coral/foundation/form/textfield"  
                            fieldLabel="Title"  
                            name="./title"/>  
                </items>  
            </column>  
        </items>  
    </content>  
</jcr:root>
```

Sling Model

```
import com.adobe.cq.export.json.ComponentExporter;  
  
public interface RandomNumberComponent extends ComponentExporter {  
    public String getTitle();  
}
```

```
RandomNumberComponentImpl  
import com.adobe.cq.export.json.ComponentExporter;  
import com.adobe.cq.export.json.ExporterConstants;  
import org.apache.sling.api.SlingHttpServletRequest;  
import org.apache.sling.models.annotations.DefaultInjectionStrategy;  
import org.apache.sling.models.annotations.Exporter;  
import org.apache.sling.models.annotations.Model;  
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;  
  
@Model(  
        adaptables = SlingHttpServletRequest.class,  
        adapters = { RandomNumberComponent.class,ComponentExporter.class },  
        resourceType = RandomNumberComponentImpl.RESOURCE_TYPE,  
        defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL  
)  
@Exporter(  
        name = ExporterConstants.SLING_MODEL_EXPORTER_NAME,  
        extensions = ExporterConstants.SLING_MODEL_EXTENSION  
)  
public class RandomNumberComponentImpl implements  RandomNumberComponent {  
  
    @ValueMapValue  
    private String title;  
  
    @Override  
    public String getTitle() {  
        return title;  
    }  
  
    static final String RESOURCE_TYPE = "aemreact2024/components/randomnumbercomponent";  
  
    // This function is important to export JSON depending on resourcetype.  
    @Override  
    public String getExportedType() {  
        return RandomNumberComponentImpl.RESOURCE_TYPE;  
    }  
}
```

UI component

Create RandomNumberComponent in ui.frontend\src\components and create js and css fles

```
RandomNumberComponent.js  
import { MapTo } from '@adobe/aem-react-editable-components';  
import DOMPurify from 'dompurify';  
import React, { Component } from 'react';  
import extractModelId from '../../utils/extract-model-id';  
  
// This will help us to include TitleText component specific CSS  
require('./RandomNumberComponent.css');  
const RandomNumberComponentEditConfig = {  
  
  emptyLabel: 'Configure RandomNumberComponent ',  
  
  /**  
   * emptyLabel will be a component placeholder if nothing is  
   * authored or below values are false.  
   */  
  isEmpty: function(props) {  
    return !props || !props.title || props.title.trim().length < 1;  
  }  
};  
  
class RandomNumberComponent extends Component {  
    constructor(props) {  
        super(props);  
        this.state = {  
            randomId: null,  
            loading: true,  
            error: null,  
        };  
    }  
  
    componentDidMount() {  
        this.fetchRandomData();  
    }  
  
    fetchRandomData = () => {  
        fetch('https://random-data-api.com/api/number/random_number')  
            .then(response => response.json())  
            .then(data => {  
                this.setState({  
                    randomId: data.id,  
                    loading: false,  
                });  
            })  
            .catch(error => {  
                this.setState({  
                    error: error.message,  
                    loading: false,  
                });  
            });  
    };  
  
    render() {  
        const { title } = this.props;  
        const { randomId, loading, error } = this.state;  
  
  
  
        return (  
            <div>  
                <h1>{title} {randomId}</h1>  
            </div>  
        );  
    }  
}  
  
  
/**  
 * This component is map to aemreact/components/title-text  
 * resourceType to load JSON.  
 * It will return TitleText component if it is authored and not empty else  
 * it will return TitleTextEditConfig default constant.  
 */  
export default MapTo('aemreact2024/components/randomnumbercomponent')(  
  RandomNumberComponent,  
  RandomNumberComponentEditConfig  
);
```

deploy the component and check the random number generated(highlighted in red)

Press enter or click to view image in full size

![]()
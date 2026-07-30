---
type: Learning
title: 'Nested aem components '
topic: AEM
tags:
  - aem
  - components
status: stable
generated:
  by: 'human:kiran'
  at: '2026-07-30T07:06:31.294Z'
verified:
  - by: agent-kiran/seed-script
    at: '2026-07-30T07:06:31.294Z'
---
The sling model will give a component that extends Container which dictates the allowed components via policy. In react component, the EditableComponent will be mapped to parent and the `add components` related aem container is mapped to `cqPath/*`. This is very important else the child container will take the focus of authoring dialog instead of whole component.

In below example, we have a aem carousel component that provide `:items` representing the cards or images to be displayed inside the carousel and also have title, layout, cta etc attributes that define the content placement around carousel. 

On FE, the design dictates that the title should appear on left side and carousel on right. in editor mode, we should display a `Add Components` aem container to add the components to the carousel and we're manually iterating through `cqItems`[which are `:items` in aem java component] as children to a 3rdparty carousel component (here we're using `react-slick` slider as carousel that accepts slides as children) and passing that data to another aem Container to itentify and display the relevant component via `:type` of every `cqItem`. To achive this level of dynamic configuration & rendering, we mapped the FE components to aem components via aem react's `MapTo` function. 

The error hoc has aem's `EditableCOmponent` which accepts all the props. The important point here is the props always has `cqPath` that defines the path of aem component. no 2 elements should have same path. only EditableComponent have `cqPath` that acts as parent. in below case, the dynamic placeholder to add components has resourcepath which is same as cqPath suffuxed with `/*`. This represents that, that particular placeholder is responsible for adding **child elements**. as we're manually looping through `cqItems`, the container that take the cqItem, have the cqPath suffixed by the **itemName of cqItem**. this helps author to edit individual items in editor mode thus fulfilling the below criteria:

- aem editor treat complete react element as authorable
- we can place the add components section anywhere for similar setup for different components
- every child element is indivudually authorable

## example react component (carousel):

```typescript
// errorboundary hoc
import { Config, EditableComponent, MappedComponentProperties, ModelProps } from '@adobe/aem-react-editable-components';
import { Component, ComponentType, ErrorInfo, ReactNode } from 'react';

type ErrorBoundaryProps = {
  children?: ReactNode;
  fallbackUI?: ReactNode;
  componentName?: string;
};

type ErrorBoundaryState = {
  hasError: boolean;
};

type ComponentProps<T> = { model: T & ModelProps };

export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = {
      hasError: false,
    };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    console.error('ErrorBoundary caught an error', error, errorInfo);
  }

  render(): ReactNode {
    if (this.state.hasError) {
      return this.props.fallbackUI ? (
        this.props.fallbackUI
      ) : (
        <div>Something went wrong in {this.props.componentName}</div>
      );
    }
    return this.props.children;
  }
}

export const withErrorBoundary = <P extends object>(
  Component: ComponentType<ComponentProps<P>>,
  componentEditConfig: Config<MappedComponentProperties & ComponentProps<P>>,
) =>
  function WrappedComponent(props: ComponentProps<P>) {
    return (
      <EditableComponent config={componentEditConfig} {...props}>
        <ErrorBoundary componentName={componentEditConfig.emptyLabel}>
          <Component {...props} />
        </ErrorBoundary>
      </EditableComponent>
    );
  };

// import components
MapTo(`${aem_site}/components/carousel`)(withErrorBoundary(ContentCarousel, ContentCarouselEditConfig));
```

```typescript
import { Container, ModelProps } from '@adobe/aem-react-editable-components';
import { Box, Flex, useBreakpointValue } from '@chakra-ui/react';
import React from 'react';
import { pxToRem } from '../../foundation/chakra/utils';
import { Carousel } from '../../molecules/Carousel';
import { TitleLockup, TitleLockupProps, TitleLockupVariant } from '../../organisms/TitleLockup';
import { ContentCarouselProps, TitleLayout } from './ContentCarousel.model';
import styles from './ContentCarousel.module.scss';

export const ContentCarouselEditConfig = {
  emptyLabel: 'Carousel',
  isEmpty: (props: { model?: { cqItemsOrder?: string[] } }) => {
    const { cqItemsOrder = [] } = props?.model || {};
    return cqItemsOrder.length === 0;
  },
  resourceType: 'panynjaviationprogram/components/carousel',
};

export const ContentCarousel = (props: { model: ContentCarouselProps & ModelProps; isInEditor?: boolean }) => {
  console.log('carousel props', props);
  const {
    cqItems = {},
    cqItemsOrder = [],
    resourcePath,
    titleLayout = TitleLayout.NO_TITLE,
    eyebrow,
    title,
    description,
    ctaItem,
    backgroundStyle,
    ariaLabel,
    previousCtaAriaLabel,
    nextCtaAriaLabel,
    children,
  } = props.model;

  const isDesktop = useBreakpointValue({ base: false, lg: true });

  const showTitleLockup = titleLayout !== TitleLayout.NO_TITLE;
  const showTitleLockupLeft = isDesktop && showTitleLockup && titleLayout !== TitleLayout.EYEBROW_ONLY;

  const getTitleLockupProps = (): TitleLockupProps => {
    if (titleLayout === TitleLayout.EYEBROW_ONLY) {
      return {
        variant: TitleLockupVariant.STACK_LARGE,
        eyebrow,
        title: '',
      };
    } else if (titleLayout === TitleLayout.LARGE_TITLE) {
      return {
        variant: TitleLockupVariant.STACK_LARGE,
        eyebrow,
        title: title || '',
        description,
        ctaItems: ctaItem ? [ctaItem] : [],
      };
    } else if (titleLayout === TitleLayout.SMALL_TITLE) {
      return {
        variant: TitleLockupVariant.STACK_MEDIUM,
        eyebrow,
        title: title || '',
        description,
        ctaItems: ctaItem ? [ctaItem] : [],
      };
    }
    return {
      variant: TitleLockupVariant.STACK_LARGE,
      title: '',
    };
  };

  return (
    <>
      <Flex
        direction={showTitleLockupLeft ? 'row' : 'column'}
        gap={showTitleLockupLeft ? 0 : isDesktop ? '{spacing.container.xl}' : '{spacing.container.lg}'}
        align="stretch"
        data-testid="carousel-with-title"
        className={`${styles.ContentCarouselContainer} ${backgroundStyle === 'color' ? styles.showBackgroundColor : ''}`}
      >
        {showTitleLockup ? (
          <Box
            flex={showTitleLockupLeft ? `0 0 ${pxToRem(416)}` : 'auto'}
            minW={showTitleLockupLeft ? `${pxToRem(416)}` : undefined}
          >
            <TitleLockup {...getTitleLockupProps()} />
          </Box>
        ) : null}
        <Box flex="1" minW={0}>
          <Carousel
            ariaLabel={ariaLabel}
            previousCtaAriaLabel={previousCtaAriaLabel}
            nextCtaAriaLabel={nextCtaAriaLabel}
            className={styles.carouselContainer}
          >
            {props.isInEditor ? (
              <Box className={styles.addComponents}>
                <Container cqItems={{}} cqItemsOrder={[]} cqPath={`${resourcePath}/*`} />
              </Box>
            ) : null}
            {children
              ? (children as React.ReactElement[]).map((child: React.ReactElement, idx: number) =>
                  React.cloneElement(child as React.ReactElement<{ model?: Record<string, unknown> }>, {
                    key: idx,
                    model: {
                      ...(child?.props ? (child.props as { model?: Record<string, unknown> }).model || {} : {}),
                      className: `${styles.cardContainer} ${styles.elevated} ${idx === 0 ? styles.first : ''} ${idx === (children as React.ReactElement[]).length - 1 ? styles.last : ''}`,
                    },
                  }),
                )
              : null}
            {!children
              ? cqItemsOrder.map((itemName, idx) => {
                  const containerProps = {
                    cqItems: {
                      [itemName]: {
                        ...cqItems[itemName],
                        className: `${styles.cardContainer} ${styles.elevated} ${idx === 0 ? styles.first : ''} ${idx === cqItemsOrder.length - 1 && !props.isInEditor ? styles.last : ''}`,
                      } as ModelProps['cqItems'] & { className: string },
                    } as ModelProps['cqItems'],
                    cqItemsOrder: [itemName],
                  };
                  return (
                    <Container
                      key={`${itemName}-${idx}`}
                      className={styles.containerWrapper}
                      cqPath={`${resourcePath}/${itemName}`}
                      {...containerProps}
                    />
                  );
                })
              : null}
          </Carousel>
        </Box>
      </Flex>
    </>
  );
};
```

## Java sling model:

```java
package com.panynjaviationprogram.core.models.components;

import com.adobe.cq.export.json.ComponentExporter;
import com.adobe.cq.export.json.ExporterConstants;
import com.adobe.cq.wcm.style.ComponentStyleInfo;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.panynjaviationprogram.core.models.common.base.BaseComponentModel;
import com.panynjaviationprogram.core.models.common.base.BaseContainerModel;
import com.panynjaviationprogram.core.models.fragments.CTAItem;

import lombok.Getter;

import java.util.Optional;

import org.apache.sling.api.SlingHttpServletRequest;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.annotations.DefaultInjectionStrategy;
import org.apache.sling.models.annotations.Exporter;
import org.apache.sling.models.annotations.Model;
import org.apache.sling.models.annotations.Via;
import org.apache.sling.models.annotations.injectorspecific.*;

@Model(
        adaptables = {Resource.class, SlingHttpServletRequest.class},
        adapters = { ComponentExporter.class },
        resourceType = CarouselModel.RESOURCE_TYPE,
        defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL
)
@Exporter(
        name = ExporterConstants.SLING_MODEL_EXPORTER_NAME,
        extensions = ExporterConstants.SLING_MODEL_EXTENSION
)
public class CarouselModel extends BaseContainerModel {

    public static final String RESOURCE_TYPE = "panynjaviationprogram/components/carousel";

    @Getter
    @ValueMapValue
    private String titleLayout;

    @Getter
    @ValueMapValue
    private String eyebrow;

    @Getter
    @ValueMapValue
    private String title;

    @Getter
    @ValueMapValue
    private String description;

    @Getter
    @Self
    @Via("resource")
    private CTAItem ctaItem;

    @JsonProperty("backgroundStyle")
    public String getAppliedCssClasses() {
        return Optional.ofNullable(resource)
                .map(res -> res.adaptTo(ComponentStyleInfo.class))
                .map(ComponentStyleInfo::getAppliedCssClasses)
                .filter(css -> !css.isEmpty())
                .orElse("");
    }
}
```

## BaseModelContainer.java

```java
package com.panynjaviationprogram.core.models.common.base;

import java.util.ArrayList;
import java.util.Iterator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

import org.apache.sling.api.SlingHttpServletRequest;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.annotations.DefaultInjectionStrategy;
import org.apache.sling.models.annotations.Exporter;
import org.apache.sling.models.annotations.Model;

import com.adobe.cq.export.json.ComponentExporter;
import com.adobe.cq.export.json.ContainerExporter;
import com.adobe.cq.export.json.ExporterConstants;

@Model(
    adaptables = {Resource.class, SlingHttpServletRequest.class},
    adapters = {ComponentExporter.class, ContainerExporter.class},
    defaultInjectionStrategy = DefaultInjectionStrategy.OPTIONAL
)
@Exporter(
    name = ExporterConstants.SLING_MODEL_EXPORTER_NAME,
    extensions = ExporterConstants.SLING_MODEL_EXTENSION
)
public class BaseContainerModel extends BaseComponentModel implements ContainerExporter {

    /**
     * Returns a map of child components adapted to ComponentExporter.
     * <p>
     * If the container has no children or no valid ComponentExporter children,
     * this method returns {@code null}, which prevents empty ":items" in JSON output.
     *
     * @return a map of child names to ComponentExporter, or {@code null} if none exist
     */
  @Override
  public Map<String, ? extends ComponentExporter> getExportedItems() {
      Resource childrenRoot = resource.getChild("items");
      Iterator<Resource> childrenIter = (childrenRoot != null) ? childrenRoot.listChildren() : resource.listChildren();

      if (childrenIter == null || !childrenIter.hasNext()) {
          return null; // return null if no children
      }

      Map<String, ComponentExporter> items = new LinkedHashMap<>();
      while (childrenIter.hasNext()) {
          Resource child = childrenIter.next();
          if (child == null) continue;

          ComponentExporter exporter = child.adaptTo(ComponentExporter.class);
          if (exporter != null) {
              items.put(child.getName(), exporter);
          }
      }

      return items.isEmpty() ? null : items; // return null if no valid child exporters
  }

  /**
     * Returns the order of child component names as a String array.
     * <p>
     * If the container has no children or no valid ComponentExporter children,
     * this method returns {@code null}, which prevents empty ":itemsOrder" in JSON output.
     *
     * @return an array of child names in order, or {@code null} if none exist
     */
  @Override
  public String[] getExportedItemsOrder() {
      Resource childrenRoot = resource.getChild("items");
      Iterator<Resource> childrenIter = (childrenRoot != null) ? childrenRoot.listChildren() : resource.listChildren();

      if (childrenIter == null || !childrenIter.hasNext()) {
          return null; // return null if no children
      }

      List<String> order = new ArrayList<>();
      while (childrenIter.hasNext()) {
          Resource child = childrenIter.next();
          if (child == null) continue;

          ComponentExporter exporter = child.adaptTo(ComponentExporter.class);
          if (exporter != null) {
              order.add(child.getName());
          }
      }

      return order.isEmpty() ? null : order.toArray(new String[0]);
  }

    public String getResourcePath() {
        return resource.getPath();
    }
}
```

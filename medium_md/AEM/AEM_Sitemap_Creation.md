---
title: "AEM Sitemap Creation"
url: https://medium.com/p/4877b3a8391a
---

# AEM Sitemap Creation

[Original](https://medium.com/p/4877b3a8391a)

# AEM Sitemap Creation

[![Imran Khan](https://miro.medium.com/v2/resize:fill:64:64/1*qB5cH4JYH-vgBSoEJHR2IQ.jpeg)](/@toimrank?source=post_page---byline--4877b3a8391a---------------------------------------)

[Imran Khan](/@toimrank?source=post_page---byline--4877b3a8391a---------------------------------------)

3 min read

·

Sep 26, 2023

--

1

Listen

Share

More

As part of this blog, we will try to understand everything around sitemaps and how to implement them in AEM following a step-by-step process for both AEM on prem and AEM as a cloud service.

A sitemap helps search engines identify the list of URLs eligible for crawling. We can see our site pages as part of a Google search as soon as the page gets crawled by Google.

We and search engines access sitemaps for any website using <site\_domain>/sitemap.xml. Scroll down to the end of the page to see the list of pages applicable for crawling.

e.g. <https://www.google.com/sitemap.xml>

Below is a sample sitemap example that contains the page path and last modified date.

```
<urlset   
  xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"   
  xmlns:xhtml="http://www.w3.org/1999/xhtml"   
  xmlns:video="http://www.google.com/schemas/sitemap-video/1.1"   
  xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"   
  xmlns:news="http://www.google.com/schemas/sitemap-news/0.9">  
  <url>  
    <loc>/content/practice/us/en/things-to-do.html</loc>  
    <lastmod>2023-09-11T13:01:03.478Z</lastmod>  
  </url>  
  <url>  
    <loc>/content/practice/us/en/things-to-do/all-experiences.html</loc>  
    <lastmod>2023-09-11T13:01:04.38Z</lastmod>  
  </url>  
</urlset>
```

As part of current implementation, **there are different ways to create Sitemap for author and publish**.

## Author Sitemap Implementation

Using the below OSGI configuration and setting allOnDemand to true will allow us to create a sitemap. Place the below configuration as part of the author conig file config.author:

*org.apache.sling.sitemap.impl.SitemapGeneratorManagerImpl~practice.cfg.json*

```
{  
  "allOnDemand": true  
}
```

***Note: allOnDemand configuration is having a drawback as it process data and generate sitemap everytime we hit the URL to generate a site map.***

## Common Configuration for both autho and publish

Below is the **common configuration for both author and publish,** which allows us to include the **last modified date and represent data in XML format.**

Place the below configuration as part of the CONIG file to apply to both authors and publish:

com.adobe.aem.wcm.seo.impl.sitemap.PageTreeSitemapGeneratorImpl.cfg.json

```
{  
  "enableLastModified": true,  
  "lastModifiedSource": "cq:lastModified",  
  "enableLanguageAlternates": false  
}
```

## Page Properties Update

To generate a sitemap it is mandatory to **enable sitemap** as part of root page property under advanced tab as shown below.

![]()

### Exclude Page and apply some other properties

We can apply the below noindex property as part of robot tags if we don’t want that page to get indexed.

We can also apply other Root Tags property options specific to that page, such as follow, nofollow, noarchive, etc.

![]()

## Generate Sitemap on author

Hit below URL to generate a sitemap as part of author:

<http://localhost:4502/content/pracitce/en.sitemap.xml>

Press enter or click to view image in full size

![]()

## Publish Sitemap Implementation

Above allowOnDemand, cannot be use in publish to generate a sitemap because every time it process and generate a sitemap.

1. Create below configuration as part of publish config which will run a scheduler depending on give time or period to generate a sitemap considering below sitemap.

*org.apache.sling.sitemap.impl.SitemapScheduler~practice.cfg.json*

```
{  
  "scheduler.name": "Practice Daily Sitemap Scheduler",  
  "scheduler.expression": "0 0 2 1/1 * ? *",  
  "searchPath": "/content/practice/us"  
}
```

***Note: Every time scheduler runs will generate sitemap folder inside /var/sitemaps*** ***folder like /var/sitemaps/content/practice/us/sitemap.xml hierarchy.***

2. Generating a site will also require below publish configurations to consider extension, resourcet ype and selectors to generate a sitemap.

*org.apache.sling.sitemap.impl.SitemapServlet~practice.cfg.json*

```
{  
 "sling.servlet.extensions": "xml",  
 "sling.servlet.resourceTypes": [  
  "pracitce/components/structure/homepage",  
  "practice/components/structure/profile",  
  "practice/components/ea/structure/search"  
 ],  
 "sling.servlet.selectors": [  
  "sitemap",  
  "sitemap-index"  
 ]  
}
```

## Generate Sitemap on author

Enable sitemap as part of advanced tab page properties and publish page.

Hit below URL to generate a sitemap as part of author:

[http://localhost:4503/content/pracitce/en.sitemap.xml](http://localhost:4502/content/pracitce/en.sitemap.xml)

![]()

## Dispatcher Update

It will require below small amount of updates within dispatcher to access/render sitemap

1. Allow below entry as part of dispatcher/src/conf.dispatcher.d/filters/filters.any file.

```
/0200 { /type "allow" /path "/content/*" /selectors '(sitemap-index|sitemap)' /extension "xml" }
```

2. Allow .xml extension as part of rewrite rules dispatcher/src/conf.d/rewrites/rewrite.rules file.

```
RewriteCond %{REQUEST_URI} (.html|.jpe?g|.png|.svg|.xml)$
```

I hope you found out this article interesting and informative. Please clap and share it with your friends to spread the knowledge.

You can follow me for upcoming blogs [follow](/@toimrank).  
Thank you !!!
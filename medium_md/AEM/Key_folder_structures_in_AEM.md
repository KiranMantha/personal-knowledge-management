---
title: "Key folder structures in AEM"
url: https://medium.com/p/433b616dfba1
---

# Key folder structures in AEM

[Original](https://medium.com/p/433b616dfba1)

Member-only story

# Key folder structures in AEM

[![Jeetendrakumar Sahu](https://miro.medium.com/v2/resize:fill:64:64/1*MfW7Wfz4gnXpJGQIteRDwg.png)](/@j.abhimanyu.sahu?source=post_page---byline--433b616dfba1---------------------------------------)

[Jeetendrakumar Sahu](/@j.abhimanyu.sahu?source=post_page---byline--433b616dfba1---------------------------------------)

3 min read

·

Dec 5, 2024

--

Listen

Share

More

In **Adobe Experience Manager (AEM)**, folder structures are integral for organizing and managing content, configurations, and assets. Here’s a breakdown of key folder structures in AEM, their purpose, and examples:

## `/apps`

### Purpose:

* Stores application-specific code, templates, components, and scripts.
* Developers customize and extend AEM here.

### Explanation:

* Houses all custom functionality, such as templates, components, dialogs, and client libraries.
* Is not editable by content authors.
* Designed to separate application-specific resources from core AEM libraries.

### Example:

```
/apps/my-website/components/   -> Custom AEM components  
/apps/my-website/templates/   -> Page templates  
/apps/my-website/clientlibs/  -> CSS and JavaScript files
```

## `/libs`

### Purpose:

* Contains core AEM libraries and default implementations.

### Explanation:

* Includes out-of-the-box features, components, and configurations.
* Direct editing here is discouraged as it can break AEM updates.
* Instead, overlay or extend functionalities into the `/apps` folder.

### Example:

```
/libs/foundation/components/  -> AEM core components like Text, Image  
/libs/granite/               -> Core Granite UI elements
```

## `/content`

### Purpose:

* Stores all website content, pages, and assets created by authors.

### Explanation:

* Organized in a hierarchy that represents the site structure.
* Each site or language variation is represented as a subfolder.

### Example:

```
/content/my-website/en/       -> English site content  
/content/my-website/fr/       -> French site content  
/content/dam/                 -> Digital assets like images, videos, PDFs
```

## `/conf`

### Purpose:

* Stores site-specific configurations, editable templates, and policies.

### Explanation:

* Includes configurations like editable templates, workflows, and content policies for components.
* Introduced in AEM 6.3 to decouple content structure (`/content`) and configuration.

### Example:

```
/conf/my-website/settings/wcm/templates/  -> Editable templates  
/conf/my-website/settings/dam/            -> Asset folder configurations
```

## `/etc` (Deprecated)

### Purpose:

* Legacy folder for configurations, workflows, and tools (replaced by `/conf`).

### Explanation:

* Was used before AEM 6.3 to store site configurations, workflows, and tools.
* Avoid using this folder in modern AEM projects.

### Example:

```
/etc/designs/my-website/  -> Legacy design configurations  
/etc/workflow/            -> Legacy workflows
```

## `/var`

### Purpose:

* Stores runtime data and temporary information.

### Explanation:

* Used for caching, logs, and other operational data.
* Avoid manual changes in this folder.

### Example:

```
/var/workflow/instances/  -> Runtime workflow instance data  
/var/cache/               -> Cache files
```

## `/tmp`

### Purpose:

* Temporary folder for runtime storage.

### Explanation:

* Contains temporary files generated during operations, such as uploads or replication processes.
* Regularly cleaned by the system.

## `/home`

### Purpose:

* Stores user-specific data, including preferences and profiles.

### Explanation:

* A place for user-specific storage in AEM, such as dashboards or preferences.

### Example:

```
/home/users/author/     -> Author's profile and preferences  
/home/groups/           -> Group-specific data
```

## `/oak:index`

### Purpose:

* Stores indexes for Oak repository queries.

### Explanation:

* Critical for performance optimization in querying the JCR.
* Should be carefully managed by developers or administrators.

### Example:

```
/oak:index/damAssetLucene -> Index for searching DAM assets
```

**Summary Table**

Press enter or click to view image in full size

![]()

Each folder serves a specific purpose in AEM, providing a clear separation of responsibilities for developers, content authors, and system administrators. Properly organizing and utilizing these folders ensures efficient AEM projects.

## Here’s a concise summary of which folders are cached and not cached in AEM’s Dispatcher:

### Folders Cached

`/content`

* Example: Pages, images, and static content like **HTML**, **CSS**, **JS**, and assets.

`/etc.clientlibs`

* Example: Client libraries (CSS & JS bundles).

### Folders NOT Cached

`/apps`

* Contains custom application code, templates, and components.

`/libs`

* Core AEM libraries and out-of-the-box components.

`/conf`

* Editable templates, content policies, and site configurations.

`/var`

* Runtime data like workflows and cache.

`/tmp`

* Temporary runtime files.

`/oak:index`

* Indexes for repository queries.

`/home`

* User and group-specific data.

**Administrative and Dynamic Paths**

* Examples: `/bin`, `/crx`, `/system`, `/userprofile`, `/error`, `/search`.

### Rule of Thumb:

* **Static content** (HTML, CSS, JS, images) is cached.
* **Dynamic, administrative, and system content** is not cached.
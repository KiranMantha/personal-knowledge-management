---
title: "GraphQL simple guide for AEM ( Adobe Experience Manager )"
url: https://medium.com/p/7f2b64de0345
---

# GraphQL simple guide for AEM ( Adobe Experience Manager )

[Original](https://medium.com/p/7f2b64de0345)

# GraphQL simple guide for AEM ( Adobe Experience Manager )

[![Mircea Gabriel Dumitrescu](https://miro.medium.com/v2/resize:fill:64:64/1*TW-JpYR1nk7ciXTnm9yAmA.png)](/@mirceagab?source=post_page---byline--7f2b64de0345---------------------------------------)

[Mircea Gabriel Dumitrescu](/@mirceagab?source=post_page---byline--7f2b64de0345---------------------------------------)

5 min read

·

Dec 17, 2024

--

4

Listen

Share

More

Press enter or click to view image in full size

![]()

Integrating GraphQL with Adobe Experience Manager (AEM) typically involves leveraging AEM’s Content Fragment Models and the GraphQL APIs provided by AEM. This allows you to expose AEM content as structured data via GraphQL queries.

GraphQL can be integrated with AEM, including the setup, queries, and use cases.

## Key Components of AEM GraphQL

**Content Fragment Models:**

Content Fragments are structured content in AEM. These are similar to “content types” in a CMS. You define a Content Fragment Model that specifies the fields and structure of your content.

**AEM GraphQL API:**

AEM provides a GraphQL API that allows you to query Content Fragments as JSON data. AEM Cloud Service and AEM 6.5+ (with Service Pack 8 or higher) support the GraphQL API.

The endpoint typically looks like this: ***/content/cq:graphql/global/endpoint.json***

## Steps to Integrate GraphQL with AEM

### Set Up Content Fragment Models

**1. Navigate to AEM:**

Go to Tools → Assets → Content Fragment Models.

**2. Create a Model:**

- Define a new model, e.g., ArticleModel.

- Add fields such as title, description, author, and publishDate.

- You can use field types like Text, Date, Number, or even nested Content References.

**3. Save and Publish the Content Fragment Model.**

### Create Content Fragments

**1. Navigate to Assets:**

Go to Assets → Files and create a folder for your content fragments.

**2. Create Content Fragments Based on the Model:**

• Select the model you created (e.g., ArticleModel).

• Add content: Title, description, author name, etc.

• Save and publish the fragments.

### Enable GraphQL in AEM

**1. Enable GraphQL Endpoint:**

• Navigate to AEM’s GraphQL API settings under:

Tools → General → GraphQL

• Ensure that the GraphQL endpoint is enabled.

**2. Access the Endpoint:**

The default endpoint to query the fragments looks like: /***content/cq:graphql/global/endpoint.json***

Replace global with your project-specific configuration.

## Querying AEM Content with GraphQL

You can use tools like Postman or GraphQL Playground to test your GraphQL queries.

Here’s an example query to fetch articles from the ArticleModel:

**GraphQL Query Example:**

```
{  
  articleList {  
    items {  
      title  
      description  
      author  
      publishDate  
    }  
  }  
}
```

**Response:**

```
{  
  "data": {  
    "articleList": {  
      "items": [  
        {  
          "title": "GraphQL in AEM",  
          "description": "Learn how to integrate GraphQL with AEM.",  
          "author": "John Doe",  
          "publishDate": "2024-06-17"  
        }  
      ]  
    }  
  }  
}
```

## Integrate AEM GraphQL with React

To integrate AEM’s GraphQL endpoint with a React frontend, you can use Apollo Client or fetch to retrieve data and display it.

**Example:**

```
import React from "react";  
import { ApolloClient, InMemoryCache, ApolloProvider, gql, useQuery } from "@apollo/client";  
  
// Initialize Apollo Client  
const client = new ApolloClient({  
  uri: "http://localhost:4502/content/cq:graphql/global/endpoint.json",  
  cache: new InMemoryCache(),  
});  
  
// Define the GraphQL query  
const GET_ARTICLES = gql`  
  query {  
    articleList {  
      items {  
        title  
        description  
        author  
        publishDate  
      }  
    }  
  }  
`;  
  
// React component  
const ArticleList = () => {  
  const { loading, error, data } = useQuery(GET_ARTICLES);  
  
  if (loading) return <p>Loading...</p>;  
  if (error) return <p>Error: {error.message}</p>;  
  
  return (  
    <div>  
      <h1>Articles</h1>  
      {data.articleList.items.map((article, index) => (  
        <div key={index}>  
          <h2>{article.title}</h2>  
          <p>{article.description}</p>  
          <p><strong>Author:</strong> {article.author}</p>  
          <p><strong>Date:</strong> {article.publishDate}</p>  
        </div>  
      ))}  
    </div>  
  );  
};  
  
function App() {  
  return (  
    <ApolloProvider client={client}>  
      <ArticleList />  
    </ApolloProvider>  
  );  
}  
  
export default App;
```

### How It All Ties Together

**1. Backend (AEM):**

• AEM exposes Content Fragments via its GraphQL API endpoint.

• GraphQL queries are executed against the endpoint to fetch the structured content.

**2. Frontend (React):**

• Apollo Client fetches the GraphQL data from the AEM endpoint.

• The React components render the fetched data dynamically.

## What if i don’t use React or a Frontend Framework ?

If you’re not using React and instead working with a plain vanilla JavaScript frontend, you can still integrate AEM’s GraphQL API using standard browser features like fetch() to query and display data. Here’s how you can achieve it step by step:

***The AEM GraphQL endpoint remains the same.***

### Vanilla JavaScript Integration

**HTML Template**

Create a simple HTML file to display the content fetched from AEM.

```
<!DOCTYPE html>  
<html lang="en">  
<head>  
  <meta charset="UTF-8">  
  <meta name="viewport" content="width=device-width, initial-scale=1.0">  
  <title>AEM GraphQL Integration</title>  
  <style>  
    body { font-family: Arial, sans-serif; margin: 20px; }  
    .article { border: 1px solid #ccc; padding: 10px; margin-bottom: 15px; }  
    .article h2 { margin: 0; }  
  </style>  
</head>  
<body>  
  <h1>Articles</h1>  
  <div id="articles-container">Loading...</div>  
  
  <script>  
    // GraphQL query to fetch articles  
    const GRAPHQL_QUERY = JSON.stringify({  
      query: `  
        query {  
          articleList {  
            items {  
              title  
              description  
              author  
              publishDate  
            }  
          }  
        }  
      `  
    });  
  
    // Fetch data from AEM GraphQL endpoint  
    async function fetchArticles() {  
      try {  
        const response = await fetch('http://localhost:4502/content/cq:graphql/global/endpoint.json', {  
          method: 'POST',  
          headers: {  
            'Content-Type': 'application/json',  
            'Authorization': 'Basic ' + btoa('admin:admin') // Replace with proper credentials  
          },  
          body: GRAPHQL_QUERY  
        });  
  
        if (!response.ok) throw new Error('Network response was not ok');  
  
        const result = await response.json();  
        displayArticles(result.data.articleList.items);  
      } catch (error) {  
        console.error('Error fetching GraphQL data:', error);  
        document.getElementById('articles-container').innerHTML = "Failed to load articles.";  
      }  
    }  
  
    // Render articles dynamically into the DOM  
    function displayArticles(articles) {  
      const container = document.getElementById('articles-container');  
      container.innerHTML = ''; // Clear loading message  
  
      articles.forEach(article => {  
        const articleDiv = document.createElement('div');  
        articleDiv.className = 'article';  
        articleDiv.innerHTML = `  
          <h2>${article.title}</h2>  
          <p><strong>Description:</strong> ${article.description}</p>  
          <p><strong>Author:</strong> ${article.author}</p>  
          <p><strong>Published:</strong> ${article.publishDate}</p>  
        `;  
        container.appendChild(articleDiv);  
      });  
    }  
  
    // Execute the function on page load  
    fetchArticles();  
  </script>  
</body>  
</html>
```

### How It Works

**1. GraphQL Query:**

A GraphQL query is defined as a JSON string and sent to the AEM GraphQL endpoint using the fetch() API.

**2. Authorization:**

• Basic Authentication (btoa(‘username:password’)) is used for AEM authentication.

• For production, use tokens or secured mechanisms like OAuth instead.

**3. Fetch Data:**

The fetch() function makes a POST request to the AEM GraphQL endpoint with the query.

**4. Render Data:**

The displayArticles() function dynamically creates HTML elements for each article and appends them to the container.

***Here’s an example JSON response from AEM’s GraphQL API:***

```
{  
  "data": {  
    "articleList": {  
      "items": [  
        {  
          "title": "GraphQL in AEM",  
          "description": "Learn how to integrate GraphQL with Adobe Experience Manager.",  
          "author": "John Doe",  
          "publishDate": "2024-06-17"  
        },  
        {  
          "title": "Headless CMS Benefits",  
          "description": "Why headless CMS architectures are gaining popularity.",  
          "author": "Jane Smith",  
          "publishDate": "2024-06-18"  
        }  
      ]  
    }  
  }  
}
```

Thank you guys for reading, let me know if you want to see how to implement pagination or additional filtering!
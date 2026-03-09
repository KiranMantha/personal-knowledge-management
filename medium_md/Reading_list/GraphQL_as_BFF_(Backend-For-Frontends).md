---
title: "GraphQL as BFF (Backend-For-Frontends)"
url: https://medium.com/p/ceecd6a4143b
---

# GraphQL as BFF (Backend-For-Frontends)

[Original](https://medium.com/p/ceecd6a4143b)

[![Kapil Vij](https://miro.medium.com/v2/resize:fill:64:64/1*kBfSMADR7eLfnXNVCmLr_A.jpeg)](/?source=post_page---byline--ceecd6a4143b---------------------------------------)

[Kapil Vij](/?source=post_page---byline--ceecd6a4143b---------------------------------------)

5 min read

·

Aug 3, 2023

--

Listen

Share

More

**GraphQL as BFF (Backend-For-Frontends)**

Press enter or click to view image in full size

![]()

A “Backend-For-Frontend” is a data transformation layer placed between a client and the API to avoid over-fetching and under-fetching

> GraphQL, the Facebook-incubated data query language, is moving into its own open-source foundation. Facebook announced GraphQL back in 2012 and open sourced it in 2015. Today, it’s being used by companies that range from Airbnb to Audi, GitHub, Netflix, Shopify, Twitter and The New York Times.

Usually frontend clients work with available REST API’s. And in order to paint the required UI design, FE’s end calling multiple REST API’s and using few data from each endpoint. This is actually called as over-fetching of data and can hamper user experience on slow connections.

Press enter or click to view image in full size

![]()

Look at the above diagram to see primary difference in REST and GraphQL.  
Below are the steps involved in any BFF

1. The FE client sends a request to the BFF — (here its GraphQL).
2. The GraphQL then communicates with the internal microservices and collects the requested data.
3. It then aggregates the data into the format requested by the FE’s
4. It returns the formatted data back to the FE client.

GraphQL provides a layer of abstraction between the Frontend clients and the Backend systems. In this abstraction, GraphQL models data as **nodes**. Connections among these nodes are **edges**. Thus, data is a graph of interconnected objects rather than resources accessed via multiple endpoints.

**Persisted Queries:**

A technique for improving GraphQL network performance by enabling clients to execute operations by passing an identifier, instead of by passing the entire operation string.

For very large operation strings, APQ meaningfully reduces bandwidth use and speeds up client loading times.

To Know More how it works :[**Persisted Queries**](https://www.apollographql.com/docs/apollo-server/performance/apq/)

**Docstring** :

Provides the description of a type, field, or argument. Docstrings automatically appear in many common GraphQL tools, including the Apollo Studio Explorer.

```
"""  
Description for the Student  
"""  
type Student {  
  """  
  Description for student Name  
  """  
  name: String!  
  
  classData(  
    """  
    Must be an integer value i.e. 4  
    """  
    standard: Int  
      
    """  
    Must be an String i.e. "D"  
    """  
    section: String  
  )  
}
```

**Important Terminologies:**

**Schema** : It acts as a contract between FE and BFF. You only query those fields which are present in schema. If backend wants to introduce any extra field which is non existing earlier will require change in Schema as a first step and then only FE’s can start querying it.

> *Your GraphQL server uses a* ***schema*** *to describe the shape of your available data. This schema defines a hierarchy of* ***types*** *with* ***fields*** *that are populated from your back-end data stores. The schema also specifies exactly which* ***queries*** *and* ***mutations*** *are available for clients to execute.*

**Resolvers** : A **resolver** is a function that’s responsible for populating the data for a single field in your schema**.** It can populate that data in any way you define, such as by fetching data from a back-end database or a third-party API.

**Playground** : Used to run queries / mutations similar to how Rest API calls work on Postman Rest Client. Also helps seeing the Schema

Link : <https://www.graphqlbin.com/v2/new>

**Query** : The Query type is a special object type that defines all of the top-level **entry points** for queries that clients execute against your server.

Each field of the **Query** type defines the name and return type of a different entry point. The Query type for our example schema might resemble the following:

```
type Query {  
  books: [Book]  
  authors: [Author]  
}
```

This Query type defines two fields: books and authors. Each field returns a list of the corresponding type.

With a REST-based API, books and authors would probably be returned by different endpoints (e.g., /api/books and /api/authors). The flexibility of GraphQL enables clients to query both resources with a single request.

**Mutation :** The Mutation type is similar in structure and purpose to the Query type. Whereas the Query type defines entry points for *read* operations, the Mutation type defines entry points for *write* operations.

Each field of the Mutation type defines the signature and return type of a different entry point. The Mutation type for our example schema might resemble the following:

```
type Mutation {  
  addBook(title: String, author: String): Book  
}
```

This Mutation type defines a single available mutation, addBook. The mutation accepts two arguments (title and author) and returns a newly created Book object. As you’d expect, this Book object conforms to the structure that we defined in our schema.

**Directives**: A **directive** decorates part of a GraphQL schema or operation with additional configuration. Tools like Apollo Server can read a GraphQL document’s directives and perform custom logic as appropriate.

Press enter or click to view image in full size

![]()

## Naming Conventions:

* **Field names** should use **camelCase**. Many GraphQL clients are written in JavaScript, Java, Kotlin, or Swift, all of which recommend camelCase for variable names.
* **Type names** should use **PascalCase**. This matches how classes are defined in the languages mentioned above.
* **Enum names** should use **PascalCase**.
* **Enum values** should use **ALL\_CAPS**, because they are similar to constants.

## Versioning :

Nobody stops you to create versioning on GraphQL API’s similar to REST API. But GraphQL had a string opinion on **avoiding versioning** for the continuous evolution of Schema

Versioning is primarily used when there is breaking change in API and we want to handle it for backward compatibility for older clients. But since with GraphQL clients can only request what is in Schema, so older client will never new data additions. And similarly new clients will stop requesting if something gets deprecated using directives.

This fundamental helps us in avoiding breaking changes and creating a version-less API.

==================== Thats All Folks ! =====================

**References** :

<https://www.apollographql.com/docs/>

<https://graphql.org/learn/queries/>

<https://graphql.org/learn/best-practices/>
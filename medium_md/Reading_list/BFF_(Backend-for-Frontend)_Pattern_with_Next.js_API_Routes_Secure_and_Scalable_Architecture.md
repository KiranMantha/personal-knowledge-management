---
title: "BFF (Backend-for-Frontend) Pattern with Next.js API Routes: Secure and Scalable Architecture"
url: https://medium.com/p/d6e088a39855
---

# BFF (Backend-for-Frontend) Pattern with Next.js API Routes: Secure and Scalable Architecture

[Original](https://medium.com/p/d6e088a39855)

# BFF (Backend-for-Frontend) Pattern with Next.js API Routes: Secure and Scalable Architecture

[![Zafer Bozkurt](https://miro.medium.com/v2/resize:fill:64:64/1*mWtIQ6g2-XqNJNe3pi8boQ.jpeg)](/@zaferbozkurt?source=post_page---byline--d6e088a39855---------------------------------------)

[Zafer Bozkurt](/@zaferbozkurt?source=post_page---byline--d6e088a39855---------------------------------------)

9 min read

·

Dec 29, 2025

--

1

Listen

Share

More

Managing communication between frontend and backend securely and efficiently is crucial in modern web applications. For applications dealing with sensitive data and user authentication, using an intermediary layer instead of direct client-side access to backend APIs provides a more robust solution from both security and architectural perspectives.

In this article, we’ll explore how to implement the BFF (Backend-for-Frontend) pattern using Next.js API Routes through a real-world project example. You can find the complete source code on [GitHub](https://github.com/zaferbozkurt/nextjs-bff).

Press enter or click to view image in full size

![]()

### **What is the BFF Pattern?**

The BFF (Backend-for-Frontend) pattern is an architectural approach that suggests creating a customized backend layer for each frontend application. Key advantages of this pattern include:

* **Security**: API keys and sensitive information are not exposed on the client-side
* **Flexibility**: Data transformation can be performed according to frontend requirements
* **Centralized Error Handling**: All API errors can be managed from a single point
* **Rate Limiting and Caching**: Can be implemented at a central location
* **Isolation from Backend Changes**: Backend API changes don’t directly affect the frontend

### **Project Architecture**

In our example project, the BFF pattern is implemented as follows:

```
Frontend (React Components)  
    ↓  
API Helper (Client-side)  
    ↓  
Next.js API Routes "/api/server/[...endpoint]" - (Server-side)  
    ↓  
Backend API (External Service)
```

### **1. Next.js API Route Handler**

The core of the project is an API handler created using Next.js’s catch-all route feature. This handler acts as a proxy between the frontend and backend API:

```
import axios, { AxiosError } from "axios";  
import { NextRequest, NextResponse } from "next/server";  
  
async function handler(request: NextRequest): Promise<NextResponse> {  
  const { pathname, search } = request.nextUrl;  
  const endpoint = `${pathname.replace("/api/server", "")}${search}`;  
  
  // Check API_URL  
  const apiUrl = process.env.API_URL;  
  if (!apiUrl) {  
    return NextResponse.json(  
      { error: "API_URL environment variable is not set" },  
      { status: 500 }  
    );  
  }  
  
  if (endpoint) {  
    const headers: any = {  
      "Content-Type": "application/json",  
    };  
  
    // Parse request body  
    let body = undefined;  
    if (request.method !== "GET" && request.method !== "HEAD") {  
      try {  
        body = await request.json();  
      } catch (error) {  
        // Use undefined if body is missing or cannot be parsed  
      }  
    }  
  
    try {  
      // Send request to backend API  
      const response = await axios.request({  
        url: endpoint,  
        method: request.method,  
        data: body,  
        baseURL: apiUrl,  
        headers: headers,  
        validateStatus: () => true, // Accept all status codes  
      });  
  
      return NextResponse.json(response.data, { status: response.status });  
    } catch (e) {  
      const axiosError = e as AxiosError;  
  
      // Return appropriate status code on error  
      const errorMessage =  
        axiosError.response?.data ||  
        axiosError.message ||  
        "Internal Server Error";  
  
      return NextResponse.json(  
        { error: errorMessage },  
        {  
          status: axiosError.response?.status || 500,  
        }  
      );  
    }  
  } else {  
    return NextResponse.json({ data: "Api Not Found" }, { status: 404 });  
  }  
}  
  
export { handler as GET, handler as POST, handler as PUT, handler as DELETE };
```

**Key Points:**

* **Catch-all Route**: All API endpoints are captured in a single handler using the `[…endpoint]` syntax, eliminating the need for individual route handlers
* **Environment Variables**: Backend API URL is securely retrieved using `process.env.API\_URL` (not exposed to client-side)
* **Error Handling**: Errors from the backend are forwarded to the frontend with appropriate HTTP status codes
* **Flexibility**: All HTTP methods (GET, POST, PUT, DELETE) are managed by a single handler
* **Status Code Validation**: The `validateStatus: () => true` option ensures all response status codes are handled, not just successful ones

### 2. Client-side API Instance

On the frontend, a simple Axios instance is used to route requests to the BFF endpoint:

```
import axios from "axios";  
  
export const api = axios.create({  
  baseURL: "/api/server"  
});
```

This simple structure routes all API calls to the BFF layer through the `/api/server` endpoint.

### 3. Request Functions

API calls are organized as domain-specific functions. These functions send requests to BFF endpoints using the Axios instance. In our example project, we’ve created a file for Posts using the DummyJSON API:

```
import { api } from "../client/api";  
  
export interface Post {  
  id: number;  
  userId: number;  
  title: string;  
  body: string;  
}  
  
export interface CreatePostData {  
  title: string;  
  body: string;  
  userId: number;  
}  
  
// GET: Fetch all posts  
export const fetchAllPosts = async (): Promise<Post[]> => {  
  const { data } = await api.get("/posts");  
  return data.posts || data; // DummyJSON returns posts in an array  
};  
  
// GET: Fetch a specific post  
export const fetchPostById = async (postId: number): Promise<Post> => {  
  const { data } = await api.get(`/posts/${postId}`);  
  return data;  
};  
  
// POST: Create a new post  
export const createPost = async (  
  postData: CreatePostData  
): Promise<Post> => {  
  const { data } = await api.post("/posts/add", postData);  
  return data;  
};
```

This structure allows API calls to be managed centrally, separated by domain, and reused across components.

### 4. React Query Integration

API calls are managed with React Query. Separate hook files are created for each domain:

```
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";  
import {  
  fetchAllPosts,  
  fetchPostById,  
  createPost,  
  type Post,  
  type CreatePostData,  
} from "@/api/requests/posts";  
  
// GET: Fetch all posts  
export const usePosts = () => {  
  return useQuery<Post[]>({  
    queryKey: ["posts"],  
    queryFn: fetchAllPosts,  
  });  
};  
  
// GET: Fetch a specific post  
export const usePost = (postId: number) => {  
  return useQuery<Post>({  
    queryKey: ["post", postId],  
    queryFn: () => fetchPostById(postId),  
    enabled: Boolean(postId),  
  });  
};  
  
// POST: Create a new post  
export const useCreatePost = () => {  
  const queryClient = useQueryClient();  
  
  return useMutation<Post, Error, CreatePostData>({  
    mutationFn: createPost,  
    onSuccess: () => {  
      // Refresh post list  
      queryClient.invalidateQueries({ queryKey: ["posts"] });  
    },  
  });  
};
```

The React Query Provider must be added to the root layout:

```
"use client";  
  
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";  
import { useState } from "react";  
  
export function QueryProvider({ children }: { children: React.ReactNode }) {  
  const [queryClient] = useState(  
    () =>  
      new QueryClient({  
        defaultOptions: {  
          queries: {  
            staleTime: 60 * 1000, // 1 minute  
            refetchOnWindowFocus: false,  
          },  
        },  
      })  
  );  
  
  return (  
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>  
  );  
}
```

### 5. Component Implementation

Finally, components use React Query hooks to fetch and display data. Here’s an example component that demonstrates the complete flow:

```
"use client";  
  
import { usePosts, useCreatePost } from "@/hooks/usePosts";  
import { useState } from "react";  
  
export function PostsList() {  
  const { data: posts, isLoading, error } = usePosts();  
  const createPostMutation = useCreatePost();  
  const [title, setTitle] = useState("");  
  const [body, setBody] = useState("");  
  const [showAll, setShowAll] = useState(false);  
  
  const handleSubmit = async (e: React.FormEvent) => {  
    e.preventDefault();  
    if (!title || !body) return;  
  
    createPostMutation.mutate(  
      { title, body, userId: 1 },  
      {  
        onSuccess: () => {  
          setTitle("");  
          setBody("");  
        },  
      }  
    );  
  };  
  
  if (isLoading) return <div>Loading...</div>;  
  if (error) return <div>Error: {error.message}</div>;  
  
  return (  
    <div className="space-y-6">  
      {/* Create Post Form */}  
      <form onSubmit={handleSubmit}>  
        <input  
          value={title}  
          onChange={(e) => setTitle(e.target.value)}  
          placeholder="Post title"  
          required  
        />  
        <textarea  
          value={body}  
          onChange={(e) => setBody(e.target.value)}  
          placeholder="Post content"  
          required  
        />  
        <button type="submit" disabled={createPostMutation.isPending}>  
          {createPostMutation.isPending ? "Creating..." : "Create Post"}  
        </button>  
      </form>  
  
      {/* Posts List */}  
      <div>  
        <h2>Posts ({posts?.length || 0})</h2>  
        <div className="grid">  
          {posts  
            ?.slice(0, showAll ? posts.length : 6)  
            .map((post) => (  
              <div key={post.id}>  
                <h3>{post.title}</h3>  
                <p>{post.body}</p>  
              </div>  
            ))}  
        </div>  
        {posts && posts.length > 6 && (  
          <button onClick={() => setShowAll(!showAll)}>  
            {showAll ? "Show Less" : "Show All"}  
          </button>  
        )}  
      </div>  
    </div>  
  );  
}
```

## Security Advantages

### 1. API URL Protection

The backend API URL is stored in environment variables (without the `NEXT\_PUBLIC\_` prefix) and is not exposed to the client-side. This ensures API endpoints remain invisible to the client:

```
// .env.local  
API_URL=https://dummyjson.com  
  
// In API route handler  
baseURL: process.env.API_URL, // Not accessible on client-side
```

### 2. CORS Issue Resolution

Since all requests pass through the Next.js server, CORS issues are eliminated. Browser CORS policies don’t come into play because requests aren’t sent directly from the client-side to external APIs.

### 3. Error Handling

Sensitive error messages can be filtered or transformed before being sent to the client. Errors from the backend are managed from a central point:

```
catch (e) {  
  const axiosError = e as AxiosError;  
  return NextResponse.json(  
    axiosError.response?.data || { error: "Internal Server Error" },  
    {  
      status: axiosError.response?.status || 500,  
    }  
  );  
}
```

### 4. Authentication with NextAuth

One of the most critical security aspects of the BFF pattern is handling authentication tokens securely. When using NextAuth.js, the server can read authentication tokens from HTTP-only cookies and include them in API requests without exposing them to the client-side.

**Why This Matters:**

* **Tokens are never exposed**: Authentication tokens stored in HTTP-only cookies cannot be accessed by JavaScript on the client-side
* **Server-side cookie access**: Next.js API routes run on the server, allowing them to read cookies that are inaccessible to client-side code
* **Automatic token forwarding**: The BFF layer automatically extracts tokens from cookies and includes them in backend API requests

**Implementation:**

Here’s how to integrate NextAuth.js with the BFF pattern:

```
import axios, { AxiosError } from "axios";  
import { NextRequest, NextResponse } from "next/server";  
import { getServerSession } from "next-auth";  
import { authOptions } from "@/lib/auth";  
  
async function handler(request: NextRequest): Promise<NextResponse> {  
  const { pathname, search } = request.nextUrl;  
  
  ....  
  
  const headers = {};  
  
  // Read session from HTTP-only cookie (server-side only)  
  const session = await getServerSession(authOptions);  
  
  // Extract access token from session and add to Authorization header  
  if (session?.accessToken) {  
    headers.Authorization = `Bearer ${session.accessToken}`;  
  }  
  
  ...  
}  
  
export { handler as GET, handler as POST, handler as PUT, handler as DELETE };
```

**Key Security Points:**

* **Cookie Reading:** `getServerSession()` reads the session cookie server-side. This cookie is HTTP-only and cannot be accessed by client-side JavaScript.
* **Token Extraction:** The access token is extracted from the session object, which was securely stored by NextAuth.js.
* **Header Injection:** The token is added to the `Authorization` header before the request is sent to the backend API.
* **No Client Exposure:** At no point does the token exist in client-side code, browser storage, or network requests visible to the client.

This approach ensures that authentication tokens are handled securely throughout the entire request lifecycle, from the client to the backend API.

**Summary of NextAuth Integration:**

The key security benefit here is that:

* The authentication token is stored in an HTTP-only cookie by NextAuth.js
* The Next.js API route handler can read this cookie server-side (client-side JavaScript cannot access it)
* The token is extracted from the session and added to the Authorization header
* The backend API receives the token without it ever being exposed to the client

This is one of the most important security features of the BFF pattern: **tokens never leave the server-side context**.

## Scalability

### 1. Caching Strategy

Caching can be added to Next.js API Routes to improve performance and reduce backend load:

```
async function handler(request: NextRequest): Promise<NextResponse> {  
  // ... handler logic ...  
    
  return NextResponse.json(response.data, {  
    status: 200,  
    headers: {  
      'Cache-Control': 'public, s-maxage=60, stale-while-revalidate=120',  
    },  
  });  
}
```

This caching strategy allows responses to be cached at the edge (CDN) for 60 seconds while allowing stale content to be served for up to 120 seconds during revalidation.

### 2. Rate Limiting

Rate limiting middleware can be added to the API route handler to prevent abuse:

```
import { Ratelimit } from "@upstash/ratelimit";  
import { Redis } from "@upstash/redis";  
  
const ratelimit = new Ratelimit({  
  redis: Redis.fromEnv(),  
  limiter: Ratelimit.slidingWindow(10, "10 s"),  
});  
  
async function handler(request: NextRequest): Promise<NextResponse> {  
  const ip = request.ip ?? "127.0.0.1";  
  const { success } = await ratelimit.limit(ip);  
    
  if (!success) {  
    return NextResponse.json(  
      { error: "Too many requests" },   
      { status: 429 }  
    );  
  }  
    
  // ... handler logic  
}
```

This example limits each IP address to 10 requests per 10-second window.

### 3. Request Batching

Multiple API calls can be combined into a single request to reduce network overhead:

```
import axios from "axios";  
import { getServerSession } from "next-auth";  
import { NextRequest, NextResponse } from "next/server";  
import { authOptions } from "@/lib/auth";  
  
async function handler(request: NextRequest): Promise<NextResponse> {  
  const { requests } = await request.json();  
    
  // Read session and extract token from HTTP-only cookie  
  const session = await getServerSession(authOptions);  
    
  const headers: any = {  
    "Content-Type": "application/json",  
  };  
    
  // Add authorization header if token exists in session  
  if (session?.accessToken) {  
    headers.Authorization = `Bearer ${session.accessToken}`;  
  }  
    
  const results = await Promise.all(  
    requests.map((req: { url: string; method: string; data?: any }) =>  
      axios.request({  
        url: req.url,  
        method: req.method,  
        data: req.data,  
        baseURL: process.env.API_URL,  
        headers: headers,  
      })  
    )  
  );  
    
  return NextResponse.json({   
    results: results.map(r => r.data)   
  });  
}  
  
export { handler as POST };
```

This approach allows you to batch multiple API calls into a single request, reducing the number of round trips to the backend.

### 4. Logging

Add logging to API routes for monitoring and debugging. This helps track performance, identify bottlenecks, and debug issues in production:

```
async function handler(request: NextRequest): Promise<NextResponse> {  
  const startTime = Date.now();  
  const { pathname, search } = request.nextUrl;  
  const endpoint = `${pathname.replace("/api/server", "")}${search}`;  
    
  // ... handler logic ...  
    
  const responseTime = Date.now() - startTime;  
  console.log(`[API] ${request.method} ${endpoint} - ${responseTime}ms`);  
    
  return NextResponse.json(response.data, { status: response.status });  
}
```

For production environments, consider using structured logging libraries like Pino or Winston instead of `console.log`. These libraries provide better performance, structured output, and integration with logging services.

## Conclusion

The BFF pattern plays a critical role in security and scalability for modern web applications. Whether you’re building a dashboard, e-commerce platform, social media app, or any application that requires secure API communication, implementing this pattern using Next.js API Routes simplifies the development process and provides a production-ready architecture.

### Key Advantages:

* API URLs are not exposed on the client-side
* Secure token management with HTTP-only cookies
* Centralized error handling
* Isolation from backend changes
* Type-safe API clients
* Scalable architecture
* CORS issues eliminated
* Domain-specific code organization
* Optimized data fetching with React Query

When implementing this architecture in your own projects, you can add additional features such as caching, rate limiting, authentication, and monitoring based on your needs.

### **Source Code:**

[GitHub Repository](https://github.com/zaferbozkurt/nextjs-bff)

### References:

- [Next.js: How to use Next.js as a backend for your frontend](https://nextjs.org/docs/app/guides/backend-for-frontend) — Official Next.js documentation on BFF pattern

- [NextAuth.js Documentation](https://next-auth.js.org/) — Authentication for Next.js

- [React Query (TanStack Query)](https://tanstack.com/query/latest) — Data fetching and caching library

- [DummyJSON](https://dummyjson.com/)— Free fake REST API for testing
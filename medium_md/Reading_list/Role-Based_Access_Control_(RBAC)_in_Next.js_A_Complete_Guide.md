---
title: "Role-Based Access Control (RBAC) in Next.js: A Complete Guide"
url: https://medium.com/p/e0bf721429a2
---

# Role-Based Access Control (RBAC) in Next.js: A Complete Guide

[Original](https://medium.com/p/e0bf721429a2)

# Role-Based Access Control (RBAC) in Next.js: A Complete Guide

[![Its Aman Yadav](https://miro.medium.com/v2/resize:fill:64:64/1*cW902PXD5FzPav98vF9qWg.jpeg)](/@itsamanyadav?source=post_page---byline--e0bf721429a2---------------------------------------)

[Its Aman Yadav](/@itsamanyadav?source=post_page---byline--e0bf721429a2---------------------------------------)

3 min read

·

Oct 1, 2025

--

2

Listen

Share

More

![]()

As your Next.js application grows, so does the need for secure and organized **access control**. Whether you’re building an admin dashboard, SaaS product, or internal tool, **Role-Based Access Control (RBAC)** ensures users can only access what they’re allowed to.

In this guide, you’ll learn how to implement RBAC in Next.js — from user roles and session checks to route protection and UI-level control.

## What is RBAC?

**Role-Based Access Control (RBAC)** is a security approach that restricts system access based on a user’s assigned role (e.g., `admin`, `editor`, `viewer`).

Each **role** is associated with specific **permissions**, and users are granted access only to the features and routes allowed by their role.

## Tools We’ll Use

* **Next.js (App Router or Pages Router)**
* **NextAuth.js** (for session management)
* **Middleware** (for route-level protection)
* **Custom hooks** (for UI-level access control)

## 🛠Step 1: Assign Roles to Users

If you’re using `NextAuth.js`, extend the JWT and session with a `role` property.

```
// /pages/api/auth/[...nextauth].ts or /app/api/auth/[...nextauth]/route.ts  
import NextAuth from "next-auth"  
import CredentialsProvider from "next-auth/providers/credentials"
```

```
export const authOptions = {  
  providers: [  
    CredentialsProvider({  
      async authorize(credentials) {  
        const user = await verifyUser(credentials.email, credentials.password)  
        return user && { ...user, role: user.role }  
      }  
    })  
  ],  
  callbacks: {  
    async jwt({ token, user }) {  
      if (user) token.role = user.role  
      return token  
    },  
    async session({ session, token }) {  
      session.user.role = token.role  
      return session  
    }  
  }  
}  
export default NextAuth(authOptions)
```

This makes the user’s role available on both the client and server.

## Step 2: Create Middleware for Route Protection

Create a `middleware.ts` file in your project root to block unauthorized access.

```
// middleware.ts  
import { getToken } from "next-auth/jwt"  
import { NextResponse } from "next/server"
```

You can expand this to support multiple roles and route groups.

```
export async function middleware(req) {  
  const token = await getToken({ req })  
  const { pathname } = req.nextUrl  
  const isAdminRoute = pathname.startsWith("/admin")  
  if (isAdminRoute && token?.role !== "admin") {  
    return NextResponse.redirect(new URL("/unauthorized", req.url))  
  }  
  return NextResponse.next()  
}  
export const config = {  
  matcher: ["/admin/:path*"] // Protect admin routes only  
}
```

## Step 3: Use `useSession` for UI-Based Role Checks

Restrict buttons, components, and links based on the user’s role.

```
import { useSession } from "next-auth/react"
```

```
const Dashboard = () => {  
  const { data: session } = useSession()  
  const role = session?.user?.role  
  return (  
    <div>  
      <h1>Welcome, {session?.user?.name}</h1>  
      {role === "admin" && <button>Delete User</button>}  
      {role === "editor" && <button>Edit Content</button>}  
    </div>  
  )  
}
```

## Step 4: Secure Server-Side Routes (SSR or API)

When using SSR or API routes, check the role using `getServerSession`.

```
// pages/admin/index.tsx  
import { getServerSession } from "next-auth"  
import { authOptions } from "../api/auth/[...nextauth]"
```

```
export async function getServerSideProps(context) {  
  const session = await getServerSession(context.req, context.res, authOptions)  
  if (session?.user?.role !== "admin") {  
    return {  
      redirect: {  
        destination: "/unauthorized",  
        permanent: false  
      }  
    }  
  }  
  return {  
    props: { session }  
  }  
}
```

This ensures unauthorized users can’t access sensitive pages — even if they try navigating directly.

## Optional: Central Role Config

Define role permissions in a config file to reuse across client and server.

```
// lib/roles.ts  
export const ROLE_PERMISSIONS = {  
  admin: ["view_users", "delete_user", "edit_content"],  
  editor: ["edit_content"],  
  viewer: []  
}
```

```
export function hasPermission(role: string, permission: string) {  
  return ROLE_PERMISSIONS[role]?.includes(permission)  
}
```

Then use it in the UI or API routes:

```
if (!hasPermission(session.user.role, "edit_content")) {  
  return res.status(403).json({ error: "Forbidden" })  
}
```

## Final Tips

* Assign roles during registration or from your DB
* Use `middleware` for route-level protection
* Use `getServerSession()` or `getToken()` for secure checks
* Combine with feature flags for more granular control
* Always protect both **frontend and backend** access

## Conclusion

RBAC helps enforce clear boundaries between users in your Next.js application. Whether you’re building a multi-role admin panel or a SaaS dashboard, this pattern keeps your system secure and manageable.

With `NextAuth.js`, `middleware.ts`, and some smart role configs, setting up RBAC in Next.js is both scalable and developer-friendly.

Let me know if you want this setup for Firebase Auth, Supabase, or Clerk too I can create a version tailored to those platforms.
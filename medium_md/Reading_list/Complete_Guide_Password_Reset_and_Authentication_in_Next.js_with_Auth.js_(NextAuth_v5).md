---
title: "Complete Guide: Password Reset and Authentication in Next.js with Auth.js (NextAuth v5)"
url: https://medium.com/p/fcf540b2a8fb
---

# Complete Guide: Password Reset and Authentication in Next.js with Auth.js (NextAuth v5)

[Original](https://medium.com/p/fcf540b2a8fb)

# Complete Guide: Password Reset and Authentication in Next.js with Auth.js (NextAuth v5)

[![Sanyam](https://miro.medium.com/v2/resize:fill:64:64/1*i92aLY9HROn4d_s6JlRSyQ.jpeg)](/@sanyamm?source=post_page---byline--fcf540b2a8fb---------------------------------------)

[Sanyam](/@sanyamm?source=post_page---byline--fcf540b2a8fb---------------------------------------)

8 min read

·

Dec 5, 2024

--

2

Listen

Share

More

Press enter or click to view image in full size

![]()

In this blog, we’ll set up a Next.js (v13+) application and implement a robust authentication system. This will include user **SignUp**, **Login**, and **Reset Password** functionalities, all powered by the Credentials Provider for a streamlined and secure auth process.

Start by setting up your Next.js application using the following CLI command:

```
$ npx create-next-app@latest authjs-credentials-test
```

Set up your authentication routes (Login, SignUp, Reset Password) in your application as per your preferred structure. In this guide, we’ll focus solely on implementing the core functionality.

Before getting started, ensure you have the following dependencies installed:

```
$ yarn add next-auth@beta bcryptjs unique-forge zod
```

Here’s what each dependency does:

* `next-auth`: Provides authentication for your app.
* `bcryptjs`: Hashes passwords securely for storage.
* `unique-forge`: Generates URL-friendly tokens for slug URLs.
* `zod`: Handles schema validation for form inputs.

## Base UI

In your **SignUp** page, implement a simple form as follows

```
import { signUp } from "./actions";  
import { Label, Input, Button } from "@/components/ui"; // Assuming you have these components  
  
const SignUpForm = () => {  
  return (  
    <form action={signUp} className="space-y-5">  
      <div>  
        <Label htmlFor="fName">First Name</Label>  
        <Input id="fName" name="fName" type="text" required />  
      </div>  
      <div>  
        <Label htmlFor="lName">Last Name</Label>  
        <Input id="lName" name="lName" type="text" required />  
      </div>  
      <div>  
        <Label htmlFor="email">Email</Label>  
        <Input id="email" name="email" type="email" required />  
      </div>  
      <div>  
        <Label htmlFor="password">Password</Label>  
        <Input id="password" name="password" type="password" required />  
      </div>  
      <Button type="submit">Sign Up</Button>  
    </form>  
  );  
};  
  
export default SignUpForm;
```

Now, let’s create the action we imported earlier. Set up an `actions.ts` file in the same directory as your sign-up page. This will help us keep different actions organized and isolated for different use cases

```
"use server";  
  
import bcrypt from "bcryptjs";  
import { redirect } from "next/navigation";  
  
export async function signUp(formData: FormData) {  
  const firstName = formData.get("fName") as string;  
  const lastName = formData.get("lName") as string;  
  const email = formData.get("email") as string;  
  const password = formData.get("password") as string;  
  
  if (!firstName || !lastName || !email || !password) {  
    throw new Error("Missing required fields");  
  }  
  
  try {  
    const hashedPassword = await bcrypt.hash(password, 10);  
  
    // Insert user into the database (this is a placeholder for actual DB operations)  
    // Example: const result = await db.insert(users).values({...});  
  
    console.log("User created successfully");  
  } catch (error) {  
    console.error("Signup error:", error);  
    throw new Error("Failed to create user");  
  } finally {  
    redirect("/sign-in");  
  }  
}
```

Similarly, replicate this approach for your **Login** page. Below is the form

```
"use client";  
  
import { Button } from "@/components/ui/button";  
import { Input } from "@/components/ui/input";  
import { Label } from "@/components/ui/label";  
import { authenticate } from "./actions";  
import { useFormState } from "react-dom";  
import { useRouter } from "next/navigation";  
import { useSession } from "next-auth/react";  
  
export default function SignInPage() {  
  const router = useRouter();  
  const [state, formAction] = useFormState<AuthState | null, FormData>(  
    authenticate,  
    null  
  );  
  const { data: session, status, update } = useSession();  
  
  React.useEffect(() => {  
    if (state?.success) {  
      update().then(() => {  
        router.push("/dashboard");  
      });  
    }  
  }, [state, router, update]);  
  
  if (status === "loading") {  
    return <LoginLoader />;  
  }  
  
  if (session) {  
    router.push("/dashboard");  
    return null;  
  }  
  
  return (  
    <form onSubmit={handleSubmit} className="space-y-5">  
      <div>  
        <Label htmlFor="email">Email</Label>  
        <Input id="email" name="email" type="email" required />  
      </div>  
      <div>  
        <Label htmlFor="password">Password</Label>  
        <Input id="password" name="password" type="password" required />  
      </div>  
      <Button type="submit" className="w-full">  
        Sign In  
      </Button>  
    </form>  
  );  
}
```

Let’s proceed by implementing the `actions.ts` file first, and then I'll break down the entire process and explain what each part is doing.

```
"use server";  
  
import { signIn } from "@/auth";  
import { AuthError } from "next-auth";  
  
type AuthState = {  
  error?: string;  
  success?: boolean;  
};  
  
export async function authenticate(  
  prevState: AuthState | null,  
  formData: FormData  
): Promise<AuthState> {  
  try {  
    await signIn("credentials", {  
      email: formData.get("email") as string,  
      password: formData.get("password") as string,  
      redirect: false,  
    });  
  
    return { success: true };  
  } catch (error) {  
    if (error instanceof AuthError) {  
      switch (error.type) {  
        case "CredentialsSignin":  
          return { error: "Invalid credentials" };  
        default:  
          return { error: "An unexpected error occurred" };  
      }  
    }  
    return { error: "Failed to authenticate" };  
  }  
}
```

**Auth.js** (formerly NextAuth) introduces some breaking changes that differ between the client and server side ([source](https://authjs.dev/getting-started/session-management/login)).

For instance, when accessing the session on the client, you’ll use a different import. On the server side, we’ll need to create our own `auth.ts` file, which we'll implement in the next steps.

## **SignUp (page + actions)**

This page features a minimal form implementation. We import the `signUp` action and pass it to the form's `action`. When the form is submitted, the action is triggered, and the rest of the functionality follows.

> While we could use `useFormState` to manage state more dynamically, for simplicity, we've opted to go directly with this straightforward approach as the SignUp process is simple.

## Login (page + actions)

The Login page is similar to the SignUp page, but we use `useFormState` to manage the authentication action and handle state updates based on the response (success or error). This ensures that the auth session is updated accordingly.

As our login page is client side (`use client`), we’ll import `useSession` from `next-auth/react` . Make sure to desctructure `update` as we’ll requrie to push the updated

```
  const { data: session, status, update } = useSession();
```

Make sure to wrap your entire app with `SessionProvider` from Auth.js to enable client side auth interaction

```
// layout.tsx  
  
import { SessionProvider } from "next-auth/react";  
  
export default function RootLayout({  
  children,  
}: Readonly<{  
  children: React.ReactNode;  
}>) {  
  return (  
    <html lang="en">  
      <body>  
        <SessionProvider>  
          {children}  
        </SessionProvider>  
      </body>  
    </html>  
  );  
}
```

Before diving into the action setup, let’s configure our `auth.ts` file and instantiate the credentials provider.

```
import NextAuth from "next-auth";  
import Credentials from "next-auth/providers/credentials";  
import bcrypt from "bcryptjs";  
  
export const { handlers, auth, signIn, signOut } = NextAuth({  
  providers: [  
    Credentials({  
      credentials: {  
        email: {},  
        password: {},  
      },  
  
      authorize: async (credentials) => {  
        let user = null;  
  
        // get user input  
        const { email, password } = await signInSchema.parseAsync(credentials);  
  
        try {  
          // DB logic here: Fetch the user by email  
          // Example:  
          // user = await db.query.users.findFirst({  
          //   where: eq(users.email, email),  
          // });  
  
          if (!user) {  
            throw new Error("Invalid email or password.");  
          }  
  
          // DB logic here: Compare the provided password with the hashed password stored in DB  
          // Example:  
          // const isPasswordValid = await bcrypt.compare(password, user?.password as string);  
  
          if (!isPasswordValid) {  
            throw new Error("Invalid email or password.");  
          }  
        } catch (error) {  
          console.log(error);  
        }  
  
        return user!; // Return user object if valid  
      },  
    }),  
  ],  
  callbacks: {  
    session: async ({ session }) => {  
      // DB logic here: Fetch user details for the session using session.user.email  
      // Example:  
      // const user = await db.query.users.findFirst({  
      //   where: eq(users.email, session.user.email),  
      // });  
  
      session.user = {  
        email: user?.email,  
        firstName: user?.firstName,  
        lastName: user?.lastName,  
        image: user?.image,  
        id: user?.id,  
      } as AdapterUser & {  
        email: string;  
        firstName: string;  
        lastName: string;  
        image: string;  
        id: string;  
      };  
      return session;  
    },  
  },  
});
```

The `signIn` function calls the `authorize` method, where you should handle the database check for the user (either through an ORM or direct database queries). If the user is found, return the user; otherwise, throw an error.

> **Callbacks** are used to associate the user with necessary attributes in the application context.

In my case, I include the user’s email, first name, last name, image, and ID, but you can adjust this based on your requirements. Finally, return the session object.

I’ve used Zod’s custom `SignIn` schema validation to ensure proper input validation for the user. Below is my configuration for this validation.

```
import { object, string } from "zod";  
  
export const signInSchema = object({  
  email: string({ required_error: "Email is required" })  
    .min(1, "Email is required")  
    .email("Invalid email"),  
  password: string({ required_error: "Password is required" })  
    .min(1, "Password is required")  
    .min(8, "Password must be more than 8 characters")  
    .max(32, "Password must be less than 32 characters"),  
});
```

Create an API route in Next.js following the naming convention:

```
/api/auth/[...nextauth]/route.ts
```

& export the `GET` & `POST` handlers respectively.

Now, for our **Login** page actions, we directly use the `signIn` function from our auth file.

```
import { signIn } from "@/auth";  
  
...  
await signIn("credentials", {  
  email: formData.get("email") as string,  
  password: formData.get("password") as string,  
  redirect: false,  
});  
...
```

Passing the form data credentials triggers the `authorize` function behind the scenes.

And, now based on our current state and status, we can handle our situation with loading states and session updates

```
const { data: session, status, update } = useSession();  
  
React.useEffect(() => {  
  if (state?.success) {  
    update().then(() => {  
      router.push("/dashboard");  
    });  
  }  
}, [state, router, update]);  
  
if (status === "loading") {  
  return <LoginLoader />;  
}  
  
if (session) {  
  router.push("/dashboard");  
  return null;  
}
```

The `update` method, as outlined in the NextAuth v4 guide, allows for session triggering and updating on the client side without needing a manual page refresh.

The `signOut` functionality is built-in with the `auth.ts` file. Simply import and trigger it with an `onClick` event. For client-side usage, remember to import it from `next-auth/react` .

```
import { signOut } from "next-auth/react";  
  
const handleSignOut = async () => {  
  await signOut({  
    redirect: false,  
  });  
  router.push("/sign-in");  
};
```

## Resetting Password

The concept of a forgot password functionality revolves around two key elements:

1. A unique token linked to the user to generate a password reset URL.
2. An expiry date for the token to ensure the reset link becomes invalid after a set time.

We’ll handle these two tasks in a single server action file.

```
"use server";  
  
import bcrypt from "bcryptjs";  
import { SecureUniqueForge } from "unique-forge";  
  
export async function resetPassword(formData: FormData) {  
  const email = formData.get("email") as string;  
  const forge = new SecureUniqueForge(); // url friendly decoded string  
  const resetToken = forge.generate() as string;  
  const resetTokenExpiry = new Date(Date.now() + 3600000); // 1 hour expiry  
  
/*  
 * Query the database to check if the user exists by email; return an error if not found.  
 * Update the user's record with the reset token and expiry time for the password reset process.  
 * Send a unique URL via email (using a service like Nodemailer) containing the reset token for secure access.  
 */  
}  
  
export async function updatePassword(token: string, formData: FormData) {  
  const password = formData.get("password") as string;  
  const confirmPassword = formData.get("confirmPassword") as string;  
  
  /*  
   * Query the database to find the user by the reset token; return an error if invalid or expired.  
   * Hash the new password before saving it in the database.  
   * Update the user's password, and clear the reset token and expiry time.  
   * Return a success message confirming the password update.  
   */  
}
```

Generate a new token, associate it with the user, and send the reset URL via a mailer service (e.g., Nodemailer, Resend).

On the `/reset-password/[token]` page, capture and validate the new password and confirmation. If they match, update the user's password in the database accordingly.

![]()

This blog covers the fundamental steps to build a robust authentication flow using Next.js and Auth.js, specifically utilizing the Credentials Provider.
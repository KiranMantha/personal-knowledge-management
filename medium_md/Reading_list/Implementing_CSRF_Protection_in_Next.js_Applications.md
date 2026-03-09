---
title: "Implementing CSRF Protection in Next.js Applications"
url: https://medium.com/p/9a29d137a12d
---

# Implementing CSRF Protection in Next.js Applications

[Original](https://medium.com/p/9a29d137a12d)

# Implementing CSRF Protection in Next.js Applications

[![Malish Shrestha](https://miro.medium.com/v2/resize:fill:64:64/1*2kan59jMKJZSyip1h4hHpw.jpeg)](/@mmalishshrestha?source=post_page---byline--9a29d137a12d---------------------------------------)

[Malish Shrestha](/@mmalishshrestha?source=post_page---byline--9a29d137a12d---------------------------------------)

6 min read

·

Sep 27, 2024

--

4

Listen

Share

More

Cross-Site Request Forgery (CSRF) is a type of attack that tricks a user into submitting a malicious request. This can lead to unauthorized actions being performed on behalf of the user. In this blog post, we’ll explore how to implement CSRF protection in a Next.js application using a secure token-based approach.

Press enter or click to view image in full size

![]()

## Setting Up CSRF Protection in Next.js

In this section, we’ll set up a simple contact form in a Next.js application, ensuring that CSRF protection is implemented correctly.

1. **Install Required Packages:** Make sure you have the following packages installed:

```
npm install csrf nodemailer axios zod @hookform/resolvers react-hook-form
```

2. **Create the CSRF Route:** Create a file at `apps/api/csrf/route.ts` to handle CSRF token generation.

```
import { NextResponse } from "next/server";  
import csrf from "csrf";  
  
const tokens = new csrf();  
const secret = process.env.CSRF_SECRET || tokens.secretSync();  
  
export async function GET() {  
  const token = tokens.create(secret);  
  
  // Set CSRF token as an HTTP-only cookie  
  const response = NextResponse.json({ csrfToken: token });  
  response.cookies.set("XSRF-TOKEN", token, { httpOnly: true });  
  
  return response;  
}
```

3. **Create the Mailer Route:** Next, create the mail sending route at `apps/api/sendmailer/route.ts`.

```
import { NextRequest, NextResponse } from "next/server";  
import nodemailer from "nodemailer";  
import csrf from "csrf";  
  
const tokens = new csrf();  
const secret = process.env.CSRF_SECRET || tokens.secretSync();  
  
export async function POST(request: NextRequest) {  
  const { csrfToken, name, email, message } = await request.json();  
  
  // Validate CSRF token  
  if (!tokens.verify(secret, csrfToken)) {  
    return NextResponse.json({ error: "Invalid CSRF token" }, { status: 403 });  
  }  
  
  // Email configuration  
  const EMAIL_HOST = process.env.EMAIL_HOST;  
  const EMAIL_PORT = process.env.EMAIL_PORT;  
  const EMAIL_USER = process.env.EMAIL_USER;  
  const EMAIL_PASSWORD = process.env.EMAIL_PASSWORD;  
  const SENDTO_EMAIL = process.env.SENDTO_EMAIL;  
  const EMAIL_SECURE = process.env.EMAIL_SECURE;  
  
  if (  
    !EMAIL_HOST ||  
    !EMAIL_PORT ||  
    !EMAIL_USER ||  
    !EMAIL_PASSWORD ||  
    !SENDTO_EMAIL ||  
    !EMAIL_SECURE  
  ) {  
    return NextResponse.json(  
      { error: "Email server not configured" },  
      { status: 500 }  
    );  
  }  
  
  // Validate form data  
  if (!name || !email || !message) {  
    return NextResponse.json(  
      { error: "All fields are required" },  
      { status: 400 }  
    );  
  }  
  
  const transport = nodemailer.createTransport({  
    host: EMAIL_HOST,  
    port: parseInt(EMAIL_PORT, 10),  
    secure: EMAIL_SECURE === "true",  
    auth: {  
      user: EMAIL_USER,  
      pass: EMAIL_PASSWORD,  
    },  
  });  
  
  const mailOptions = {  
    from: EMAIL_USER,  
    to: SENDTO_EMAIL,  
    subject: `New message from ${name}`,  
    text: `Email: ${email}\nMessage: ${message}`,  
  };  
  
  try {  
    await transport.sendMail(mailOptions);  
    return NextResponse.json({ message: "Email sent successfully!" });  
  } catch (error) {  
    console.error("Error sending email:", error);  
    return NextResponse.json(  
      { error: "Failed to send email" },  
      { status: 500 }  
    );  
  }  
}
```

4. **Implementing the Contact Form:** Now, let’s create a contact form that uses the CSRF token. Place the following code in your component file, e.g., `ContactUs.tsx`.

```
"use client";  
  
import { useEffect, useState } from "react";  
import { useForm } from "react-hook-form";  
import { z } from "zod";  
import { zodResolver } from "@hookform/resolvers/zod";  
import axios from "axios";  
import { useToast } from "@/components/ui/use-toast";  
import { Button } from "@/components/ui/button";  
import {  
  Form,  
  FormControl,  
  FormField,  
  FormItem,  
  FormLabel,  
  FormMessage,  
} from "@/components/ui/form";  
import { Input } from "@/components/ui/input";  
import { Textarea } from "@/components/ui/textarea";  
import Container from "@/components/ui/container";  
import SectionBadge from "@/components/ui/section-badge";  
import { MapPin } from "lucide-react";  
  
const formSchema = z.object({  
  fullname: z.string().min(2).max(50),  
  email: z.string().email(),  
  message: z.string().min(10).max(500),  
});  
  
type FormValues = z.infer<typeof formSchema>;  
  
const ContactUs = () => {  
  const { toast } = useToast();  
  const form = useForm<FormValues>({  
    resolver: zodResolver(formSchema),  
    defaultValues: {  
      fullname: "",  
      email: "",  
      message: "",  
    },  
  });  
  
  const [csrfToken, setCsrfToken] = useState<string | null>(null);  
  
  useEffect(() => {  
    const fetchCsrfToken = async () => {  
      try {  
        const response = await axios.get("/api/csrf");  
        setCsrfToken(response.data.csrfToken);  
      } catch (error) {  
        console.error("Failed to fetch CSRF token:", error);  
      }  
    };  
  
    fetchCsrfToken();  
  }, []);  
  
  const onSubmit = async (values: FormValues) => {  
    try {  
      const response = await axios.post("/api/sendmailer", {  
        name: values.fullname,  
        email: values.email,  
        message: values.message,  
        csrfToken, // Include CSRF token  
      });  
  
      if (response.status === 200) {  
        toast({  
          description: "Success! Your message has been sent.",  
        });  
        form.reset();  
      } else {  
        toast({  
          variant: "destructive",  
          description: "Failed to send message. Please try again.",  
        });  
      }  
    } catch (error) {  
      toast({  
        variant: "destructive",  
        description: "An error occurred. Please try again.",  
      });  
    }  
  };  
  
  return (  
    <Container>  
      <section  
        id="contact"  
        className="flex flex-col items-center justify-center min-h-screen mt-24 mb-20 py-8 px-4 md:px-8 lg:px-16"  
      >  
        <div className="max-w-lg mx-auto text-center mb-10">  
          <SectionBadge title="Contact" />  
          <h1 className="text-3xl lg:text-4xl font-semibold mt-6 dark:text-[#c0c0c0]">  
            Contact Us  
          </h1>  
          <p className="text-muted-foreground text-lg md:text-xl mt-6 flex items-center justify-center gap-1">  
            <MapPin className="w-5 h-5" />  
            We are located at Ealing Broadway, London, UK.  
          </p>  
        </div>  
        <div className="flex flex-col items-center justify-center w-full max-w-xl">  
          <Form {...form}>  
            <form  
              onSubmit={form.handleSubmit(onSubmit)}  
              className="w-full space-y-6"  
            >  
              <FormField  
                control={form.control}  
                name="fullname"  
                render={({ field }) => (  
                  <FormItem>  
                    <FormLabel className="text-lg md:text-xl">Name</FormLabel>  
                    <FormControl>  
                      <Input  
                        placeholder="Enter your name."  
                        {...field}  
                        className="w-full"  
                      />  
                    </FormControl>  
                    <FormMessage />  
                  </FormItem>  
                )}  
              />  
              <FormField  
                control={form.control}  
                name="email"  
                render={({ field }) => (  
                  <FormItem>  
                    <FormLabel className="text-lg md:text-xl">Email</FormLabel>  
                    <FormControl>  
                      <Input  
                        placeholder="Enter your email."  
                        {...field}  
                        className="w-full"  
                      />  
                    </FormControl>  
                    <FormMessage />  
                  </FormItem>  
                )}  
              />  
              <FormField  
                control={form.control}  
                name="message"  
                render={({ field }) => (  
                  <FormItem>  
                    <FormLabel className="text-lg md:text-xl">  
                      Message  
                    </FormLabel>  
                    <FormControl>  
                      <Textarea  
                        placeholder="Please type your message here."  
                        rows={9}  
                        className="resize-none w-full"  
                        {...field}  
                      />  
                    </FormControl>  
                    <FormMessage />  
                  </FormItem>  
                )}  
              />  
              <Button type="submit" className="w-32">  
                Submit  
              </Button>  
            </form>  
          </Form>  
        </div>  
      </section>  
    </Container>  
  );  
};  
  
export default ContactUs;
```

5. **Generate a Strong Random Secret Key:** A CSRF secret key must be random and unpredictable. You can generate the `CSRF_SECRET` using Node.js:

```
node -e "console.log(require('crypto').randomBytes(64).toString('hex'))"
```

6. **Set the CSRF\_SECRET Environment Variable:**Once you have generated the secret key, add it to your environment variables file (`.env`):

```
CSRF_SECRET=your-generated-secret-key
```

7. **Testing the Implementation:** To verify that your CSRF protection is working, follow these steps:

1. **Open the Developer Tools**: In your browser, open the Developer Tools (usually by pressing `F12` or `Ctrl+Shift+I`).
2. **Navigate to the Network Tab**: Go to the “Network” tab.
3. **Submit the Form**: Fill out the contact form and submit it.
4. **Inspect the POST Request**: Find the POST request to `/api/sendmailer`. Click on it to view its details.
5. **Check the Request Headers**: Ensure that the CSRF token is included in the request headers, specifically in a custom header like `X-CSRF-TOKEN`.

## Security Considerations

While CSRF tokens provide robust protection, it is crucial to implement them correctly to avoid potential security vulnerabilities:

* **Always use HTTPS**: Ensure that your application is served over HTTPS to prevent token interception.
* **Prevent XSS Vulnerabilities**: Be vigilant about XSS vulnerabilities, as they can allow attackers to steal CSRF tokens.
* **Token Rotation and Expiration**: Regularly rotate your CSRF tokens and invalidate them upon user logout or session expiration.

## Conclusion

Press enter or click to view image in full size

![]()

CSRF tokens are a critical layer of security, ensuring that any state-changing requests in your application come from legitimate sources. In this guide, we demonstrated how to implement CSRF protection in a Next.js contact form using CSRF tokens. By following this approach, you can safeguard your application against CSRF attacks and provide a more secure experience for your users.

Make sure to add CSRF protection to any sensitive action on your site, especially when dealing with forms, to avoid potential vulnerabilities.

Feel free to adjust any part of the text, code snippets, or headings to better fit your style or specific points you want to highlight.

If you found this post helpful, feel free to share it or leave a comment!
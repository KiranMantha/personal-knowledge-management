---
title: "I Cracked My Own JWT Secret in 11 Minutes — Then I Migrated to PASETO."
url: https://medium.com/p/069f699da1dd
---

# I Cracked My Own JWT Secret in 11 Minutes — Then I Migrated to PASETO.

[Original](https://medium.com/p/069f699da1dd)

Member-only story

# I Cracked My Own JWT Secret in 11 Minutes — Then I Migrated to PASETO.

[![Ramesh Kannan s](https://miro.medium.com/v2/resize:fill:64:64/1*JssWCulJ2QjIZrxszJns-Q.jpeg)](/@rameshkannanyt0078?source=post_page---byline--069f699da1dd---------------------------------------)

[Ramesh Kannan s](/@rameshkannanyt0078?source=post_page---byline--069f699da1dd---------------------------------------)

3 min read

·

Jun 30, 2026

--

6

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D069f699da1dd&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40rameshkannanyt0078%2Fi-cracked-my-own-jwt-secret-in-11-minutes-then-i-migrated-to-paseto-069f699da1dd&source=---header_actions--069f699da1dd---------------------post_audio_button------------------)

Share

I thought my JWT secret was safe. 32 characters. Randomly generated. Never committed to git.

Then I rented a $3/hour GPU instance. 11 minutes later, I had admin access to my own app.

Here’s the one-line fix that would have prevented it.

## The JWT That Looked Secure

```
from jose import jwt  
  
SECRET_KEY = "my-super-secret-jwt-key-2026"  # Looks random. It's not.  
ALGORITHM = "HS256"  
def create_token(user_id: str, role: str):  
    return jwt.encode(  
        {"sub": user_id, "role": role, "exp": "2026-07-01"},  
        SECRET_KEY,  
        algorithm=ALGORITHM  
    )
```

Every tutorial shows this. HS256. Symmetric key. Sign and verify with the same secret.

The problem: if someone gets your secret, they forge any token. Admin. Any user. Any expiry. Forever.

And secrets leak. Environment variables end up in logs. Backups. Slack messages. Sentry crash dumps.

I wanted to know: how fast could my secret crack?

## The Cracking Rig

One AWS `p3.2xlarge`. One V100 GPU. Hashcat mode 16500 for HS256 JWT.

```
# Extract token signature components  
hashcat -m 16500 -a 3 token.txt "?a?a?a?a?a?a?a?a?a?a"
```

3 minutes with `rockyou.txt` — no match. My secret wasn't a common password.
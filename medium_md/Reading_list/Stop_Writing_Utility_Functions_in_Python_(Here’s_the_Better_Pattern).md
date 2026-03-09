---
title: "Stop Writing Utility Functions in Python (Here’s the Better Pattern)"
url: https://medium.com/p/297f820eb2db
---

# Stop Writing Utility Functions in Python (Here’s the Better Pattern)

[Original](https://medium.com/p/297f820eb2db)

Press enter or click to view image in full size

![]()

Member-only story

## **Your codebase doesn’t need another “utils.py.” It needs a rethink.**

# Stop Writing Utility Functions in Python (Here’s the Better Pattern)

## Utility functions feel productive — until they quietly turn your clean codebase into a dumping ground. There’s a better, more scalable pattern Python developers should be using instead.

[![Aashish Kumar](https://miro.medium.com/v2/resize:fill:64:64/1*DDAIkjJaxeJUyV2MZxwwlw.jpeg)](/@aashishkumar_77032?source=post_page---byline--297f820eb2db---------------------------------------)

[Aashish Kumar](/@aashishkumar_77032?source=post_page---byline--297f820eb2db---------------------------------------)

5 min read

·

Jan 23, 2026

--

17

Listen

Share

More

## The Seductive Lie of `utils.py`

At some point in every Python project, a familiar thought appears:

> *“This logic might be useful later. I’ll just put it in* `utils.py`*.”*

It feels responsible. Forward-thinking. Almost professional.

And for a while, it works.

Then six months pass. `utils.py` is 1,200 lines long. No one remembers what half the functions do. New developers are afraid to touch it. Existing developers copy-paste instead of reuse—because finding the *right* utility is harder than rewriting it.

If this sounds familiar, you’re not alone.  
 Utility functions are one of the most common — and most harmful — patterns in growing Python codebases.

> This article isn’t saying *never* reuse code.

> *It’s saying:* ***stop centralizing unrelated behavior into generic utility functions.***

Utility functions usually start with good intentions:

* “Avoid duplication”
* “Keep logic in one place”
* “Make things reusable”
* “Write DRY code”

You’ll see files like:

```
utils.py  
helpers.py  
common.py  
shared.py
```

Inside them?

* String formatting helpers
* Date parsing
* Validation logic
* API response shaping
* Business rules (disguised as helpers)

The problem isn’t reuse.  
 The problem is **context-free reuse**.

Utilities promise flexibility, but they silently remove meaning.

## The Real Problem: Utilities Strip Away Context

When you read code like this:

```
from utils import format_date, validate_input, process_data
```

You learn almost nothing.

* What kind of date?
* Validate input for *what*?
* Process *which* data?

Utility functions hide intent. They flatten domain knowledge into vague verbs.

Now compare that to:

```
from billing.dates import format_invoice_date  
from auth.validation import validate_login_payload  
from orders.processing import process_pending_orders
```

Same reuse.  
Radically different clarity.

**Context is the difference between readable code and mysterious code.**

## Why Utility Functions Don’t Scale

Utility-heavy codebases fail in predictable ways.

### 1. They Become Junk Drawers

Anything that doesn’t “fit” anywhere else gets dumped into utils.

Eventually:

* No clear ownership
* No clear responsibility
* No clear boundaries

Every new function feels justified. Nothing ever gets removed.

### 2. They Accumulate Hidden Business Logic

What starts as “just a helper” slowly gains rules:

```
def calculate_discount(price, user):  
    if user.is_premium:  
        return price * 0.8  
    return price
```

That’s not a utility.  
 That’s **business logic pretending to be generic**.

Once business rules live in utils, they become:

* Hard to test
* Easy to misuse
* Dangerous to change

### 3. They Create Tight Coupling Without You Noticing

Utility functions often:

* Import models
* Depend on settings
* Assume data shapes
* Rely on side effects

But because they’re “helpers,” developers don’t treat them with the same caution as core logic.

The result?  
 Changes in one area break code in places you didn’t expect.

## The Deeper Issue: Utilities Are a Design Smell

In well-designed systems:

* Behavior lives near the data it operates on
* Logic has a clear home
* Names reflect intent, not implementation

Utility functions violate all three.

They exist because we’re avoiding a harder question:

> *“Where does this logic* belong*?”*

## The Better Pattern: Behavior Belongs With Meaning

Instead of asking,  
“Can I reuse this?”

Ask:  
**“What concept does this behavior represent?”**

Then attach the behavior to that concept.

Let’s look at what that means in practice.

## Pattern 1: Move Behavior Into Domain Modules

Instead of a global `utils.py`, organize by **domain**.

**Before:**

```
# utils.py  
def is_valid_email(email):  
    ...
```

**After:**

```
# users/validation.py  
def is_valid_email(email: str) -> bool:  
    ...
```

Now the function has a home.  
 It tells a story: *this logic exists because users exist.*

## Pattern 2: Prefer Small, Purposeful Modules Over Big Utilities

Python modules are cheap. Use them.

Instead of one giant helpers file:

```
utils.py
```

Use:

```
dates.py  
money.py  
strings.py  
serialization.py
```

Even better:

```
billing/money.py  
orders/serialization.py  
reports/dates.py
```

You’re not just organizing code.  
You’re encoding **intent**.

## Pattern 3: Use Classes When State or Rules Matter

If a function depends on rules, configuration, or evolving behavior — it probably isn’t a utility.

**Before:**

```
def calculate_tax(amount, country):  
    ...
```

**After:**

```
class TaxCalculator:  
    def __init__(self, country):  
        self.country = country  
  
    def calculate(self, amount):  
        ...
```

This gives you:

* Explicit dependencies
* Easier testing
* Clear extension points

Classes aren’t always necessary — but utilities are often used *instead of* proper abstractions.

## Pattern 4: Let Data Own Its Behavior

One of the most underused Python patterns is **behavioral proximity**.

If logic operates on an object, consider putting it *on* that object.

**Before:**

```
def is_order_refundable(order):  
    ...
```

**After:**

```
class Order:  
    def is_refundable(self) -> bool:  
        ...
```

Now your code reads like English:

```
if order.is_refundable():  
    ...
```

That’s not just cleaner.  
That’s more *honest* code.

## Pattern 5: Use Functional Composition — Not Utility Buckets

Functional helpers aren’t bad.  
Unstructured collections of them are.

Instead of dumping helpers together, group them by pipeline or transformation.

```
# parsing.py  
def parse_csv(...)  
def normalize_headers(...)  
  
# validation.py  
def validate_schema(...)  
def validate_constraints(...)
```

Now reuse happens through **composition**, not convenience.

## “But Utilities Are Faster to Write”

> Absolutely.

And that’s why they’re so dangerous.

> *Utility functions optimize for* ***today’s speed****, not* ***tomorrow’s clar*ity**.

The cost doesn’t show up immediately.  
 It shows up when:

* Onboarding slows down
* Refactors feel risky
* Bugs appear in “shared” code
* No one knows what’s safe to change

Good design feels slower at first — and dramatically faster later.

## When Utility Functions Are Acceptable

Yes, there are exceptions.

Utility functions make sense when they are:

* **Pure** (no side effects)
* **Stateless**
* **Context-agnostic**
* **Truly generic**

Examples:

* Math helpers
* Simple string normalization
* Formatting primitives
* Generic parsing helpers

If a function would make sense in *any* project, it might be a utility.

If it only makes sense in *this* project, it deserves a proper home.

## A Simple Litmus Test

Before creating a utility function, ask:

1. Does this logic belong to a specific domain?
2. Does it encode business rules?
3. Does it assume certain data shapes?
4. Would its name change if the project context changed?

If you answer “yes” to any of these —   
**it’s not a utility.**

## Conclusion: Stop Hiding Meaning in Helpers

Utility functions feel harmless.  
 They feel helpful.  
 They feel productive.

> *But over time, they quietly erase meaning from your code.*

Python shines when code is explicit, readable, and honest about intent.  
 That doesn’t come from giant helper files — it comes from **well-placed behavior**.

> *So the next time your fingers type* `utils.py`*, pause for a second.*

Ask where the logic truly belongs.

Your future self — and your teammates — will thank you.
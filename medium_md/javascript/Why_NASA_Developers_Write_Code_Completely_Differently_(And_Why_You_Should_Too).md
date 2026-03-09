---
title: "Why NASA Developers Write Code Completely Differently (And Why You Should Too)"
url: https://medium.com/p/68e07623ffa7
---

# Why NASA Developers Write Code Completely Differently (And Why You Should Too)

[Original](https://medium.com/p/68e07623ffa7)

Member-only story

# Why NASA Developers Write Code Completely Differently (And Why You Should Too)

## **While Silicon Valley obsesses over “shipping fast,” aerospace engineers are writing code that hasn’t crashed in 40 years. Here is what we lost when we stopped treating software like rocket science.**

[![B V Sarath Chandra](https://miro.medium.com/v2/resize:fill:64:64/1*8WdpRZsuzsiKXa8IWvf22A@2x.jpeg)](https://medium.com/@bvsarathc06?source=post_page---byline--68e07623ffa7---------------------------------------)

[B V Sarath Chandra](https://medium.com/@bvsarathc06?source=post_page---byline--68e07623ffa7---------------------------------------)

8 min read

·

Jan 13, 2026

--

63

Listen

Share

More

Press enter or click to view image in full size

![]()

For the last decade, I have worked in the heart of the “Move Fast and Break Things” culture.

I have seen startups deploy to production on Fridays. I have seen “hotfixes” written in 30 seconds. I have seen the mantra “Perfect is the enemy of good” used to justify memory leaks, race conditions, and technical debt that would make a banker weep.

Then, I met a software engineer from JPL (Jet Propulsion Laboratory).

I asked him what framework they used. He laughed.

I asked him how often they deployed. He stopped laughing.

*“When your code is 140 million miles away,”* he said, *“you don’t get to restart the server.”*

While modern web developers are debating React Server Components vs. Client Components, aerospace engineers are practicing a lost art: Software as Survival.

Their code doesn’t just run; it endures. It survives radiation, cosmic rays, and 20-year missions without a single reboot.

Press enter or click to view image in full size

![]()

The secret? They approach software development like a nuclear reactor, not a To-Do list app.

## The Philosophy That Changes Everything

### Defensive Design: Trust No One (Not Even Yourself)

In Silicon Valley, we write code that assumes success.

We assume the API will respond. We assume the database is up. We assume the user won’t input an emoji into the age field.

In Aerospace, they write code that assumes catastrophe.

This is called Defensive Design.

When I looked at the code for the Mars Rover, I noticed something strange. Every single function checked its inputs. Every single variable assignment was verified.

It felt paranoid.

“Why are you checking if speed is a number? You just set it to a number on the line before!” I asked.

The engineer replied: *“Because in radiation-heavy environments, a single bit flip in memory is a real, documented risk. A 0 becomes a 1. Suddenly, the rover is doing 400mph instead of 4mph.”*

```
// Silicon Valley Style: "It'll probably be fine."  
function setRoverSpeed(targetSpeed) {  
  this.currentSpeed = targetSpeed;   
  // If targetSpeed is "fast" (string) or NaN, the physics engine explodes.  
}  
  
// NASA Style: "Trust Physics, Not Variables."  
function setRoverSpeed(targetSpeed) {  
  // 1. Check Data Type  
  if (typeof targetSpeed !== 'number') {  
     return ERROR_INVALID_INPUT;  
  }  
    
  // 2. Check Physical Constraints (Rover max speed is 0.1 m/s)  
  if (targetSpeed < 0 || targetSpeed > MAX_DESIGN_LIMIT) {  
     logAnomaly("Speed request out of physical bounds");  
     return ERROR_UNSAFE_OPERATION;  
  }  
  
  // 3. Redundant State Verification  
  this.currentSpeed = targetSpeed;  
  return SUCCESS;  
}
```

This mindset shift is profound.

* **Web Developer:** “If this fails, show an error modal.”
* **NASA Developer:** “If this fails, the parachute doesn’t open and $2 billion hits the ground at terminal velocity.”

## The Power of “The Power of Ten”

NASA’s JPL follows a strict set of coding rules called “The Power of Ten.”

These rules would get you laughed out of a hackathon. But they are why the Voyager probes are still sending data after 47 years.

### Rule 1: No Dynamic Memory Allocation (After Initialization)

In JavaScript/Python, we create objects constantly. const user = new User().

Garbage collectors clean up the mess.

NASA’s flight-critical software forbids dynamic memory allocation after initialization.

Once the rocket launches, you cannot ask for more RAM. All memory is pre-allocated.

Why? Because “Out of Memory” errors are impossible if you never ask for memory. Garbage Collection pauses are unpredictable.

The Lesson: Predictability > Convenience.

### Rule 2: No Recursion

Recursion is elegant. It is beautiful.

It is also banned.

Why? Because recursion can lead to infinite loops or stack overflows. A fixed-loop structure (like for i in range(10)) is deterministic. You know exactly how long it takes to run.

```
# The "Elegant" Web Way (Risk: Infinite Loop / Stack Overflow)  
def find_root_node(node):  
    if node.parent is None:  
        return node  
    return find_root_node(node.parent) # What if there is a cycle? Crash.  
  
# The "Boring" Aerospace Way (Risk: Zero)  
def find_root_node(node):  
    # Hard limit: Never trust the data structure to be correct  
    MAX_DEPTH = 1000   
      
    for _ in range(MAX_DEPTH):  
        if node.parent is None:  
            return node  
        node = node.parent  
          
    # If we hit the limit, stop safely. Don't crash.  
    return ERROR_TREE_CYCLE_DETECTED
```

The Lesson: If you can’t prove when it stops, don’t start it.

### Rule 3: The Limit of Complexity

Functions should be short enough to print on a single sheet of paper (about 60 lines).

This isn’t just about readability. It is about verifiability.

If a function is longer than 60 lines, the number of possible execution paths explodes. It becomes impossible to test every scenario.

## The “Zero-Defect” Mentality

### The Margaret Hamilton Legacy

There is a famous photo of Margaret Hamilton standing next to a stack of paper as tall as she is. That was the code for the Apollo Guidance Computer.

Press enter or click to view image in full size

![]()

That code landed humans on the moon.

“There were no mission-ending software bugs during the Apollo 11 landing.”

There were *hardware* overload alarms (the 1201 and 1202 alarms), but the software did exactly what it was designed to do: it prioritized critical tasks (landing) and dropped low-priority tasks (radar updates).

This wasn’t luck. It was Asynchronous Executive Scheduling.

Modern web apps crash if you click a button too fast. The Apollo computer handled being overloaded 15 minutes before landing on the moon and simply said, “I’m busy, I’ll ignore the radar for a second.”

## The “Egoless” Code Review

In many tech companies, Code Reviews are a battle of egos. *“Why didn’t you use a map function here?”* or *“This isn’t the React way.”*

In critical systems engineering, they practice Egoless Programming.

Code is not “yours.” It belongs to the mission.

They sit in a room, project the code on a wall, and tear it apart line by line.

If someone finds a bug in your code, you don’t feel defensive. You feel relief.

“Thank you,” you say. “You just saved the mission.”

They don’t review for “style.” They review for:

1. What happens if this input is null?
2. What happens if this loop runs 1 million times?
3. What happens if the sensor disconnects right here?

## The Results Speak for Themselves

### Voyager 1: The Ultimate Legacy Code

Voyager 1 was launched in 1977. It has less computing power than your car key fob.

Press enter or click to view image in full size

![]()

It is currently 15 billion miles away, in interstellar space.

In recent years, Voyager 1 started sending back corrupted telemetry.

The engineers — working with 50-year-old documentation — debugged a corrupted memory chip from Earth. They uploaded a patch to a computer built when disco was popular.

It worked.

Compare that to a modern IoT smart fridge that stops working because the manufacturer turned off a server.

## Why This Matters for You (The “Web Dev” Reality Check)

You might be thinking: *“I build e-commerce sites, not rockets. I don’t need this.”*

But you do.

Because “Move Fast and Break Things” has broken everything.

* We have banking apps that go down on paydays.
* We have healthcare portals that leak patient data.
* We have AI chatbots that hallucinate racial slurs.

We accepted “flakiness” as the price of speed. NASA proves that is a lie.

## How to Apply “Rocket Science” to Your Code

You don’t need to write Assembly to benefit from this.

### 1. Static Analysis is Your Safety Net

NASA uses tools to mathematically prove code correctness.

You can use TypeScript in “Strict Mode.” You can use Linters.

Treat warnings as errors. If the linter complains, the rocket doesn’t launch.

### 2. Fail Safe, Not Fail Hard

When a React component errors, the whole page often goes white (White Screen of Death).

That is “Fail Hard.”

Fail Safe means: If the “Recommended Products” widget fails, the “Add to Cart” button must still work.

Isolate your critical paths.

```
// The "Fail Hard" (White Screen of Death)  
try {  
  loadRecommendations();  
} catch (error) {  
  // React error boundary catches this, but unmounts the whole page  
  throw new Error("Component Failed");   
}  
  
// The "Fail Safe" (Mission Continues)  
try {  
  loadRecommendations();  
} catch (error) {  
  // 1. Log the state *before* the crash  
  telemetry.log("Recs failed", systemState);  
    
  // 2. Hide the feature, don't kill the app  
  this.showRecommendations = false;  
    
  // 3. Ensure Critical Path remains active  
  // The 'Checkout' button is isolated and keeps working  
}
```

### 3. Log the “Why”, Not Just the “What”

Don’t just log Error: 500.

Log the state of the system before the crash.

The Apollo engineers knew exactly why the 1201 alarm went off because the system was designed to tell them why it was overloaded, not just that it was overloaded.

### 4. The “Bus Factor” of Documentation

If you got hit by a bus tomorrow, could your team deploy your code?

NASA documentation is legendary. They write manuals for people who haven’t been born yet.

Write your README as if the person reading it has to debug your code at 3 AM, 20 years from now, while you are in a cryo-sleep chamber.

## The Cultural Shift

The transition from “Coder” to “Engineer” is mental.

A Coder asks: “Does it work?”

An Engineer asks: “What happens when it stops working?”

We live in a world that runs on software. Our cars, our pacemakers, our power grids, our finances.

Maybe it’s time we stopped treating our code like a disposable toy and started treating it like a mission-critical instrument.

You don’t have to build rockets to have a rocket-scientist mindset.

You just have to decide that failure is not an option.

*Have you ever worked on a system where failure wasn’t allowed? How did it change your coding style? Let me know in the comments.*

If you found this article valuable, here are a few more pieces you might cherish:

[## 10 Spark Interview Red Flags That Instantly Give You Away

### The Answers That Sound Right — and Still Get You Rejected

blog.dataengineerthings.org](https://blog.dataengineerthings.org/10-spark-interview-red-flags-that-instantly-give-you-away-2fb2fb8a62ab?source=post_page-----68e07623ffa7---------------------------------------)

[## You’ve Got To Be Smart To Solve This PySpark Interview Question!

### “We don’t ask easy questions here,” smiled the interviewer. “Let’s see how you think.”

medium.com](https://medium.com/towards-data-engineering/youve-got-to-be-smart-to-solve-this-pyspark-interview-question-57b7e56d79ae?source=post_page-----68e07623ffa7---------------------------------------)

[## PySpark Interview Question By Netflix

### You should try this one.

blog.dataengineerthings.org](https://blog.dataengineerthings.org/pyspark-interview-question-by-netflix-962021f26239?source=post_page-----68e07623ffa7---------------------------------------)

[## Multimodal AI: When AI Learns to See, Hear, and Think Like Humans

### Photo by Igor Omilaev on Unsplash

medium.com](https://medium.com/data-science-collective/multimodal-ai-when-ai-learns-to-see-hear-and-think-like-humans-df17377825b6?source=post_page-----68e07623ffa7---------------------------------------)

💕 Thanks for reading! Clap, highlight, and respond to leave your mark. *follow me on* [***Medium***](https://medium.com/@bvsarathc06)if you’d like to see me continue adding more value.
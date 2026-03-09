---
title: "The Biggest Mistake I See in React Native Projects (and How to Avoid It)"
url: https://medium.com/p/4461159b1fba
---

# The Biggest Mistake I See in React Native Projects (and How to Avoid It)

[Original](https://medium.com/p/4461159b1fba)

# The Biggest Mistake I See in React Native Projects (and How to Avoid It)

[![Mayco Faciolo](https://miro.medium.com/v2/resize:fill:64:64/1*CwJSIgxfzVTTzINc0aW3gg.jpeg)](/@mdfaciolo?source=post_page---byline--4461159b1fba---------------------------------------)

[Mayco Faciolo](/@mdfaciolo?source=post_page---byline--4461159b1fba---------------------------------------)

3 min read

·

Jan 16, 2026

--

Listen

Share

More

Press enter or click to view image in full size

![]()

After several years working with React Native — on small apps, mid-sized products, and production systems with real users — I keep seeing the same pattern over and over again.

It’s not performance.  
It’s not Expo.  
It’s not whether you use Zustand, Redux, or Context.

**👉 The biggest mistake is mixing responsibilities from day one.**

And the worst part?  
It usually starts with good intentions.

### React Native is not the problem

React Native scales.  
Meta proved it.  
Shopify proved it.  
Plenty of teams proved it.

What **doesn’t scale** looks like this:

```
export function HomeScreen() {  
 const [loading, setLoading] = useState(false);  
 const [data, setData] = useState([]);  
  
useEffect(() => {  
 fetch("https://api.example.com/data")  
 .then(res => res.json())  
 .then(setData);  
 }, []);  
  
return (  
 <View>  
 {loading && <Loader />}  
 {data.map(item => (  
 <Text key={item.id}>{item.name}</Text>  
 ))}  
 </View>  
 );  
}
```

In a single file, you now have:

* UI
* Business logic
* Networking
* State management
* Product decisions

It works… **until it doesn’t.**

### How the problem starts (and no one notices)

At the beginning, everything sounds reasonable:

* “It’s just a small screen”
* “We’ll refactor later”
* “No need to abstract yet”

Two months later:

* Screens with **800+ lines**
* Hooks that fetch, cache, transform data, and handle errors
* Bugs no one wants to touch
* New features that break existing ones

And then comes the most expensive sentence in software development:

> Let’s not touch it — it works…

### The clearest symptom

If your component:

* Knows the endpoint name
* Decides what to do when a request fails
* Transforms backend data
* Manages complex state
* Renders UI

**👉 That component has too much responsibility.**

### A simple way to avoid it

You don’t need over-engineering.  
You need **clear separation from the start.**

1. **Screens orchestrate, they don’t decide**

```
function HomeScreen() {  
 const { data, isLoading, error } = useHomeData();  
if (isLoading) return <Loader />;  
 if (error) return <ErrorState />;  
return <HomeView data={data} />;  
}
```

A screen:

* Doesn’t know about endpoints
* Doesn’t transform data
* Doesn’t contain business rules

**2. Hooks handle business logic**

```
export function useHomeData() {  
 return useApiRequest(getHomeData);  
}
```

Hooks:

* Encapsulate logic
* Are testable
* Are reusable
* Never render UI

**3. Services do one thing only**

```
export async function getHomeData() {  
 const response = await api.get("/home");  
 return response.data;  
}
```

Services:

* Talk to the API
* Don’t know about UI
* Don’t manage visual states

**4. UI components should be as dumb as possible**

```
export function HomeView({ data }) {  
 return (  
 <View>  
 {data.map(item => (  
 <Text key={item.id}>{item.name}</Text>  
 ))}  
 </View>  
 );  
}
```

If a UI component fails, the problem is visual.  
That’s a feature, not a limitation.

### “But mixing everything is faster at the beginning”

True.  
So is not wearing a seatbelt.

You don’t pay the cost on day one.  
You pay it when:

* The team grows
* The product grows
* You need to move fast without breaking everything

### **The rule that helps me the most**

> If your UI needs to know how data is fetched, something is wrong.

React Native doesn’t fail because of the technology.  
It fails because of **early architectural decisions.**

### Final thoughts

You don’t need:

* Extreme Clean Architecture
* 20 layers
* Complex patterns

You do need:

* Clear responsibility boundaries
* A bit of future thinking
* Code that other people can understand

React Native scales.  
**Mess doesn’t.**
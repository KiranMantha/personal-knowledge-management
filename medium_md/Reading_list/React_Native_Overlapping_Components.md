---
title: "React Native Overlapping Components"
url: https://medium.com/p/15c46af94872
---

# React Native Overlapping Components

[Original](https://medium.com/p/15c46af94872)

Press enter or click to view image in full size

![]()

# React Native Overlapping Components

[![Karthik Balasubramanian](https://miro.medium.com/v2/resize:fill:64:64/1*EbEIuVq0V8RsgPdb2rw2Uw@2x.jpeg)](/@_iam_karthik?source=post_page---byline--15c46af94872---------------------------------------)

[Karthik Balasubramanian](/@_iam_karthik?source=post_page---byline--15c46af94872---------------------------------------)

4 min read

·

Jun 5, 2020

--

2

Listen

Share

More

Hey folks, let us see how to get these overlapping containers to work together in React Native.

![]()

## Setting up React Native Project.

(*Skip to next section, if already done..*)

Go ahead to this link <https://reactnative.dev/docs/environment-setup#docsNav> and follow the steps on creating a new react native project.

```
npx react-native init RNOverlappingContainers
```

To start the application run `npx react-native run-ios` inside your React Native project folder. Open your project in VS Code and head to the file named App.js.And remove the code under the `return` statement and replace it with:

```
return {  
 <>  
  <View>  
  </View>  
 <>  
}
```

You have successfully finished creating a project.

There are basically two containers, let us give them names:

1. Image Container, and
2. Bottom Container

So the first container is positioned `absolute` in the screen and the second container has a `paddingTop` of the image’s height.  
I have prepared a rough sketch on how the skeleton would look.

Press enter or click to view image in full size

![]()

Ignore my bad sense of drawing.

Let us start coding to get our overlapping containers working.

Create a `src` folder in the project root directory.   
Add a folder `OverlappingContainers`

> Create a file `<BottomContainer.js>` .

This is the Bottom Container component which is wrapped inside an Animated ScrollView with some basic animations.

> Create a file `<ImageContainer.js>` .

This is the Image Container Component which renders an Animated Image with scale animation, you can see the effect at the end of this blog.

> Create a file `<LoadingAtom.js>` .

Just a placeholder content for the scroll view, it can be anything.

> Create an `index.js` file which will be wrapping the above containers

Wrap both of your components inside the <SafeAreaView/> component which React Native provides. The BottomContainer wraps the content of the scroll view.

***I have assigned the Image Height to 450px. This can vary depending upon the design and screen dimensions.***

Okay now, let us try running the app !!

![]()

That’s neat !!

Used libraries (For the placeholder content) :

1. [React Native SVG](https://github.com/react-native-community/react-native-svg)

2. [React Native Content Loader](https://github.com/kostimarko/rn-content-loader)

The image is from 

[Unsplash](/u/2053395ac335?source=post_page---user_mention--15c46af94872---------------------------------------)

, photographed by @[julie\_soul](https://unsplash.com/@julie_soul/portfolio).

**Special Case for Android :**

The above implementation is enough to get things working well with iOS, but you will have a default grey background in Android.

Something like this :

Press enter or click to view image in full size

![]()

If you want the status bar the same as iOS. You will have to do as follows :

1. Add `backgroundColor` and `translucent` property to <StatusBar/>

```
<StatusBar   
     barStyle='light-content'   
     backgroundColor='transparent'   
     translucent={true}   
/>
```

2. Add an empty <View> of which equals the height of the status bar. For this, I have used a library, which you can find [here](https://www.npmjs.com/package/react-native-status-bar-height). Install and use it like this conditionally just in case of Android:

```
<View   
   style={{   
       height: Platform.OS === 'android' ? getStatusBarHeight() : 0   
   }}  
/>
```

Now it would look like this.

Press enter or click to view image in full size

![]()

> Animations Breakdown

Let us try to break down the animations used in here.

1. Creating an Animated Value

```
const [scrollY, setScrollY] = useState(new Animated.Value(0));
```

2. Attach this scrollY value to the `onScroll` event of the `<ScrollView>`

```
onScroll={  
     Animated.event(         [{ nativeEvent: { contentOffset: { y: scrollY } } }],         { useNativeDriver: true },         () => { },          // Optional async listener     )  
}
```

3. Use the animated value to apply the scale animation on your `<Image/>`

```
transform: [  {      scale: scrollY.interpolate({          inputRange: [0, imageHeight],          outputRange: [1.2, 1],          extrapolate: 'clamp'       })  }]
```

This gives the feel of image scaling down to its original size while you scroll.

4. Use the same animated value to animate the `borderRadius` of the `<View/>`

```
const animateBorderRadius = scrollY.interpolate(            {               inputRange: [0, 450 - 100],               outputRange: [40, 0],            }  
);
```

This basically animates your `borderRadius` value from 40 to 0, while scrolling up. You can use it like this :

```
<Animated.View   
      style={[               styles.block,                {                    borderTopLeftRadius: animateBorderRadius,                    borderTopRightRadius: animateBorderRadius                 }       ]}>         {props.children}</Animated.View>
```

> This is *Karthik* representing [Timeless](http://timeless.co/)**.**

You can find the repo [here.](https://github.com/Karthik-B-06/RNOverlappingContainers)

If you find this blog post helpful, share it with a friend.

If you find any difficulties please feel free to add your comments.
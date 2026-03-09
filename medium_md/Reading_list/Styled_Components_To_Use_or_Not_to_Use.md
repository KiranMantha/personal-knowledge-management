---
title: "Styled Components: To Use or Not to Use?"
url: https://medium.com/p/a6bb4a7ffc21
---

# Styled Components: To Use or Not to Use?

[Original](https://medium.com/p/a6bb4a7ffc21)

# Styled Components: To Use or Not to Use?

[![Talia Marcassa](https://miro.medium.com/v2/resize:fill:64:64/0*zvodXviaJfzC74KB.jpg)](/@talialongname?source=post_page---byline--a6bb4a7ffc21---------------------------------------)

[Talia Marcassa](/@talialongname?source=post_page---byline--a6bb4a7ffc21---------------------------------------)

5 min read

·

Jun 5, 2018

--

11

Listen

Share

More

![]()

At CrowdRiff, we’re constantly looking for ways to improve our projects. The recent trend towards CSS in JavaScript was hard to ignore, so we decided to implement the [Styled Components](https://www.styled-components.com/) library in one of our newer codebases.

To be honest, I was skeptical — I like CSS! I understand how it works and I like when JavaScript and CSS have distinct files. I know what files to look at when we have a visual bug, I have a fairly solid handle on how SCSS works, and I understand our codebase’s established patterns of CSS.

But setting skepticism aside, I decided to try it out.

### Spoiler: We Didn’t Hate It

*Disclaimer: Our stack is React/Redux, so the examples below assume a basic understanding of those frameworks.*

For our use case, we didn’t convert our entire project to Styled Components. We chose to keep the majority of our CSS in the more traditional (i.e. separated) file structure and use Styled Components for elements whose styling (colours, images, etc.) is configured by the user.

### What We Liked About Styled Components

1. *It Makes Components Less Bulky*

In our use case, there’s a lot of heavy lifting that has to be done through CSS to inject user-specific styling into a component. Many components’ render methods end up containing style objects that clutter them up and split the CSS into two places, making the code harder to parse. Styled Components help keep the concerns of styling and element architecture separated and make components more readable.

Furthermore, when you have components that rely on JavaScript for their style, Styled Components gives control of those states back to CSS instead of using a multitude of conditional class names.

Below is a render method using props to set specific colours. the handleHover is not written below but it would be responsible for setting the ‘isHovered’ piece of state.

```
// The render method of some component  
render() {  
const style = {  
  color: `${this.props.themeColor}`,  
}  
const hoverStyle = {  
  color: `${this.props.hoverThemeColor}`  
}  return (  
    <button  
      onMouseEnter={this.handleHover}  
      onMouseOut={this.handleHover}  
      style={this.state.isHovered ? hoverStyle : style}  
    >  
      Click Me!  
    </button>  
  );  
}
```

Here is the same code but using Styled Components:

```
// Declare your Styled Component, in the same file or a different file than your component  
import styled from 'styled-components';const BrandedButton = styled.button`  
  color: ${props => props.themeColor};  
  &:hover {  
    color: ${props => props.themeHoverColor};  
  }  
`  
render(){  
  return (  
    <BrandedButton themeHoverColor="pink" themeColor="blue" >  
      Click Me!  
    </BrandedButton>  
  );  
}
```

Instead of relying on two separate style objects and having to use React event handlers to setup a simple hover state, we use a styled component. This makes it easy to inject values that only exist in JavaScript into our CSS while still allowing CSS to handle the various UI states.

*2. The ThemeProvider*

The [ThemeProvider](https://www.styled-components.com/docs/advanced) is used as a wrapper that injects theme props into all of its child components. If you’re using a state library like Redux, you can avoid having multiple connected components request the same properties from state by using the ThemeProvider to pass these props to all your styled components.

We found the ThemeProvider particularly useful when building a ‘configuration’ page, which is essentially a duplicate page that allows a user to customize certain stylistic elements, like colour. We wrapped our configuration page in a ThemeProvider that was referencing a different piece of state than the non-editable portion of the app. That allowed us to reuse all the styled components while also showing the user feedback as they updated their stylistic elements.

*3. The CSS Function*

With Styled Components’ [css](https://www.styled-components.com/docs/api) function, you can use props to conditionally render css, which meant that we no longer had to render conditional class names based on props. This reduces clutter in your components as well as maintains a separation of concerns between CSS and JavaScript.

Take this button, for example:

```
import styled from 'styled-components';const Button = styled.button`  
  color: ${props => props.isSecondary ? ‘blue’ : ‘white’};  
`
```

What if we wanted to add a third iteration of this button? It would quickly become difficult with the ternary pattern. With the css function from Styled Components, you can easily add as many conditions as you’d like!

Here, we used Styled Components to give a button different colours depending on its props.

```
// Declaring the styled component  
const Button = styled.button`  
  color: ‘white’;  
  ${props => props.isSecondary && css`  
     color: ‘blue’;  
  `}  
  ${props => props.isDisabled && css`  
     color: ‘grey’;  
  `}  
`  
// Using the disabled iteration of the styled component  
  <Button isDisabled />
```

The button is styled to have white text by default, but if an ‘isDisabled’ prop is applied, the color property will be overwritten since it appears later in the style declaration, and the button will be given a colour of grey.

*4. Testing*

We implemented the [Jest Styled Components](https://github.com/styled-components/jest-styled-components) library for our testing in Jest. It makes testing styled components painless by creating consistent class names and allowing you to assert specific CSS rules that might be important to the integrity of your app.

Below is an example of an assertion that Jest Styled Components allow you to make on your component:

```
expect(button).toHaveStyleRule('color', 'blue');
```

Pairing these simple assertions with the various states of your app is a powerful pattern to catch visual regressions.

**What We Found Slightly Frustrating About Styled Components**

There were certain style rules that we found hard to apply to Styled Components; namely, rules that set the placement of an element on a page (e.g. margin or display properties). They were difficult to standardize, so we still ended up leaning heavily on plain ol’ CSS for component placement in the flow of elements.

The syntax of Styled Components also takes some time to get used to, but if you’re familiar with template literals then it shouldn’t be too much of a stretch. Also, Styled Components does a great job with its [docs](https://www.styled-components.com/) and has been in the ecosystem for long enough that there are many examples around the internet!

**The verdict: Use!**Overall, we’d definitely recommend Styled Components. Sure, there were some bumps along the way, but it reduced the complexity of our codebase. Styled Components FTW.

*Photo by* [*Marc Steenbeke*](https://unsplash.com/photos/wZXvTIwFpHc?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) *on* [*Unsplash*](https://unsplash.com/?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)*.*

*Thank you to the* 

[*CrowdRiff*](/u/aeadd22edd9e?source=post_page---user_mention--a6bb4a7ffc21---------------------------------------)

 *team for all of the editing!*
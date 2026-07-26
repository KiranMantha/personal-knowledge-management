---
title: "Creating a “Read More” component in React"
url: https://medium.com/p/4afd1d17d40b
---

# Creating a “Read More” component in React

[Original](https://medium.com/p/4afd1d17d40b)

# Creating a “Read More” component in React

[![Filipe Pfluck](https://miro.medium.com/v2/resize:fill:64:64/0*gleetp9cobSFTp6h.jpg)](/@filipepfluckdev?source=post_page---byline--4afd1d17d40b---------------------------------------)

[Filipe Pfluck](/@filipepfluckdev?source=post_page---byline--4afd1d17d40b---------------------------------------)

5 min read

·

Oct 4, 2023

--

6

[Listen](/m/signin?actionUrl=https%3A%2F%2Fmedium.com%2Fplans%3Fdimension%3Dpost_audio_button%26postId%3D4afd1d17d40b&operation=register&redirect=https%3A%2F%2Fmedium.com%2F%40filipepfluckdev%2Fcreating-a-read-more-component-in-react-4afd1d17d40b&source=---header_actions--4afd1d17d40b---------------------post_audio_button------------------)

Share

When you want to display a long text, frequently you don’t want to show the whole text all at once to the user. Either because you are showing multiple items, or because it doesn’t fit the layout, or even because therewould be too much information in the screen. In such cases, you may want to add a “Read more” button, that when clicked, expand and show the whole text. This component is tricky to get right, for several reasons. Firstly, you don’t want to show the button, unless the text is actually longer than you expect. Secondly, you don’t want to cause layout shifts if you’re working with SSR. And thirdly, and often ignored, you want to follow accessibility guidelines. Today, I will hopefully show you an implementation of such component, following this key principles.

## Getting started

To get started, create a React project. I will create one using NextJS. I will be using tailwind for the sake of simplicity, but feel free to use your prefered styling solution.

```
yarn create next-app
```

Answer the questions in the terminal, and the project will be scaffolded. Then, open the project in your favorite code editor.

## Creating the component

I will create a new file in src/components/ReadMore.tsx  
Let’s start by adding the basic markup, some properties, and a state to represent if it is expanded or not

```
import { useState } from 'react'  
  
interface ReadMoreProps {  
  id: string  
  text: string  
  amountOfWords?: number  
}  
  
export const ReadMore = ({id, text, amountOfWords = 36}: ReadMoreProps) => {  
  const [isExpanded, setIsExpanded] = useState(false)  
  
  return (  
    <p>  
      {text}  
    </p>  
  )  
}
```

I added id and text properties, which are strings, and an amountOfWords property, which is an optional number. If not provided, the value will be 36, but you can adjust this to match your needs. Now, let’s split the text based on the amountOfWords provided.

```
import { useState } from 'react'  
  
interface ReadMoreProps {  
  id: string  
  text: string  
  amountOfWords?: number  
}  
  
export const ReadMore = ({id, text, amountOfWords = 36}: ReadMoreProps) => {  
  const [isExpanded, setIsExpanded] = useState(false)  
    
  const splittedText = text.split(' ')  
  const itCanOverflow = splittedText.length > amountOfWords  
  const beginText = itCanOverflow  
    ? splittedText.slice(0, amountOfWords - 1).join(' ')  
    : text  
  const endText = splittedText.slice(amountOfWords - 1).join(' ')  
  
  return (  
    <p>  
      {text}  
    </p>  
  )  
}
```

First, we are splitting the text into an array of words. Then, we check if the amount of words is larger than the amountOfWords property. Then, we use the slice method to separate the text into beginText and endText. Now let’s render some content based on this information.

```
import { useState } from 'react'  
  
interface ReadMoreProps {  
  id: string  
  text: string  
  amountOfWords?: number  
}  
  
export const ReadMore = ({id, text, amountOfWords = 36}: ReadMoreProps) => {  
  const [isExpanded, setIsExpanded] = useState(false)  
    
  const splittedText = text.split(' ')  
  const itCanOverflow = splittedText.length > amountOfWords  
  const beginText = itCanOverflow  
    ? splittedText.slice(0, amountOfWords - 1).join(' ')  
    : text  
  const endText = splittedText.slice(amountOfWords - 1).join(' ')  
  
  return (  
    <p id={id}>  
      {beginText}  
      {itCanOverflow && (  
          <>  
            {!isExpanded && <span>... </span>}  
            <span className={`${!isExpanded && 'hidden'}`} >   
              {endText}  
            </span>  
            <span   
              className='text-violet-400 ml-2'  
              onClick={() => setIsExpanded(!isExpanded)}  
            >  
              {isExpanded ? 'show less' : 'show more'}  
            </span>  
          </>  
      )}  
    </p>  
  )  
}
```

Now, if the text can overflow, we are displaying the endText and a button to toggle between show more and show less. If the text is not expanded, we are adding a hidden classname to the end text, which in tailwind means display: none. This code should be working so far, but it has several accessibility issues. First, the show more/show less should be a button, nor a span. The reason I added a span is because this way it will be displayed as a text inside the paragraph. But if we want it to behave like a button, then we need to add some properties to it.

```
import { useState } from 'react'  
  
interface ReadMoreProps {  
  id: string  
  text: string  
  amountOfWords?: number  
}  
  
export const ReadMore = ({ id, text, amountOfWords = 36 }: ReadMoreProps) => {  
  const [isExpanded, setIsExpanded] = useState(false)  
  const splittedText = text.split(' ')  
  const itCanOverflow = splittedText.length > amountOfWords  
  const beginText = itCanOverflow  
    ? splittedText.slice(0, amountOfWords - 1).join(' ')  
    : text  
  const endText = splittedText.slice(amountOfWords - 1).join(' ')  
    
  const handleKeyboard = (e) => {  
    if (e.code === 'Space' || e.code === 'Enter') {  
      setIsExpanded(!isExpanded)  
    }  
  }  
  
  return (  
    <p id={id}>  
      {beginText}  
      {itCanOverflow && (  
        <>  
          {!isExpanded && <span>... </span>}  
          <span   
            className={`${!isExpanded && 'hidden'}`}   
            aria-hidden={!isExpanded}  
          >  
            {endText}  
          </span>  
          <span  
            className='text-violet-400 ml-2'  
            role="button"  
            tabIndex={0}  
            aria-expanded={isExpanded}  
            aria-controls={id}  
            onKeyDown={handleKeyboard}  
            onClick={() => setIsExpanded(!isExpanded)}  
          >  
            {isExpanded ? 'show less' : 'show more'}  
          </span>  
        </>  
      )}  
    </p>  
  )  
}
```

role=’button’ informs the assistive technology (e.g screen readers) that this is actually a button. TabIndex={0} makes this element focusable by the keyboard, and the onKeyDown function triggers the button when pressing space or enter. The aria properties inform usefull informations to the assistive technology. We are also adding aria-hidden to the endText, so it won’t be announced when it is collapsed. If you want, you can add an aria-label to the button, to give more context to the user about which text will be expanded. And that’s it! Now let’s use this component on our application.

```
// src/app/page.tsx  
  
import { ReadMore } from "@/components/ReadMore";  
  
export default function Home() {  
  return (  
    <main className="p-20 flex items-center justify-center w-screen h-screen">  
      <div className="w-80">  
      <ReadMore id="read-more-text" text="Lorem ipsum dolor sit amet consectetur adipisicing elit. Beatae perspiciatis eligendi, similique quisquam esse aliquam possimus, illum quaerat eaque illo dolor officiis. Temporibus odit, pariatur corporis ipsa odio officia tenetur? Lorem ipsum dolor sit amet consectetur adipisicing elit. Beatae perspiciatis eligendi, similique quisquam esse aliquam possimus, illum quaerat eaque illo dolor officiis. Temporibus odit, pariatur corporis ipsa odio officia tenetur?" />  
      </div>  
    </main>  
  )  
}
```

Press enter or click to view image in full size

![]()

Press enter or click to view image in full size

![]()

That’s it! This read more component does not cause layout shift when using SSR, and is fully accessible. You can customize this code to meet your criteria better, if needed.
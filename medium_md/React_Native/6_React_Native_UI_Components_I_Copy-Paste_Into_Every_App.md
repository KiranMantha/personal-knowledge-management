---
title: "6 React Native UI Components I Copy-Paste Into Every App"
url: https://medium.com/p/a00970088437
---

# 6 React Native UI Components I Copy-Paste Into Every App

[Original](https://medium.com/p/a00970088437)

Member-only story

# 6 React Native UI Components I Copy-Paste Into Every App

## These are not just UI components. They are a design system. Reusable, minimal, and well-designed with cleaner code for faster development

[![Abdul Basit](https://miro.medium.com/v2/resize:fill:64:64/1*Zir5s7NdiFlUQydsmAUatw.jpeg)](https://medium.com/@basit.miyanjee?source=post_page---byline--a00970088437---------------------------------------)

[Abdul Basit](https://medium.com/@basit.miyanjee?source=post_page---byline--a00970088437---------------------------------------)

11 min read

·

Jan 31, 2026

--

3

Listen

Share

More

2026 is a year of mobile apps and communities.

And when it comes to building mobile apps fast, React Native is one of the best choices for UI development. It’s cross-platform, and since most of us already have a React and JavaScript background, adapting to React Native feels natural and easy.

When building apps, one thing matters the most, and that is SPEED.

> Code with speed.
>
> Build with speed.
>
> Ship with speed.

Today I’m sharing 6 reusable React Native UI components that I personally use in my React Native apps to speed up development.

They are minimal and well-designed.

> These are not just UI components. They are a design system.

I built these components with readability, flexibility, and customization in mind, so updating or extending them later is simple and requires a single prompt.

You can just copy and paste these components into your `components/ui` folder and start using them right away.

> ***Note:*** *All components are created using Expo.*

You can find all the code in this open-source ***RN Design System*** GitHub repository.

[## GitHub - AbdulBasit313/rn-design-system: A minimal React Native design system built for real apps

### A minimal React Native design system built for real apps - AbdulBasit313/rn-design-system

github.com](https://github.com/AbdulBasit313/rn-design-system?source=post_page-----a00970088437---------------------------------------)

Let’s get started.

## 1. Button

Press enter or click to view image in full size

![React Native Button UI component]()

Button is the most used UI component in almost every app.

It’s better to create one button component that addresses your whole design system and use it everywhere, so when it's time to update, just update in one component and get effect everywhere.

This button component is a complete design system that supports multiple variants, like primary and secondary, along with icons and a loading state.

**Button Component Code**

```
import { ReactNode } from 'react'  
import {  
  ActivityIndicator,  
  Pressable,  
  StyleSheet,  
  Text,  
  TextStyle,  
  View,  
  ViewStyle,  
} from 'react-native'  
  
type ButtonVariant = 'primary' | 'secondary' | 'outline' | 'ghost'  
  
interface ButtonProps {  
  title?: string  
  icon?: ReactNode  
  onPress?: () => void  
  disabled?: boolean  
  loading?: boolean  
  variant?: ButtonVariant  
  style?: ViewStyle  
}  
  
const BASE_STYLES = {  
  container: {  
    paddingVertical: 12,  
    paddingHorizontal: 20,  
    borderRadius: 8,  
    alignItems: 'center',  
    justifyContent: 'center',  
  } satisfies ViewStyle,  
  
  text: {  
    fontSize: 16,  
    fontWeight: '600',  
  } satisfies TextStyle,  
}  
  
const DISABLED_STYLES = {  
  container: {  
    backgroundColor: '#E7E8E9',  
    borderWidth: 0,  
  } satisfies ViewStyle,  
  
  text: {  
    color: '#9FA3A9',  
  },  
}  
  
const VARIANTS = {  
  primary: {  
    container: {  
      backgroundColor: '#E8AE1B',  
    },  
    text: {  
      color: '#fff',  
    },  
  },  
  secondary: {  
    container: {  
      backgroundColor: '#473401',  
    },  
    text: {  
      color: '#fff',  
    },  
  },  
  outline: {  
    container: {  
      backgroundColor: 'transparent',  
      borderWidth: 1,  
      borderColor: '#E8AE1B',  
    },  
    text: {  
      color: '#E8AE1B',  
    },  
  },  
  ghost: {  
    container: {  
      backgroundColor: 'transparent',  
    },  
    text: {  
      color: '#E8AE1B',  
    },  
  },  
} satisfies Record<ButtonVariant, { container: ViewStyle; text: any }>  
  
const Button = ({  
  title,  
  icon,  
  onPress,  
  disabled = false,  
  loading = false,  
  variant = 'primary',  
  style,  
  ...rest  
}: ButtonProps) => {  
  const isDisabled = disabled || loading  
  const variantStyles = VARIANTS[variant]  
  
  return (  
    <Pressable  
      onPress={onPress}  
      disabled={isDisabled}  
      {...rest}  
      style={({ pressed }) => [  
        BASE_STYLES.container,  
        variantStyles.container,  
        pressed && !isDisabled && styles.pressed,  
        pressed && !isDisabled && styles.shrink,  
        isDisabled && DISABLED_STYLES.container,  
        style,  
      ]}  
    >  
      <View style={styles.content}>  
        {loading ? (  
          <ActivityIndicator color="#9FA3A9" />  
        ) : (  
          <>  
            {icon && <View style={title ? styles.icon : styles.iconOnly}>{icon}</View>}  
  
            {title && (  
              <Text  
                style={[BASE_STYLES.text, variantStyles.text, isDisabled && DISABLED_STYLES.text]}  
              >  
                {title}  
              </Text>  
            )}  
          </>  
        )}  
      </View>  
    </Pressable>  
  )  
}  
  
export default Button  
  
const styles = StyleSheet.create({  
  content: {  
    flexDirection: 'row',  
    alignItems: 'center',  
  },  
  
  icon: {  
    marginRight: 8,  
  },  
  
  iconOnly: {  
    marginRight: 0,  
  },  
  
  pressed: {  
    opacity: 0.9,  
  },  
  
  shrink: {  
    transform: [{ scale: 0.96 }],  
  },  
})
```

**Use Case with Demo**

```
import Button from '@/components/ui/button'  
import Spacer from '@/components/ui/spacer'  
import { Ionicons } from '@expo/vector-icons'  
import { StyleSheet, Text, View } from 'react-native'  
  
export default function ButtonDemo() {  
  const handlePress = (variant: string, state: string = '') => {  
    const buttonName = state ? `${variant} ${state}` : variant  
    console.log(`${buttonName} pressed`)  
  }  
  
  return (  
    <View>  
      {/* Primary Variant */}  
      <View>  
        <Text style={styles.sectionTitle}>Primary</Text>  
  
        <Button title="Buy Now" onPress={() => handlePress('Primary')} />  
  
        <Spacer height={12} />  
  
        <Text style={styles.sectionTitle}>Loading</Text>  
        <Button title="Primary Loading" loading onPress={() => handlePress('Primary', 'loading')} />  
      </View>  
  
      <Spacer height={32} />  
  
      {/* Secondary Variant */}  
      <View>  
        <Text style={styles.sectionTitle}>Secondary</Text>  
        <View style={[styles.row, styles.gap10]}>  
          <Button title="Add to Cart" variant="secondary" />  
          <Button  
            title="Save"  
            variant="secondary"  
            icon={<Ionicons name="save-outline" size={20} color="#fff" />}  
          />  
          <Button  
            icon={<Ionicons name="settings" size={24} color="#fff" />}  
            variant="secondary"  
            onPress={() => handlePress('Primary', 'icon only')}  
          />  
        </View>  
  
        <Spacer height={12} />  
      </View>  
  
      <Spacer height={10} />  
  
      {/* Outline Variant */}  
      <View>  
        <Text style={styles.sectionTitle}>Outline</Text>  
  
        <View style={[styles.row, styles.gap10]}>  
          <Button title="Delete" variant="outline" onPress={() => handlePress('Outline')} />  
  
          <Button  
            title=""  
            variant="outline"  
            icon={<Ionicons name="trash-bin-outline" size={20} color="#E8AE1B" />}  
            onPress={() => handlePress('Outline', 'with icon')}  
          />  
        </View>  
      </View>  
  
      <Spacer height={32} />  
  
      {/* Ghost Variant */}  
      <View>  
        <Text style={styles.sectionTitle}>Text Button</Text>  
  
        <View style={[styles.row, styles.gap10]}>  
          <Button title="Learn More" variant="ghost" onPress={() => handlePress('Ghost')} />  
  
          <Button  
            title="Like"  
            variant="ghost"  
            icon={<Ionicons name="heart" size={20} color="#E8AE1B" />}  
            onPress={() => handlePress('Ghost', 'like')}  
          />  
        </View>  
      </View>  
    </View>  
  )  
}  
  
const styles = StyleSheet.create({  
  sectionTitle: {  
    fontSize: 14,  
    fontWeight: '600',  
    color: '#aaa',  
    marginBottom: 8,  
  },  
  gap10: {  
    gap: 10,  
  },  
  row: {  
    flexDirection: 'row',  
    alignItems: 'center',  
  },  
})
```

Here, you can also learn how I built this [button component step by step.](https://medium.com/javascript-in-plain-english/react-native-button-design-system-1a7ac0c535a6)

## 2. Input

Press enter or click to view image in full size

![]()

Every app needs user input.

Whether it’s a login form, sign-up form, feedback, contact form, or even a search bar, inputs are everywhere.

This input component also supports an icon, making it clean and flexible for different use cases.

**Input Component Code**

```
import { Ionicons } from '@expo/vector-icons'  
import React from 'react'  
import { StyleSheet, TextInput, View } from 'react-native'  
  
interface InputProps {  
  icon: keyof typeof Ionicons.glyphMap  
  placeholder: string  
  secureTextEntry?: boolean  
}  
  
export default function Input({ icon, placeholder, secureTextEntry }: InputProps) {  
  return (  
    <View style={styles.container}>  
      <Ionicons name={icon} size={20} color={colors.icon} />  
      <TextInput  
        placeholder={placeholder}  
        placeholderTextColor={colors.placeholder}  
        secureTextEntry={secureTextEntry}  
        style={styles.input}  
      />  
    </View>  
  )  
}  
  
const colors = {  
  background: '#FFFFFF',  
  border: '#E5E7EB', // gray-200  
  text: '#111827', // gray-900  
  placeholder: '#9CA3AF', // gray-400  
  icon: '#6B7280', // gray-500  
}  
  
const styles = StyleSheet.create({  
  container: {  
    flexDirection: 'row',  
    alignItems: 'center',  
    height: 56,  
    paddingHorizontal: 16,  
    borderRadius: 14,  
    backgroundColor: colors.background,  
    borderWidth: 1,  
    borderColor: colors.border,  
  },  
  
  input: {  
    flex: 1,  
    marginLeft: 12,  
    fontSize: 16,  
    color: colors.text,  
  },  
})
```

**Use Case with Demo**

```
import React from 'react'  
import { Pressable, StyleSheet, Text, View } from 'react-native'  
import Input from '../ui/input'  
import Spacer from '../ui/spacer'  
  
export default function LoginDemo() {  
  return (  
    <View style={styles.container}>  
      <Text style={styles.heading}>Welcome Back</Text>  
      <Text style={styles.subText}>Login to your account</Text>  
  
      <Spacer height={32} />  
  
      <Input icon="mail-outline" placeholder="Email address" />  
  
      <Spacer height={16} />  
  
      <Input icon="lock-closed-outline" placeholder="Password" secureTextEntry />  
  
      <Spacer height={24} />  
  
      <Pressable style={styles.button}>  
        <Text style={styles.buttonText}>Login</Text>  
      </Pressable>  
    </View>  
  )  
}  
  
const styles = StyleSheet.create({  
  container: {  
    padding: 16,  
    backgroundColor: '#FFFFFF',  
    flex: 1,  
    justifyContent: 'center',  
  },  
  
  heading: {  
    fontSize: 24,  
    fontWeight: '700',  
    color: '#111827',  
  },  
  
  subText: {  
    marginTop: 4,  
    fontSize: 14,  
    color: '#6B7280',  
  },  
  
  button: {  
    height: 52,  
    borderRadius: 14,  
    backgroundColor: '#111827',  
    alignItems: 'center',  
    justifyContent: 'center',  
  },  
  
  buttonText: {  
    color: '#FFFFFF',  
    fontSize: 16,  
    fontWeight: '600',  
  },  
})
```

## 3. Filter Tabs

Press enter or click to view image in full size

![React Native Tabs UI component]()

If your app displays data, chances are you’re rendering it in a list.

And when that list gets long, we need filter tabs.

This UI component helps users filter data easily, and for better UI/UX, the selected tab is visually highlighted.

**Tabs Component Code**

```
import { Pressable, StyleSheet, Text } from 'react-native'  
  
interface TabProps {  
  label: string  
  active: boolean  
  onPress: () => void  
}  
  
function Tab({ label, active, onPress }: TabProps) {  
  return (  
    <Pressable  
      onPress={onPress}  
      style={({ pressed }) => [  
        styles.tab,  
        active && styles.activeTab,  
        pressed && styles.pressedTab,  
      ]}  
    >  
      <Text style={[styles.text, active && styles.activeText]}>{label}</Text>  
    </Pressable>  
  )  
}  
  
export default Tab  
  
const styles = StyleSheet.create({  
  tab: {  
    paddingHorizontal: 16,  
    paddingVertical: 8,  
    borderRadius: 8,  
    backgroundColor: '#F3F4F6', // gray-100  
    borderColor: '#F3F4F6', // gray-200  
    borderWidth: 1,  
  },  
  
  activeTab: {  
    backgroundColor: '#FFFFFF',  
    borderWidth: 1,  
    borderColor: '#E5E7EB', // gray-200  
  },  
  
  pressedTab: {  
    transform: [{ scale: 0.97 }],  
    opacity: 0.9,  
  },  
  
  text: {  
    fontSize: 13,  
    fontWeight: '600',  
    color: '#6B7280', // gray-500  
  },  
  
  activeText: {  
    color: '#111827', // gray-900  
  },  
})
```

**Use Case with Demo**

```
import React, { useState } from 'react'  
import { StyleSheet, View } from 'react-native'  
import Tab from '../ui/tab'  
  
const TABS = ['All', 'Active', 'Completed']  
  
export default function FilterTabsDemo() {  
  const [activeTab, setActiveTab] = useState('All')  
  
  return (  
    <View style={styles.container}>  
      {TABS.map((tab) => (  
        <Tab key={tab} label={tab} active={activeTab === tab} onPress={() => setActiveTab(tab)} />  
      ))}  
    </View>  
  )  
}  
  
const styles = StyleSheet.create({  
  container: {  
    flexDirection: 'row',  
    gap: 12,  
    padding: 16,  
    backgroundColor: '#FFFFFF',  
  },  
})
```

## 4. Tags | Badge

Press enter or click to view image in full size

![React Native Tags UI component]()

Badges are another very common UI component.

We usually use them to show status, labels, or quick information.

You can easily add more style variants and reuse this badge throughout your app without repeating code.

**Status Badge Component Code**

```
import { Ionicons } from '@expo/vector-icons'  
import React from 'react'  
import { StyleSheet, Text, View } from 'react-native'  
  
type BadgeVariant = 'completed' | 'inProgress'  
  
type BadgeProps = {  
  variant: BadgeVariant  
}  
  
const BADGE_CONFIG: Record<  
  BadgeVariant,  
  {  
    label: string  
    color: string  
    bgColor: string  
    borderColor: string  
    icon: React.ReactNode  
  }  
> = {  
  completed: {  
    label: 'Done',  
    color: '#059669', // emerald-600  
    bgColor: '#ECFDF5', // emerald-50  
    borderColor: '#A7F3D0', // emerald-200  
    icon: <Ionicons name="checkmark-circle" size={14} color="#059669" />,  
  },  
  inProgress: {  
    label: 'Active',  
    color: '#D97706', // amber-600  
    bgColor: '#FFFBEB', // amber-50  
    borderColor: '#FDE68A', // amber-200  
    icon: <Ionicons name="flash" size={14} color="#D97706" />,  
  },  
}  
  
export default function Badge({ variant }: BadgeProps) {  
  const config = BADGE_CONFIG[variant]  
  
  return (  
    <View  
      style={[  
        styles.base,  
        {  
          backgroundColor: config.bgColor,  
          borderColor: config.borderColor,  
        },  
      ]}  
    >  
      {config.icon}  
      <Text style={[styles.text, { color: config.color }]}>{config.label}</Text>  
    </View>  
  )  
}  
  
const styles = StyleSheet.create({  
  base: {  
    flexDirection: 'row',  
    alignItems: 'center',  
    gap: 6,  
    paddingHorizontal: 8,  
    paddingVertical: 6,  
    borderRadius: 8,  
    borderWidth: 1,  
  },  
  text: {  
    fontSize: 11,  
    fontWeight: '600',  
    textTransform: 'uppercase',  
    letterSpacing: 0.5,  
  },  
})
```

**Use Case with Demo**

```
import React from 'react'  
import { StyleSheet, Text, View } from 'react-native'  
import Badge from '../ui/badge'  
  
export default function BadgeDemo() {  
  return (  
    <View style={styles.container}>  
      <Text style={styles.heading}>My Quizzes</Text>  
      <Text style={styles.subHeading}>Track your progress</Text>  
  
      <View style={styles.row}>  
        <Text style={styles.title}>JavaScript Basics</Text>  
        <Badge variant="completed" />  
      </View>  
  
      <View style={styles.row}>  
        <Text style={styles.title}>React Hooks</Text>  
        <Badge variant="inProgress" />  
      </View>  
    </View>  
  )  
}  
  
const styles = StyleSheet.create({  
  container: {  
    padding: 16,  
    backgroundColor: '#FFFFFF',  
  },  
  heading: {  
    fontSize: 20,  
    fontWeight: '700',  
    color: '#111827',  
    lineHeight: 26,  
  },  
  subHeading: {  
    marginTop: 4,  
    fontSize: 13,  
    color: '#6B7280',  
  },  
  row: {  
    flexDirection: 'row',  
    justifyContent: 'space-between',  
    alignItems: 'center',  
    paddingVertical: 20,  
    borderBottomWidth: 1,  
    borderBottomColor: '#e2e8f0',  
  },  
  title: {  
    fontSize: 14,  
    fontWeight: '500',  
    color: '#4b5563',  
  },  
})
```

## 5. Spacer

Press enter or click to view image in full size

![React Native Spacer UI component]()

In React Native, spacing is something we deal with all the time.

Instead of adding `marginTop` or `marginBottom` everywhere, a Spacer component makes layouts cleaner and more consistent.

We avoid adding margins inside reusable components because it limits flexibility.

This spacer component solves that problem neatly.

**Spacer Component Code**

```
import { View } from 'react-native'  
  
interface SpacerProps {  
  width?: number | '100%' | 'auto'  
  height?: number | string  
}  
  
const Spacer = ({ width = '100%', height = 40 }: SpacerProps) => {  
  return <View style={{ width: width as any, height: height as any }} />  
}  
  
export default Spacer
```

**Use Case with Demo**

```
import React from 'react'  
import { StyleSheet, Text, View } from 'react-native'  
import Spacer from '../ui/spacer'  
  
export default function SpacerDemo() {  
  return (  
    <View style={styles.container}>  
      <Text style={styles.heading}>Spacer Demo</Text>  
  
      <Text style={styles.text}>Above</Text>  
      <Spacer height={16} />  
      <Text style={styles.text}>Below (16px)</Text>  
  
      <Spacer height={24} />  
  
      <View style={styles.row}>  
        <View style={styles.box} />  
        <Spacer width={12} height="auto" />  
        <View style={styles.box} />  
        <Spacer width={12} height="auto" />  
        <View style={styles.box} />  
      </View>  
  
      <Spacer height={24} />  
  
      <Spacer height={1} width="100%" />  
    </View>  
  )  
}  
  
const styles = StyleSheet.create({  
  container: {  
    padding: 16,  
    backgroundColor: '#FFFFFF',  
  },  
  heading: {  
    fontSize: 18,  
    fontWeight: '700',  
    marginBottom: 16,  
  },  
  text: {  
    fontSize: 14,  
    color: '#374151',  
  },  
  row: {  
    flexDirection: 'row',  
    alignItems: 'center',  
  },  
  box: {  
    width: 40,  
    height: 40,  
    borderRadius: 6,  
    backgroundColor: '#E5E7EB',  
  },  
})
```

## 6. Divider

Press enter or click to view image in full size

![React Native Divider UI component]()

Dividers are also a simple UI element, but they add detail to UI UX.

You’ll often see a horizontal line separating content sections.

With this component, you can create a plain line, a dashed line, or even a divider with text in between.

**Divider Component Code**

```
import React from 'react'  
import { StyleSheet, Text, TextStyle, View, ViewStyle } from 'react-native'  
  
interface DividerProps {  
  color?: string  
  thickness?: number  
  spacing?: number  
  vertical?: boolean  
  text?: string  
  dashed?: boolean  
  style?: ViewStyle  
  textStyle?: TextStyle  
}  
  
export default function Divider({  
  color = '#E5E7EB',  
  thickness = 1,  
  spacing = 16,  
  vertical = false,  
  text,  
  dashed = false,  
  style,  
  textStyle,  
}: DividerProps) {  
  if (text && !vertical) {  
    return (  
      <View style={[styles.textContainer, { marginVertical: spacing }]}>  
        <Line color={color} thickness={thickness} dashed={dashed} />  
        <Text style={[styles.text, textStyle]}>{text}</Text>  
        <Line color={color} thickness={thickness} dashed={dashed} />  
      </View>  
    )  
  }  
  
  return (  
    <View  
      style={[  
        styles.line,  
        {  
          backgroundColor: dashed ? 'transparent' : color,  
          marginVertical: vertical ? 0 : spacing,  
          marginHorizontal: vertical ? spacing : 0,  
          ...(vertical  
            ? { width: thickness, height: '100%' }  
            : { height: thickness, width: '100%' }),  
          borderStyle: dashed ? 'dashed' : 'solid',  
          borderWidth: dashed ? thickness : 0,  
          borderColor: dashed ? color : undefined,  
        },  
        style,  
      ]}  
    />  
  )  
}  
  
interface LineProps {  
  color: string  
  thickness: number  
  dashed: boolean  
}  
  
function Line({ color, thickness, dashed }: LineProps) {  
  return (  
    <View  
      style={[  
        styles.flexLine,  
        {  
          height: thickness,  
          backgroundColor: dashed ? 'transparent' : color,  
          borderStyle: dashed ? 'dashed' : 'solid',  
          borderWidth: dashed ? thickness : 0,  
          borderColor: dashed ? color : undefined,  
        },  
      ]}  
    />  
  )  
}  
  
const styles = StyleSheet.create({  
  line: {  
    alignSelf: 'stretch',  
  },  
  
  flexLine: {  
    flex: 1,  
  },  
  
  textContainer: {  
    flexDirection: 'row',  
    alignItems: 'center',  
  },  
  
  text: {  
    marginHorizontal: 12,  
    fontSize: 13,  
    fontWeight: '500',  
    color: '#6B7280',  
  },  
})
```

**Use Case with Demo**

```
import React from 'react'  
import { StyleSheet, Text, View } from 'react-native'  
import Divider from '../ui/divider'  
  
export default function DividerDemo() {  
  return (  
    <View style={styles.container}>  
      <Text style={styles.heading}>Divider Examples</Text>  
  
      {/* Basic divider */}  
      <Divider />  
  
      <Text style={styles.sectionText}>Content Section</Text>  
  
      {/* With spacing */}  
      <Divider spacing={24} />  
  
      {/* Dashed divider */}  
      <Divider dashed />  
  
      <Text style={styles.sectionText}>Another Section</Text>  
  
      {/* Text divider */}  
      <Divider text="OR" />  
  
      {/* Custom text */}  
      <Divider text="CONTINUE" dashed textStyle={{ fontSize: 12, letterSpacing: 1 }} />  
  
      {/* Vertical divider */}  
      <View style={styles.row}>  
        <Text style={styles.inlineText}>Left</Text>  
        <Divider vertical style={{ height: 24 }} />  
        <Text style={styles.inlineText}>Right</Text>  
      </View>  
    </View>  
  )  
}  
  
const styles = StyleSheet.create({  
  container: {  
    padding: 16,  
    backgroundColor: '#FFFFFF',  
  },  
  
  heading: {  
    fontSize: 18,  
    fontWeight: '700',  
    color: '#111827',  
    marginBottom: 16,  
  },  
  
  sectionText: {  
    fontSize: 14,  
    color: '#374151',  
    marginVertical: 8,  
  },  
  
  row: {  
    flexDirection: 'row',  
    alignItems: 'center',  
    gap: 12,  
    marginTop: 24,  
  },  
  
  inlineText: {  
    fontSize: 14,  
    color: '#374151',  
  },  
})
```

Did this help you?

This is my second article on React Native.

Visit my profile to read my other articles, and follow me for more React Native content.
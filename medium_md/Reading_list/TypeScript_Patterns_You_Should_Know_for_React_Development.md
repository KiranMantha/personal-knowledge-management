---
title: "TypeScript Patterns You Should Know for React Development"
url: https://medium.com/p/d43129494027
---

# TypeScript Patterns You Should Know for React Development

[Original](https://medium.com/p/d43129494027)

# TypeScript Patterns You Should Know for React Development

[![Frontend Highlights](https://miro.medium.com/v2/resize:fill:64:64/1*ISIQMnQqz3UzRTGB0_d4jw.jpeg)](/@ignatovich.dm?source=post_page---byline--d43129494027---------------------------------------)

[Frontend Highlights](/@ignatovich.dm?source=post_page---byline--d43129494027---------------------------------------)

3 min read

·

Dec 27, 2024

--

3

Listen

Share

More

As TypeScript adoption continues to grow in the React ecosystem, understanding advanced patterns can dramatically improve your code quality, scalability, and developer experience. This article highlights essential TypeScript patterns for React development, along with practical examples to help you make the most of these tools.

## 1. Discriminated Unions: Managing Complex State

Discriminated unions are a powerful way to handle state with multiple variations or “modes.” By combining union types with a “discriminator” property, you can ensure type safety and avoid bugs caused by invalid states.

Example: Loading States

```
type FetchState =  
  | { status: 'idle' }  
  | { status: 'loading' }  
  | { status: 'success'; data: string[] }  
  | { status: 'error'; error: string };  
  
const fetchReducer = (state: FetchState, action: any): FetchState => {  
  switch (action.type) {  
    case 'FETCH_START':  
      return { status: 'loading' };  
    case 'FETCH_SUCCESS':  
      return { status: 'success', data: action.payload };  
    case 'FETCH_ERROR':  
      return { status: 'error', error: action.payload };  
    default:  
      return state;  
  }  
};
```

**Why It’s Useful:**  
Discriminated unions allow your state transitions to be explicit, avoiding invalid combinations like having both `data` and `error`.

## 2. Generics: Reusable and Flexible Components

Generics make your components or hooks reusable while preserving strong type definitions. This is particularly helpful for handling lists, forms, or APIs with varying data structures.

Example: Reusable Table Component

```
type TableProps<T> = {  
  data: T[];  
  renderRow: (item: T) => React.ReactNode;  
};  
  
function Table<T>({ data, renderRow }: TableProps<T>) {  
  return (  
    <table>  
      <tbody>{data.map((item, index) => <tr key={index}>{renderRow(item)}</tr>)}</tbody>  
    </table>  
  );  
}  
  
// Usage  
type User = { id: number; name: string };  
const users: User[] = [{ id: 1, name: 'Alice' }, { id: 2, name: 'Bob' }];  
  
<Table  
  data={users}  
  renderRow={(user) => (  
    <>  
      <td>{user.id}</td>  
      <td>{user.name}</td>  
    </>  
  )}  
/>;
```

**Why It’s Useful:**  
Generics make your components adaptable without losing the benefits of type inference, saving you from repetitive code.

## 3. Mapped Types: Transforming Props and State

Mapped types allow you to create new types by transforming existing ones. This is especially helpful when defining derived states or prop interfaces.

Example: Partial Form Props

```
type FormValues = {  
  name: string;  
  email: string;  
  age: number;  
};  
  
type FormErrors<T> = {  
  [K in keyof T]?: string;  
};  
  
const errors: FormErrors<FormValues> = {  
  name: "Name is required",  
  email: "Email is invalid",  
};
```

**Why It’s Useful:**  
Mapped types are ideal for managing forms, APIs, or configuration objects with varying properties.

## 4. Advanced Typing for React Props and State

### Typed Props with `defaultProps`

When using `defaultProps`, you can ensure type safety by leveraging TypeScript’s partial type support.

```
type ButtonProps = {  
  label: string;  
  onClick?: () => void;  
};  
  
const Button = ({ label, onClick = () => {} }: ButtonProps) => (  
  <button onClick={onClick}>{label}</button>  
);
```

### Readonly State

To enforce immutability in your state, use `Readonly` or `ReadonlyArray`.

```
type State = Readonly<{  
  items: string[];  
}>;  
  
const [state, setState] = useState<State>({ items: ['Item 1'] });
```

**Why It’s Useful:**  
Strongly typed props and state reduce runtime errors and make your intent clear to other developers.

## 5. Dynamic Forms with TypeScript and React

Dynamic forms often involve complex types that depend on user inputs. TypeScript can help enforce correctness, even for dynamic structures.

Example: Dynamic Form Fields

```
type Field = {  
  id: string;  
  label: string;  
  value: string;  
};  
  
type FormState = {  
  fields: Field[];  
};  
  
const DynamicForm: React.FC = () => {  
  const [formState, setFormState] = useState<FormState>({ fields: [] });  
  
  const addField = () => {  
    setFormState((prev) => ({  
      fields: [...prev.fields, { id: Date.now().toString(), label: '', value: '' }],  
    }));  
  };  
  
  return (  
    <div>  
      {formState.fields.map((field) => (  
        <input  
          key={field.id}  
          placeholder={field.label}  
          value={field.value}  
          onChange={(e) =>  
            setFormState((prev) => ({  
              fields: prev.fields.map((f) =>  
                f.id === field.id ? { ...f, value: e.target.value } : f  
              ),  
            }))  
          }  
        />  
      ))}  
      <button onClick={addField}>Add Field</button>  
    </div>  
  );  
};
```

**Why It’s Useful:**  
Dynamic forms are a common feature in many applications. TypeScript ensures that each field is properly typed and updated.

## Conclusion

TypeScript is more than just a static typing tool — it’s a way to write more robust, maintainable, and scalable React applications. By mastering patterns like discriminated unions, generics, and advanced prop typing, you can unlock the full potential of TypeScript in your projects. Whether you’re building dynamic forms, reusable components, or managing complex state, these patterns ensure a smooth and efficient development experience.
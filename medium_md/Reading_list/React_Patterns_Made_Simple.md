---
title: "React Patterns Made Simple"
url: https://medium.com/p/f55a2d885294
---

# React Patterns Made Simple

[Original](https://medium.com/p/f55a2d885294)

# React Patterns Made Simple

[![Babek Naghiyev](https://miro.medium.com/v2/resize:fill:64:64/1*RRnM2mu8OjgR5vbDyi39Pg@2x.jpeg)](/?source=post_page---byline--f55a2d885294---------------------------------------)

[Babek Naghiyev](/?source=post_page---byline--f55a2d885294---------------------------------------)

5 min read

·

Aug 3, 2025

--

5

Listen

Share

More

Press enter or click to view image in full size

![]()

## Factory Pattern

Pick the right component based on data.

```
function ButtonFactory({ type, children, onClick }) {  
  if (type === 'primary') {  
    return <Button className="bg-blue-500 text-white px-4 py-2" onClick={onClick}>{children}</button>;  
  }  
    
  if (type === 'danger') {  
    return <Button className="bg-red-500 text-white px-4 py-2" onClick={onClick}>{children}</button>;  
  }  
    
  return <Button className="bg-gray-300 px-4 py-2" onClick={onClick}>{children}</button>;  
}
```

```
// Icon factory  
icons = {  
  'home': () => lazy(() => import('./HomeIcon.tsx')),  
}  
  
function Icon({ name, size = 24 }) {  
  const iconFactory = icons[name];  
  const Component = iconFactory ? iconFactory() : null;  
  return (  
      <Component size={size}/>  
  );  
}  
// Usage  
function App() {  
  return (  
    <div>  
      <ButtonFactory type="primary">Save</Button>  
      <ButtonFactory type="danger">Delete</Button>  
      <Icon name="heart" size={32} />  
      <Icon name="star" />  
    </div>  
  );  
}
```

## Singleton Pattern

One shared thing across your whole app.

```
// Simple global store  
let globalUser = null;  
let listeners = [];  
  
const userStore = {  
  getUser: () => globalUser,  
    
  setUser: (user) => {  
    globalUser = user;  
    listeners.forEach(callback => callback(user));  
  },  
    
  subscribe: (callback) => {  
    listeners.push(callback);  
    return () => {  
      listeners = listeners.filter(l => l !== callback);  
    };  
  }  
};  
// Hook to use the store  
function useUser() {  
  const [user, setUser] = useState(userStore.getUser());  
    
  useEffect(() => {  
    const unsubscribe = userStore.subscribe(setUser);  
    return unsubscribe;  
  }, []);  
    
  return {  
    user,  
    login: (newUser) => userStore.setUser(newUser),  
    logout: () => userStore.setUser(null)  
  };  
}  
// Components using the same user  
function Header() {  
  const { user, logout } = useUser();  
    
  return (  
    <header>  
      {user ? (  
        <div>  
          Hello, {user.name}!   
          <button onClick={logout}>Logout</button>  
        </div>  
      ) : (  
        <div>Please login</div>  
      )}  
    </header>  
  );  
}  
function Profile() {  
  const { user } = useUser();  
    
  if (!user) return <div>Not logged in</div>;  
    
  return (  
    <div>  
      <h1>{user.name}</h1>  
      <p>{user.email}</p>  
    </div>  
  );  
}
```

## Observer Pattern

Components that watch for changes.

```
// Simple event system  
const events = {  
  listeners: {},  
    
  on: (event, callback) => {  
    if (!events.listeners[event]) {  
      events.listeners[event] = [];  
    }  
    events.listeners[event].push(callback);  
  },  
    
  emit: (event, data) => {  
    if (events.listeners[event]) {  
      events.listeners[event].forEach(callback => callback(data));  
    }  
  }  
};  
  
// Shopping cart that others can watch  
function useCart() {  
  const [items, setItems] = useState([]);  
    
  const addItem = (item) => {  
    const newItems = [...items, item];  
    setItems(newItems);  
    events.emit('cart-changed', newItems);  
  };  
    
  return { items, addItem };  
}  
// Cart counter that watches cart changes  
function CartCounter() {  
  const [count, setCount] = useState(0);  
    
  useEffect(() => {  
    events.on('cart-changed', (items) => {  
      setCount(items.length);  
    });  
  }, []);  
    
  return <div>Cart: {count} items</div>;  
}  
// Product that adds to cart  
function Product({ product }) {  
  const { addItem } = useCart();  
    
  return (  
    <div>  
      <h3>{product.name}</h3>  
      <p>${product.price}</p>  
      <button onClick={() => addItem(product)}>  
        Add to Cart  
      </button>  
    </div>  
  );  
}
```

## Strategy Pattern

Different ways to do the same thing.

```
const sortMethods = {  
  name: (items) => [...items].sort((a, b) => a.name.localeCompare(b.name)),  
  price: (items) => [...items].sort((a, b) => a.price - b.price),  
  newest: (items) => [...items].sort((a, b) => new Date(b.date) - new Date(a.date))  
};  
  
  
function ProductList({ products }) {  
  const [sortBy, setSortBy] = useState('name');  
    
  const sortedProducts = sortMethods[sortBy](products);  
    
  return (  
    ...  
  );  
}  
// Usage  
function SignupForm() {  
  return (  
    <form>  
      <FormField   
        name="email"   
        type="email"   
        validation={['required', 'email']}  
        placeholder="Email"  
      />  
      <FormField   
        name="password"   
        type="password"   
        validation={['required', validators.minLength(8)]}  
        placeholder="Password"  
      />  
    </form>  
  );  
}
```

## Command Pattern

Save actions so you can undo them.

```
function useUndo() {  
  const [history, setHistory] = useState([]);  
  const [current, setCurrent] = useState(-1);  
    
  const execute = (action, undo) => {  
    const newHistory = history.slice(0, current + 1);  
    newHistory.push({ action, undo });  
    setHistory(newHistory);  
    setCurrent(newHistory.length - 1);  
    action();  
  };  
    
  const undo = () => {  
    if (current >= 0) {  
      history[current].undo();  
      setCurrent(current - 1);  
    }  
  };  
    
  const redo = () => {  
    if (current < history.length - 1) {  
      const next = current + 1;  
      history[next].action();  
      setCurrent(next);  
    }  
  };  
    
  return {  
    execute,  
    undo,  
    redo,  
    canUndo: current >= 0,  
    canRedo: current < history.length - 1  
  };  
}
```

```
function DrawingApp() {  
  const [lines, setLines] = useState([]);  
  const { execute, undo, redo, canUndo, canRedo } = useUndo();  
    
  const addLine = (line) => {  
    execute(  
      () => setLines(prev => [...prev, line]),  
      () => setLines(prev => prev.slice(0, -1))  
    );  
  };  
    
  const clearAll = () => {  
    const oldLines = lines;  
    execute(  
      () => setLines([]),  
      () => setLines(oldLines)  
    );  
  };  
    
  return (  
    <div>  
      <button onClick={undo} disabled={!canUndo}>Undo</button>  
      <button onClick={redo} disabled={!canRedo}>Redo</button>  
      <button onClick={clearAll}>Clear</button>  
        
      <div>  
        {lines.map((line, i) => (  
          <div key={i}>{line}</div>  
        ))}  
      </div>  
        
      <button onClick={() => addLine(`Line ${lines.length + 1}`)}>  
        Add Line  
      </button>  
    </div>  
  );  
}
```

## Decorator Pattern

Add extra stuff to components.

```
function withLoading(Component) {  
  return function LoadingComponent({ isLoading, ...props }) {  
    if (isLoading) {  
      return <div>Loading...</div>;  
    }  
    return <Component {...props} />;  
  };  
}
```

```
// Add error handling  
function withError(Component) {  
  return function ErrorComponent({ error, ...props }) {  
    if (error) {  
      return <div style={{color: 'red'}}>Error: {error}</div>;  
    }  
    return <Component {...props} />;  
  };  
}  
// Original component  
function UserList({ users }) {  
  return (  
    <ul>  
      {users.map(user => (  
        <li key={user.id}>{user.name}</li>  
      ))}  
    </ul>  
  );  
}  
// Enhanced component  
const EnhancedUserList = withError(withLoading(UserList));  
function App() {  
  const [users, setUsers] = useState([]);  
  const [loading, setLoading] = useState(true);  
  const [error, setError] = useState(null);  
    
  useEffect(() => {  
    fetch('/api/users')  
      .then(res => res.json())  
      .then(setUsers)  
      .catch(setError)  
      .finally(() => setLoading(false));  
  }, []);  
    
  return (  
    <EnhancedUserList   
      users={users}  
      isLoading={loading}  
      error={error}  
    />  
  );  
}
```

## Adapter Pattern

Make different things work the same way.

```
// Different data formats  
const oldApiUser = {  
  user_name: 'John',  
  user_email: 'john@email.com',  
  profile_pic: 'pic.jpg'  
};  
  
const newApiUser = {  
  name: 'John',  
  email: 'john@email.com',  
  avatar: 'pic.jpg'  
};  
// Adapter function  
function adaptUser(user, format) {  
  if (format === 'old') {  
    return {  
      name: user.user_name,  
      email: user.user_email,  
      avatar: user.profile_pic  
    };  
  }  
  return user; // already new format  
}  
function UserCard({ user, format = 'new' }) {  
  const adaptedUser = adaptUser(user, format);  
    
  return (  
    <div>  
      <img src={adaptedUser.avatar} alt={adaptedUser.name} />  
      <h3>{adaptedUser.name}</h3>  
      <p>{adaptedUser.email}</p>  
    </div>  
  );  
}  
// Usage with different data  
function App() {  
  return (  
    <div>  
      <UserCard user={oldApiUser} format="old" />  
      <UserCard user={newApiUser} format="new" />  
    </div>  
  );  
}
```

## Compound Components

Components that work together.

```
function Modal({ isOpen, onClose, children }) {  
  if (!isOpen) return null;  
    
  return (  
    <div className="modal-backdrop" onClick={onClose}>  
      <div className="modal-content" onClick={e => e.stopPropagation()}>  
        {children}  
      </div>  
    </div>  
  );  
}
```

```
Modal.Header = function ModalHeader({ children }) {  
  return <div className="modal-header">{children}</div>;  
};  
Modal.Body = function ModalBody({ children }) {  
  return <div className="modal-body">{children}</div>;  
};  
Modal.Footer = function ModalFooter({ children }) {  
  return <div className="modal-footer">{children}</div>;  
};  
// Easy to use  
function App() {  
  const [showModal, setShowModal] = useState(false);  
    
  return (  
    <div>  
      <button onClick={() => setShowModal(true)}>Open Modal</button>  
        
      <Modal isOpen={showModal} onClose={() => setShowModal(false)}>  
        <Modal.Header>  
          <h2>Delete Item</h2>  
        </Modal.Header>  
        <Modal.Body>  
          <p>Are you sure you want to delete this?</p>  
        </Modal.Body>  
        <Modal.Footer>  
          <button onClick={() => setShowModal(false)}>Cancel</button>  
          <button onClick={() => setShowModal(false)}>Delete</button>  
        </Modal.Footer>  
      </Modal>  
    </div>  
  );  
}
```

## Custom Hooks

Share logic between components.

```
// Simple data fetching hook  
function useApi(url) {  
  const [data, setData] = useState(null);  
  const [loading, setLoading] = useState(true);  
  const [error, setError] = useState(null);  
    
  useEffect(() => {  
    fetch(url)  
      .then(res => res.json())  
      .then(setData)  
      .catch(setError)  
      .finally(() => setLoading(false));  
  }, [url]);  
    
  return { data, loading, error };  
}
```

```
// Use the same logic in different components  
function UserProfile() {  
  const { data: user, loading, error } = useApi('/api/user');  
    
  if (loading) return <div>Loading user...</div>;  
  if (error) return <div>Error loading user</div>;  
    
  return <div>Hello, {user.name}!</div>;  
}  
function UserPosts() {  
  const { data: posts, loading, error } = useApi('/api/posts');  
    
  if (loading) return <div>Loading posts...</div>;  
  if (error) return <div>Error loading posts</div>;  
    
  return (  
    <ul>  
      {posts.map(post => <li key={post.id}>{post.title}</li>)}  
    </ul>  
  );  
}
```

## When to Use What

* **Factory**: Different components based on data type
* **Singleton**: Global stuff like user state, theme
* **Observer**: Components that react to events
* **Strategy**: Different ways to do the same task
* **Command**: When you need undo/redo
* **Decorator**: Add features without changing original
* **Adapter**: Handle different data formats
* **Compound**: Components that belong together
* **Custom Hooks**: Share logic between components

Keep it simple. Use patterns when they solve real problems, not because they’re cool.

Clap and share if you liked.
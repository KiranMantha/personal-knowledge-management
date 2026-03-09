---
title: "Implementing MVVM in React: A Real-World Guide"
url: https://medium.com/p/479529545721
---

# Implementing MVVM in React: A Real-World Guide

[Original](https://medium.com/p/479529545721)

# Implementing MVVM in React: A Real-World Guide

[![Digvijay Mahapatra](https://miro.medium.com/v2/resize:fill:64:64/1*8ASM5Vrc-KPbd57PwBEy3g.png)](https://medium.com/@gitfudge?source=post_page---byline--479529545721---------------------------------------)

[Digvijay Mahapatra](https://medium.com/@gitfudge?source=post_page---byline--479529545721---------------------------------------)

4 min read

·

Nov 20, 2024

--

6

Listen

Share

More

Press enter or click to view image in full size

![]()

Hey folks! 👋 After spending some time building React applications, I’ve found that as apps grow larger, maintaining a clean architecture becomes crucial. Today, I’ll share how implementing MVVM (Model-View-ViewModel) pattern in React has saved our team from countless headaches and made our codebase much more manageable.

## Why Should You Care? The Good Stuff First! 🎯

**1. Your Code Becomes Super Organized**  
 — Clear separation between data, logic, and UI components  
 — Each part of your code has one job and does it well  
 — No more “where should I put this logic?” moments

**2. Testing Becomes a Breeze**  
 — Business logic is isolated in ViewModels  
 — UI components are purely presentational  
 — You can test each part independently without mocking the entire universe

**3. Reusability On Steroids**  
 — ViewModels can be reused across different components  
 — Logic stays consistent throughout your app  
 — Less copy-paste, more single source of truth

**4. State Management That Makes Sense**  
 — Clear data flow throughout your application  
 — Predictable state updates  
 — Easier debugging when things go wrong (and they will!)

## Let’s See It In Action! 💻

Let’s build a simple e-commerce product listing page with filters and sorting. Here’s how we’d structure it using MVVM:

## Directory Structure

```
src/  
├── pages/  
│ └── ProductsPage/  
│ ├── index.tsx      # Main page component  
│ ├── index.hook.ts  # Page hook  
│ ├── index.store.ts # State management  
│ ├── ViewModel.ts   # ViewModel implementation  
│ ├── types.ts       # TypeScript interfaces  
│ ├── components/   
│ │ ├── ProductGrid/  
│ │ ├── FilterPanel/  
│ │ └── SortingOptions/  
│ └── styles/
```

## 1. Define Your Model

```
// models/Product.model.ts  
export interface Product {  
 id: string;  
 name: string;  
 price: number;  
 category: string;  
 inStock: boolean;  
}  
  
export interface FilterOptions {  
 category: string[];  
 minPrice: number;  
 maxPrice: number;  
 inStock: boolean;  
}
```

## 2. Set Up Your Store

```
// pages/ProductsPage/index.store.ts  
import { create } from ‘zustand’;  
  
interface ProductsPageState {  
  products: Product[];  
  filters: FilterOptions;  
  setProducts: (products: Product[]) => void;  
  setFilters: (filters: FilterOptions) => void;  
}  
  
const useProductsStore = create<ProductsPageState>((set) => ({  
  products: [],  
  filters: {  
   category: [],  
   minPrice: 0,  
   maxPrice: 1000,  
   inStock: false  
  },  
  setProducts: (products) => set({ products }),  
  setFilters: (filters) => set({ filters })  
}));
```

## 3. Create Your ViewModel

```
// pages/ProductsPage/ViewModel.ts  
class ProductsViewModel {  
  private store: ProductsStore;  
  private uiStore: UIStore;  
  
  constructor(store: ProductsStore, uiStore: UIStore) {  
    this.store = store;  
    this.uiStore = uiStore;  
  }  
  
  public async fetchProducts() {  
    try {  
      this.uiStore.showLoader();  
      const { data } = await ProductsAPI.getProducts(this.store.filters);  
      this.store.setProducts(data);  
    } catch (error) {  
      toast.error(‘Could not fetch products’);  
    } finally {  
      this.uiStore.hideLoader();  
    }  
  }  
  
  public updateFilters(filters: Partial<FilterOptions>) {  
    this.store.setFilters({  
      …this.store.filters,  
      …filters  
    });  
  }  
  
  public shouldShowEmptyState(): boolean {  
    return !this.uiStore().isLoading && this.getFilteredProducts().length === 0;  
  }  
  
  public shouldShowError(): boolean {  
    return !!this.uiStore().error;  
  }  
  
  public shouldShowLoading(): boolean {  
    return this.uiStore().isLoading;  
  }  
  
  public shouldShowProductDetails(): boolean {  
    return !!this.uiStore().selectedProductId;  
  }  
}
```

## 4. The Custom Hook

```
// pages/ProductsPage/index.hook.ts  
const useProductsPage = () => {  
  const productsStore = useProductsStore();  
  const uiStore = useUIStore();  
  const viewModel = new ProductsViewModel(productsStore, uiStore);  
    
  // isRefreshing and refreshDone are here in case you have logic that’s outside the viewmodel and specific to the page itself  
  return {  
    viewModel,  
    isRefreshing: uiStore.isRefreshing,  
    refreshDone: () => uiStore.setRefreshing(false),  
  };  
};
```

## 5. The View Component

```
// pages/ProductsPage/index.tsx  
const ProductsPage: FC = () => {  
  const { viewModel, isRefreshing, refreshDone } = useProductsPage();  
    
  useEffect(() => {  
    viewModel.fetchProducts();  
  }, [viewModel]);  
  
  useEffect(() => {  
    if (isRefreshing) {  
      viewModel.fetchProducts();  
      refreshDone();  
    }  
  }, [isRefreshing]);  
  
  return (  
    <div className=”products-page”>  
      <FilterPanel />  
      <ProductGrid />  
      <SortingOptions />  
    </div>  
  );  
};
```

## Best Practices I’ve Learned the Hard Way 😅

### **1. Keep ViewModels Focused**

```
// Good  
class ProductsViewModel {  
  fetchProducts() { /* … */ }  
  updateFilters() { /* … */ }  
  sortProducts() { /* … */ }  
}  
  
// Bad — mixing concerns  
class ProductsViewModel {  
  fetchProducts() { /* … */ }  
  updateUserProfile() { /* … */ }  
  handleCheckout() { /* … */ }  
}
```

### 2. Handle Cleanup Properly

```
useEffect(() => {  
  const controller = new AbortController();  
  viewModel.fetchProducts(controller.signal);  
    
  return () => controller.abort();  
}, [viewModel]);
```

### 3. Don’t Memoize ViewModels

```
// Good  
const viewModel = new ProductsViewModel(store);  
  
// Bad — will break reactivity  
const viewModel = useMemo(() => new ProductsViewModel(store), [store]);
```

## The Not-So-Great Parts (Let’s Be Honest) 😕

**1. More Boilerplate**  
 — You’ll write more initial code  
 — More files to manage  
 — Steeper learning curve for new team members

**2. Might Be Overkill**  
 — For simple CRUD apps, this could be excessive  
 — Small projects might not see the benefits  
 — Takes time to set up properly

**3. Team Buy-in Required**  
 — Everyone needs to understand and follow the pattern  
 — Requires consistent conventions  
 — Documentation becomes crucial

## Wrapping Up 🎁

MVVM in React isn’t a silver bullet, but it’s been a game-changer for our team’s productivity and code quality. Start small, maybe implement it in one feature first, and see how it feels. Remember, the goal is to make your code more maintainable and your life easier!

Feel free to drop any questions in the comments. Happy coding! 🚀

## Optimizations

[**Read further**](https://medium.com/p/71e20b1e8197) on how we solve view model instance duplication and keep the GC happy

Find the repository that puts the MVVM architecture in practice [here](https://github.com/gitfudge0/mvvm-base), but I’d recommend reading the next article in the series before doing so.

## In Plain English 🚀

*Thank you for being a part of the* [***In Plain English***](https://plainenglish.io/) *community! Before you go:*

* Be sure to **clap** and **follow** the writer ️👏**️️**
* Follow us: [**X**](https://x.com/inPlainEngHQ) | [**LinkedIn**](https://www.linkedin.com/company/inplainenglish/) | [**YouTube**](https://www.youtube.com/channel/UCtipWUghju290NWcn8jhyAw) | [**Discord**](https://discord.gg/in-plain-english-709094664682340443) | [**Newsletter**](https://newsletter.plainenglish.io/) | [**Podcast**](https://open.spotify.com/show/7qxylRWKhvZwMz2WuEoua0)
* [**Create a free AI-powered blog on Differ.**](https://differ.blog/)
* More content at [**PlainEnglish.io**](https://plainenglish.io/)
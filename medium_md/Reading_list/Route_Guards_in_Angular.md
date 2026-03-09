---
title: "Route Guards in Angular"
url: https://medium.com/p/c9da0d815ef4
---

# Route Guards in Angular

[Original](https://medium.com/p/c9da0d815ef4)

Press enter or click to view image in full size

![]()

# Route Guards in Angular

[![hisham abd elshafouk](https://miro.medium.com/v2/da:true/resize:fill:64:64/0*efF0KWFwO1AUGTOE)](/@hish.abdelshafouk?source=post_page---byline--c9da0d815ef4---------------------------------------)

[hisham abd elshafouk](/@hish.abdelshafouk?source=post_page---byline--c9da0d815ef4---------------------------------------)

4 min read

·

Nov 20, 2023

--

Listen

Share

More

In Angular, guards are special classes used to control and manage access to different parts of an application. They decide whether a user can navigate to a particular route or perform certain actions based on specific conditions, like checking if the user is logged in or has the necessary permissions. Guards act as gatekeepers, allowing or preventing access to different parts of the application, ensuring security and controlling the flow of navigation within the app.

## Types of Route Guards in Angular:

### CanActivate:

* Determines if a route can be activated and allows navigation based on certain conditions.
* Implemented using `CanActivate` interface.

### Use Case — Authentication Guard:

Let’s say you have an application with a dashboard page that should only be accessible to authenticated users. The `CanActivate` guard ensures that only authenticated users can access this page, redirecting unauthenticated users to the login page.

AuthGuard Service:

```
import { Injectable } from '@angular/core';  
import { CanActivate, Router } from '@angular/router';  
import { AuthService } from './auth.service';  
  
@Injectable({  
  providedIn: 'root'  
})  
export class AuthGuard implements CanActivate {  
  
  constructor(private authService: AuthService, private router: Router) {}  
  
  canActivate(): boolean {  
    if (this.authService.isAuthenticated()) {  
      return true; // Allow access if the user is authenticated  
    } else {  
      this.router.navigate(['/login']); // Redirect to login if not authenticated  
      return false; // Prevent access to the route  
    }  
  }  
}
```

Route Configuration:

```
import { NgModule } from '@angular/core';  
import { Routes, RouterModule } from '@angular/router';  
import { DashboardComponent } from './dashboard.component';  
import { AuthGuard } from './auth.guard';  
  
const routes: Routes = [  
  {  
    path: 'dashboard',  
    component: DashboardComponent,  
    canActivate: [AuthGuard] // Apply the AuthGuard to protect the dashboard route  
  },  
  // Other route configurations  
];  
  
@NgModule({  
  imports: [RouterModule.forRoot(routes)],  
  exports: [RouterModule]  
})  
export class AppRoutingModule { }
```

AuthService:

This assumes there’s an `AuthService` that provides a method `isAuthenticated()` to check if the user is logged in.

### CanActivateChild:

* Similar to `CanActivate` but controls the activation of child routes.
* Implemented using `CanActivateChild` interface.

### Use Case — Admin Panel Access:

Imagine an admin panel within an application containing multiple child routes that should only be accessible to authenticated administrators.

AuthGuard Service:

```
import { Injectable } from '@angular/core';  
import { CanActivateChild, Router } from '@angular/router';  
import { AuthService } from './auth.service';  
  
@Injectable({  
  providedIn: 'root'  
})  
export class AdminAuthGuard implements CanActivateChild {  
  
  constructor(private authService: AuthService, private router: Router) {}  
  
  canActivateChild(): boolean {  
    if (this.authService.isUserLoggedIn() && this.authService.isAdmin()) {  
      return true; // Allow access if the user is logged in and is an admin  
    } else {  
      this.router.navigate(['/unauthorized']); // Redirect if not authorized  
      return false; // Prevent access to admin child routes  
    }  
  }  
}
```

Route Configuration:

```
import { NgModule } from '@angular/core';  
import { Routes, RouterModule } from '@angular/router';  
import { AdminPanelComponent } from './admin-panel.component';  
import { AdminAuthGuard } from './admin-auth.guard';  
  
const routes: Routes = [  
  {  
    path: 'admin',  
    component: AdminPanelComponent,  
    canActivateChild: [AdminAuthGuard], // Apply AdminAuthGuard to protect child routes  
    children: [  
      // Child routes accessible only to authenticated admins  
      // Example: /admin/users, /admin/settings, etc.  
    ]  
  },  
  // Other route configurations  
];  
  
@NgModule({  
  imports: [RouterModule.forRoot(routes)],  
  exports: [RouterModule]  
})  
export class AppRoutingModule { }
```

### CanDeactivate:

* Checks if a route can be deactivated, often used to confirm navigation away from a route.
* Implemented using `CanDeactivate` interface.

### Use Case — Preventing Unsaved Changes:

Consider a form-editing feature within an application where users can modify certain data. You want to ensure that users are prompted with a confirmation before leaving the editing page if they’ve made changes that haven’t been saved.

Deactivation Guard Service:

```
import { Injectable } from '@angular/core';  
import { CanDeactivate } from '@angular/router';  
import { Observable } from 'rxjs';  
import { EditComponent } from './edit.component';  
  
export interface CanComponentDeactivate {  
  canDeactivate: () => Observable<boolean> | Promise<boolean> | boolean;  
}  
  
@Injectable({  
  providedIn: 'root'  
})  
export class PreventUnsavedChangesGuard implements CanDeactivate<CanComponentDeactivate> {  
  
  canDeactivate(component: CanComponentDeactivate): Observable<boolean> | Promise<boolean> | boolean {  
    return component.canDeactivate ? component.canDeactivate() : true;  
  }  
}
```

Component Implementation:

```
import { Component } from '@angular/core';  
import { CanComponentDeactivate } from './prevent-unsaved-changes.guard';  
  
@Component({  
  selector: 'app-edit',  
  template: `  
    <!-- Your edit form -->  
  `  
})  
export class EditComponent implements CanComponentDeactivate {  
  
  // Track if changes are made to the form  
  hasUnsavedChanges = false;  
  
  // Method to check if there are unsaved changes  
  canDeactivate(): boolean {  
    if (this.hasUnsavedChanges) {  
      return confirm('You have unsaved changes. Are you sure you want to leave?');  
    }  
    return true;  
  }  
}
```

### CanLoad:

* Prevents a module from being loaded lazily until certain conditions are met.
* Implemented using `CanLoad` interface.

### Use Case — Role-Based Module Loading:

Consider a scenario where your application has a premium feature module that should only be loaded for users with a specific subscription or premium status.

CanLoad Guard Service:

```
import { Injectable } from '@angular/core';  
import { CanLoad, Route, UrlSegment } from '@angular/router';  
import { AuthService } from './auth.service';  
  
@Injectable({  
  providedIn: 'root'  
})  
export class PremiumFeatureGuard implements CanLoad {  
  
  constructor(private authService: AuthService) {}  
  
  canLoad(route: Route, segments: UrlSegment[]): boolean {  
    if (this.authService.isUserPremium()) {  
      return true; // Allow lazy loading if the user is premium  
    } else {  
      // Handle cases where the user is not premium (redirect, show message, etc.)  
      return false; // Prevent lazy loading of the premium feature module  
    }  
  }  
}
```

Lazy Loaded Module Configuration:

```
import { NgModule } from '@angular/core';  
import { RouterModule, Routes } from '@angular/router';  
import { PremiumFeatureGuard } from './premium-feature.guard';  
  
const routes: Routes = [  
  {  
    path: 'premium',  
    canLoad: [PremiumFeatureGuard], // Apply PremiumFeatureGuard to prevent lazy loading  
    loadChildren: () => import('./premium-feature/premium-feature.module').then(m => m.PremiumFeatureModule)  
  },  
  // Other route configurations  
];  
  
@NgModule({  
  imports: [RouterModule.forRoot(routes)],  
  exports: [RouterModule]  
})  
export class AppRoutingModule { }
```
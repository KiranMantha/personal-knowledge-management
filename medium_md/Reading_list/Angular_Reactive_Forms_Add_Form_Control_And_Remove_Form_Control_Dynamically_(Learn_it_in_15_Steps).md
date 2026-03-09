---
title: "Angular Reactive Forms Add Form Control And Remove Form Control Dynamically (Learn it in 15 Steps)"
url: https://medium.com/p/a9c968c7f4b4
---

# Angular Reactive Forms Add Form Control And Remove Form Control Dynamically (Learn it in 15 Steps)

[Original](https://medium.com/p/a9c968c7f4b4)

# Angular Reactive Forms Add Form Control And Remove Form Control Dynamically (Learn it in 15 Steps)

[![Srikanth](https://miro.medium.com/v2/resize:fill:64:64/1*d2bIn_yKaffsKhaB4P-kBA.jpeg)](/?source=post_page---byline--a9c968c7f4b4---------------------------------------)

[Srikanth](/?source=post_page---byline--a9c968c7f4b4---------------------------------------)

11 min read

·

Oct 24, 2022

--

Listen

Share

More

**Hi Everyone !!!,** Thanks for visiting my medium I hope you doing well “**Wish you a very Happy Diwali 2022”**. Please find the below steps to implement the **Reactive Forms** and Also how to **add** and **remove** **form** **controls** in the angular application dynamically.

Press enter or click to view image in full size

![]()

0. Before **starting** the **application**, you need to know about **Reactive Forms** in **angular**. If you know about forms you can **ignore this step.**

***Basically, We are using forms for taking the inputs from the user and storing those inputs inside the database, In that way, we can store the information permanently. For taking the inputs from the user we need to create a form at the UI level.***

***We have a two-way data binding concept in side form syntax to save the details in angular .ts file and sent it back to the server by using ajax calls, But it is not a good way. So in angular, we have two approaches to implement forms and form validations.***

Those are two approaches inside reactive forms,

* Template Driven Forms
* Reactive Forms

But in the **Template-driven forms approach,** we will write most of the code in **Html**. But in this approach, if you want to do any **implementations** most of them we will write inside an **Html** file(validations etc.).

And in the **Reactive Forms approach,** we will write the logic at **.ts** file ( Creating **form groups, form controls, and validations, etc.** )and it is an **industry-level** approach (Meaning most of the **industries** will follow this **approach** only).

**In Reactive Forms,** by using **Form builder** we can create **forms** and In **Form Builder,** we have **form groups, form controls,** and **form arrays.** By combining **form groups, Form arrays** and **form controls** we will create the **forms** **( Here form controls are like input fields ).**

I think you understood something, In the below example, I am going to implement **remove form control** and **add form control** based on **selection** **change** inside **forms**. For more information, please visit the official [**angular.io**](https://angular.io/guide/reactive-forms) website.

1. Create an angular project with the below command.

```
ng new angular-forms-add-or-remove-control
```

2. After **successful creation** of the angular app, change the file directory to **project-name**. by using the below command

```
cd angular-forms-add-or-remove-control
```

3. Open the project in vs code using **“code .”** or open with **“vs code”** after that **run** the project by using the **“ng serve”** command and Open the project in chrome using [***localhost:4200***](http://localhost:4200)

4. Open the **app component** in vs code and **remove the content** which is created by **angular CLI** while creating the app.

> ***If you know how to add bootstrap in the angular application, You can ignore the below step (Step No 5).***

5. **Install** the **bootstrap** library by using the **below command** and also import the URL inside **styles.scss** file to load the **bootstrap styles** inside the **application**.

```
npm install bootstrap
```

* Import the bootstrap in styles.scss file as below

```
@import ‘../node_modules/bootstrap/dist/css/bootstrap.min.css’;
```

6. Open the **“app.module.ts”** file in vs code by using **Ctrl + P** and **add** **“ReactiveFormsModule”**, and **“FormsModule”** in **imports[]**.

```
import { FormsModule, ReactiveFormsModule } from '@angular/forms';  
@NgModule({  
  declarations: [  
    AppComponent,  
    SignupComponent  
  ],  
  imports: [  
    BrowserModule,  
    AppRoutingModule,  
    ReactiveFormsModule,  
    FormsModule  
  ],  
  providers: [],  
  bootstrap: [AppComponent]  
})  
export class AppModule { }
```

7. Open the **“app.component.ts”** file in vs code by using **Ctrl + P** and add “FormBuilder” as a dependency in “**constructor**”.

```
import { Component, OnInit } from '@angular/core';  
import { FormBuilder, FormGroup} from "@angular/forms";  
@Component({  
  selector: 'app-root',  
  templateUrl: './app.component.html',  
  styleUrls: ['./app.component.scss']  
})  
export class AppComponent implements OnInit{public form:FormGroup;  
constructor(private formBuilder: FormBuilder){}public ngOnInit(): void {}  
   
}
```

8. Create a **form variable** above the constructor and **formInit()** method to initialize the **form** and call the **formInit()** method from either **constructor** or **ngOnInit**.

```
import { Component, OnInit } from '@angular/core';  
import { FormBuilder,FormGroup} from "@angular/forms";  
@Component({  
  selector: 'app-root',  
  templateUrl: './app.component.html',  
  styleUrls: ['./app.component.scss']  
})  
export class AppComponent implements OnInit{public form:FormGroup;  
constructor(private formBuilder: FormBuilder){  
  this.formInit();  
}public ngOnInit(): void {}public formInit(){}  
   
}
```

9. And create a **formGroup** using **formBuilder** and add the form controls **e.g. firstName, secondName, etc.** inside the form group in the following way.

```
import { Component, OnInit } from '@angular/core';  
import { FormBuilder, Validators, FormGroup} from "@angular/forms";  
@Component({  
  selector: 'app-root',  
  templateUrl: './app.component.html',  
  styleUrls: ['./app.component.scss']  
})  
export class AppComponent implements OnInit{public form:FormGroup;  
  constructor(private formBuilder: FormBuilder){  
    this.formInit()  
  }public ngOnInit(): void {}public formInit(){  
    this.form = this.formBuilder.group({  
      firstName:['', Validators.required],  
      secondName:['', Validators.required],  
      middleName:[''],  
      username:['', Validators.required],  
      email:['', Validators.required],  
      mobile:['', [Validators.required,Validators.minLength(10),Validators.maxLength(10)]],  
      password:['', Validators.required],  
      workStatus:['', Validators.required],  
      gender:['', Validators.required],  
      qualifications:[[]],  
    })  
  }  
   
}
```

10. **Oops !!** Not added Html inside **app.component.html** file to display the form in the UI. Add the **form** tag inside **app.component.html** and also add the **formGroup** value as a form tag attribute.

```
<div class="container-fluid mt-3">  
  <form class="form" [formGroup]="form">  
    <h3 class="mt-3 mb-3">User Registration</h3>  </form>  
</div>
```

11.After that add, the input tag along with formControlName is “firstName”

```
<div class="container-fluid mt-3">  
  <form class="form" [formGroup]="form">  
    <h3 class="mt-3 mb-3">User Registration</h3>  
    <fieldset>  
      <legend>  
         User Details  
      </legend>  
      <div class="row mt-3">  
        <label class="label col-md-2" for="firstName">First Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="firstName" name="firstName"  
          id="firstName" placeholder="Enter First Name" />  
      </div>  
    </fieldset>  
  </form>  
</div>
```

12. Same way add all the **formControls** in the following way along with **radio** and **select dropdowns**. Also, display **form values** inside the **Html** file to check the **values** when we changed the **content** inside the input.

```
<div class="container-fluid mt-3">  
  <form class="form" [formGroup]="form">  
    <h3 class="mt-3 mb-3">User Registration</h3>  
    <fieldset>  
      <legend>  
         User Details  
      </legend>  
      <div class="row mt-3">  
        <label class="label col-md-2" for="firstName">First Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="firstName" name="firstName"  
          id="firstName" placeholder="Enter First Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="secondName">Second Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="secondName" name="secondName"  
          id="secondName" placeholder="Enter Second Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="middleName">Middle Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="middleName" name="middleName"  
          id="middleName" placeholder="Enter Middle Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2">Gender</label>  
        <div class="col-md-1">  
          <input type="radio" class="form-check-input" formControlName="gender" name="gender" id="male" value="male" />  
          <label class="label" for="male">Male</label>  
        </div>  
        <div class="col-md-1">  
          <input type="radio" class="form-check-input" formControlName="gender" name="gender" id="female"  
            value="female" />  
          <label class="label" for="female">Female</label>  
        </div>  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="username">Username</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="username" name="username"  
          id="username" placeholder="Enter Username" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="email">Email Address</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="email" name="email" id="email"  
          placeholder="Enter Email Address" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="password">Password</label>  
        <input type="password" class="form-control form-control-sm col-md-6" formControlName="password" name="password"  
          id="password" placeholder="Enter Password" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="mobile">Mobile</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="mobile" name="mobile"  
          id="mobile" placeholder="Enter Mobile" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="workStatus">Work Status</label>  
        <select class="form-control form-control-sm col-md-6" formControlName="workStatus" name="workStatus"  
          id="workStatus">  
          <option value="" selected disabled>Selected</option>  
          <option value="Fresher">Fresher</option>  
          <option value="Experienced">Experienced</option>  
        </select>  
      </div>  
    </fieldset>  
  </form>  
  {{form.value | json }}  
</div>
```

13. After that add, the buttons **submit** and **reset**. Here **submit** button is used for **submitting** **the form** and the **reset button** is used for **resetting** the values inside the **form**.

```
<div class="container-fluid mt-3">,  
  <form class="form" [formGroup]="form">  
    <h3 class="mt-3 mb-3">User Registration</h3>  
    <fieldset>  
      <legend>  
         User Details  
      </legend>  
      <div class="row mt-3">  
        <label class="label col-md-2" for="firstName">First Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="firstName" name="firstName"  
          id="firstName" placeholder="Enter First Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="secondName">Second Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="secondName" name="secondName"  
          id="secondName" placeholder="Enter Second Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="middleName">Middle Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="middleName" name="middleName"  
          id="middleName" placeholder="Enter Middle Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2">Gender</label>  
        <div class="col-md-1">  
          <input type="radio" class="form-check-input" formControlName="gender" name="gender" id="male" value="male" />  
          <label class="label" for="male">Male</label>  
        </div>  
        <div class="col-md-1">  
          <input type="radio" class="form-check-input" formControlName="gender" name="gender" id="female"  
            value="female" />  
          <label class="label" for="female">Female</label>  
        </div>  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="username">Username</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="username" name="username"  
          id="username" placeholder="Enter Username" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="email">Email Address</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="email" name="email" id="email"  
          placeholder="Enter Email Address" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="password">Password</label>  
        <input type="password" class="form-control form-control-sm col-md-6" formControlName="password" name="password"  
          id="password" placeholder="Enter Password" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="mobile">Mobile</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="mobile" name="mobile"  
          id="mobile" placeholder="Enter Mobile" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="workStatus">Work Status</label>  
        <select class="form-control form-control-sm col-md-6" formControlName="workStatus" name="workStatus"  
          id="workStatus">  
          <option value="" selected disabled>Selected</option>  
          <option value="Fresher">Fresher</option>  
          <option value="Experienced">Experienced</option>  
        </select>  
      </div>  
    </fieldset>  
    <div class="row mt-2">  
      <button class="btn btn-primary m-3" type="submit" [disabled]="!form.valid">Submit</button>  
      <button class="btn btn-danger m-3" type="button" (click)="resetForm()">Reset</button>  
    </div>  
  </form>  
 {{form.value | json }}   
</div>
```

14. Check the **changes** inside the **browser** by using [**localhost:4200**](http://localhost:4200/), If **anything is wrong** please check from the **first step.**

15. After that we need to add the **value changes event** for the **“workStatus”** inside **ngOnInit()** to get the value whenever the **“workStatus”** select dropdown **changes**. Also, create method **selectionChange(value)** and call the **method** from the **valueChanges** event.

```
import { Component, OnInit } from '@angular/core';  
import { FormBuilder,Validators,FormGroup, FormControl } from "@angular/forms";  
@Component({  
  selector: 'app-root',  
  templateUrl: './app.component.html',  
  styleUrls: ['./app.component.scss']  
})  
export class AppComponent implements OnInit{public form:FormGroup;  
  constructor(private formBuilder:FormBuilder){  
    this.formInit()  
  }public ngOnInit(): void {  
    this.form.get('workStatus').valueChanges.subscribe(value=>{  
      this.selectionChange(value);  
    })  
  }public formInit(){  
    this.form = this.formBuilder.group({  
      firstName:['', Validators.required],  
      secondName:['', Validators.required],  
      middleName:[''],  
      username:['', Validators.required],  
      email:['', Validators.required],  
      mobile:['', [Validators.required,Validators.minLength(10),Validators.maxLength(10)]],  
      password:['', Validators.required],  
      workStatus:['', Validators.required],  
      gender:['', Validators.required],  
      qualifications:[[]],  
    })  
  }public resetForm(){  
    this.form.reset()  
  }  
   
  public selectionChange(value) {  
      
  }  
   
}
```

16. **Up to here clear right,** Next we need to add the logic for displaying the **additional formControls** based on the user selects the “**workStatus”** **dropdown**. If the user selected **“Experienced”** as the “**workStatus”** dropdown value then I will **add the formControls** else I **will remove the formControls.**

These are the **below form controls** am **adding** and **removing** on condition **based**

**Form Controls :**

**“workExperience”, “currentCompany”, “currentCtc”, “expectedCtc”, “notice Period”, “skills”.**

```
import { Component, OnInit } from '@angular/core';  
import { FormBuilder,Validators,FormGroup, FormControl } from "@angular/forms";  
@Component({  
  selector: 'app-root',  
  templateUrl: './app.component.html',  
  styleUrls: ['./app.component.scss']  
})  
export class AppComponent implements OnInit{public form:FormGroup;  
  constructor(private formBuilder:FormBuilder){  
    this.formInit()  
  }public ngOnInit(): void {  
    this.form.get('workStatus').valueChanges.subscribe(value=>{  
      this.selectionChange(value);  
    })  
  }public formInit(){  
    this.form = this.formBuilder.group({  
      firstName:['', Validators.required],  
      secondName:['', Validators.required],  
      middleName:[''],  
      username:['', Validators.required],  
      email:['', Validators.required],  
      mobile:['', [Validators.required,Validators.minLength(10),Validators.maxLength(10)]],  
      password:['', Validators.required],  
      workStatus:['', Validators.required],  
      gender:['', Validators.required],  
      qualifications:[[]],  
    })  
  }public resetForm(){  
    this.form.reset()  
  }  
   
  public selectionChange(value) {  
    if(value && value === 'Experienced'){  
      this.form.addControl('workExperience',new FormControl('',[Validators.required]));  
      this.form.addControl('currentCompany',new FormControl('',[Validators.required]));  
      this.form.addControl('currentCtc',new FormControl('',[Validators.required]));  
      this.form.addControl('expectedCtc',new FormControl('',[Validators.required]));  
      this.form.addControl('noticePeriod',new FormControl('',[Validators.required]));  
      this.form.addControl('skills',new FormControl('',[Validators.required]));  
    }else{  
      this.form.removeControl('workExperience');  
      this.form.removeControl('currentCompany');  
      this.form.removeControl('currentCtc');  
      this.form.removeControl('expectedCtc');  
      this.form.removeControl('noticePeriod');  
      this.form.removeControl('skills');  
    }  
  }  
   
}
```

17. Here we need a **variable** for **showing** the data and **hiding** the data based on **dropdown selection**. I created a **get** method **isExperienced** to get the latest value as **true** or **false**. If the **workStatus** dropdown value is **“Experienced”** then will get the value as **true** else **false**.

```
import { Component, OnInit } from '@angular/core';  
import { FormBuilder,Validators,FormGroup, FormControl } from "@angular/forms";  
@Component({  
  selector: 'app-root',  
  templateUrl: './app.component.html',  
  styleUrls: ['./app.component.scss']  
})  
export class AppComponent implements OnInit{public form:FormGroup;  
  constructor(private formBuilder:FormBuilder){  
    this.formInit()  
  }public ngOnInit(): void {  
    this.form.get('workStatus').valueChanges.subscribe(value=>{  
      this.selectionChange(value);  
    })  
  }public formInit(){  
    this.form = this.formBuilder.group({  
      firstName:['', Validators.required],  
      secondName:['', Validators.required],  
      middleName:[''],  
      username:['', Validators.required],  
      email:['', Validators.required],  
      mobile:['', [Validators.required,Validators.minLength(10),Validators.maxLength(10)]],  
      password:['', Validators.required],  
      workStatus:['', Validators.required],  
      gender:['', Validators.required],  
      qualifications:[[]],  
    })  
  }public resetForm(){  
    this.form.reset()  
  }public get isExperienced(){  
    const value = this.form.get('workStatus').value;  
    return value && value === 'Experienced';  
  }  
   
  public selectionChange(value) {  
    if(value && value === 'Experienced'){  
      this.form.addControl('workExperience',new FormControl('',[Validators.required]));  
      this.form.addControl('currentCompany',new FormControl('',[Validators.required]));  
      this.form.addControl('currentCtc',new FormControl('',[Validators.required]));  
      this.form.addControl('expectedCtc',new FormControl('',[Validators.required]));  
      this.form.addControl('noticePeriod',new FormControl('',[Validators.required]));  
      this.form.addControl('skills',new FormControl('',[Validators.required]));  
    }else{  
      this.form.removeControl('workExperience');  
      this.form.removeControl('currentCompany');  
      this.form.removeControl('currentCtc');  
      this.form.removeControl('expectedCtc');  
      this.form.removeControl('noticePeriod');  
      this.form.removeControl('skills');  
    }  
  }  
   
}
```

18. After that, open **app.component.html**, and add the below **code** and condition for showing the **data** based on the **workStatus dropdown selection.**

```
<div class="container-fluid mt-3">  
  <form class="form" [formGroup]="form">  
    <h3 class="mt-3 mb-3">User Registration</h3>  
    <fieldset>  
      <legend>  
         User Details  
      </legend>  
      <div class="row mt-3">  
        <label class="label col-md-2" for="firstName">First Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="firstName" name="firstName"  
          id="firstName" placeholder="Enter First Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="secondName">Second Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="secondName" name="secondName"  
          id="secondName" placeholder="Enter Second Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="middleName">Middle Name</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="middleName" name="middleName"  
          id="middleName" placeholder="Enter Middle Name" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2">Gender</label>  
        <div class="col-md-1">  
          <input type="radio" class="form-check-input" formControlName="gender" name="gender" id="male" value="male" />  
          <label class="label" for="male">Male</label>  
        </div>  
        <div class="col-md-1">  
          <input type="radio" class="form-check-input" formControlName="gender" name="gender" id="female"  
            value="female" />  
          <label class="label" for="female">Female</label>  
        </div>  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="username">Username</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="username" name="username"  
          id="username" placeholder="Enter Username" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="email">Email Address</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="email" name="email" id="email"  
          placeholder="Enter Email Address" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="password">Password</label>  
        <input type="password" class="form-control form-control-sm col-md-6" formControlName="password" name="password"  
          id="password" placeholder="Enter Password" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="mobile">Mobile</label>  
        <input type="text" class="form-control form-control-sm col-md-6" formControlName="mobile" name="mobile"  
          id="mobile" placeholder="Enter Mobile" />  
      </div>  
      <div class="row mt-2">  
        <label class="label col-md-2" for="workStatus">Work Status</label>  
        <select class="form-control form-control-sm col-md-6" formControlName="workStatus" name="workStatus"  
          id="workStatus">  
          <option value="" selected disabled>Selected</option>  
          <option value="Fresher">Fresher</option>  
          <option value="Experienced">Experienced</option>  
        </select>  
      </div>  
    </fieldset>  
    <ng-container *ngIf="isExperienced">  
      <fieldset>  
        <legend>  
         Work Experience   
        </legend>  
        <div class="row mt-2">  
          <label class="label col-md-2" for="workExperience">Total Years of Experience</label>  
          <select class="form-control form-control-sm col-md-6" formControlName="workExperience" name="workExperience"  
            id="workExperience">  
            <option value="" selected disabled>Select Years Of Experience</option>  
            <option value="0-1">0 to 1 Year</option>  
            <option value="1-2">1 to 2 Years</option>  
            <option value="3-5">3 to 5 Years</option>  
            <option value="5-7">5 to 7 Years</option>  
            <option value="7-10">7 to 10 Years</option>  
            <option value="10-or-more">More than 10 Years</option>  
          </select>  
        </div><div class="row mt-2">  
          <label class="label col-md-2" for="currentCompany">Current Company Name</label>  
          <input type="text" class="form-control form-control-sm col-md-6" formControlName="currentCompany"  
            name="currentCompany" id="currentCompany" placeholder="Enter Current Company Name" />  
        </div><div class="row mt-2">  
          <label class="label col-md-2" for="currentCtc">Current CTC</label>  
          <input type="text" class="form-control form-control-sm col-md-6" formControlName="currentCtc"  
            name="currentCtc" id="currentCtc" placeholder="Enter Current CTC" />  
        </div><div class="row mt-2">  
          <label class="label col-md-2" for="expectedCtc">Expected CTC</label>  
          <input type="text" class="form-control form-control-sm col-md-6" formControlName="expectedCtc"  
            name="expectedCtc" id="expectedCtc" placeholder="Enter Expected CTC" />  
        </div><div class="row mt-2">  
          <label class="label col-md-2" for="skills">Skills Set</label>  
          <input type="text" class="form-control form-control-sm col-md-6" formControlName="skills" name="skills"  
            id="skills" placeholder="Enter Skills E.g. Java,Python" />  
        </div>  
        <div class="row mt-2">  
          <p class="m-3" style="color: red;">Note:: Give Skills as comma separated e.g. java,python</p>  
        </div><div class="row mt-2">  
          <label class="label col-md-2" for="noticePeriod">Notice Period</label>  
          <select class="form-control form-control-sm col-md-6" formControlName="noticePeriod" name="noticePeriod"  
            id="noticePeriod">  
            <option value="" selected disabled>Select Notice Period</option>  
            <option value="immediate-joiner">Immediate Joiner</option>  
            <option value="15-or-less-than">15 days or less than</option>  
            <option value="1-month">1 Month</option>  
            <option value="45-days">45 Days</option>  
            <option value="2-months">2 Months</option>  
            <option value="3-months">3 Months</option>  
            <option value="more-than-3months">More than 3 months</option>  
          </select>  
        </div>  
      </fieldset>  
    </ng-container>  
    <div class="row mt-2">  
      <button class="btn btn-primary m-3" type="submit" [disabled]="!form.valid">Submit</button>  
      <button class="btn btn-danger m-3" type="button" (click)="resetForm()">Reset</button>  
    </div>  
  </form>  
  {{form.value | json }}   
</div>
```

19. **Finally Added all the code,** Please test the changes **inside the browser**, and If anything is **wrong** please check **carefully** from the **first step.**

Output:

Press enter or click to view image in full size

![]()

**SOURCE CODE:**  
**Front End:**  
GitHub: <https://github.com/mryenagandula/angular-forms-add-or-remove-control>

**Stack blitz Project Preview:**  
<https://stackblitz.com/edit/angular-forms-add-control-remove-control>

T**hanks for reading my article, Please share your feedback, claps, and comments. In that way, it will be helped me to improve my articles in the future.**

**Please share my story with your near and dear, Also follow and subscribe to the medium. You send a mail about new topics which you don’t know. In that way, I will create articles on that topic with example.**
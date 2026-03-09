---
title: "Form validation with JavaScript"
url: https://medium.com/p/4fcf4dd32846
---

# Form validation with JavaScript

[Original](https://medium.com/p/4fcf4dd32846)

# Form validation with JavaScript

[![Ana Sampaio](https://miro.medium.com/v2/resize:fill:64:64/1*wrtumIdmnxWaL_0LlQkEDQ.jpeg)](/@anaisamp?source=post_page---byline--4fcf4dd32846---------------------------------------)

[Ana Sampaio](/@anaisamp?source=post_page---byline--4fcf4dd32846---------------------------------------)

5 min read

·

Dec 21, 2016

--

5

Listen

Share

More

Every developer knows how complex and tricky form validation can be. Ideally, users fill in the form with necessary information and finish the job successfully. However, people often make mistakes. This is where form validation comes into play.

On this article I will share our approach on how to perform form validation. These requirements turned into the main characteristics of this solution:

* Vanilla JavaScript solution
* Uses HTML5 built-in constraint validation
* Supports custom validation
* Supports server-side validation
* Displays translated error messages

Browser support

* All modern browsers, and IE10+.

## HTML5 Constraint Validation

HTML5 has introduced validation mechanisms for forms. In addition to semantic types for the <input> element (type=email, number, …), we also have constraint validation (required, maxlength, …) to ease the work of checking the form content on the client side.

Constraint validation is an algorithm browsers run natively when a form is submitted to determine its validity. On this approach, we took advantage of the constraint validation API to perform validations.

## Form validation

```
<form id=”myForm”>  
 <input type=”text” required data-value-missing=”This field is required!” />  
 …  
</form>
```

In order to take advantage of the constraint validation API, we first use **checkValidity()** method to check if the input fields contain valid data.

```
var form = document.getElementById(‘MyForm’);  
var isValidForm = form.checkValidity();
```

### Validate form

We run **checkValidity()** on form submit in order to validate all form fields. If at least one is invalid, the validation fails.

### Validate each field

By using **checkValidity()** method, we validate:

* each input element on blur event;
* each select element on change event.

This allows us to know if a particular field is valid or invalid at a given time, and makes it possible to give the user feedback right away.

## Extract the error that occurred

If an error occurs, **checkValidity()** returns false. Then we use a property called **validity** from validation API to get the error of each input field.

The **validity** property gets a **validityState** object with the information of which validations failed and which didn’t. Here’s how it looks:

```
ValidityState = {  
 badInput: false,  
 customError: false,  
 patternMismatch: false,  
 rangeOverflow: false,  
 rangeUnderflow: false,  
 stepMismatch: false,  
 tooLong: false,  
 tooShort: false,  
 typeMismatch: false,  
 valid: false,  
 valueMissing: true  
};
```

Finally, we map these properties with the data attributes of the input field to obtain the error messages. We will explain that in detail in the next section.

## Display error messages

Each input field stores all possible error messages in data attributes.

```
<form id=”myForm” novalidate>  
 <input type=”text” name=”cardnumber” id=”cardnumber”  
  required data-value-missing=”Translate(‘Required’)”  
  pattern=”\d{13,16}” data-pattern-mismatch=”Translate(‘Invalid credit card’)” >  
 …  
</form>
```

As you may have noticed, the data attributes weren’t set randomly. Each data attribute contains the property to be validated.

Consider the following example:

```
data-value-missing=”Translate(‘Required’)”
```

In this case, if **validity.valueMissing** property is **true**, we show the translated word for “Required”, stored in **data-value-missing** attribute.

![]()

The same occurs for **validity.patternMismatch** property.

Press enter or click to view image in full size

![]()

Note that we want to prevent the form from being validated before its submission and display default error messages (different on each browser). That’s why we used **novalidate** attribute in form.

## Providing feedback on form and field states

### Styling fields

We style input fields by taking advantages of **:valid** and **:invalid** CSS pseudo-classes.

These hooks represent any <input> or <form> element whose content passes or fails to validate, using HTML5 constraint validation. These allow us to easily have valid/invalid fields changing its appearance, helping the user identify the errors and correct them right away.

By default, the browser does not apply a style to these pseudo-classes, so we can define our own.

```
input:valid {  
 border-bottom: 1px solid $color-success;  
}input:invalid {  
 border-bottom: 1px solid $color-error;  
}
```

However, we also depend on the form and fields state in order to provide feedback to the user. For example, we don’t want to show the “required” errors if the user didn’t interact with the form yet.

### Field and form state

To give feedback to the user if a field is valid or not at a given time, we have to control the state of an input. There are 3 possible states:

* **Visited**: when the user has visited the input.
* **Dirty**: when the user has tried to change the value of the input.
* **Virtually\_dirty**: when a custom validation has to mark an input as it was somehow changed to take validation in place. (Necessary for custom validations only — see next section.)

When these states are active, success or error styling is displayed.

```
input.visited.dirty:valid {  
 border-bottom: 1px solid $color-success;  
}
```

![]()

The form has also its own state:

* **Submitted**: when the user has submitted the form, at least once.

When a form is submitted, all fields will be validated (despite their state), and user feedback must be provided.

```
form.submitted input:invalid {  
 border-bottom: 1px solid $color-error;  
}
```

Press enter or click to view image in full size

![]()

## Custom Validations

Custom validations allow us to apply a specific rule to a given input field. This means that we are able to define a validation method, set an event when validation method is triggered, set an error message (optional — error can be provided from server), and set the field where the message is shown (optional — by default is the given input field).

```
<input type=”text” name=”cardnumber” id=”cardnumber”  
 required data-value-missing=”Required”  
 pattern=”\d{13,16}” data-pattern-mismatch=”Invalid credit card”  
 data-custom-pattern=”Card number is not valid for selected card type”>// Add custom validation to credit card number input when adding a new credit cardvar formValidator = new FormValidator(myForm);formValidator.addCustomValidation(cardNumber, _validateCreditCard, ‘blur’, errorMessage);// Extracts card number and card type values, and returns true on valid card numberfunction _validateCreditCard() {  
 …  
 // set of rules to be validated  
 // make an AJAX call if server-side validation is necessary:  
 // — return true if valid,  
 // — return false and the corresponding error message if invalid.  
}
```

## Conclusion

Validating forms has been a complex development experience. Although there are a few JavaScript based solutions, none of them are a fit in to what we needed. Also, developing on the top of someone else’s solution can easily turn into a painful job.

Our approach, based on HTML5 constraint validation, allowed us to implement form validations natively. Then, by taking advantage of its API and the CSS hooks, we were able to build a powerful solution for custom validations — including server-side validations via AJAX, and provide immediate feedback to the user, with error messages in any language supported.
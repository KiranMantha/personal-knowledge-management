The Luhn algorithm (or "modulus 10") is a simple checksum formula used to validate identification numbers like credit cards and IMEI codes. It is designed to catch accidental input errors, such as mistyped digits.

### Luhn's Algo

**Algo Logic:**

To calculate or validate using the Luhn formula:
- Double every second digit starting from the rightmost digit (the check digit) and moving left.
- Sum the digits if any doubled product is greater than 9 (e.g., if \(6 \times 2 = 12\), add \(1+2=3\)). 
- Alternatively, subtract 9.Sum all numbers (both the untouched digits and the newly modified doubled digits).
- Check modulo 10: If the total sum is perfectly divisible by 10 (i.e., ends in 0), the number is valid.

```javascript
function isValidCreditCard(ccNumber) {
  function normalize(num) {
    return num > 9 ? num - 9 : num; // Because in Luhn, doubled digits are only ever 10–18.
  }

  const digits = ccNumber
    .replace(/\s/g, "")
    .split("")
    .map(Number);

  let sum = 0;
  let shouldDouble = false;

  for (let i = digits.length - 1; i >= 0; i--) {
    let digit = digits[i];

    if (shouldDouble) {
      digit = normalize(digit * 2);
    }

    sum += digit;
    shouldDouble = !shouldDouble;
  }

  return sum % 10 === 0;
}
```

### Identify Card Type

**Identification Guide**
- Visa: Starts with 4 and typically contains 13, 16, or 19 digits.
- Mastercard: Starts with 51 through 55, or 2221 through 2720 and contains 16 digits.
- American Express (Amex): Starts with 34 or 37 and contains 15 digits.

```javascript
function getCardType(cardNumber) {
    // Remove any spaces or dashes from the input
    const cleanNumber = cardNumber.replace(/\D/g, '');
    const len = cleanNumber.length;

    // Define rules for each network (prefix pattern and allowed lengths)
    const cardRules = [
        {
            type: 'visa',
            prefix: /^4/,
            lengths: [13, 16, 19]
        },
        {
            type: 'mastercard',
            prefix: /^(5[1-5]|222[1-9]|22[3-9]\d|2[3-6]\d{2}|27[0-1]\d|2720)/,
            lengths: [16]
        },
        {
            type: 'amex',
            prefix: /^3[47]/, // Refined to target exact Amex prefixes (34 and 37)
            lengths: [15]
        }
    ];

    // Evaluate rules
    for (const rule of cardRules) {
        if (rule.prefix.test(cleanNumber)) {
            // Checks if the current length is strictly allowed for this network
            if (rule.lengths.includes(len)) {
                return rule.type; // Returns 'visa', 'mastercard', or 'amex'
            }
            return `invalid_${rule.type}_length`; // Identifies prefix match but bad length
        }
    }
    return 'unknown';
}
```

### Validate card with card type identification

```javascript
function validateCreditCard(cardNumber) {
    const cardType = getCardType(cardNumber);
    const isValidCard = isValidCreditCard(cardNumber);

    return {
        cardType,
        isValidCard,
    };
}
```
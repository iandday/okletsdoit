# ExpenseSchema

## Properties

| Name              | Type    |
| ----------------- | ------- |
| `id`              | string  |
| `item`            | string  |
| `slug`            | string  |
| `description`     | string  |
| `date`            | Date    |
| `categoryId`      | string  |
| `vendorId`        | string  |
| `quantity`        | number  |
| `unitPrice`       | string  |
| `additionalPrice` | string  |
| `estimatedAmount` | string  |
| `actualAmount`    | string  |
| `url`             | string  |
| `purchased`       | boolean |
| `variance`        | string  |
| `calculatedPrice` | string  |
| `createdAt`       | Date    |
| `updatedAt`       | Date    |

## Example

```typescript
import type { ExpenseSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    item: null,
    slug: null,
    description: null,
    date: null,
    categoryId: null,
    vendorId: null,
    quantity: null,
    unitPrice: null,
    additionalPrice: null,
    estimatedAmount: null,
    actualAmount: null,
    url: null,
    purchased: null,
    variance: null,
    calculatedPrice: null,
    createdAt: null,
    updatedAt: null,
} satisfies ExpenseSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ExpenseSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# ExpenseCreateSchema

## Properties

| Name              | Type                                  |
| ----------------- | ------------------------------------- |
| `item`            | string                                |
| `description`     | string                                |
| `date`            | Date                                  |
| `categoryId`      | string                                |
| `vendorId`        | string                                |
| `quantity`        | number                                |
| `unitPrice`       | [UnitPrice](UnitPrice.md)             |
| `additionalPrice` | [AdditionalPrice](AdditionalPrice.md) |
| `estimatedAmount` | [EstimatedAmount](EstimatedAmount.md) |
| `actualAmount`    | [ActualAmount](ActualAmount.md)       |
| `url`             | string                                |

## Example

```typescript
import type { ExpenseCreateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    item: null,
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
} satisfies ExpenseCreateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ExpenseCreateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

# ListEntryUpdateSchema

## Properties

| Name                  | Type                                    |
| --------------------- | --------------------------------------- |
| `item`                | string                                  |
| `description`         | string                                  |
| `listId`              | string                                  |
| `order`               | number                                  |
| `isCompleted`         | boolean                                 |
| `purchased`           | boolean                                 |
| `vendorId`            | string                                  |
| `associatedExpenseId` | string                                  |
| `quantity`            | number                                  |
| `unitPrice`           | [UnitPrice1](UnitPrice1.md)             |
| `additionalPrice`     | [AdditionalPrice1](AdditionalPrice1.md) |
| `url`                 | string                                  |

## Example

```typescript
import type { ListEntryUpdateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    item: null,
    description: null,
    listId: null,
    order: null,
    isCompleted: null,
    purchased: null,
    vendorId: null,
    associatedExpenseId: null,
    quantity: null,
    unitPrice: null,
    additionalPrice: null,
    url: null,
} satisfies ListEntryUpdateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ListEntryUpdateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

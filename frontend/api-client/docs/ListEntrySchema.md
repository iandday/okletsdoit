# ListEntrySchema

## Properties

| Name                  | Type    |
| --------------------- | ------- |
| `id`                  | string  |
| `item`                | string  |
| `slug`                | string  |
| `description`         | string  |
| `listId`              | string  |
| `order`               | number  |
| `isCompleted`         | boolean |
| `completedAt`         | Date    |
| `purchased`           | boolean |
| `vendorId`            | string  |
| `associatedExpenseId` | string  |
| `quantity`            | number  |
| `unitPrice`           | string  |
| `additionalPrice`     | string  |
| `totalPrice`          | string  |
| `url`                 | string  |
| `image`               | string  |
| `createdAt`           | Date    |
| `updatedAt`           | Date    |

## Example

```typescript
import type { ListEntrySchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    item: null,
    slug: null,
    description: null,
    listId: null,
    order: null,
    isCompleted: null,
    completedAt: null,
    purchased: null,
    vendorId: null,
    associatedExpenseId: null,
    quantity: null,
    unitPrice: null,
    additionalPrice: null,
    totalPrice: null,
    url: null,
    image: null,
    createdAt: null,
    updatedAt: null,
} satisfies ListEntrySchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as ListEntrySchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

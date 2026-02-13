# AccommodationSchema

## Properties

| Name                | Type   |
| ------------------- | ------ |
| `id`                | string |
| `name`              | string |
| `slug`              | string |
| `description`       | string |
| `url`               | string |
| `phoneNumber`       | string |
| `addressLineOne`    | string |
| `addressLineTwo`    | string |
| `city`              | string |
| `state`             | string |
| `zipcode`           | string |
| `accommodationType` | string |
| `order`             | number |
| `createdAt`         | Date   |
| `updatedAt`         | Date   |

## Example

```typescript
import type { AccommodationSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    name: null,
    slug: null,
    description: null,
    url: null,
    phoneNumber: null,
    addressLineOne: null,
    addressLineTwo: null,
    city: null,
    state: null,
    zipcode: null,
    accommodationType: null,
    order: null,
    createdAt: null,
    updatedAt: null,
} satisfies AccommodationSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as AccommodationSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

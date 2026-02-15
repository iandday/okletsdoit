# QRCodeBase64Schema

## Properties

| Name           | Type   |
| -------------- | ------ |
| `qrCodeBase64` | string |
| `rsvpCode`     | string |
| `rsvpUrl`      | string |

## Example

```typescript
import type { QRCodeBase64Schema } from "";

// TODO: Update the object below with actual values
const example = {
    qrCodeBase64: null,
    rsvpCode: null,
    rsvpUrl: null,
} satisfies QRCodeBase64Schema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as QRCodeBase64Schema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

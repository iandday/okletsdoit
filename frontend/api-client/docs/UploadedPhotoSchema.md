# UploadedPhotoSchema

## Properties

| Name            | Type    |
| --------------- | ------- |
| `id`            | string  |
| `photoFile`     | string  |
| `thumbnailFile` | string  |
| `contentType`   | string  |
| `fileSize`      | number  |
| `width`         | number  |
| `height`        | number  |
| `camera`        | string  |
| `checksum`      | string  |
| `uploadedAt`    | Date    |
| `isApproved`    | boolean |
| `isDeleted`     | boolean |
| `favoriteCount` | number  |
| `flagged`       | boolean |
| `status`        | string  |

## Example

```typescript
import type { UploadedPhotoSchema } from "";

// TODO: Update the object below with actual values
const example = {
    id: null,
    photoFile: null,
    thumbnailFile: null,
    contentType: null,
    fileSize: null,
    width: null,
    height: null,
    camera: null,
    checksum: null,
    uploadedAt: null,
    isApproved: null,
    isDeleted: null,
    favoriteCount: null,
    flagged: null,
    status: null,
} satisfies UploadedPhotoSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as UploadedPhotoSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

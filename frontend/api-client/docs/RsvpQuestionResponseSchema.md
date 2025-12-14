
# RsvpQuestionResponseSchema


## Properties

Name | Type
------------ | -------------
`id` | string
`submissionId` | string
`questionId` | string
`responseText` | string
`responseChoiceIds` | Array&lt;string&gt;
`createdAt` | Date
`updatedAt` | Date

## Example

```typescript
import type { RsvpQuestionResponseSchema } from ''

// TODO: Update the object below with actual values
const example = {
  "id": null,
  "submissionId": null,
  "questionId": null,
  "responseText": null,
  "responseChoiceIds": null,
  "createdAt": null,
  "updatedAt": null,
} satisfies RsvpQuestionResponseSchema

console.log(example)

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example)
console.log(exampleJSON)

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as RsvpQuestionResponseSchema
console.log(exampleParsed)
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)



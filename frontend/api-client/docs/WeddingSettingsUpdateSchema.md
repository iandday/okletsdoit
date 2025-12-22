# WeddingSettingsUpdateSchema

## Properties

| Name                         | Type    |
| ---------------------------- | ------- |
| `defaultDataLoaded`          | boolean |
| `allowRsvp`                  | boolean |
| `allowPhotos`                | boolean |
| `weddingDate`                | Date    |
| `showFaq`                    | boolean |
| `rsvpStartDate`              | Date    |
| `rsvpEndDate`                | Date    |
| `rsvpAcceptButton`           | string  |
| `rsvpDeclineButton`          | string  |
| `rsvpAttendingLabel`         | string  |
| `rsvpAccommodationLabel`     | string  |
| `rsvpVipLabel`               | string  |
| `rsvpAcceptIntro`            | string  |
| `rsvpAcceptSuccessMessage`   | string  |
| `rsvpDeclineSuccessMessage`  | string  |
| `rsvpAccommodationIntro`     | string  |
| `rsvpVipIntro`               | string  |
| `rsvpShowAccommodationIntro` | boolean |
| `rsvpShowVipIntro`           | boolean |
| `rsvpEnableEmailUpdates`     | boolean |
| `rsvpEmailUpdateLabel`       | string  |
| `rsvpSuccessHeadline`        | string  |
| `standardGroupLabel`         | string  |
| `vipGroupLabel`              | string  |

## Example

```typescript
import type { WeddingSettingsUpdateSchema } from "";

// TODO: Update the object below with actual values
const example = {
    defaultDataLoaded: null,
    allowRsvp: null,
    allowPhotos: null,
    weddingDate: null,
    showFaq: null,
    rsvpStartDate: null,
    rsvpEndDate: null,
    rsvpAcceptButton: null,
    rsvpDeclineButton: null,
    rsvpAttendingLabel: null,
    rsvpAccommodationLabel: null,
    rsvpVipLabel: null,
    rsvpAcceptIntro: null,
    rsvpAcceptSuccessMessage: null,
    rsvpDeclineSuccessMessage: null,
    rsvpAccommodationIntro: null,
    rsvpVipIntro: null,
    rsvpShowAccommodationIntro: null,
    rsvpShowVipIntro: null,
    rsvpEnableEmailUpdates: null,
    rsvpEmailUpdateLabel: null,
    rsvpSuccessHeadline: null,
    standardGroupLabel: null,
    vipGroupLabel: null,
} satisfies WeddingSettingsUpdateSchema;

console.log(example);

// Convert the instance to a JSON string
const exampleJSON: string = JSON.stringify(example);
console.log(exampleJSON);

// Parse the JSON string back to an object
const exampleParsed = JSON.parse(exampleJSON) as WeddingSettingsUpdateSchema;
console.log(exampleParsed);
```

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

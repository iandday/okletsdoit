# CoreApi

All URIs are relative to _http://localhost_

| Method                                                                            | HTTP request                                                  | Description                 |
| --------------------------------------------------------------------------------- | ------------------------------------------------------------- | --------------------------- |
| [**coreApiCreateAccommodation**](CoreApi.md#coreapicreateaccommodation)           | **POST** /api/core/accommodations                             | Create Accommodation        |
| [**coreApiCreateIdea**](CoreApi.md#coreapicreateidea)                             | **POST** /api/core/ideas                                      | Create Idea                 |
| [**coreApiCreateInspiration**](CoreApi.md#coreapicreateinspiration)               | **POST** /api/core/inspirations                               | Create Inspiration          |
| [**coreApiCreateQuestion**](CoreApi.md#coreapicreatequestion)                     | **POST** /api/core/questions                                  | Create Question             |
| [**coreApiCreateQuestionUrl**](CoreApi.md#coreapicreatequestionurl)               | **POST** /api/core/question-urls                              | Create Question Url         |
| [**coreApiCreateRsvpQuestion**](CoreApi.md#coreapicreatersvpquestion)             | **POST** /api/core/rsvp-questions                             | Create Rsvp Question        |
| [**coreApiCreateRsvpQuestionChoice**](CoreApi.md#coreapicreatersvpquestionchoice) | **POST** /api/core/rsvp-question-choices                      | Create Rsvp Question Choice |
| [**coreApiCreateTimeline**](CoreApi.md#coreapicreatetimeline)                     | **POST** /api/core/timelines                                  | Create Timeline             |
| [**coreApiCreateTip**](CoreApi.md#coreapicreatetip)                               | **POST** /api/core/tips                                       | Create Tip                  |
| [**coreApiDeleteAccommodation**](CoreApi.md#coreapideleteaccommodation)           | **DELETE** /api/core/accommodations/{accommodation_id}        | Delete Accommodation        |
| [**coreApiDeleteIdea**](CoreApi.md#coreapideleteidea)                             | **DELETE** /api/core/ideas/{idea_id}                          | Delete Idea                 |
| [**coreApiDeleteInspiration**](CoreApi.md#coreapideleteinspiration)               | **DELETE** /api/core/inspirations/{inspiration_id}            | Delete Inspiration          |
| [**coreApiDeleteInspirationImage**](CoreApi.md#coreapideleteinspirationimage)     | **DELETE** /api/core/inspirations/{inspiration_id}/image      | Delete Inspiration Image    |
| [**coreApiDeleteQuestion**](CoreApi.md#coreapideletequestion)                     | **DELETE** /api/core/questions/{question_id}                  | Delete Question             |
| [**coreApiDeleteQuestionUrl**](CoreApi.md#coreapideletequestionurl)               | **DELETE** /api/core/question-urls/{url_id}                   | Delete Question Url         |
| [**coreApiDeleteRsvpQuestion**](CoreApi.md#coreapideletersvpquestion)             | **DELETE** /api/core/rsvp-questions/{question_id}             | Delete Rsvp Question        |
| [**coreApiDeleteRsvpQuestionChoice**](CoreApi.md#coreapideletersvpquestionchoice) | **DELETE** /api/core/rsvp-question-choices/{choice_id}        | Delete Rsvp Question Choice |
| [**coreApiDeleteTimeline**](CoreApi.md#coreapideletetimeline)                     | **DELETE** /api/core/timelines/{timeline_id}                  | Delete Timeline             |
| [**coreApiDeleteTip**](CoreApi.md#coreapideletetip)                               | **DELETE** /api/core/tips/{tip_id}                            | Delete Tip                  |
| [**coreApiGetAccommodation**](CoreApi.md#coreapigetaccommodation)                 | **GET** /api/core/accommodations/{accommodation_id}           | Get Accommodation           |
| [**coreApiGetCategoriesContent**](CoreApi.md#coreapigetcategoriescontent)         | **GET** /api/core/rsvp-categories-content                     | Get Categories Content      |
| [**coreApiGetIdea**](CoreApi.md#coreapigetidea)                                   | **GET** /api/core/ideas/{idea_id}                             | Get Idea                    |
| [**coreApiGetInspiration**](CoreApi.md#coreapigetinspiration)                     | **GET** /api/core/inspirations/{inspiration_id}               | Get Inspiration             |
| [**coreApiGetQuestion**](CoreApi.md#coreapigetquestion)                           | **GET** /api/core/questions/{question_id}                     | Get Question                |
| [**coreApiGetQuestionUrl**](CoreApi.md#coreapigetquestionurl)                     | **GET** /api/core/question-urls/{url_id}                      | Get Question Url            |
| [**coreApiGetRsvpQuestion**](CoreApi.md#coreapigetrsvpquestion)                   | **GET** /api/core/rsvp-questions/{question_id}                | Get Rsvp Question           |
| [**coreApiGetRsvpQuestionChoice**](CoreApi.md#coreapigetrsvpquestionchoice)       | **GET** /api/core/rsvp-question-choices/{choice_id}           | Get Rsvp Question Choice    |
| [**coreApiGetTimeline**](CoreApi.md#coreapigettimeline)                           | **GET** /api/core/timelines/{timeline_id}                     | Get Timeline                |
| [**coreApiGetTip**](CoreApi.md#coreapigettip)                                     | **GET** /api/core/tips/{tip_id}                               | Get Tip                     |
| [**coreApiGetWeddingSettings**](CoreApi.md#coreapigetweddingsettings)             | **GET** /api/core/wedding-settings                            | Get Wedding Settings        |
| [**coreApiListAccommodations**](CoreApi.md#coreapilistaccommodations)             | **GET** /api/core/accommodations                              | List Accommodations         |
| [**coreApiListIdeas**](CoreApi.md#coreapilistideas)                               | **GET** /api/core/ideas                                       | List Ideas                  |
| [**coreApiListInspirations**](CoreApi.md#coreapilistinspirations)                 | **GET** /api/core/inspirations                                | List Inspirations           |
| [**coreApiListQuestionUrls**](CoreApi.md#coreapilistquestionurls)                 | **GET** /api/core/question-urls                               | List Question Urls          |
| [**coreApiListQuestions**](CoreApi.md#coreapilistquestions)                       | **GET** /api/core/questions                                   | List Questions              |
| [**coreApiListRsvpQuestions**](CoreApi.md#coreapilistrsvpquestions)               | **GET** /api/core/rsvp-questions                              | List Rsvp Questions         |
| [**coreApiListTimelines**](CoreApi.md#coreapilisttimelines)                       | **GET** /api/core/timelines                                   | List Timelines              |
| [**coreApiListTips**](CoreApi.md#coreapilisttips)                                 | **GET** /api/core/tips                                        | List Tips                   |
| [**coreApiUpdateAccommodation**](CoreApi.md#coreapiupdateaccommodation)           | **PUT** /api/core/accommodations/{accommodation_id}           | Update Accommodation        |
| [**coreApiUpdateIdea**](CoreApi.md#coreapiupdateidea)                             | **PUT** /api/core/ideas/{idea_id}                             | Update Idea                 |
| [**coreApiUpdateInspiration**](CoreApi.md#coreapiupdateinspiration)               | **PUT** /api/core/inspirations/{inspiration_id}               | Update Inspiration          |
| [**coreApiUpdateQuestion**](CoreApi.md#coreapiupdatequestion)                     | **PUT** /api/core/questions/{question_id}                     | Update Question             |
| [**coreApiUpdateQuestionUrl**](CoreApi.md#coreapiupdatequestionurl)               | **PUT** /api/core/question-urls/{url_id}                      | Update Question Url         |
| [**coreApiUpdateRsvpQuestion**](CoreApi.md#coreapiupdatersvpquestion)             | **PUT** /api/core/rsvp-questions/{question_id}                | Update Rsvp Question        |
| [**coreApiUpdateRsvpQuestionChoice**](CoreApi.md#coreapiupdatersvpquestionchoice) | **PUT** /api/core/rsvp-question-choices/{choice_id}           | Update Rsvp Question Choice |
| [**coreApiUpdateTimeline**](CoreApi.md#coreapiupdatetimeline)                     | **PUT** /api/core/timelines/{timeline_id}                     | Update Timeline             |
| [**coreApiUpdateTip**](CoreApi.md#coreapiupdatetip)                               | **PUT** /api/core/tips/{tip_id}                               | Update Tip                  |
| [**coreApiUpdateWeddingSettings**](CoreApi.md#coreapiupdateweddingsettings)       | **PUT** /api/core/wedding-settings                            | Update Wedding Settings     |
| [**coreApiUploadInspirationImage**](CoreApi.md#coreapiuploadinspirationimage)     | **POST** /api/core/inspirations/{inspiration_id}/upload-image | Upload Inspiration Image    |

## coreApiCreateAccommodation

> AccommodationSchema coreApiCreateAccommodation(accommodationCreateSchema)

Create Accommodation

Create a new accommodation

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateAccommodationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // AccommodationCreateSchema
    accommodationCreateSchema: ...,
  } satisfies CoreApiCreateAccommodationRequest;

  try {
    const data = await api.coreApiCreateAccommodation(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                          | Type                                                      | Description | Notes |
| ----------------------------- | --------------------------------------------------------- | ----------- | ----- |
| **accommodationCreateSchema** | [AccommodationCreateSchema](AccommodationCreateSchema.md) |             |       |

### Return type

[**AccommodationSchema**](AccommodationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateIdea

> IdeaSchema coreApiCreateIdea(ideaCreateSchema)

Create Idea

Create a new idea

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateIdeaRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // IdeaCreateSchema
    ideaCreateSchema: ...,
  } satisfies CoreApiCreateIdeaRequest;

  try {
    const data = await api.coreApiCreateIdea(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                 | Type                                    | Description | Notes |
| -------------------- | --------------------------------------- | ----------- | ----- |
| **ideaCreateSchema** | [IdeaCreateSchema](IdeaCreateSchema.md) |             |       |

### Return type

[**IdeaSchema**](IdeaSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateInspiration

> InspirationSchema coreApiCreateInspiration(inspirationCreateSchema)

Create Inspiration

Create a new inspiration

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateInspirationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // InspirationCreateSchema
    inspirationCreateSchema: ...,
  } satisfies CoreApiCreateInspirationRequest;

  try {
    const data = await api.coreApiCreateInspiration(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                        | Type                                                  | Description | Notes |
| --------------------------- | ----------------------------------------------------- | ----------- | ----- |
| **inspirationCreateSchema** | [InspirationCreateSchema](InspirationCreateSchema.md) |             |       |

### Return type

[**InspirationSchema**](InspirationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateQuestion

> QuestionSchema coreApiCreateQuestion(questionCreateSchema)

Create Question

Create a new question

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // QuestionCreateSchema
    questionCreateSchema: ...,
  } satisfies CoreApiCreateQuestionRequest;

  try {
    const data = await api.coreApiCreateQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                     | Type                                            | Description | Notes |
| ------------------------ | ----------------------------------------------- | ----------- | ----- |
| **questionCreateSchema** | [QuestionCreateSchema](QuestionCreateSchema.md) |             |       |

### Return type

[**QuestionSchema**](QuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateQuestionUrl

> QuestionURLSchema coreApiCreateQuestionUrl(questionURLCreateSchema)

Create Question Url

Create a new question URL

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateQuestionUrlRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // QuestionURLCreateSchema
    questionURLCreateSchema: ...,
  } satisfies CoreApiCreateQuestionUrlRequest;

  try {
    const data = await api.coreApiCreateQuestionUrl(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                        | Type                                                  | Description | Notes |
| --------------------------- | ----------------------------------------------------- | ----------- | ----- |
| **questionURLCreateSchema** | [QuestionURLCreateSchema](QuestionURLCreateSchema.md) |             |       |

### Return type

[**QuestionURLSchema**](QuestionURLSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateRsvpQuestion

> RsvpQuestionSchema coreApiCreateRsvpQuestion(rsvpQuestionCreateSchema)

Create Rsvp Question

Create a new RSVP question

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateRsvpQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // RsvpQuestionCreateSchema
    rsvpQuestionCreateSchema: ...,
  } satisfies CoreApiCreateRsvpQuestionRequest;

  try {
    const data = await api.coreApiCreateRsvpQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                         | Type                                                    | Description | Notes |
| ---------------------------- | ------------------------------------------------------- | ----------- | ----- |
| **rsvpQuestionCreateSchema** | [RsvpQuestionCreateSchema](RsvpQuestionCreateSchema.md) |             |       |

### Return type

[**RsvpQuestionSchema**](RsvpQuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateRsvpQuestionChoice

> RsvpQuestionChoiceSchema coreApiCreateRsvpQuestionChoice(rsvpQuestionChoiceCreateSchema)

Create Rsvp Question Choice

Create a new RSVP question choice

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateRsvpQuestionChoiceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // RsvpQuestionChoiceCreateSchema
    rsvpQuestionChoiceCreateSchema: ...,
  } satisfies CoreApiCreateRsvpQuestionChoiceRequest;

  try {
    const data = await api.coreApiCreateRsvpQuestionChoice(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                               | Type                                                                | Description | Notes |
| ---------------------------------- | ------------------------------------------------------------------- | ----------- | ----- |
| **rsvpQuestionChoiceCreateSchema** | [RsvpQuestionChoiceCreateSchema](RsvpQuestionChoiceCreateSchema.md) |             |       |

### Return type

[**RsvpQuestionChoiceSchema**](RsvpQuestionChoiceSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateTimeline

> TimelineSchema coreApiCreateTimeline(timelineCreateSchema)

Create Timeline

Create a new timeline event

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateTimelineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // TimelineCreateSchema
    timelineCreateSchema: ...,
  } satisfies CoreApiCreateTimelineRequest;

  try {
    const data = await api.coreApiCreateTimeline(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                     | Type                                            | Description | Notes |
| ------------------------ | ----------------------------------------------- | ----------- | ----- |
| **timelineCreateSchema** | [TimelineCreateSchema](TimelineCreateSchema.md) |             |       |

### Return type

[**TimelineSchema**](TimelineSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiCreateTip

> TipsSchema coreApiCreateTip(tipsCreateSchema)

Create Tip

Create a new tip

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiCreateTipRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // TipsCreateSchema
    tipsCreateSchema: ...,
  } satisfies CoreApiCreateTipRequest;

  try {
    const data = await api.coreApiCreateTip(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                 | Type                                    | Description | Notes |
| -------------------- | --------------------------------------- | ----------- | ----- |
| **tipsCreateSchema** | [TipsCreateSchema](TipsCreateSchema.md) |             |       |

### Return type

[**TipsSchema**](TipsSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteAccommodation

> coreApiDeleteAccommodation(accommodationId)

Delete Accommodation

Soft delete an accommodation

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteAccommodationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    accommodationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteAccommodationRequest;

  try {
    const data = await api.coreApiDeleteAccommodation(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                | Type     | Description | Notes                     |
| ------------------- | -------- | ----------- | ------------------------- |
| **accommodationId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteIdea

> coreApiDeleteIdea(ideaId)

Delete Idea

Soft delete an idea

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteIdeaRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    ideaId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteIdeaRequest;

  try {
    const data = await api.coreApiDeleteIdea(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name       | Type     | Description | Notes                     |
| ---------- | -------- | ----------- | ------------------------- |
| **ideaId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteInspiration

> coreApiDeleteInspiration(inspirationId)

Delete Inspiration

Soft delete an inspiration

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteInspirationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    inspirationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteInspirationRequest;

  try {
    const data = await api.coreApiDeleteInspiration(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name              | Type     | Description | Notes                     |
| ----------------- | -------- | ----------- | ------------------------- |
| **inspirationId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteInspirationImage

> coreApiDeleteInspirationImage(inspirationId)

Delete Inspiration Image

Delete image from an inspiration

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteInspirationImageRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    inspirationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteInspirationImageRequest;

  try {
    const data = await api.coreApiDeleteInspirationImage(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name              | Type     | Description | Notes                     |
| ----------------- | -------- | ----------- | ------------------------- |
| **inspirationId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteQuestion

> coreApiDeleteQuestion(questionId)

Delete Question

Soft delete a question

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    questionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteQuestionRequest;

  try {
    const data = await api.coreApiDeleteQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name           | Type     | Description | Notes                     |
| -------------- | -------- | ----------- | ------------------------- |
| **questionId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteQuestionUrl

> coreApiDeleteQuestionUrl(urlId)

Delete Question Url

Soft delete a question URL

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteQuestionUrlRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    urlId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteQuestionUrlRequest;

  try {
    const data = await api.coreApiDeleteQuestionUrl(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name      | Type     | Description | Notes                     |
| --------- | -------- | ----------- | ------------------------- |
| **urlId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteRsvpQuestion

> coreApiDeleteRsvpQuestion(questionId)

Delete Rsvp Question

Soft delete an RSVP question

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteRsvpQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    questionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteRsvpQuestionRequest;

  try {
    const data = await api.coreApiDeleteRsvpQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name           | Type     | Description | Notes                     |
| -------------- | -------- | ----------- | ------------------------- |
| **questionId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteRsvpQuestionChoice

> coreApiDeleteRsvpQuestionChoice(choiceId)

Delete Rsvp Question Choice

Soft delete an RSVP question choice

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteRsvpQuestionChoiceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    choiceId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteRsvpQuestionChoiceRequest;

  try {
    const data = await api.coreApiDeleteRsvpQuestionChoice(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name         | Type     | Description | Notes                     |
| ------------ | -------- | ----------- | ------------------------- |
| **choiceId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteTimeline

> coreApiDeleteTimeline(timelineId)

Delete Timeline

Soft delete a timeline event

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteTimelineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    timelineId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteTimelineRequest;

  try {
    const data = await api.coreApiDeleteTimeline(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name           | Type     | Description | Notes                     |
| -------------- | -------- | ----------- | ------------------------- |
| **timelineId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiDeleteTip

> coreApiDeleteTip(tipId)

Delete Tip

Soft delete a tip

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiDeleteTipRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    tipId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiDeleteTipRequest;

  try {
    const data = await api.coreApiDeleteTip(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name      | Type     | Description | Notes                     |
| --------- | -------- | ----------- | ------------------------- |
| **tipId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetAccommodation

> AccommodationSchema coreApiGetAccommodation(accommodationId)

Get Accommodation

Get a specific accommodation by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetAccommodationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    accommodationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetAccommodationRequest;

  try {
    const data = await api.coreApiGetAccommodation(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                | Type     | Description | Notes                     |
| ------------------- | -------- | ----------- | ------------------------- |
| **accommodationId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**AccommodationSchema**](AccommodationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetCategoriesContent

> Array&lt;CategoryContentSchema&gt; coreApiGetCategoriesContent(publishedOnly)

Get Categories Content

Get all categories with their associated questions and tips

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiGetCategoriesContentRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // boolean (optional)
        publishedOnly: true,
    } satisfies CoreApiGetCategoriesContentRequest;

    try {
        const data = await api.coreApiGetCategoriesContent(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name              | Type      | Description | Notes                           |
| ----------------- | --------- | ----------- | ------------------------------- |
| **publishedOnly** | `boolean` |             | [Optional] [Defaults to `true`] |

### Return type

[**Array&lt;CategoryContentSchema&gt;**](CategoryContentSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetIdea

> IdeaSchema coreApiGetIdea(ideaId)

Get Idea

Get a specific idea by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetIdeaRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    ideaId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetIdeaRequest;

  try {
    const data = await api.coreApiGetIdea(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name       | Type     | Description | Notes                     |
| ---------- | -------- | ----------- | ------------------------- |
| **ideaId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**IdeaSchema**](IdeaSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetInspiration

> InspirationSchema coreApiGetInspiration(inspirationId)

Get Inspiration

Get a specific inspiration by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetInspirationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    inspirationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetInspirationRequest;

  try {
    const data = await api.coreApiGetInspiration(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name              | Type     | Description | Notes                     |
| ----------------- | -------- | ----------- | ------------------------- |
| **inspirationId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**InspirationSchema**](InspirationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetQuestion

> QuestionSchema coreApiGetQuestion(questionId)

Get Question

Get a specific question by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    questionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetQuestionRequest;

  try {
    const data = await api.coreApiGetQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name           | Type     | Description | Notes                     |
| -------------- | -------- | ----------- | ------------------------- |
| **questionId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**QuestionSchema**](QuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetQuestionUrl

> QuestionURLSchema coreApiGetQuestionUrl(urlId)

Get Question Url

Get a specific question URL by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetQuestionUrlRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    urlId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetQuestionUrlRequest;

  try {
    const data = await api.coreApiGetQuestionUrl(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name      | Type     | Description | Notes                     |
| --------- | -------- | ----------- | ------------------------- |
| **urlId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**QuestionURLSchema**](QuestionURLSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetRsvpQuestion

> RsvpQuestionSchema coreApiGetRsvpQuestion(questionId)

Get Rsvp Question

Get a specific RSVP question by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetRsvpQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    questionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetRsvpQuestionRequest;

  try {
    const data = await api.coreApiGetRsvpQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name           | Type     | Description | Notes                     |
| -------------- | -------- | ----------- | ------------------------- |
| **questionId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**RsvpQuestionSchema**](RsvpQuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetRsvpQuestionChoice

> RsvpQuestionChoiceSchema coreApiGetRsvpQuestionChoice(choiceId)

Get Rsvp Question Choice

Get a specific RSVP question choice by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetRsvpQuestionChoiceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    choiceId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetRsvpQuestionChoiceRequest;

  try {
    const data = await api.coreApiGetRsvpQuestionChoice(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name         | Type     | Description | Notes                     |
| ------------ | -------- | ----------- | ------------------------- |
| **choiceId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**RsvpQuestionChoiceSchema**](RsvpQuestionChoiceSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetTimeline

> TimelineSchema coreApiGetTimeline(timelineId)

Get Timeline

Get a specific timeline event by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetTimelineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    timelineId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetTimelineRequest;

  try {
    const data = await api.coreApiGetTimeline(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name           | Type     | Description | Notes                     |
| -------------- | -------- | ----------- | ------------------------- |
| **timelineId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**TimelineSchema**](TimelineSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetTip

> TipsSchema coreApiGetTip(tipId)

Get Tip

Get a specific tip by ID

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiGetTipRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    tipId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiGetTipRequest;

  try {
    const data = await api.coreApiGetTip(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name      | Type     | Description | Notes                     |
| --------- | -------- | ----------- | ------------------------- |
| **tipId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**TipsSchema**](TipsSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiGetWeddingSettings

> WeddingSettingsSchema coreApiGetWeddingSettings()

Get Wedding Settings

Get wedding settings (singleton)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiGetWeddingSettingsRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    try {
        const data = await api.coreApiGetWeddingSettings();
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

This endpoint does not need any parameter.

### Return type

[**WeddingSettingsSchema**](WeddingSettingsSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListAccommodations

> PagedAccommodationSchema coreApiListAccommodations(name, accommodationType, city, state, page, pageSize)

List Accommodations

List all accommodations (non-deleted)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiListAccommodationsRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // string (optional)
        name: name_example,
        // string (optional)
        accommodationType: accommodationType_example,
        // string (optional)
        city: city_example,
        // string (optional)
        state: state_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies CoreApiListAccommodationsRequest;

    try {
        const data = await api.coreApiListAccommodations(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                  | Type     | Description | Notes                                |
| --------------------- | -------- | ----------- | ------------------------------------ |
| **name**              | `string` |             | [Optional] [Defaults to `undefined`] |
| **accommodationType** | `string` |             | [Optional] [Defaults to `undefined`] |
| **city**              | `string` |             | [Optional] [Defaults to `undefined`] |
| **state**             | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**              | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize**          | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedAccommodationSchema**](PagedAccommodationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListIdeas

> PagedIdeaSchema coreApiListIdeas(name, page, pageSize)

List Ideas

List all ideas (non-deleted)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiListIdeasRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // string (optional)
        name: name_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies CoreApiListIdeasRequest;

    try {
        const data = await api.coreApiListIdeas(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name         | Type     | Description | Notes                                |
| ------------ | -------- | ----------- | ------------------------------------ |
| **name**     | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**     | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize** | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedIdeaSchema**](PagedIdeaSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListInspirations

> PagedInspirationSchema coreApiListInspirations(name, page, pageSize)

List Inspirations

List all inspirations (non-deleted)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiListInspirationsRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // string (optional)
        name: name_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies CoreApiListInspirationsRequest;

    try {
        const data = await api.coreApiListInspirations(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name         | Type     | Description | Notes                                |
| ------------ | -------- | ----------- | ------------------------------------ |
| **name**     | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**     | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize** | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedInspirationSchema**](PagedInspirationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListQuestionUrls

> Array&lt;QuestionURLSchema&gt; coreApiListQuestionUrls(questionId)

List Question Urls

List all question URLs (non-deleted), optionally filtered by question_id

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiListQuestionUrlsRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string (optional)
    questionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies CoreApiListQuestionUrlsRequest;

  try {
    const data = await api.coreApiListQuestionUrls(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name           | Type     | Description | Notes                                |
| -------------- | -------- | ----------- | ------------------------------------ |
| **questionId** | `string` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**Array&lt;QuestionURLSchema&gt;**](QuestionURLSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListQuestions

> PagedQuestionSchema coreApiListQuestions(category, published, page, pageSize)

List Questions

List all questions (non-deleted)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiListQuestionsRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // string (optional)
        category: category_example,
        // boolean (optional)
        published: true,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies CoreApiListQuestionsRequest;

    try {
        const data = await api.coreApiListQuestions(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name          | Type      | Description | Notes                                |
| ------------- | --------- | ----------- | ------------------------------------ |
| **category**  | `string`  |             | [Optional] [Defaults to `undefined`] |
| **published** | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **page**      | `number`  |             | [Optional] [Defaults to `1`]         |
| **pageSize**  | `number`  |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedQuestionSchema**](PagedQuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListRsvpQuestions

> PagedRsvpQuestionSchema coreApiListRsvpQuestions(published, questionType, page, pageSize)

List Rsvp Questions

List all RSVP questions (non-deleted)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiListRsvpQuestionsRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // boolean (optional)
        published: true,
        // string (optional)
        questionType: questionType_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies CoreApiListRsvpQuestionsRequest;

    try {
        const data = await api.coreApiListRsvpQuestions(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name             | Type      | Description | Notes                                |
| ---------------- | --------- | ----------- | ------------------------------------ |
| **published**    | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **questionType** | `string`  |             | [Optional] [Defaults to `undefined`] |
| **page**         | `number`  |             | [Optional] [Defaults to `1`]         |
| **pageSize**     | `number`  |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedRsvpQuestionSchema**](PagedRsvpQuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListTimelines

> PagedTimelineSchema coreApiListTimelines(name, published, confirmed, page, pageSize)

List Timelines

List all timeline events (non-deleted)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiListTimelinesRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // string (optional)
        name: name_example,
        // boolean (optional)
        published: true,
        // boolean (optional)
        confirmed: true,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies CoreApiListTimelinesRequest;

    try {
        const data = await api.coreApiListTimelines(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name          | Type      | Description | Notes                                |
| ------------- | --------- | ----------- | ------------------------------------ |
| **name**      | `string`  |             | [Optional] [Defaults to `undefined`] |
| **published** | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **confirmed** | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **page**      | `number`  |             | [Optional] [Defaults to `1`]         |
| **pageSize**  | `number`  |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedTimelineSchema**](PagedTimelineSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiListTips

> PagedTipsSchema coreApiListTips(category, published, page, pageSize)

List Tips

List all tips (non-deleted)

### Example

```ts
import { Configuration, CoreApi } from "";
import type { CoreApiListTipsRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const config = new Configuration({
        // To configure API key authorization: SessionAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: ServiceTokenAuth
        apiKey: "YOUR API KEY",
        // To configure API key authorization: XSessionTokenAuth
        apiKey: "YOUR API KEY",
    });
    const api = new CoreApi(config);

    const body = {
        // string (optional)
        category: category_example,
        // boolean (optional)
        published: true,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies CoreApiListTipsRequest;

    try {
        const data = await api.coreApiListTips(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name          | Type      | Description | Notes                                |
| ------------- | --------- | ----------- | ------------------------------------ |
| **category**  | `string`  |             | [Optional] [Defaults to `undefined`] |
| **published** | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **page**      | `number`  |             | [Optional] [Defaults to `1`]         |
| **pageSize**  | `number`  |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedTipsSchema**](PagedTipsSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateAccommodation

> AccommodationSchema coreApiUpdateAccommodation(accommodationId, accommodationUpdateSchema)

Update Accommodation

Update an accommodation

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateAccommodationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    accommodationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // AccommodationUpdateSchema
    accommodationUpdateSchema: ...,
  } satisfies CoreApiUpdateAccommodationRequest;

  try {
    const data = await api.coreApiUpdateAccommodation(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                          | Type                                                      | Description | Notes                     |
| ----------------------------- | --------------------------------------------------------- | ----------- | ------------------------- |
| **accommodationId**           | `string`                                                  |             | [Defaults to `undefined`] |
| **accommodationUpdateSchema** | [AccommodationUpdateSchema](AccommodationUpdateSchema.md) |             |                           |

### Return type

[**AccommodationSchema**](AccommodationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateIdea

> IdeaSchema coreApiUpdateIdea(ideaId, ideaUpdateSchema)

Update Idea

Update an idea

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateIdeaRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    ideaId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // IdeaUpdateSchema
    ideaUpdateSchema: ...,
  } satisfies CoreApiUpdateIdeaRequest;

  try {
    const data = await api.coreApiUpdateIdea(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                 | Type                                    | Description | Notes                     |
| -------------------- | --------------------------------------- | ----------- | ------------------------- |
| **ideaId**           | `string`                                |             | [Defaults to `undefined`] |
| **ideaUpdateSchema** | [IdeaUpdateSchema](IdeaUpdateSchema.md) |             |                           |

### Return type

[**IdeaSchema**](IdeaSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateInspiration

> InspirationSchema coreApiUpdateInspiration(inspirationId, inspirationUpdateSchema)

Update Inspiration

Update an inspiration

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateInspirationRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    inspirationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // InspirationUpdateSchema
    inspirationUpdateSchema: ...,
  } satisfies CoreApiUpdateInspirationRequest;

  try {
    const data = await api.coreApiUpdateInspiration(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                        | Type                                                  | Description | Notes                     |
| --------------------------- | ----------------------------------------------------- | ----------- | ------------------------- |
| **inspirationId**           | `string`                                              |             | [Defaults to `undefined`] |
| **inspirationUpdateSchema** | [InspirationUpdateSchema](InspirationUpdateSchema.md) |             |                           |

### Return type

[**InspirationSchema**](InspirationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateQuestion

> QuestionSchema coreApiUpdateQuestion(questionId, questionUpdateSchema)

Update Question

Update a question

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    questionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // QuestionUpdateSchema
    questionUpdateSchema: ...,
  } satisfies CoreApiUpdateQuestionRequest;

  try {
    const data = await api.coreApiUpdateQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                     | Type                                            | Description | Notes                     |
| ------------------------ | ----------------------------------------------- | ----------- | ------------------------- |
| **questionId**           | `string`                                        |             | [Defaults to `undefined`] |
| **questionUpdateSchema** | [QuestionUpdateSchema](QuestionUpdateSchema.md) |             |                           |

### Return type

[**QuestionSchema**](QuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateQuestionUrl

> QuestionURLSchema coreApiUpdateQuestionUrl(urlId, questionURLUpdateSchema)

Update Question Url

Update a question URL

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateQuestionUrlRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    urlId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // QuestionURLUpdateSchema
    questionURLUpdateSchema: ...,
  } satisfies CoreApiUpdateQuestionUrlRequest;

  try {
    const data = await api.coreApiUpdateQuestionUrl(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                        | Type                                                  | Description | Notes                     |
| --------------------------- | ----------------------------------------------------- | ----------- | ------------------------- |
| **urlId**                   | `string`                                              |             | [Defaults to `undefined`] |
| **questionURLUpdateSchema** | [QuestionURLUpdateSchema](QuestionURLUpdateSchema.md) |             |                           |

### Return type

[**QuestionURLSchema**](QuestionURLSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateRsvpQuestion

> RsvpQuestionSchema coreApiUpdateRsvpQuestion(questionId, rsvpQuestionUpdateSchema)

Update Rsvp Question

Update an RSVP question

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateRsvpQuestionRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    questionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // RsvpQuestionUpdateSchema
    rsvpQuestionUpdateSchema: ...,
  } satisfies CoreApiUpdateRsvpQuestionRequest;

  try {
    const data = await api.coreApiUpdateRsvpQuestion(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                         | Type                                                    | Description | Notes                     |
| ---------------------------- | ------------------------------------------------------- | ----------- | ------------------------- |
| **questionId**               | `string`                                                |             | [Defaults to `undefined`] |
| **rsvpQuestionUpdateSchema** | [RsvpQuestionUpdateSchema](RsvpQuestionUpdateSchema.md) |             |                           |

### Return type

[**RsvpQuestionSchema**](RsvpQuestionSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateRsvpQuestionChoice

> RsvpQuestionChoiceSchema coreApiUpdateRsvpQuestionChoice(choiceId, rsvpQuestionChoiceUpdateSchema)

Update Rsvp Question Choice

Update an RSVP question choice

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateRsvpQuestionChoiceRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    choiceId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // RsvpQuestionChoiceUpdateSchema
    rsvpQuestionChoiceUpdateSchema: ...,
  } satisfies CoreApiUpdateRsvpQuestionChoiceRequest;

  try {
    const data = await api.coreApiUpdateRsvpQuestionChoice(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                               | Type                                                                | Description | Notes                     |
| ---------------------------------- | ------------------------------------------------------------------- | ----------- | ------------------------- |
| **choiceId**                       | `string`                                                            |             | [Defaults to `undefined`] |
| **rsvpQuestionChoiceUpdateSchema** | [RsvpQuestionChoiceUpdateSchema](RsvpQuestionChoiceUpdateSchema.md) |             |                           |

### Return type

[**RsvpQuestionChoiceSchema**](RsvpQuestionChoiceSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateTimeline

> TimelineSchema coreApiUpdateTimeline(timelineId, timelineUpdateSchema)

Update Timeline

Update a timeline event

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateTimelineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    timelineId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // TimelineUpdateSchema
    timelineUpdateSchema: ...,
  } satisfies CoreApiUpdateTimelineRequest;

  try {
    const data = await api.coreApiUpdateTimeline(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                     | Type                                            | Description | Notes                     |
| ------------------------ | ----------------------------------------------- | ----------- | ------------------------- |
| **timelineId**           | `string`                                        |             | [Defaults to `undefined`] |
| **timelineUpdateSchema** | [TimelineUpdateSchema](TimelineUpdateSchema.md) |             |                           |

### Return type

[**TimelineSchema**](TimelineSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateTip

> TipsSchema coreApiUpdateTip(tipId, tipsUpdateSchema)

Update Tip

Update a tip

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateTipRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    tipId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // TipsUpdateSchema
    tipsUpdateSchema: ...,
  } satisfies CoreApiUpdateTipRequest;

  try {
    const data = await api.coreApiUpdateTip(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                 | Type                                    | Description | Notes                     |
| -------------------- | --------------------------------------- | ----------- | ------------------------- |
| **tipId**            | `string`                                |             | [Defaults to `undefined`] |
| **tipsUpdateSchema** | [TipsUpdateSchema](TipsUpdateSchema.md) |             |                           |

### Return type

[**TipsSchema**](TipsSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUpdateWeddingSettings

> WeddingSettingsSchema coreApiUpdateWeddingSettings(weddingSettingsUpdateSchema)

Update Wedding Settings

Update wedding settings

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUpdateWeddingSettingsRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // WeddingSettingsUpdateSchema
    weddingSettingsUpdateSchema: ...,
  } satisfies CoreApiUpdateWeddingSettingsRequest;

  try {
    const data = await api.coreApiUpdateWeddingSettings(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                            | Type                                                          | Description | Notes |
| ------------------------------- | ------------------------------------------------------------- | ----------- | ----- |
| **weddingSettingsUpdateSchema** | [WeddingSettingsUpdateSchema](WeddingSettingsUpdateSchema.md) |             |       |

### Return type

[**WeddingSettingsSchema**](WeddingSettingsSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## coreApiUploadInspirationImage

> InspirationSchema coreApiUploadInspirationImage(inspirationId, image)

Upload Inspiration Image

Upload or update image for an inspiration

### Example

```ts
import {
  Configuration,
  CoreApi,
} from '';
import type { CoreApiUploadInspirationImageRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const config = new Configuration({
    // To configure API key authorization: SessionAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: ServiceTokenAuth
    apiKey: "YOUR API KEY",
    // To configure API key authorization: XSessionTokenAuth
    apiKey: "YOUR API KEY",
  });
  const api = new CoreApi(config);

  const body = {
    // string
    inspirationId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // Blob
    image: BINARY_DATA_HERE,
  } satisfies CoreApiUploadInspirationImageRequest;

  try {
    const data = await api.coreApiUploadInspirationImage(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name              | Type     | Description | Notes                     |
| ----------------- | -------- | ----------- | ------------------------- |
| **inspirationId** | `string` |             | [Defaults to `undefined`] |
| **image**         | `Blob`   |             | [Defaults to `undefined`] |

### Return type

[**InspirationSchema**](InspirationSchema.md)

### Authorization

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: `multipart/form-data`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

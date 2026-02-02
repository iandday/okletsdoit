# GuestlistApi

All URIs are relative to _http://localhost_

| Method                                                                                                             | HTTP request                                                 | Description                           |
| ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------ | ------------------------------------- |
| [**guestlistApiCreateGuest**](GuestlistApi.md#guestlistapicreateguest)                                             | **POST** /api/guestlist/guests                               | Create Guest                          |
| [**guestlistApiCreateGuestGroup**](GuestlistApi.md#guestlistapicreateguestgroup)                                   | **POST** /api/guestlist/guest-groups                         | Create Guest Group                    |
| [**guestlistApiCreateRsvpResponse**](GuestlistApi.md#guestlistapicreatersvpresponse)                               | **POST** /api/guestlist/rsvp-responses                       | Create Rsvp Response                  |
| [**guestlistApiCreateRsvpSubmission**](GuestlistApi.md#guestlistapicreatersvpsubmission)                           | **POST** /api/guestlist/rsvp-submissions                     | Create Rsvp Submission                |
| [**guestlistApiDeclineRsvp**](GuestlistApi.md#guestlistapideclinersvp)                                             | **POST** /api/guestlist/rsvp-decline/{rsvp_code}             | Decline Rsvp                          |
| [**guestlistApiDeleteGuest**](GuestlistApi.md#guestlistapideleteguest)                                             | **DELETE** /api/guestlist/guests/{guest_id}                  | Delete Guest                          |
| [**guestlistApiDeleteGuestGroup**](GuestlistApi.md#guestlistapideleteguestgroup)                                   | **DELETE** /api/guestlist/guest-groups/{group_id}            | Delete Guest Group                    |
| [**guestlistApiDeleteRsvpResponse**](GuestlistApi.md#guestlistapideletersvpresponse)                               | **DELETE** /api/guestlist/rsvp-responses/{response_id}       | Delete Rsvp Response                  |
| [**guestlistApiDeleteRsvpSubmission**](GuestlistApi.md#guestlistapideletersvpsubmission)                           | **DELETE** /api/guestlist/rsvp-submissions/{submission_id}   | Delete Rsvp Submission                |
| [**guestlistApiExportAddressCsv**](GuestlistApi.md#guestlistapiexportaddresscsv)                                   | **GET** /api/guestlist/export_address_csv                    | Export Address Csv                    |
| [**guestlistApiGetGuest**](GuestlistApi.md#guestlistapigetguest)                                                   | **GET** /api/guestlist/guests/{guest_id}                     | Get Guest                             |
| [**guestlistApiGetGuestGroup**](GuestlistApi.md#guestlistapigetguestgroup)                                         | **GET** /api/guestlist/guest-groups/{group_id}               | Get Guest Group                       |
| [**guestlistApiGetRsvpAcceptanceQuestions**](GuestlistApi.md#guestlistapigetrsvpacceptancequestions)               | **GET** /api/guestlist/rsvp-acceptance-questions/{rsvp_code} | Get Rsvp Acceptance Questions         |
| [**guestlistApiGetRsvpAcceptenceQuestionsPreview**](GuestlistApi.md#guestlistapigetrsvpacceptencequestionspreview) | **GET** /api/guestlist/rsvp-acceptance-questions/preview     | Get Rsvp Acceptence Questions Preview |
| [**guestlistApiGetRsvpResponse**](GuestlistApi.md#guestlistapigetrsvpresponse)                                     | **GET** /api/guestlist/rsvp-responses/{response_id}          | Get Rsvp Response                     |
| [**guestlistApiGetRsvpSubmission**](GuestlistApi.md#guestlistapigetrsvpsubmission)                                 | **GET** /api/guestlist/rsvp-submissions/{submission_id}      | Get Rsvp Submission                   |
| [**guestlistApiListGuestGroups**](GuestlistApi.md#guestlistapilistguestgroups)                                     | **GET** /api/guestlist/guest-groups                          | List Guest Groups                     |
| [**guestlistApiListGuests**](GuestlistApi.md#guestlistapilistguests)                                               | **GET** /api/guestlist/guests                                | List Guests                           |
| [**guestlistApiListRsvpResponses**](GuestlistApi.md#guestlistapilistrsvpresponses)                                 | **GET** /api/guestlist/rsvp-responses                        | List Rsvp Responses                   |
| [**guestlistApiListRsvpSubmissions**](GuestlistApi.md#guestlistapilistrsvpsubmissions)                             | **GET** /api/guestlist/rsvp-submissions                      | List Rsvp Submissions                 |
| [**guestlistApiUpdateGuest**](GuestlistApi.md#guestlistapiupdateguest)                                             | **PUT** /api/guestlist/guests/{guest_id}                     | Update Guest                          |
| [**guestlistApiUpdateGuestGroup**](GuestlistApi.md#guestlistapiupdateguestgroup)                                   | **PUT** /api/guestlist/guest-groups/{group_id}               | Update Guest Group                    |
| [**guestlistApiUpdateRsvpResponse**](GuestlistApi.md#guestlistapiupdatersvpresponse)                               | **PUT** /api/guestlist/rsvp-responses/{response_id}          | Update Rsvp Response                  |
| [**guestlistApiUpdateRsvpSubmission**](GuestlistApi.md#guestlistapiupdatersvpsubmission)                           | **PUT** /api/guestlist/rsvp-submissions/{submission_id}      | Update Rsvp Submission                |

## guestlistApiCreateGuest

> GuestSchema guestlistApiCreateGuest(guestCreateSchema)

Create Guest

Create a new guest

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiCreateGuestRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // GuestCreateSchema
    guestCreateSchema: ...,
  } satisfies GuestlistApiCreateGuestRequest;

  try {
    const data = await api.guestlistApiCreateGuest(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                  | Type                                      | Description | Notes |
| --------------------- | ----------------------------------------- | ----------- | ----- |
| **guestCreateSchema** | [GuestCreateSchema](GuestCreateSchema.md) |             |       |

### Return type

[**GuestSchema**](GuestSchema.md)

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

## guestlistApiCreateGuestGroup

> GuestGroupSchema guestlistApiCreateGuestGroup(guestGroupCreateSchema)

Create Guest Group

Create a new guest group

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiCreateGuestGroupRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // GuestGroupCreateSchema
    guestGroupCreateSchema: ...,
  } satisfies GuestlistApiCreateGuestGroupRequest;

  try {
    const data = await api.guestlistApiCreateGuestGroup(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                       | Type                                                | Description | Notes |
| -------------------------- | --------------------------------------------------- | ----------- | ----- |
| **guestGroupCreateSchema** | [GuestGroupCreateSchema](GuestGroupCreateSchema.md) |             |       |

### Return type

[**GuestGroupSchema**](GuestGroupSchema.md)

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

## guestlistApiCreateRsvpResponse

> RsvpQuestionResponseSchema guestlistApiCreateRsvpResponse(rsvpQuestionResponseCreateSchema)

Create Rsvp Response

Create a new RSVP question response

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiCreateRsvpResponseRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // RsvpQuestionResponseCreateSchema
    rsvpQuestionResponseCreateSchema: ...,
  } satisfies GuestlistApiCreateRsvpResponseRequest;

  try {
    const data = await api.guestlistApiCreateRsvpResponse(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                                 | Type                                                                    | Description | Notes |
| ------------------------------------ | ----------------------------------------------------------------------- | ----------- | ----- |
| **rsvpQuestionResponseCreateSchema** | [RsvpQuestionResponseCreateSchema](RsvpQuestionResponseCreateSchema.md) |             |       |

### Return type

[**RsvpQuestionResponseSchema**](RsvpQuestionResponseSchema.md)

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

## guestlistApiCreateRsvpSubmission

> RsvpSubmissionSchema guestlistApiCreateRsvpSubmission(rsvpSubmissionCreateSchema)

Create Rsvp Submission

Create a new RSVP submission

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiCreateRsvpSubmissionRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // RsvpSubmissionCreateSchema
    rsvpSubmissionCreateSchema: ...,
  } satisfies GuestlistApiCreateRsvpSubmissionRequest;

  try {
    const data = await api.guestlistApiCreateRsvpSubmission(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                           | Type                                                        | Description | Notes |
| ------------------------------ | ----------------------------------------------------------- | ----------- | ----- |
| **rsvpSubmissionCreateSchema** | [RsvpSubmissionCreateSchema](RsvpSubmissionCreateSchema.md) |             |       |

### Return type

[**RsvpSubmissionSchema**](RsvpSubmissionSchema.md)

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

## guestlistApiDeclineRsvp

> RsvpDeclineResponseSchema guestlistApiDeclineRsvp(rsvpCode)

Decline Rsvp

Decline an RSVP using the rsvp code

### Example

```ts
import { Configuration, GuestlistApi } from "";
import type { GuestlistApiDeclineRsvpRequest } from "";

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
    const api = new GuestlistApi(config);

    const body = {
        // string
        rsvpCode: rsvpCode_example,
    } satisfies GuestlistApiDeclineRsvpRequest;

    try {
        const data = await api.guestlistApiDeclineRsvp(body);
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
| **rsvpCode** | `string` |             | [Defaults to `undefined`] |

### Return type

[**RsvpDeclineResponseSchema**](RsvpDeclineResponseSchema.md)

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

## guestlistApiDeleteGuest

> guestlistApiDeleteGuest(guestId)

Delete Guest

Soft delete a guest

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiDeleteGuestRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    guestId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiDeleteGuestRequest;

  try {
    const data = await api.guestlistApiDeleteGuest(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name        | Type     | Description | Notes                     |
| ----------- | -------- | ----------- | ------------------------- |
| **guestId** | `string` |             | [Defaults to `undefined`] |

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

## guestlistApiDeleteGuestGroup

> guestlistApiDeleteGuestGroup(groupId)

Delete Guest Group

Soft delete a guest group

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiDeleteGuestGroupRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    groupId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiDeleteGuestGroupRequest;

  try {
    const data = await api.guestlistApiDeleteGuestGroup(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name        | Type     | Description | Notes                     |
| ----------- | -------- | ----------- | ------------------------- |
| **groupId** | `string` |             | [Defaults to `undefined`] |

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

## guestlistApiDeleteRsvpResponse

> guestlistApiDeleteRsvpResponse(responseId)

Delete Rsvp Response

Soft delete an RSVP question response

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiDeleteRsvpResponseRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    responseId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiDeleteRsvpResponseRequest;

  try {
    const data = await api.guestlistApiDeleteRsvpResponse(body);
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
| **responseId** | `string` |             | [Defaults to `undefined`] |

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

## guestlistApiDeleteRsvpSubmission

> guestlistApiDeleteRsvpSubmission(submissionId)

Delete Rsvp Submission

Delete an RSVP submission

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiDeleteRsvpSubmissionRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    submissionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiDeleteRsvpSubmissionRequest;

  try {
    const data = await api.guestlistApiDeleteRsvpSubmission(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name             | Type     | Description | Notes                     |
| ---------------- | -------- | ----------- | ------------------------- |
| **submissionId** | `string` |             | [Defaults to `undefined`] |

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

## guestlistApiExportAddressCsv

> guestlistApiExportAddressCsv()

Export Address Csv

### Example

```ts
import { Configuration, GuestlistApi } from "";
import type { GuestlistApiExportAddressCsvRequest } from "";

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
    const api = new GuestlistApi(config);

    try {
        const data = await api.guestlistApiExportAddressCsv();
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

## guestlistApiGetGuest

> GuestSchema guestlistApiGetGuest(guestId)

Get Guest

Get a specific guest by ID

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiGetGuestRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    guestId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiGetGuestRequest;

  try {
    const data = await api.guestlistApiGetGuest(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name        | Type     | Description | Notes                     |
| ----------- | -------- | ----------- | ------------------------- |
| **guestId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**GuestSchema**](GuestSchema.md)

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

## guestlistApiGetGuestGroup

> GuestGroupSchema guestlistApiGetGuestGroup(groupId)

Get Guest Group

Get a specific guest group by ID

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiGetGuestGroupRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    groupId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiGetGuestGroupRequest;

  try {
    const data = await api.guestlistApiGetGuestGroup(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name        | Type     | Description | Notes                     |
| ----------- | -------- | ----------- | ------------------------- |
| **groupId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**GuestGroupSchema**](GuestGroupSchema.md)

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

## guestlistApiGetRsvpAcceptanceQuestions

> Array&lt;RsvpQuestionResponseSchema&gt; guestlistApiGetRsvpAcceptanceQuestions(rsvpCode)

Get Rsvp Acceptance Questions

Get or create RSVP acceptance questions for a guest group

### Example

```ts
import { Configuration, GuestlistApi } from "";
import type { GuestlistApiGetRsvpAcceptanceQuestionsRequest } from "";

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
    const api = new GuestlistApi(config);

    const body = {
        // string
        rsvpCode: rsvpCode_example,
    } satisfies GuestlistApiGetRsvpAcceptanceQuestionsRequest;

    try {
        const data = await api.guestlistApiGetRsvpAcceptanceQuestions(body);
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
| **rsvpCode** | `string` |             | [Defaults to `undefined`] |

### Return type

[**Array&lt;RsvpQuestionResponseSchema&gt;**](RsvpQuestionResponseSchema.md)

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

## guestlistApiGetRsvpAcceptenceQuestionsPreview

> Array&lt;RsvpQuestionResponseSchema&gt; guestlistApiGetRsvpAcceptenceQuestionsPreview()

Get Rsvp Acceptence Questions Preview

Get RSVP acceptance questions for preview mode

### Example

```ts
import { Configuration, GuestlistApi } from "";
import type { GuestlistApiGetRsvpAcceptenceQuestionsPreviewRequest } from "";

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
    const api = new GuestlistApi(config);

    try {
        const data = await api.guestlistApiGetRsvpAcceptenceQuestionsPreview();
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

[**Array&lt;RsvpQuestionResponseSchema&gt;**](RsvpQuestionResponseSchema.md)

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

## guestlistApiGetRsvpResponse

> RsvpQuestionResponseSchema guestlistApiGetRsvpResponse(responseId)

Get Rsvp Response

Get a specific RSVP question response by ID

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiGetRsvpResponseRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    responseId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiGetRsvpResponseRequest;

  try {
    const data = await api.guestlistApiGetRsvpResponse(body);
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
| **responseId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**RsvpQuestionResponseSchema**](RsvpQuestionResponseSchema.md)

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

## guestlistApiGetRsvpSubmission

> RsvpSubmissionSchema guestlistApiGetRsvpSubmission(submissionId)

Get Rsvp Submission

Get a specific RSVP submission by ID

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiGetRsvpSubmissionRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    submissionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies GuestlistApiGetRsvpSubmissionRequest;

  try {
    const data = await api.guestlistApiGetRsvpSubmission(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name             | Type     | Description | Notes                     |
| ---------------- | -------- | ----------- | ------------------------- |
| **submissionId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**RsvpSubmissionSchema**](RsvpSubmissionSchema.md)

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

## guestlistApiListGuestGroups

> PagedGuestGroupSchema guestlistApiListGuestGroups(name, email, phone, city, state, zipCode, relationship, priority, rsvpCode, page, pageSize)

List Guest Groups

List all guest groups (non-deleted)

### Example

```ts
import { Configuration, GuestlistApi } from "";
import type { GuestlistApiListGuestGroupsRequest } from "";

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
    const api = new GuestlistApi(config);

    const body = {
        // string (optional)
        name: name_example,
        // string (optional)
        email: email_example,
        // string (optional)
        phone: phone_example,
        // string (optional)
        city: city_example,
        // string (optional)
        state: state_example,
        // string (optional)
        zipCode: zipCode_example,
        // string (optional)
        relationship: relationship_example,
        // number (optional)
        priority: 56,
        // string (optional)
        rsvpCode: rsvpCode_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies GuestlistApiListGuestGroupsRequest;

    try {
        const data = await api.guestlistApiListGuestGroups(body);
        console.log(data);
    } catch (error) {
        console.error(error);
    }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name             | Type     | Description | Notes                                |
| ---------------- | -------- | ----------- | ------------------------------------ |
| **name**         | `string` |             | [Optional] [Defaults to `undefined`] |
| **email**        | `string` |             | [Optional] [Defaults to `undefined`] |
| **phone**        | `string` |             | [Optional] [Defaults to `undefined`] |
| **city**         | `string` |             | [Optional] [Defaults to `undefined`] |
| **state**        | `string` |             | [Optional] [Defaults to `undefined`] |
| **zipCode**      | `string` |             | [Optional] [Defaults to `undefined`] |
| **relationship** | `string` |             | [Optional] [Defaults to `undefined`] |
| **priority**     | `number` |             | [Optional] [Defaults to `undefined`] |
| **rsvpCode**     | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**         | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize**     | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedGuestGroupSchema**](PagedGuestGroupSchema.md)

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

## guestlistApiListGuests

> PagedGuestSchema guestlistApiListGuests(groupId, page, pageSize)

List Guests

List all guests, optionally filtered by group

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiListGuestsRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string (optional)
    groupId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // number (optional)
    page: 56,
    // number (optional)
    pageSize: 56,
  } satisfies GuestlistApiListGuestsRequest;

  try {
    const data = await api.guestlistApiListGuests(body);
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
| **groupId**  | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**     | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize** | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedGuestSchema**](PagedGuestSchema.md)

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

## guestlistApiListRsvpResponses

> PagedRsvpQuestionResponseSchema guestlistApiListRsvpResponses(submissionId, page, pageSize)

List Rsvp Responses

List all RSVP question responses, optionally filtered by submission

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiListRsvpResponsesRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string (optional)
    submissionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // number (optional)
    page: 56,
    // number (optional)
    pageSize: 56,
  } satisfies GuestlistApiListRsvpResponsesRequest;

  try {
    const data = await api.guestlistApiListRsvpResponses(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name             | Type     | Description | Notes                                |
| ---------------- | -------- | ----------- | ------------------------------------ |
| **submissionId** | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**         | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize**     | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedRsvpQuestionResponseSchema**](PagedRsvpQuestionResponseSchema.md)

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

## guestlistApiListRsvpSubmissions

> PagedRsvpSubmissionSchema guestlistApiListRsvpSubmissions(rsvpCode, page, pageSize)

List Rsvp Submissions

List all RSVP submissions

### Example

```ts
import { Configuration, GuestlistApi } from "";
import type { GuestlistApiListRsvpSubmissionsRequest } from "";

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
    const api = new GuestlistApi(config);

    const body = {
        // string (optional)
        rsvpCode: rsvpCode_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies GuestlistApiListRsvpSubmissionsRequest;

    try {
        const data = await api.guestlistApiListRsvpSubmissions(body);
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
| **rsvpCode** | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**     | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize** | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedRsvpSubmissionSchema**](PagedRsvpSubmissionSchema.md)

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

## guestlistApiUpdateGuest

> GuestSchema guestlistApiUpdateGuest(guestId, guestUpdateSchema)

Update Guest

Update a guest

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiUpdateGuestRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    guestId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // GuestUpdateSchema
    guestUpdateSchema: ...,
  } satisfies GuestlistApiUpdateGuestRequest;

  try {
    const data = await api.guestlistApiUpdateGuest(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                  | Type                                      | Description | Notes                     |
| --------------------- | ----------------------------------------- | ----------- | ------------------------- |
| **guestId**           | `string`                                  |             | [Defaults to `undefined`] |
| **guestUpdateSchema** | [GuestUpdateSchema](GuestUpdateSchema.md) |             |                           |

### Return type

[**GuestSchema**](GuestSchema.md)

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

## guestlistApiUpdateGuestGroup

> GuestGroupSchema guestlistApiUpdateGuestGroup(groupId, guestGroupUpdateSchema)

Update Guest Group

Update a guest group

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiUpdateGuestGroupRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    groupId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // GuestGroupUpdateSchema
    guestGroupUpdateSchema: ...,
  } satisfies GuestlistApiUpdateGuestGroupRequest;

  try {
    const data = await api.guestlistApiUpdateGuestGroup(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                       | Type                                                | Description | Notes                     |
| -------------------------- | --------------------------------------------------- | ----------- | ------------------------- |
| **groupId**                | `string`                                            |             | [Defaults to `undefined`] |
| **guestGroupUpdateSchema** | [GuestGroupUpdateSchema](GuestGroupUpdateSchema.md) |             |                           |

### Return type

[**GuestGroupSchema**](GuestGroupSchema.md)

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

## guestlistApiUpdateRsvpResponse

> RsvpQuestionResponseSchema guestlistApiUpdateRsvpResponse(responseId, rsvpQuestionResponseUpdateSchema)

Update Rsvp Response

Update an RSVP question response

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiUpdateRsvpResponseRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    responseId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // RsvpQuestionResponseUpdateSchema
    rsvpQuestionResponseUpdateSchema: ...,
  } satisfies GuestlistApiUpdateRsvpResponseRequest;

  try {
    const data = await api.guestlistApiUpdateRsvpResponse(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                                 | Type                                                                    | Description | Notes                     |
| ------------------------------------ | ----------------------------------------------------------------------- | ----------- | ------------------------- |
| **responseId**                       | `string`                                                                |             | [Defaults to `undefined`] |
| **rsvpQuestionResponseUpdateSchema** | [RsvpQuestionResponseUpdateSchema](RsvpQuestionResponseUpdateSchema.md) |             |                           |

### Return type

[**RsvpQuestionResponseSchema**](RsvpQuestionResponseSchema.md)

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

## guestlistApiUpdateRsvpSubmission

> RsvpSubmissionSchema guestlistApiUpdateRsvpSubmission(submissionId, rsvpSubmissionUpdateSchema)

Update Rsvp Submission

Update an RSVP submission

### Example

```ts
import {
  Configuration,
  GuestlistApi,
} from '';
import type { GuestlistApiUpdateRsvpSubmissionRequest } from '';

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
  const api = new GuestlistApi(config);

  const body = {
    // string
    submissionId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // RsvpSubmissionUpdateSchema
    rsvpSubmissionUpdateSchema: ...,
  } satisfies GuestlistApiUpdateRsvpSubmissionRequest;

  try {
    const data = await api.guestlistApiUpdateRsvpSubmission(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                           | Type                                                        | Description | Notes                     |
| ------------------------------ | ----------------------------------------------------------- | ----------- | ------------------------- |
| **submissionId**               | `string`                                                    |             | [Defaults to `undefined`] |
| **rsvpSubmissionUpdateSchema** | [RsvpSubmissionUpdateSchema](RsvpSubmissionUpdateSchema.md) |             |                           |

### Return type

[**RsvpSubmissionSchema**](RsvpSubmissionSchema.md)

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

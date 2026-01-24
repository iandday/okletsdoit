# DeadlinesApi

All URIs are relative to _http://localhost_

| Method                                                                                     | HTTP request                                                   | Description              |
| ------------------------------------------------------------------------------------------ | -------------------------------------------------------------- | ------------------------ |
| [**deadlineApiCreateDeadline**](DeadlinesApi.md#deadlineapicreatedeadline)                 | **POST** /api/deadline/deadlines                               | Create Deadline          |
| [**deadlineApiCreateDeadlineList**](DeadlinesApi.md#deadlineapicreatedeadlinelist)         | **POST** /api/deadline/deadline-lists                          | Create Deadline List     |
| [**deadlineApiDeleteDeadline**](DeadlinesApi.md#deadlineapideletedeadline)                 | **DELETE** /api/deadline/deadlines/{deadline_id}               | Delete Deadline          |
| [**deadlineApiDeleteDeadlineList**](DeadlinesApi.md#deadlineapideletedeadlinelist)         | **DELETE** /api/deadline/deadline-lists/{list_id}              | Delete Deadline List     |
| [**deadlineApiGetDeadline**](DeadlinesApi.md#deadlineapigetdeadline)                       | **GET** /api/deadline/deadlines/{deadline_id}                  | Get Deadline             |
| [**deadlineApiGetDeadlineList**](DeadlinesApi.md#deadlineapigetdeadlinelist)               | **GET** /api/deadline/deadline-lists/{list_id}                 | Get Deadline List        |
| [**deadlineApiListDeadlineLists**](DeadlinesApi.md#deadlineapilistdeadlinelists)           | **GET** /api/deadline/deadline-lists                           | List Deadline Lists      |
| [**deadlineApiListDeadlines**](DeadlinesApi.md#deadlineapilistdeadlines)                   | **GET** /api/deadline/deadlines                                | List Deadlines           |
| [**deadlineApiToggleDeadlineComplete**](DeadlinesApi.md#deadlineapitoggledeadlinecomplete) | **POST** /api/deadline/deadlines/{deadline_id}/toggle_complete | Toggle Deadline Complete |
| [**deadlineApiUpdateDeadline**](DeadlinesApi.md#deadlineapiupdatedeadline)                 | **PUT** /api/deadline/deadlines/{deadline_id}                  | Update Deadline          |
| [**deadlineApiUpdateDeadlineList**](DeadlinesApi.md#deadlineapiupdatedeadlinelist)         | **PUT** /api/deadline/deadline-lists/{list_id}                 | Update Deadline List     |

## deadlineApiCreateDeadline

> DeadlineSchema deadlineApiCreateDeadline(deadlineCreateSchema)

Create Deadline

Create a new deadline

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiCreateDeadlineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // DeadlineCreateSchema
    deadlineCreateSchema: ...,
  } satisfies DeadlineApiCreateDeadlineRequest;

  try {
    const data = await api.deadlineApiCreateDeadline(body);
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
| **deadlineCreateSchema** | [DeadlineCreateSchema](DeadlineCreateSchema.md) |             |       |

### Return type

[**DeadlineSchema**](DeadlineSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiCreateDeadlineList

> DeadlineListSchema deadlineApiCreateDeadlineList(deadlineListCreateSchema)

Create Deadline List

Create a new deadline list

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiCreateDeadlineListRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // DeadlineListCreateSchema
    deadlineListCreateSchema: ...,
  } satisfies DeadlineApiCreateDeadlineListRequest;

  try {
    const data = await api.deadlineApiCreateDeadlineList(body);
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
| **deadlineListCreateSchema** | [DeadlineListCreateSchema](DeadlineListCreateSchema.md) |             |       |

### Return type

[**DeadlineListSchema**](DeadlineListSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiDeleteDeadline

> deadlineApiDeleteDeadline(deadlineId)

Delete Deadline

Soft delete a deadline

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiDeleteDeadlineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string
    deadlineId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies DeadlineApiDeleteDeadlineRequest;

  try {
    const data = await api.deadlineApiDeleteDeadline(body);
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
| **deadlineId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiDeleteDeadlineList

> deadlineApiDeleteDeadlineList(listId)

Delete Deadline List

Soft delete a deadline list

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiDeleteDeadlineListRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string
    listId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies DeadlineApiDeleteDeadlineListRequest;

  try {
    const data = await api.deadlineApiDeleteDeadlineList(body);
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
| **listId** | `string` |             | [Defaults to `undefined`] |

### Return type

`void` (Empty response body)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiGetDeadline

> DeadlineSchema deadlineApiGetDeadline(deadlineId)

Get Deadline

Get a specific deadline by ID

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiGetDeadlineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string
    deadlineId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies DeadlineApiGetDeadlineRequest;

  try {
    const data = await api.deadlineApiGetDeadline(body);
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
| **deadlineId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**DeadlineSchema**](DeadlineSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiGetDeadlineList

> DeadlineListSchema deadlineApiGetDeadlineList(listId)

Get Deadline List

Get a specific deadline list by ID

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiGetDeadlineListRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string
    listId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies DeadlineApiGetDeadlineListRequest;

  try {
    const data = await api.deadlineApiGetDeadlineList(body);
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
| **listId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**DeadlineListSchema**](DeadlineListSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiListDeadlineLists

> PagedDeadlineListSchema deadlineApiListDeadlineLists(page, pageSize)

List Deadline Lists

List all deadline lists (non-deleted)

### Example

```ts
import { Configuration, DeadlinesApi } from "";
import type { DeadlineApiListDeadlineListsRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const api = new DeadlinesApi();

    const body = {
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies DeadlineApiListDeadlineListsRequest;

    try {
        const data = await api.deadlineApiListDeadlineLists(body);
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
| **page**     | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize** | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedDeadlineListSchema**](PagedDeadlineListSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiListDeadlines

> PagedDeadlineSchema deadlineApiListDeadlines(deadlineListId, completed, assignedToId, overdue, search, page, pageSize)

List Deadlines

List all deadlines (non-deleted) with optional filtering

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiListDeadlinesRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string (optional)
    deadlineListId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // boolean (optional)
    completed: true,
    // string (optional)
    assignedToId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // boolean (optional)
    overdue: true,
    // string (optional)
    search: search_example,
    // number (optional)
    page: 56,
    // number (optional)
    pageSize: 56,
  } satisfies DeadlineApiListDeadlinesRequest;

  try {
    const data = await api.deadlineApiListDeadlines(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name               | Type      | Description | Notes                                |
| ------------------ | --------- | ----------- | ------------------------------------ |
| **deadlineListId** | `string`  |             | [Optional] [Defaults to `undefined`] |
| **completed**      | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **assignedToId**   | `string`  |             | [Optional] [Defaults to `undefined`] |
| **overdue**        | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **search**         | `string`  |             | [Optional] [Defaults to `undefined`] |
| **page**           | `number`  |             | [Optional] [Defaults to `1`]         |
| **pageSize**       | `number`  |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedDeadlineSchema**](PagedDeadlineSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiToggleDeadlineComplete

> DeadlineSchema deadlineApiToggleDeadlineComplete(deadlineId)

Toggle Deadline Complete

Toggle the completion status of a deadline

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiToggleDeadlineCompleteRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string
    deadlineId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies DeadlineApiToggleDeadlineCompleteRequest;

  try {
    const data = await api.deadlineApiToggleDeadlineComplete(body);
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
| **deadlineId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**DeadlineSchema**](DeadlineSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiUpdateDeadline

> DeadlineSchema deadlineApiUpdateDeadline(deadlineId, deadlineUpdateSchema)

Update Deadline

Update a deadline

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiUpdateDeadlineRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string
    deadlineId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // DeadlineUpdateSchema
    deadlineUpdateSchema: ...,
  } satisfies DeadlineApiUpdateDeadlineRequest;

  try {
    const data = await api.deadlineApiUpdateDeadline(body);
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
| **deadlineId**           | `string`                                        |             | [Defaults to `undefined`] |
| **deadlineUpdateSchema** | [DeadlineUpdateSchema](DeadlineUpdateSchema.md) |             |                           |

### Return type

[**DeadlineSchema**](DeadlineSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## deadlineApiUpdateDeadlineList

> DeadlineListSchema deadlineApiUpdateDeadlineList(listId, deadlineListUpdateSchema)

Update Deadline List

Update a deadline list

### Example

```ts
import {
  Configuration,
  DeadlinesApi,
} from '';
import type { DeadlineApiUpdateDeadlineListRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new DeadlinesApi();

  const body = {
    // string
    listId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // DeadlineListUpdateSchema
    deadlineListUpdateSchema: ...,
  } satisfies DeadlineApiUpdateDeadlineListRequest;

  try {
    const data = await api.deadlineApiUpdateDeadlineList(body);
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
| **listId**                   | `string`                                                |             | [Defaults to `undefined`] |
| **deadlineListUpdateSchema** | [DeadlineListUpdateSchema](DeadlineListUpdateSchema.md) |             |                           |

### Return type

[**DeadlineListSchema**](DeadlineListSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

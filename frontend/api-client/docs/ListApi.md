# ListApi

All URIs are relative to _http://localhost_

| Method                                                          | HTTP request                                                 | Description       |
| --------------------------------------------------------------- | ------------------------------------------------------------ | ----------------- |
| [**listApiCreateList**](ListApi.md#listapicreatelist)           | **POST** /api/lists/lists                                    | Create List       |
| [**listApiCreateListEntry**](ListApi.md#listapicreatelistentry) | **POST** /api/lists/list-entries                             | Create List Entry |
| [**listApiDeleteList**](ListApi.md#listapideletelist)           | **DELETE** /api/lists/lists/{list_id}                        | Delete List       |
| [**listApiDeleteListEntry**](ListApi.md#listapideletelistentry) | **DELETE** /api/lists/list-entries/{entry_id}                | Delete List Entry |
| [**listApiGetList**](ListApi.md#listapigetlist)                 | **GET** /api/lists/lists/{list_id}                           | Get List          |
| [**listApiGetListEntry**](ListApi.md#listapigetlistentry)       | **GET** /api/lists/list-entries/{entry_id}                   | Get List Entry    |
| [**listApiListListEntries**](ListApi.md#listapilistlistentries) | **GET** /api/lists/list-entries                              | List List Entries |
| [**listApiListLists**](ListApi.md#listapilistlists)             | **GET** /api/lists/lists                                     | List Lists        |
| [**listApiToggleCompleted**](ListApi.md#listapitogglecompleted) | **POST** /api/lists/list-entries/{entry_id}/toggle-completed | Toggle Completed  |
| [**listApiTogglePurchased**](ListApi.md#listapitogglepurchased) | **POST** /api/lists/list-entries/{entry_id}/toggle-purchased | Toggle Purchased  |
| [**listApiUpdateList**](ListApi.md#listapiupdatelist)           | **PUT** /api/lists/lists/{list_id}                           | Update List       |
| [**listApiUpdateListEntry**](ListApi.md#listapiupdatelistentry) | **PUT** /api/lists/list-entries/{entry_id}                   | Update List Entry |

## listApiCreateList

> ListSchema listApiCreateList(listCreateSchema)

Create List

Create a new list

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiCreateListRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // ListCreateSchema
    listCreateSchema: ...,
  } satisfies ListApiCreateListRequest;

  try {
    const data = await api.listApiCreateList(body);
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
| **listCreateSchema** | [ListCreateSchema](ListCreateSchema.md) |             |       |

### Return type

[**ListSchema**](ListSchema.md)

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

## listApiCreateListEntry

> ListEntrySchema listApiCreateListEntry(listEntryCreateSchema)

Create List Entry

Create a new list entry

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiCreateListEntryRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // ListEntryCreateSchema
    listEntryCreateSchema: ...,
  } satisfies ListApiCreateListEntryRequest;

  try {
    const data = await api.listApiCreateListEntry(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                      | Type                                              | Description | Notes |
| ------------------------- | ------------------------------------------------- | ----------- | ----- |
| **listEntryCreateSchema** | [ListEntryCreateSchema](ListEntryCreateSchema.md) |             |       |

### Return type

[**ListEntrySchema**](ListEntrySchema.md)

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

## listApiDeleteList

> listApiDeleteList(listId)

Delete List

Soft delete a list

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiDeleteListRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    listId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ListApiDeleteListRequest;

  try {
    const data = await api.listApiDeleteList(body);
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

[SessionAuth](../README.md#SessionAuth), [ServiceTokenAuth](../README.md#ServiceTokenAuth), [XSessionTokenAuth](../README.md#XSessionTokenAuth)

### HTTP request headers

- **Content-Type**: Not defined
- **Accept**: Not defined

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## listApiDeleteListEntry

> listApiDeleteListEntry(entryId)

Delete List Entry

Soft delete a list entry

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiDeleteListEntryRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    entryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ListApiDeleteListEntryRequest;

  try {
    const data = await api.listApiDeleteListEntry(body);
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
| **entryId** | `string` |             | [Defaults to `undefined`] |

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

## listApiGetList

> ListSchema listApiGetList(listId)

Get List

Get a specific list by ID

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiGetListRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    listId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ListApiGetListRequest;

  try {
    const data = await api.listApiGetList(body);
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

[**ListSchema**](ListSchema.md)

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

## listApiGetListEntry

> ListEntrySchema listApiGetListEntry(entryId)

Get List Entry

Get a specific list entry by ID

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiGetListEntryRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    entryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ListApiGetListEntryRequest;

  try {
    const data = await api.listApiGetListEntry(body);
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
| **entryId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**ListEntrySchema**](ListEntrySchema.md)

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

## listApiListListEntries

> PagedListEntrySchema listApiListListEntries(item, listId, isCompleted, purchased, vendorId, associatedExpenseId, page, pageSize)

List List Entries

List all list entries (non-deleted)

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiListListEntriesRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string (optional)
    item: item_example,
    // string (optional)
    listId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // boolean (optional)
    isCompleted: true,
    // boolean (optional)
    purchased: true,
    // string (optional)
    vendorId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // string (optional)
    associatedExpenseId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // number (optional)
    page: 56,
    // number (optional)
    pageSize: 56,
  } satisfies ListApiListListEntriesRequest;

  try {
    const data = await api.listApiListListEntries(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                    | Type      | Description | Notes                                |
| ----------------------- | --------- | ----------- | ------------------------------------ |
| **item**                | `string`  |             | [Optional] [Defaults to `undefined`] |
| **listId**              | `string`  |             | [Optional] [Defaults to `undefined`] |
| **isCompleted**         | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **purchased**           | `boolean` |             | [Optional] [Defaults to `undefined`] |
| **vendorId**            | `string`  |             | [Optional] [Defaults to `undefined`] |
| **associatedExpenseId** | `string`  |             | [Optional] [Defaults to `undefined`] |
| **page**                | `number`  |             | [Optional] [Defaults to `1`]         |
| **pageSize**            | `number`  |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedListEntrySchema**](PagedListEntrySchema.md)

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

## listApiListLists

> PagedListSchema listApiListLists(name, page, pageSize)

List Lists

List all lists (non-deleted)

### Example

```ts
import { Configuration, ListApi } from "";
import type { ListApiListListsRequest } from "";

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
    const api = new ListApi(config);

    const body = {
        // string (optional)
        name: name_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies ListApiListListsRequest;

    try {
        const data = await api.listApiListLists(body);
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

[**PagedListSchema**](PagedListSchema.md)

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

## listApiToggleCompleted

> ListEntrySchema listApiToggleCompleted(entryId)

Toggle Completed

Toggle the completed status of a list entry

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiToggleCompletedRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    entryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ListApiToggleCompletedRequest;

  try {
    const data = await api.listApiToggleCompleted(body);
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
| **entryId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**ListEntrySchema**](ListEntrySchema.md)

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

## listApiTogglePurchased

> ListEntrySchema listApiTogglePurchased(entryId)

Toggle Purchased

Toggle the purchased status of a list entry

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiTogglePurchasedRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    entryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ListApiTogglePurchasedRequest;

  try {
    const data = await api.listApiTogglePurchased(body);
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
| **entryId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**ListEntrySchema**](ListEntrySchema.md)

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

## listApiUpdateList

> ListSchema listApiUpdateList(listId, listUpdateSchema)

Update List

Update a list

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiUpdateListRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    listId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // ListUpdateSchema
    listUpdateSchema: ...,
  } satisfies ListApiUpdateListRequest;

  try {
    const data = await api.listApiUpdateList(body);
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
| **listId**           | `string`                                |             | [Defaults to `undefined`] |
| **listUpdateSchema** | [ListUpdateSchema](ListUpdateSchema.md) |             |                           |

### Return type

[**ListSchema**](ListSchema.md)

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

## listApiUpdateListEntry

> ListEntrySchema listApiUpdateListEntry(entryId, listEntryUpdateSchema)

Update List Entry

Update a list entry

### Example

```ts
import {
  Configuration,
  ListApi,
} from '';
import type { ListApiUpdateListEntryRequest } from '';

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
  const api = new ListApi(config);

  const body = {
    // string
    entryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // ListEntryUpdateSchema
    listEntryUpdateSchema: ...,
  } satisfies ListApiUpdateListEntryRequest;

  try {
    const data = await api.listApiUpdateListEntry(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                      | Type                                              | Description | Notes                     |
| ------------------------- | ------------------------------------------------- | ----------- | ------------------------- |
| **entryId**               | `string`                                          |             | [Defaults to `undefined`] |
| **listEntryUpdateSchema** | [ListEntryUpdateSchema](ListEntryUpdateSchema.md) |             |                           |

### Return type

[**ListEntrySchema**](ListEntrySchema.md)

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

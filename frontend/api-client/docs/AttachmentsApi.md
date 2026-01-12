# AttachmentsApi

All URIs are relative to _http://localhost_

| Method                                                                                 | HTTP request                                               | Description       |
| -------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ----------------- |
| [**attachmentsApiCreateAttachment**](AttachmentsApi.md#attachmentsapicreateattachment) | **POST** /api/attachments/attachments                      | Create Attachment |
| [**attachmentsApiDeleteAttachment**](AttachmentsApi.md#attachmentsapideleteattachment) | **DELETE** /api/attachments/attachments/{attachment_id}    | Delete Attachment |
| [**attachmentsApiGetAttachment**](AttachmentsApi.md#attachmentsapigetattachment)       | **GET** /api/attachments/attachments/{attachment_id}       | Get Attachment    |
| [**attachmentsApiGetContentType**](AttachmentsApi.md#attachmentsapigetcontenttype)     | **GET** /api/attachments/content-types/{app_label}/{model} | Get Content Type  |
| [**attachmentsApiListAttachments**](AttachmentsApi.md#attachmentsapilistattachments)   | **GET** /api/attachments/attachments                       | List Attachments  |
| [**attachmentsApiUpdateAttachment**](AttachmentsApi.md#attachmentsapiupdateattachment) | **PUT** /api/attachments/attachments/{attachment_id}       | Update Attachment |

## attachmentsApiCreateAttachment

> AttachmentSchema attachmentsApiCreateAttachment(contentTypeId, objectId, file, name, description)

Create Attachment

Create a new attachment with file upload

### Example

```ts
import {
  Configuration,
  AttachmentsApi,
} from '';
import type { AttachmentsApiCreateAttachmentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AttachmentsApi();

  const body = {
    // number
    contentTypeId: 56,
    // string
    objectId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // Blob
    file: BINARY_DATA_HERE,
    // string (optional)
    name: name_example,
    // string (optional)
    description: description_example,
  } satisfies AttachmentsApiCreateAttachmentRequest;

  try {
    const data = await api.attachmentsApiCreateAttachment(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name              | Type     | Description | Notes                                |
| ----------------- | -------- | ----------- | ------------------------------------ |
| **contentTypeId** | `number` |             | [Defaults to `undefined`]            |
| **objectId**      | `string` |             | [Defaults to `undefined`]            |
| **file**          | `Blob`   |             | [Defaults to `undefined`]            |
| **name**          | `string` |             | [Optional] [Defaults to `undefined`] |
| **description**   | `string` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**AttachmentSchema**](AttachmentSchema.md)

### Authorization

No authorization required

### HTTP request headers

- **Content-Type**: `multipart/form-data`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

## attachmentsApiDeleteAttachment

> attachmentsApiDeleteAttachment(attachmentId)

Delete Attachment

Soft delete an attachment

### Example

```ts
import {
  Configuration,
  AttachmentsApi,
} from '';
import type { AttachmentsApiDeleteAttachmentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AttachmentsApi();

  const body = {
    // string
    attachmentId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies AttachmentsApiDeleteAttachmentRequest;

  try {
    const data = await api.attachmentsApiDeleteAttachment(body);
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
| **attachmentId** | `string` |             | [Defaults to `undefined`] |

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

## attachmentsApiGetAttachment

> AttachmentSchema attachmentsApiGetAttachment(attachmentId)

Get Attachment

Get a specific attachment by ID

### Example

```ts
import {
  Configuration,
  AttachmentsApi,
} from '';
import type { AttachmentsApiGetAttachmentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AttachmentsApi();

  const body = {
    // string
    attachmentId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies AttachmentsApiGetAttachmentRequest;

  try {
    const data = await api.attachmentsApiGetAttachment(body);
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
| **attachmentId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**AttachmentSchema**](AttachmentSchema.md)

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

## attachmentsApiGetContentType

> ContentTypeSchema attachmentsApiGetContentType(appLabel, model)

Get Content Type

Get content type ID for a given app and model

### Example

```ts
import { Configuration, AttachmentsApi } from "";
import type { AttachmentsApiGetContentTypeRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const api = new AttachmentsApi();

    const body = {
        // string
        appLabel: appLabel_example,
        // string
        model: model_example,
    } satisfies AttachmentsApiGetContentTypeRequest;

    try {
        const data = await api.attachmentsApiGetContentType(body);
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
| **appLabel** | `string` |             | [Defaults to `undefined`] |
| **model**    | `string` |             | [Defaults to `undefined`] |

### Return type

[**ContentTypeSchema**](ContentTypeSchema.md)

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

## attachmentsApiListAttachments

> PagedAttachmentSchema attachmentsApiListAttachments(contentTypeId, objectId, search, page, pageSize)

List Attachments

List all attachments (non-deleted) with filtering

### Example

```ts
import {
  Configuration,
  AttachmentsApi,
} from '';
import type { AttachmentsApiListAttachmentsRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AttachmentsApi();

  const body = {
    // number (optional)
    contentTypeId: 56,
    // string (optional)
    objectId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // string (optional)
    search: search_example,
    // number (optional)
    page: 56,
    // number (optional)
    pageSize: 56,
  } satisfies AttachmentsApiListAttachmentsRequest;

  try {
    const data = await api.attachmentsApiListAttachments(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name              | Type     | Description | Notes                                |
| ----------------- | -------- | ----------- | ------------------------------------ |
| **contentTypeId** | `number` |             | [Optional] [Defaults to `undefined`] |
| **objectId**      | `string` |             | [Optional] [Defaults to `undefined`] |
| **search**        | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**          | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize**      | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedAttachmentSchema**](PagedAttachmentSchema.md)

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

## attachmentsApiUpdateAttachment

> AttachmentSchema attachmentsApiUpdateAttachment(attachmentId, attachmentUpdateSchema)

Update Attachment

Update an attachment

### Example

```ts
import {
  Configuration,
  AttachmentsApi,
} from '';
import type { AttachmentsApiUpdateAttachmentRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new AttachmentsApi();

  const body = {
    // string
    attachmentId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // AttachmentUpdateSchema
    attachmentUpdateSchema: ...,
  } satisfies AttachmentsApiUpdateAttachmentRequest;

  try {
    const data = await api.attachmentsApiUpdateAttachment(body);
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
| **attachmentId**           | `string`                                            |             | [Defaults to `undefined`] |
| **attachmentUpdateSchema** | [AttachmentUpdateSchema](AttachmentUpdateSchema.md) |             |                           |

### Return type

[**AttachmentSchema**](AttachmentSchema.md)

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

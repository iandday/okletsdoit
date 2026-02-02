# ContactsApi

All URIs are relative to _http://localhost_

| Method                                                                  | HTTP request                                   | Description    |
| ----------------------------------------------------------------------- | ---------------------------------------------- | -------------- |
| [**contactsApiCreateContact**](ContactsApi.md#contactsapicreatecontact) | **POST** /api/contacts/contacts                | Create Contact |
| [**contactsApiDeleteContact**](ContactsApi.md#contactsapideletecontact) | **DELETE** /api/contacts/contacts/{contact_id} | Delete Contact |
| [**contactsApiGetContact**](ContactsApi.md#contactsapigetcontact)       | **GET** /api/contacts/contacts/{contact_id}    | Get Contact    |
| [**contactsApiListContacts**](ContactsApi.md#contactsapilistcontacts)   | **GET** /api/contacts/contacts                 | List Contacts  |
| [**contactsApiUpdateContact**](ContactsApi.md#contactsapiupdatecontact) | **PUT** /api/contacts/contacts/{contact_id}    | Update Contact |

## contactsApiCreateContact

> ContactSchema contactsApiCreateContact(contactCreateSchema)

Create Contact

Create a new contact

### Example

```ts
import {
  Configuration,
  ContactsApi,
} from '';
import type { ContactsApiCreateContactRequest } from '';

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
  const api = new ContactsApi(config);

  const body = {
    // ContactCreateSchema
    contactCreateSchema: ...,
  } satisfies ContactsApiCreateContactRequest;

  try {
    const data = await api.contactsApiCreateContact(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                    | Type                                          | Description | Notes |
| ----------------------- | --------------------------------------------- | ----------- | ----- |
| **contactCreateSchema** | [ContactCreateSchema](ContactCreateSchema.md) |             |       |

### Return type

[**ContactSchema**](ContactSchema.md)

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

## contactsApiDeleteContact

> contactsApiDeleteContact(contactId)

Delete Contact

Soft delete a contact

### Example

```ts
import {
  Configuration,
  ContactsApi,
} from '';
import type { ContactsApiDeleteContactRequest } from '';

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
  const api = new ContactsApi(config);

  const body = {
    // string
    contactId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ContactsApiDeleteContactRequest;

  try {
    const data = await api.contactsApiDeleteContact(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name          | Type     | Description | Notes                     |
| ------------- | -------- | ----------- | ------------------------- |
| **contactId** | `string` |             | [Defaults to `undefined`] |

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

## contactsApiGetContact

> ContactSchema contactsApiGetContact(contactId)

Get Contact

Get a specific contact by ID

### Example

```ts
import {
  Configuration,
  ContactsApi,
} from '';
import type { ContactsApiGetContactRequest } from '';

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
  const api = new ContactsApi(config);

  const body = {
    // string
    contactId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ContactsApiGetContactRequest;

  try {
    const data = await api.contactsApiGetContact(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name          | Type     | Description | Notes                     |
| ------------- | -------- | ----------- | ------------------------- |
| **contactId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**ContactSchema**](ContactSchema.md)

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

## contactsApiListContacts

> PagedContactSchema contactsApiListContacts(category, search, page, pageSize)

List Contacts

List all contacts (non-deleted) with filtering

### Example

```ts
import { Configuration, ContactsApi } from "";
import type { ContactsApiListContactsRequest } from "";

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
    const api = new ContactsApi(config);

    const body = {
        // string (optional)
        category: category_example,
        // string (optional)
        search: search_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies ContactsApiListContactsRequest;

    try {
        const data = await api.contactsApiListContacts(body);
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
| **category** | `string` |             | [Optional] [Defaults to `undefined`] |
| **search**   | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**     | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize** | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedContactSchema**](PagedContactSchema.md)

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

## contactsApiUpdateContact

> ContactSchema contactsApiUpdateContact(contactId, contactUpdateSchema)

Update Contact

Update a contact

### Example

```ts
import {
  Configuration,
  ContactsApi,
} from '';
import type { ContactsApiUpdateContactRequest } from '';

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
  const api = new ContactsApi(config);

  const body = {
    // string
    contactId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // ContactUpdateSchema
    contactUpdateSchema: ...,
  } satisfies ContactsApiUpdateContactRequest;

  try {
    const data = await api.contactsApiUpdateContact(body);
    console.log(data);
  } catch (error) {
    console.error(error);
  }
}

// Run the test
example().catch(console.error);
```

### Parameters

| Name                    | Type                                          | Description | Notes                     |
| ----------------------- | --------------------------------------------- | ----------- | ------------------------- |
| **contactId**           | `string`                                      |             | [Defaults to `undefined`] |
| **contactUpdateSchema** | [ContactUpdateSchema](ContactUpdateSchema.md) |             |                           |

### Return type

[**ContactSchema**](ContactSchema.md)

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

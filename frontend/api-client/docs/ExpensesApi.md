# ExpensesApi

All URIs are relative to _http://localhost_

| Method                                                                    | HTTP request                                      | Description     |
| ------------------------------------------------------------------------- | ------------------------------------------------- | --------------- |
| [**expensesApiCreateCategory**](ExpensesApi.md#expensesapicreatecategory) | **POST** /api/expenses/categories                 | Create Category |
| [**expensesApiCreateExpense**](ExpensesApi.md#expensesapicreateexpense)   | **POST** /api/expenses/expenses                   | Create Expense  |
| [**expensesApiDeleteCategory**](ExpensesApi.md#expensesapideletecategory) | **DELETE** /api/expenses/categories/{category_id} | Delete Category |
| [**expensesApiDeleteExpense**](ExpensesApi.md#expensesapideleteexpense)   | **DELETE** /api/expenses/expenses/{expense_id}    | Delete Expense  |
| [**expensesApiGetCategory**](ExpensesApi.md#expensesapigetcategory)       | **GET** /api/expenses/categories/{category_id}    | Get Category    |
| [**expensesApiGetExpense**](ExpensesApi.md#expensesapigetexpense)         | **GET** /api/expenses/expenses/{expense_id}       | Get Expense     |
| [**expensesApiListCategories**](ExpensesApi.md#expensesapilistcategories) | **GET** /api/expenses/categories                  | List Categories |
| [**expensesApiListExpenses**](ExpensesApi.md#expensesapilistexpenses)     | **GET** /api/expenses/expenses                    | List Expenses   |
| [**expensesApiUpdateCategory**](ExpensesApi.md#expensesapiupdatecategory) | **PUT** /api/expenses/categories/{category_id}    | Update Category |
| [**expensesApiUpdateExpense**](ExpensesApi.md#expensesapiupdateexpense)   | **PUT** /api/expenses/expenses/{expense_id}       | Update Expense  |

## expensesApiCreateCategory

> CategorySchema expensesApiCreateCategory(categoryCreateSchema)

Create Category

Create a new category

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiCreateCategoryRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // CategoryCreateSchema
    categoryCreateSchema: ...,
  } satisfies ExpensesApiCreateCategoryRequest;

  try {
    const data = await api.expensesApiCreateCategory(body);
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
| **categoryCreateSchema** | [CategoryCreateSchema](CategoryCreateSchema.md) |             |       |

### Return type

[**CategorySchema**](CategorySchema.md)

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

## expensesApiCreateExpense

> ExpenseSchema expensesApiCreateExpense(expenseCreateSchema)

Create Expense

Create a new expense

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiCreateExpenseRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // ExpenseCreateSchema
    expenseCreateSchema: ...,
  } satisfies ExpensesApiCreateExpenseRequest;

  try {
    const data = await api.expensesApiCreateExpense(body);
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
| **expenseCreateSchema** | [ExpenseCreateSchema](ExpenseCreateSchema.md) |             |       |

### Return type

[**ExpenseSchema**](ExpenseSchema.md)

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

## expensesApiDeleteCategory

> expensesApiDeleteCategory(categoryId)

Delete Category

Soft delete a category

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiDeleteCategoryRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // string
    categoryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ExpensesApiDeleteCategoryRequest;

  try {
    const data = await api.expensesApiDeleteCategory(body);
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
| **categoryId** | `string` |             | [Defaults to `undefined`] |

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

## expensesApiDeleteExpense

> expensesApiDeleteExpense(expenseId)

Delete Expense

Soft delete an expense

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiDeleteExpenseRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // string
    expenseId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ExpensesApiDeleteExpenseRequest;

  try {
    const data = await api.expensesApiDeleteExpense(body);
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
| **expenseId** | `string` |             | [Defaults to `undefined`] |

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

## expensesApiGetCategory

> CategorySchema expensesApiGetCategory(categoryId)

Get Category

Get a specific category by ID

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiGetCategoryRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // string
    categoryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ExpensesApiGetCategoryRequest;

  try {
    const data = await api.expensesApiGetCategory(body);
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
| **categoryId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**CategorySchema**](CategorySchema.md)

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

## expensesApiGetExpense

> ExpenseSchema expensesApiGetExpense(expenseId)

Get Expense

Get a specific expense by ID

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiGetExpenseRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // string
    expenseId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies ExpensesApiGetExpenseRequest;

  try {
    const data = await api.expensesApiGetExpense(body);
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
| **expenseId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**ExpenseSchema**](ExpenseSchema.md)

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

## expensesApiListCategories

> PagedCategorySchema expensesApiListCategories(name, page, pageSize)

List Categories

List all categories (non-deleted)

### Example

```ts
import { Configuration, ExpensesApi } from "";
import type { ExpensesApiListCategoriesRequest } from "";

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
    const api = new ExpensesApi(config);

    const body = {
        // string (optional)
        name: name_example,
        // number (optional)
        page: 56,
        // number (optional)
        pageSize: 56,
    } satisfies ExpensesApiListCategoriesRequest;

    try {
        const data = await api.expensesApiListCategories(body);
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

[**PagedCategorySchema**](PagedCategorySchema.md)

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

## expensesApiListExpenses

> PagedExpenseSchema expensesApiListExpenses(item, categoryId, vendorId, page, pageSize)

List Expenses

List all expenses (non-deleted)

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiListExpensesRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // string (optional)
    item: item_example,
    // string (optional)
    categoryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // string (optional)
    vendorId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // number (optional)
    page: 56,
    // number (optional)
    pageSize: 56,
  } satisfies ExpensesApiListExpensesRequest;

  try {
    const data = await api.expensesApiListExpenses(body);
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
| **item**       | `string` |             | [Optional] [Defaults to `undefined`] |
| **categoryId** | `string` |             | [Optional] [Defaults to `undefined`] |
| **vendorId**   | `string` |             | [Optional] [Defaults to `undefined`] |
| **page**       | `number` |             | [Optional] [Defaults to `1`]         |
| **pageSize**   | `number` |             | [Optional] [Defaults to `undefined`] |

### Return type

[**PagedExpenseSchema**](PagedExpenseSchema.md)

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

## expensesApiUpdateCategory

> CategorySchema expensesApiUpdateCategory(categoryId, categoryUpdateSchema)

Update Category

Update a category

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiUpdateCategoryRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // string
    categoryId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // CategoryUpdateSchema
    categoryUpdateSchema: ...,
  } satisfies ExpensesApiUpdateCategoryRequest;

  try {
    const data = await api.expensesApiUpdateCategory(body);
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
| **categoryId**           | `string`                                        |             | [Defaults to `undefined`] |
| **categoryUpdateSchema** | [CategoryUpdateSchema](CategoryUpdateSchema.md) |             |                           |

### Return type

[**CategorySchema**](CategorySchema.md)

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

## expensesApiUpdateExpense

> ExpenseSchema expensesApiUpdateExpense(expenseId, expenseUpdateSchema)

Update Expense

Update an expense

### Example

```ts
import {
  Configuration,
  ExpensesApi,
} from '';
import type { ExpensesApiUpdateExpenseRequest } from '';

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
  const api = new ExpensesApi(config);

  const body = {
    // string
    expenseId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
    // ExpenseUpdateSchema
    expenseUpdateSchema: ...,
  } satisfies ExpensesApiUpdateExpenseRequest;

  try {
    const data = await api.expensesApiUpdateExpense(body);
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
| **expenseId**           | `string`                                      |             | [Defaults to `undefined`] |
| **expenseUpdateSchema** | [ExpenseUpdateSchema](ExpenseUpdateSchema.md) |             |                           |

### Return type

[**ExpenseSchema**](ExpenseSchema.md)

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

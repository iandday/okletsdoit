# CoreApi

All URIs are relative to _http://localhost_

| Method                                                                      | HTTP request                       | Description             |
| --------------------------------------------------------------------------- | ---------------------------------- | ----------------------- |
| [**coreApiGetWeddingSettings**](CoreApi.md#coreapigetweddingsettings)       | **GET** /api/core/wedding-settings | Get Wedding Settings    |
| [**coreApiUpdateWeddingSettings**](CoreApi.md#coreapiupdateweddingsettings) | **PUT** /api/core/wedding-settings | Update Wedding Settings |

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
    const api = new CoreApi();

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

No authorization required

### HTTP request headers

- **Content-Type**: Not defined
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
  const api = new CoreApi();

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

No authorization required

### HTTP request headers

- **Content-Type**: `application/json`
- **Accept**: `application/json`

### HTTP response details

| Status code | Description | Response headers |
| ----------- | ----------- | ---------------- |
| **200**     | OK          | -                |

[[Back to top]](#) [[Back to API list]](../README.md#api-endpoints) [[Back to Model list]](../README.md#models) [[Back to README]](../README.md)

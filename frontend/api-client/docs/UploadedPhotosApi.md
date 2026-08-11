# UploadedPhotosApi

All URIs are relative to _http://localhost_

| Method                                                                                    | HTTP request                                      | Description              |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------- | ------------------------ |
| [**photosApiCompleteUploadedPhoto**](UploadedPhotosApi.md#photosapicompleteuploadedphoto) | **POST** /api/photos/uploaded/{photo_id}/complete | Complete Uploaded Photo  |
| [**photosApiCreateUploadedPhoto**](UploadedPhotosApi.md#photosapicreateuploadedphoto)     | **POST** /api/photos/create                       | Create Uploaded Photo    |
| [**photosApiDownloadUploadedPhoto**](UploadedPhotosApi.md#photosapidownloaduploadedphoto) | **GET** /api/photos/uploaded/{photo_id}/download  | Download Uploaded Photo  |
| [**photosApiListAllUploadedPhotos**](UploadedPhotosApi.md#photosapilistalluploadedphotos) | **GET** /api/photos/all                           | List All Uploaded Photos |
| [**photosApiListUploadedPhotos**](UploadedPhotosApi.md#photosapilistuploadedphotos)       | **GET** /api/photos/list                          | List Uploaded Photos     |

## photosApiCompleteUploadedPhoto

> CompleteUploadedPhotoResponseSchema photosApiCompleteUploadedPhoto(photoId)

Complete Uploaded Photo

Process the uploaded photo

### Example

```ts
import {
  Configuration,
  UploadedPhotosApi,
} from '';
import type { PhotosApiCompleteUploadedPhotoRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UploadedPhotosApi();

  const body = {
    // string
    photoId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies PhotosApiCompleteUploadedPhotoRequest;

  try {
    const data = await api.photosApiCompleteUploadedPhoto(body);
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
| **photoId** | `string` |             | [Defaults to `undefined`] |

### Return type

[**CompleteUploadedPhotoResponseSchema**](CompleteUploadedPhotoResponseSchema.md)

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

## photosApiCreateUploadedPhoto

> CreateUploadedPhotoResponseSchema photosApiCreateUploadedPhoto()

Create Uploaded Photo

Create a pending uploaded-photo record and return a presigned upload URL.

### Example

```ts
import { Configuration, UploadedPhotosApi } from "";
import type { PhotosApiCreateUploadedPhotoRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const api = new UploadedPhotosApi();

    try {
        const data = await api.photosApiCreateUploadedPhoto();
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

[**CreateUploadedPhotoResponseSchema**](CreateUploadedPhotoResponseSchema.md)

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

## photosApiDownloadUploadedPhoto

> photosApiDownloadUploadedPhoto(photoId)

Download Uploaded Photo

Return a short-lived attachment URL for downloading a photo file.

### Example

```ts
import {
  Configuration,
  UploadedPhotosApi,
} from '';
import type { PhotosApiDownloadUploadedPhotoRequest } from '';

async function example() {
  console.log("🚀 Testing  SDK...");
  const api = new UploadedPhotosApi();

  const body = {
    // string
    photoId: 38400000-8cf0-11bd-b23e-10b96e4ef00d,
  } satisfies PhotosApiDownloadUploadedPhotoRequest;

  try {
    const data = await api.photosApiDownloadUploadedPhoto(body);
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
| **photoId** | `string` |             | [Defaults to `undefined`] |

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

## photosApiListAllUploadedPhotos

> Array&lt;UploadedPhotoSchema&gt; photosApiListAllUploadedPhotos()

List All Uploaded Photos

List all uploaded photos, including those not approved.

### Example

```ts
import { Configuration, UploadedPhotosApi } from "";
import type { PhotosApiListAllUploadedPhotosRequest } from "";

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
    const api = new UploadedPhotosApi(config);

    try {
        const data = await api.photosApiListAllUploadedPhotos();
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

[**Array&lt;UploadedPhotoSchema&gt;**](UploadedPhotoSchema.md)

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

## photosApiListUploadedPhotos

> Array&lt;UploadedPhotoSchema&gt; photosApiListUploadedPhotos()

List Uploaded Photos

List all uploaded photos.

### Example

```ts
import { Configuration, UploadedPhotosApi } from "";
import type { PhotosApiListUploadedPhotosRequest } from "";

async function example() {
    console.log("🚀 Testing  SDK...");
    const api = new UploadedPhotosApi();

    try {
        const data = await api.photosApiListUploadedPhotos();
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

[**Array&lt;UploadedPhotoSchema&gt;**](UploadedPhotoSchema.md)

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

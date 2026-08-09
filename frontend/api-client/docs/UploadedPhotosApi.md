# UploadedPhotosApi

All URIs are relative to _http://localhost_

| Method                                                                                    | HTTP request                                      | Description             |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------- | ----------------------- |
| [**photosApiCompleteUploadedPhoto**](UploadedPhotosApi.md#photosapicompleteuploadedphoto) | **POST** /api/photos/uploaded/{photo_id}/complete | Complete Uploaded Photo |
| [**photosApiCreateUploadedPhoto**](UploadedPhotosApi.md#photosapicreateuploadedphoto)     | **POST** /api/photos/create                       | Create Uploaded Photo   |
| [**photosApiListUploadedPhotos**](UploadedPhotosApi.md#photosapilistuploadedphotos)       | **GET** /api/photos/list                          | List Uploaded Photos    |

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

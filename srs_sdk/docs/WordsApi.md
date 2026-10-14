# srs_sdk.WordsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_word_words_post**](WordsApi.md#create_word_words_post) | **POST** /words/ | Create Word
[**delete_word_words_word_id_delete**](WordsApi.md#delete_word_words_word_id_delete) | **DELETE** /words/{word_id} | Delete Word
[**get_due_words_words_due_get**](WordsApi.md#get_due_words_words_due_get) | **GET** /words/due/ | Get Due Words


# **create_word_words_post**
> WordOut create_word_words_post(word_create)

Create Word

### Example


```python
import srs_sdk
from srs_sdk.models.word_create import WordCreate
from srs_sdk.models.word_out import WordOut
from srs_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = srs_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with srs_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = srs_sdk.WordsApi(api_client)
    word_create = srs_sdk.WordCreate() # WordCreate | 

    try:
        # Create Word
        api_response = api_instance.create_word_words_post(word_create)
        print("The response of WordsApi->create_word_words_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WordsApi->create_word_words_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **word_create** | [**WordCreate**](WordCreate.md)|  | 

### Return type

[**WordOut**](WordOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_word_words_word_id_delete**
> delete_word_words_word_id_delete(word_id)

Delete Word

### Example


```python
import srs_sdk
from srs_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = srs_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with srs_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = srs_sdk.WordsApi(api_client)
    word_id = 56 # int | 

    try:
        # Delete Word
        api_instance.delete_word_words_word_id_delete(word_id)
    except Exception as e:
        print("Exception when calling WordsApi->delete_word_words_word_id_delete: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **word_id** | **int**|  | 

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_due_words_words_due_get**
> List[WordProgress] get_due_words_words_due_get()

Get Due Words

### Example


```python
import srs_sdk
from srs_sdk.models.word_progress import WordProgress
from srs_sdk.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = srs_sdk.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with srs_sdk.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = srs_sdk.WordsApi(api_client)

    try:
        # Get Due Words
        api_response = api_instance.get_due_words_words_due_get()
        print("The response of WordsApi->get_due_words_words_due_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling WordsApi->get_due_words_words_due_get: %s\n" % e)
```



### Parameters

This endpoint does not need any parameter.

### Return type

[**List[WordProgress]**](WordProgress.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)


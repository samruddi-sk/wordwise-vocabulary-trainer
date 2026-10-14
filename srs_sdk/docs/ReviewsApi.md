# srs_sdk.ReviewsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_history_words_history_get**](ReviewsApi.md#get_history_words_history_get) | **GET** /words/history/ | Get History
[**review_word_words_word_id_review_post**](ReviewsApi.md#review_word_words_word_id_review_post) | **POST** /words/{word_id}/review/ | Review Word


# **get_history_words_history_get**
> HistoryOut get_history_words_history_get(limit=limit)

Get History

### Example


```python
import srs_sdk
from srs_sdk.models.history_out import HistoryOut
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
    api_instance = srs_sdk.ReviewsApi(api_client)
    limit = 100 # int |  (optional) (default to 100)

    try:
        # Get History
        api_response = api_instance.get_history_words_history_get(limit=limit)
        print("The response of ReviewsApi->get_history_words_history_get:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->get_history_words_history_get: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **limit** | **int**|  | [optional] [default to 100]

### Return type

[**HistoryOut**](HistoryOut.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful Response |  -  |
**422** | Validation Error |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **review_word_words_word_id_review_post**
> ReviewOut review_word_words_word_id_review_post(word_id, review_create)

Review Word

### Example


```python
import srs_sdk
from srs_sdk.models.review_create import ReviewCreate
from srs_sdk.models.review_out import ReviewOut
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
    api_instance = srs_sdk.ReviewsApi(api_client)
    word_id = 56 # int | 
    review_create = srs_sdk.ReviewCreate() # ReviewCreate | 

    try:
        # Review Word
        api_response = api_instance.review_word_words_word_id_review_post(word_id, review_create)
        print("The response of ReviewsApi->review_word_words_word_id_review_post:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ReviewsApi->review_word_words_word_id_review_post: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **word_id** | **int**|  | 
 **review_create** | [**ReviewCreate**](ReviewCreate.md)|  | 

### Return type

[**ReviewOut**](ReviewOut.md)

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


# WordProgress


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **int** |  | 
**word** | **str** |  | 
**definition** | **str** |  | 
**language** | **str** |  | 
**created_at** | **datetime** |  | 
**last_score** | **int** |  | [optional] 
**interval** | **int** |  | [optional] [default to 0]
**easiness_factor** | **float** |  | [optional] [default to 2.5]
**repetition** | **int** |  | [optional] [default to 0]
**next_review** | **datetime** |  | [optional] 
**is_due** | **bool** |  | [optional] [default to True]

## Example

```python
from srs_sdk.models.word_progress import WordProgress

# TODO update the JSON string below
json = "{}"
# create an instance of WordProgress from a JSON string
word_progress_instance = WordProgress.from_json(json)
# print the JSON string representation of the object
print(WordProgress.to_json())

# convert the object into a dict
word_progress_dict = word_progress_instance.to_dict()
# create an instance of WordProgress from a dict
word_progress_from_dict = WordProgress.from_dict(word_progress_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)



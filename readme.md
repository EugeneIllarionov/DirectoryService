# Directory REST API example
# All request use GET method only

# Quick api guide
| http request | Result data | status codes | Params |
| ------ | ------ | ------ | ------ |
| http://127.0.0.1:8000/api/dir/            | dir list  | 200 - OK      | actual_on={%Y-%m-%d}      | 
| http://127.0.0.1:8000/api/dir/{id}/       | dir info  | 200 - OK, 404 - no directory with this id |
| http://127.0.0.1:8000/api/dir/{id}/items/ | item list | 200 - OK, 204 - no items with this params, 404 Not Found dir with this id or/and version | version={directory_verison}, value={item_value}, code={item_code}|


# Detailed example using api with curl

### To get list of all dirs:
```bash
curl -i -H "Accept: application/json" http://127.0.0.1:8000/api/dir/
```
status HTTP 200 OK
result data:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 4,
            "name": "some dir name",
            "short_name": "sdn",
            "description": "sdn desc",
            "last_version": "1.1",
            "current_version": "1.1",
            "version_count": 2
        },
        {
            "id": 5,
            "name": "some dir name 2",
            "short_name": "sdn 2",
            "description": "sdn 2 desc",
            "last_version": "1.1",
            "current_version": "1.0",
            "version_count": 3
        }
    ]
}
```
### To get a list of directories relevant for a specific date:

```bash
$ curl -i -H "Accept: application/json" http://127.0.0.1:8000/api/dir/?actual_on=2021-10-10
```
where 2021-10-10 relevant date in format "%Y-%m-%d"

### To get items of dir current version:
```bash
curl -i -H "Accept: application/json" http://127.0.0.1:8000/api/dir/5/items/
```
where 5 is dir id
result data:
```json
{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [{"code": "1","value": "1"},{ "code": "2","value": "2"}]
}
```

### To get items of current version dir:
```bash
curl -i -H "Accept: application/json" http://127.0.0.1:8000/api/dir/5/items/?version=1.0
```
where 1.0 is version of dir

### To validate or find items in dirs:
To do this you must add to request code={item_code} or/and value={item_value}
if there is no item with this code or/and value in the dictionary status will be 204 - No Content
example of finding by value:
```bash
curl -i -H "Accept: application/json" http://127.0.0.1:8000/api/dir/5/items/?value=5055
```
status HTTP 204 No Content

### example of finding by value and code
```bash
curl -i -H "Accept: application/json" http://127.0.0.1:8000/api/dir/5/items/?value=1&code=1
```
status HTTP 200 OK
result data:
```json
{
"count":1,
"next":null,
"previous":null,
"results":[{"code":"1","value":"1"}]
}
```

### example of finding items by value and code in specific dirictory version
```bash
curl -i -H "Accept: application/json" http://127.0.0.1:8000/api/dir/4/items/?version=1.1&code=2&value=22
```
status HTTP 200 OK
result data:
```json
{
"count":1,
"next":null,
"previous":null,
"results": [{"code": "2","value": "22"}]
}
```

result data limited by 10 elements in list per page to get another page add to request ?page={page_number}

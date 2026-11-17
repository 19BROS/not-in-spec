# Items API

The Items API lists and creates items. Requests and responses use JSON.

## List items

Use `GET /items`. The optional query parameter `limit` must be between 1 and 100.

## Create an item

Use `POST /items` with the required string field `name` in the body.

```sh
curl -X POST https://example.invalid/items \
  -H 'Content-Type: application/json' \
  -d '{"name":"Notebook"}'
```

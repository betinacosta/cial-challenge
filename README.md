# cial-challenge


## Decisions
- File structure: Structuring based on File-Type

## Assumptions
- The `stock_symbol` is an id like identifier.
- The `amount` is the `purchased_amount` in the stock model.
- The [POST] endpoint requested at the assignment should be a PUT ou even a PATCH as it updates an existent
record. In case the record related to the stock_symbol doesn't exist, it will create a new one and return `201`.
If it updates an existent record, with will return a `200` as it the [REST API convention](https://restfulapi.net/http-methods/).
- 
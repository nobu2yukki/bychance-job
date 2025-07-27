GET /

PUT /library/_doc/2
{
  "title": "金田と田中",
  "name": {
    "first": "Kanada",
    "last": "yuro"
  },
  "publish_date": "2002-08-11T00:00:00+0900",
  "price": 19.95
}

GET /library/_mget
{
  "docs": [
    { "_id": "1" },
    { "_id": "2" }
  ]
}
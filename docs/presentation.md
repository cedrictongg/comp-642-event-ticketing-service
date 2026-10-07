# Swagger Presentation and End-to-End Test

Go to http://localhost:8000/docs for Swagger docs. 
- Start everything from scratch by doing `docker compose down -v --remove-orphans`.
- Do `docker compose up -d --build` and verify services are up through `docker compose ps`.

API Health can also be verified at the bottom through `System GET /health`

## 1. Browse events — MySQL

Execute `GET /events`.
Expected: 200 and event listings containing IDs, titles, dates, and venue names.

## 2. View seeded event — MySQL + MongoDB + Redis
Execute `GET /events/{event_id}` with event_id = 1.
Expected: 200, source = database, relational event/venue/inventory fields, and non-null content including descriptions, tags, or reviews.

## 3. Repeat event details — Redis cache hit
Execute the same request again, before the 120-second TTL expires.
Expected: source = redis and the same event payload.

## 4. Trending — Redis
Execute `GET /trending`.
Expected: at most ten ranked event IDs/scores. Event 1's score increases for both detail requests; it need not equal 2 because prior views remain.

## 5. Create user — MySQL
Execute `POST /users/{f_name}/{l_name}` with f_name = Demo and l_name = Presenter.
Expected: success and returned userID. Record this as USER_ID. This is the current route, not POST /users with a JSON body.

## 6. Create event — MySQL
Execute `POST /admin/events` with:

```json
{
  "title": "Demo Community Workshop",
  "datetime": "2027-11-15 10:00:00",
  "venueId": 1
}
```
Expected: 201 and eventId. Record this as EVENT_ID.
Response body:
```json
{
  "eventId": 14,
  "message": "Event created"
}
```

## 7. Assign type — MySQL
Execute `POST /admin/events/{event_id}/tickets` using EVENT_ID and:

```json
{"ticket_type": "Workshops and Classes"}
```

Expected: 201. The value must already exist in TICKET_TYPES. A repeated assignment may return 400.

Response body:
```json
{
  "event_id": 1,
  "ticket_type": "Workshops and Classes"
}
```

Execute `GET /events/{event_id}` for EVENT_ID. Expect the assigned type after a cache miss. New events may have content = null because event creation does not insert MongoDB content.

## 8. Update event and verify invalidation
Request the new event twice first to populate its cache and confirm source = redis.

Execute `PUT /admin/events/{event_id}` using EVENT_ID and:

```json
{
  "title": "Updated Demo Community Workshop",
  "datetime": "2027-11-16 11:00:00",
  "venueId": 1
}
```

Expected: 200. Then GET the event again. Expect source = database and updated fields.
Response body
```json
{
  "eventId": 1,
  "message": "Event updated"
}
```

## 9. Create unpaid order and inspect history

Execute `GET /admin/events/{event_id}/inventory` for EVENT_ID. Record the starting inventory.

Execute `POST /orders`. Replace USER_ID and EVENT_ID below with numbers, not quoted strings:

```json
{
  "userId": 123,
  "orderItems": [
    {"eventId": 456, "ticketPrice": 25.00}
  ]
}
```

Here 123 and 456 are placeholders. Omit balance, status, and orderCreated so defaults are used.

Expected: returned orderId. Record ORDER_ID. Current implementation creates an unpaid order; do not claim payment processing occurred.

Execute:

- `GET /orders/{order_id}` with ORDER_ID.
- `GET /orders/{order_id}/items` with ORDER_ID.
- `GET /users/{user_id}/orders` with USER_ID.
- `GET /admin/events/{event_id}/inventory` with EVENT_ID.

Expected: matching order/item, history entry, and one fewer available seat. If event details remain stale but admin inventory changes, purchase cache invalidation is missing: record a failure rather than hiding it.

## 10. Admin activity and sales

Execute `GET /admin/events/{event_id}/activity` with EVENT_ID.

Expected: title, ticketsSold, orderValue, views. For one successful 25.00 item, ticketsSold = 1 and orderValue = 25.00 (formatting may differ).

Execute `GET /admin/events/{event_id}/sales` with EVENT_ID.

Expected: sales totals, tickets sold, venue capacity, sell-through. Compare with inventory/activity.

## 11. Review feature

Execute `POST /events/{event_id}/reviews`.

```json
{
  "userId": 0,
  "rating": 1,
  "comment": "Great!"
}
```

Expected response body:
```json
{
  "message": "Review added",
  "eventId": 1,
  "review": {
    "userId": 0,
    "rating": 1,
    "comment": "Great!"
  }
}
```

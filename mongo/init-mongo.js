db = db.getSiblingDB("event_ticketing");
db.createCollection("event_content");

db.event_content.createIndex(
  { eventId: 1 },
  {
    unique: true,
    name: "ux_event_content_event_id"
  }
);
print("MongoDB initialization placeholder completed.");
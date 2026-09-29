db = db.getSiblingDB("event_ticketing");
db.createCollection("event_content");

db.event_content.createIndex(
  { eventId: 1 },
  {
    unique: true,
    name: "ux_event_content_event_id"
  }
);

db.event_content.insertMany([
  {
    eventId: 1,
    description: "Annual technical conference covering modern backend engineering, distributed databases, and production machine learning deployments.",
    performerList: ["Tom Jacobs", "Dr. Ellen Vance", "Dr. Patel"],
    ageRestriction: "All Ages",
    venueDetails: {
      parkingInfo: "West Structure parking $20/day with validation at check-in",
      accessibility: "Ramp access at South Entrance, elevators to level 2 breakout rooms",
      securityPolicy: "Bags subject to search at entry. Laptops and phones allowed."
    },
    tags: ["technology", "software-engineering", "data-systems"],
    reviews: [
      { userId: 1042, rating: 5, comment: "The architecture session on microservices alone was worth the ticket." },
      { userId: 8819, rating: 4, comment: "Good content overall, but the wifi in Hall B was spotty." }
    ]
  },
  {
    eventId: 2,
    description: "Outdoor evening concert featuring electronic ambient and synth sets.",
    performerList: ["Ghost Signal", "K2 Soundworks"],
    ageRestriction: "18+",
    venueDetails: {
      parkingInfo: "On-site lot parking ($15 cash/card)",
      accessibility: "Designated ADA lawn section near main sound booth",
      securityPolicy: "Clear bags only. No outside alcohol or glass containers."
    },
    tags: ["live-music", "electronic", "outdoor"],
    reviews: [
      { userId: 3301, rating: 5, comment: "Sound design was incredible from the front section." }
    ]
  },
  {
    eventId: 3,
    description: "Main card MMA championship bouts featuring five scheduled fights.",
    performerList: ["Jonah Reyes", "Tariq Al-Mansoor"],
    ageRestriction: "21+",
    venueDetails: {
      parkingInfo: "Arena parking garage $25",
      accessibility: "Escalators and elevator access to upper concourse levels",
      securityPolicy: "Express metal detectors in effect. No weapons or professional cameras."
    },
    tags: ["mma", "combat-sports", "live-events"],
    reviews: []
  }
]);

print("MongoDB initialization completed successfully.");
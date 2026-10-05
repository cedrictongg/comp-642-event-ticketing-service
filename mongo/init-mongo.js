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
    description: "Iggy Pop live in concert delivering legendary punk and rock performances.",
    performerList: ["Iggy Pop"],
    ageRestriction: "18+",
    venueDetails: { parkingInfo: "West Structure parking $20/day", accessibility: "Ramp access at South Entrance", securityPolicy: "Bags subject to search." },
    tags: ["rock", "punk", "live-music"],
    reviews: [{ userId: 1042, rating: 5, comment: "Unbelievable energy on stage!" }]
  },
  {
    eventId: 2,
    description: "An intimate live music and comedy evening featuring John Stamos.",
    performerList: ["John Stamos"],
    ageRestriction: "All Ages",
    venueDetails: { parkingInfo: "On-site lot parking $15", accessibility: "Designated ADA lawn section", securityPolicy: "Clear bags only." },
    tags: ["live-music", "entertainment"],
    reviews: [{ userId: 8819, rating: 4, comment: "Great intimate show!" }]
  },
  {
    eventId: 3,
    description: "Live stand-up comedy performance by Dave Coulier.",
    performerList: ["Dave Coulier"],
    ageRestriction: "18+",
    venueDetails: { parkingInfo: "Arena parking garage $25", accessibility: "Elevator access to concourse", securityPolicy: "Metal detectors in effect." },
    tags: ["comedy", "stand-up"],
    reviews: []
  },
  {
    eventId: 4,
    description: "Regular season NBA basketball matchup between Golden State Warriors and LA Lakers.",
    performerList: ["Golden State Warriors", "Los Angeles Lakers"],
    ageRestriction: "All Ages",
    venueDetails: { parkingInfo: "VIP Lot A $40, Public Garage $25", accessibility: "ADA seating sections on lower and upper bowl", securityPolicy: "No backpacks permitted." },
    tags: ["sports", "nba", "basketball"],
    reviews: []
  },
  {
    eventId: 5,
    description: "Ariel Stink performing live set at Venue 6.",
    performerList: ["Ariel Stink"],
    ageRestriction: "21+",
    venueDetails: { parkingInfo: "Street parking available", accessibility: "Wheelchair accessible main floor", securityPolicy: "ID check at door." },
    tags: ["indie", "alternative", "live-music"],
    reviews: []
  },
  {
    eventId: 6,
    description: "Ariel Stink second show date at Venue 4.",
    performerList: ["Ariel Stink"],
    ageRestriction: "21+",
    venueDetails: { parkingInfo: "Structure B $15", accessibility: "Ramp and elevator available", securityPolicy: "Standard bag check." },
    tags: ["indie", "alternative", "live-music"],
    reviews: []
  },
  {
    eventId: 7,
    description: "Dave Matthews Sextet performing acoustic and jam sessions.",
    performerList: ["Dave Matthews Sextet"],
    ageRestriction: "All Ages",
    venueDetails: { parkingInfo: "Venue lot $20", accessibility: "ADA seating available", securityPolicy: "Clear bags only." },
    tags: ["jam-band", "acoustic", "rock"],
    reviews: []
  },
  {
    eventId: 8,
    description: "Annual technology, cloud, and AI development conference.",
    performerList: ["Keynote Speakers", "Tech Executives"],
    ageRestriction: "All Ages",
    venueDetails: { parkingInfo: "Convention center parking $30/day", accessibility: "Fully accessible facility", securityPolicy: "Conference badge required for entry." },
    tags: ["technology", "conference", "cloud"],
    reviews: []
  },
  {
    eventId: 9,
    description: "Interactive carpentry and woodworking workshop.",
    performerList: ["Master Craftsmen"],
    ageRestriction: "18+",
    venueDetails: { parkingInfo: "Free onsite parking", accessibility: "Ground level access", securityPolicy: "Safety goggles required." },
    tags: ["workshop", "crafts", "educational"],
    reviews: []
  },
  {
    eventId: 10,
    description: "Underground indie band Guck performing live.",
    performerList: ["Guck"],
    ageRestriction: "21+",
    venueDetails: { parkingInfo: "Street parking", accessibility: "Ground floor entry", securityPolicy: "21+ ID required." },
    tags: ["indie", "underground"],
    reviews: []
  },
  {
    eventId: 11,
    description: "Beach goth and garage rock concert featuring The Growlers.",
    performerList: ["The Growlers"],
    ageRestriction: "18+",
    venueDetails: { parkingInfo: "Valet $20, Lot $15", accessibility: "ADA platform available", securityPolicy: "Bags subject to search." },
    tags: ["rock", "garage-rock", "live-music"],
    reviews: []
  },
  {
    eventId: 12,
    description: "Live band performance by Rocket.",
    performerList: ["Rocket"],
    ageRestriction: "All Ages",
    venueDetails: { parkingInfo: "West Structure $20", accessibility: "Full accessibility", securityPolicy: "Standard check." },
    tags: ["rock", "live-music"],
    reviews: []
  },
  {
    eventId: 13,
    description: "Indie rock live set by Julie.",
    performerList: ["Julie"],
    ageRestriction: "All Ages",
    venueDetails: { parkingInfo: "On-site lot $15", accessibility: "ADA seating near booth", securityPolicy: "Clear bag policy." },
    tags: ["indie", "rock", "live-music"],
    reviews: []
  }
]);

print("MongoDB initialization completed successfully with 13 event records.");
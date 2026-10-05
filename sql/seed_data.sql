USE event_ticketing;

INSERT INTO USERS (USER_FNAME, USER_LNAME, ACCT_CREATED) VALUES
('John', 'Jacob', '2020-05-25 19:15:00'),
('John Jacob', 'Jingleheimerschmidt', '2020-01-25 19:15:00'),
('John Jacob', 'Jingleheimerschmidt', '2020-02-21 09:15:00'),
('Jorge', 'Guevira', '2022-02-22 19:15:00'),
('Michale', 'Fassbender', '2024-01-25 19:15:00');

INSERT INTO VENUES (VENUE_NAME, VENUE_CAPACITY) VALUES
('The Roxy', 400),
('Whiskey-a-Go-Go', 350),
('Zebulon', 400),
('Telegram Ballroom', 450),
('The Regent Theater', 600),
('The Observatory', 800),
('Los Angeles Convention Center', 22870),
('Non Plus Ultra', 200),
('Crypto.com Arena', 20000),
('Work Shop Workshop', 100);

INSERT INTO EVENTS (EVENT_TITLE, EVENT_DATETIME, VENUE_ID) VALUES
('Iggy Pop 2', '2026-05-25 20:00:00', 1),
('John Stamos Live', '2026-05-25 20:00:00', 2),
('Dave Coulier Live', '2026-05-25 20:00:00', 3),
('Golden State Warriors at Los Angeles Lakers', '2026-05-25 19:15:00', 9),
('Ariel Stink', '2026-05-27 20:00:00', 6),
('Ariel Stink', '2026-05-25 20:00:00', 4),
('Dave Matthews Sextet', '2026-05-25 20:00:00', 5),
('Dreamforce LA 2026', '2026-05-28 07:00:00', 7),
('Hammering with Hammers', '2026-05-20 10:00:00', 10),
('Guck', '2026-05-25 21:00:00', 8),
('The Growlers', '2026-05-20 19:00:00', 6),
('Rocket', '2026-06-25 20:00:00', 1),
('Julie', '2026-06-25 20:00:00', 2);

INSERT INTO TICKET_TYPES (TICKET_TYPE) VALUES
('Music'),
('Comedy and Entertainment'),
('Sports'),
('Business and Technology'),
('Workshops and Classes');

INSERT INTO TICKET_TYPE_ASSIGNMENTS (EVENT_ID, TICKET_TYPE) VALUES
-- MUSIC
(1, 'Music'),
(7, 'Music'),
(10, 'Music'),
(11, 'Music'),
-- COMEDY AND ENTERTAINMENT
(2, 'Comedy and Entertainment'),
(3, 'Comedy and Entertainment'),
(5, 'Comedy and Entertainment'),
(6, 'Comedy and Entertainment'),
(10, 'Comedy and Entertainment'),
(13, 'Comedy and Entertainment'),
-- SPORTS
(4,'Sports'),
-- BUSINESS AND TECHNOLOGY
(8, 'Business and Technology'),
(12, 'Business and Technology'),
-- WORKSHOP AND CLASSES
(9, 'Workshops and Classes');

INSERT INTO ORDERS (USER_ID) VALUES
(1),
(1),
(2),
(3),
(4);

INSERT INTO ORDER_ITEMS (ORDER_ID, EVENT_ID, TICKET_PRICE) VALUES
(1, 1, 50),
(2, 5, 50),
(3, 1, 50),
(3, 6, 45),
(3, 10, 20),
(4, 8, 200),
(5, 9, 15),
(5, 4, 700);

INSERT INTO PAYMENTS (ORDER_ID, PAYMENT_AMT) VALUES
(1, 50),
(2, 50),
(3, 100),
(5, 700);

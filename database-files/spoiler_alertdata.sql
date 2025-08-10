USE SpoilerAlert;

INSERT INTO users (userId, userName, name, email, age)
VALUES (1, 'user123', 'Alex Miller', 'alex.m@gmail.com', 28),
      (2, 'user579', 'Sophie Smith', 'sophie.s@gmail.com', 34),
      (3, 'user307', 'Ana Rodriguez', 'ana.rod@gmail.com', 22);


INSERT INTO recommendations (userId, rating)
VALUES (1, 4.5),
      (2, 2.0);


INSERT INTO shows (showID, title, rating, releaseDate, season, ageRating, streamingPlatform)
VALUES (10, 'The Rookie', 4.2, '2018-10-16', 7, 'TV-14', 'Hulu'),
      (11, 'Euphoria', 4.7, '2019-06-16', 2, 'TV-MA', 'HBO'),
      (12, 'Severance', 4.5, '2022-02-18', 2, 'TV-MA', 'Apple TV+');


INSERT INTO favorites (userId, showId)
VALUES (1, 10),
      (2, 11);


INSERT INTO directors (directorId, firstName, lastName, filmsMade, bio, socialMedia)
VALUES (100, 'Bong', 'Joon-ho', 12, 'Most known for Parasite.', '@bongjoonho'),
      (110, 'Sam', 'Levinson', 5, 'Most known for Euphoria.', '@samlevinson');


INSERT INTO reviews (writtenrevID, userId, showID, createdAt, rating, content)
VALUES (200, 1, 10, NOW(), 4.5, 'Great action and drama show!'),
      (210, 2, 11, NOW(), 4.8, 'Such a good drama show, love all the actors.');


INSERT INTO comments (commentId, reviewId, userId, createdAt, content)
VALUES (300, 200, 2, NOW(), 'Totally agree! It was intense.'),
      (310, 210, 1, NOW(), 'Loved the actors too! Some of my favorites');


INSERT INTO watchlist (toWatchId, userId, numberOfElements, createdAt, name, showId)
VALUES (400, 1, 2, NOW(), 'Must Watch', 11),
      (410, 2, 1, NOW(), 'Next Up', 12);


INSERT INTO userFeedback (feedbackId, title, content, createdAt, userId)
VALUES (500, 'App suggestion', 'Would love a dark mode for night-time binging.', NOW(), 1),
      (510, 'Bug report', 'Show page crashes sometimes.', NOW(), 2);


INSERT INTO watches (watchId, watchDate, showId, userId)
VALUES (1, '2024-10-10', 10, 1),
      (2, '2023-03-05', 11, 2);


INSERT INTO forum (forumId, topic, content, name)
VALUES (600, 'Best Action Shows', 'Let''s discuss your favorites!', 'Alex M'),
      (610, 'Teen Drama Highlights', 'Euphoria deep dive.', 'Sophie S');


INSERT INTO genre (genreId, title, description)
VALUES (700, 'Action', 'Conflict, high-intensity stories'),
      (710, 'Drama', 'Character-driven narratives.');


INSERT INTO articles (articleID, title, createdAt, rating, content, directorID, showrunnerID)
VALUES (800, 'Why Euphoria Matters', '2024-02-01', 4.6, 'An in-depth look at its social impact.', 110, NULL),
      (810, 'The Future of Sci-Fi', '2025-01-12', 4.2, 'Exploring modern sci-fi.', 100, NULL);


INSERT INTO actors (actorID, lastName, firstName, bio, socialMedia)
VALUES (900, 'Eric', 'Winter', 'Star of The Rookie.', '@ericwinter'),
      (910, 'Zendaya', 'Coleman', 'Lead in Euphoria.', '@zendaya');


INSERT INTO featured_films (actorId, featuredFilms)
VALUES (900, 'The Rookie'),
      (910, 'Euphoria');


INSERT INTO films_made (directorId, filmsMade)
VALUES (100, 12),
      (110, 5);


INSERT INTO streaming_pltfm (showId, platform)
VALUES (10, 'Hulu'),
      (11, 'HBO');


INSERT INTO coworkers (directorId, actorId)
VALUES (100, 900),
      (110, 910);


INSERT INTO keyword (showId, keyword)
VALUES (10, 'police'),
      (11, 'high school');


INSERT INTO user_forums (userId, forumId)
VALUES (1, 600),
      (2, 610);


INSERT INTO follows (followerId, followeeId)
VALUES (1, 2),
      (2, 1),
      (3, 2);


INSERT INTO featuredIn (actorId, showId)
VALUES (900, 10),
      (910, 11);


INSERT INTO show_genre (genreId, showId)
VALUES (700, 10),
      (710, 11);


INSERT INTO favorited_prod (favoritedId, showId)
VALUES (1, 10),
      (2, 11);


INSERT INTO comp_lists (toWatchId, showId)
VALUES (400, 11),
      (410, 12);


INSERT INTO watched_prod (userId, showId)
VALUES (1, 10),
      (2, 11);


INSERT INTO article_genre (genreId, articleId)
VALUES (710, 800),
      (700, 810);


INSERT INTO com_reviews (commentId, reviewId)
VALUES (300, 200),
      (310, 210);

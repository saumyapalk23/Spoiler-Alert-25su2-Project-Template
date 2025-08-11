DROP DATABASE IF EXISTS spoileralert;
CREATE DATABASE spoileralert;
USE spoileralert;

DROP TABLE IF EXISTS users;
CREATE TABLE IF NOT EXISTS users (
    userId INT  NOT NULL PRIMARY KEY,
    userName VARCHAR(50) NOT NULL,
    name VARCHAR(50),
    email VARCHAR(75) NOT NULL,
    age INT NOT NULL
);

DROP TABLE IF EXISTS recommendations;
CREATE TABLE IF NOT EXISTS recommendations(
	userId INT NOT NULL PRIMARY KEY,
	rating DECIMAL(3, 1) CHECK (rating BETWEEN 0.0 AND 5.0),
    CONSTRAINT fk_recs1 FOREIGN KEY (userId) REFERENCES users (userId)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS shows;
CREATE TABLE IF NOT EXISTS shows(
	showID INT NOT NULL PRIMARY KEY,
	title VARCHAR(50) NOT NULL,
    rating DECIMAL(3, 1) CHECK (rating BETWEEN 0.0 AND 5.0),
    releaseDate DATE,
    season INT NOT NULL,
    ageRating VARCHAR(10),
    streamingPlatform VARCHAR(25)
);

DROP TABLE IF EXISTS favorites;
CREATE TABLE favorites
(
   favoriteId  INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
   userId      INT NOT NULL,
   showId      INT,
   favoritedAt DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS directors;
CREATE TABLE IF NOT EXISTS directors(
	directorId INT NOT NULL PRIMARY KEY,
	firstName VARCHAR(50) NOT NULL,
	lastName VARCHAR(50) NOT NULL,
	filmsMade INT,
	bio TEXT,
	socialMedia VARCHAR(100)
);

DROP TABLE IF EXISTS reviews;
CREATE TABLE IF NOT EXISTS reviews(
	writtenrevID INT NOT NULL PRIMARY KEY,
    userId INT NOT NULL,
    showID INT NOT NULL,
    createdAt DATETIME DEFAULT NOW(),
    rating DECIMAL(3, 1) CHECK (rating BETWEEN 0.0 AND 5.0),
    content text,
    CONSTRAINT fk_reviewUser FOREIGN KEY (userId) REFERENCES users (userId)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    CONSTRAINT fk_reviewShow FOREIGN KEY (showId) REFERENCES shows (showId)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DROP TABLE IF EXISTS comments;
CREATE TABLE IF NOT EXISTS comments(
	commentId INT NOT NULL PRIMARY KEY,
    reviewId INT NOT NULL,
    userId INT NOT NULL,
    createdAt DATETIME DEFAULT NOW(),
    content TEXT NOT NULL,
    CONSTRAINT fk_commentReview FOREIGN KEY (reviewId) REFERENCES reviews (writtenrevID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
    CONSTRAINT fk_commentUser FOREIGN KEY (userId) REFERENCES users (userId)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

DROP TABLE IF EXISTS watchlist;
CREATE TABLE IF NOT EXISTS watchlist(
	toWatchId INT NOT NULL PRIMARY KEY,
	userId INT NOT NULL,
    numberOfElements INT,
	createdAt DATETIME,
	name VARCHAR(50),
	showId INT NOT NULL,
    CONSTRAINT fk_watchlistUsers FOREIGN KEY (userId) REFERENCES users (userId)
	ON DELETE RESTRICT,
	CONSTRAINT fk_watchlistShows FOREIGN KEY (showId) REFERENCES shows (showId)
	ON DELETE RESTRICT
);

DROP TABLE IF EXISTS userFeedback;
CREATE TABLE IF NOT EXISTS userFeedback(
    feedbackId INT NOT NULL PRIMARY KEY,
    title VARCHAR(50),
    content text NOT NULL,
    createdAt DATETIME DEFAULT NOW() NOT NULL,
    userId INT NOT NULL,
    CONSTRAINT feedback_writtenBy FOREIGN KEY (userId) REFERENCES users (userId)
	ON DELETE RESTRICT
);

DROP TABLE IF EXISTS watches;
CREATE TABLE IF NOT EXISTS watches(
	watchId INT NOT NULL PRIMARY KEY,
	watchDate DATE,
	showId INT NOT NULL,
	userId INT NOT NULL,
    CONSTRAINT fk_watchesUsers FOREIGN KEY (userId) REFERENCES users(userId)
	ON DELETE RESTRICT,
	CONSTRAINT fk_watchesShows FOREIGN KEY (showId) REFERENCES shows (showId)
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS forum;
CREATE TABLE IF NOT EXISTS forum(
	forumId INT NOT NULL PRIMARY KEY,
	topic VARCHAR(100) NOT NULL,
    content text,
    name VARCHAR(100) NOT NULL
);

DROP TABLE IF EXISTS genre;
CREATE TABLE IF NOT EXISTS genre(
	genreId INT UNSIGNED NOT NULL PRIMARY KEY,
	title VARCHAR(50) NOT NULL,
	description TEXT
);

DROP TABLE IF EXISTS articles;
CREATE TABLE IF NOT EXISTS articles(
   articleID INT PRIMARY KEY,
   title VARCHAR(100) NOT NULL,
   createdAt DATE NOT NULL,
   rating DECIMAL(3, 1) CHECK (rating BETWEEN 0.0 AND 5.0),
   content TEXT,
   directorID INT NOT NULL,
   showrunnerID INT,
   CONSTRAINT fk_articleDirector FOREIGN KEY (directorID) REFERENCES directors (directorID)
	ON UPDATE CASCADE
	ON DELETE RESTRICT
);

DROP TABLE IF EXISTS actors;
CREATE TABLE IF NOT EXISTS actors(
   actorID INT PRIMARY KEY,
   lastName VARCHAR(50) NOT NULL,
   firstName VARCHAR(50) NOT NULL,
   bio TEXT,
   socialMedia VARCHAR(100)
);

DROP TABLE IF EXISTS featured_films;
CREATE TABLE IF NOT EXISTS featured_films(
	actorId INT NOT NULL PRIMARY KEY,
	featuredFilms text,
	CONSTRAINT fk_ffActor FOREIGN KEY (actorId) REFERENCES actors (actorId)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);


DROP TABLE IF EXISTS films_made;
CREATE TABLE IF NOT EXISTS films_made(
	directorId INT NOT NULL,
	filmsMade INT NOT NULL PRIMARY KEY,
CONSTRAINT fk_filmsMadeDirector FOREIGN KEY (directorId) REFERENCES directors (directorId)
ON DELETE RESTRICT
);


DROP TABLE IF EXISTS streaming_pltfm;
CREATE TABLE IF NOT EXISTS streaming_pltfm(
    showId INT NOT NULL,
    platform VARCHAR(25) NOT NULL,
    PRIMARY KEY (showId, platform),
    CONSTRAINT FOREIGN KEY (showId) REFERENCES shows (showId)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

DROP TABLE IF EXISTS coworkers;
CREATE TABLE IF NOT EXISTS coworkers(
    directorId INT NOT NULL,
    actorId INT NOT NULL,
    PRIMARY KEY (directorId, actorId),
    CONSTRAINT FOREIGN KEY (directorId) REFERENCES directors (directorId)
    ON UPDATE CASCADE,
    CONSTRAINT FOREIGN KEY (actorId) REFERENCES actors (actorId)
);


DROP TABLE IF EXISTS keyword;
CREATE TABLE IF NOT EXISTS keyword(
    showId INT NOT NULL,
    keyword VARCHAR(50) NOT NULL,
    PRIMARY KEY (showId, keyword),
    CONSTRAINT FOREIGN KEY (showId) REFERENCES shows (showId)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);


DROP TABLE IF EXISTS user_forums;
CREATE TABLE IF NOT EXISTS user_forums(
	userId INT NOT NULL,
	forumId INT NOT NULL PRIMARY KEY,
    CONSTRAINT FOREIGN KEY fk_forumUserUser (userId) REFERENCES users (userId)
 	ON UPDATE CASCADE
 	ON DELETE CASCADE,
 	CONSTRAINT FOREIGN KEY fk_forumUserForum (forumId) REFERENCES forum (forumId)
	ON DELETE CASCADE
	ON UPDATE CASCADE
);

DROP TABLE IF EXISTS follows;
CREATE TABLE IF NOT EXISTS follows(
	followerId INT NOT NULL,
	followeeId INT NOT NULL,
	PRIMARY KEY (followerId, followeeId),
	CONSTRAINT FOREIGN KEY fk_followerUser (followerId) REFERENCES users (userId)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY fk_followeeUser (followeeId) REFERENCES users (userId)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);


DROP TABLE IF EXISTS featuredIn;
CREATE TABLE IF NOT EXISTS featuredIn(
	actorId INT NOT NULL,
	showId INT NOT NULL,
	PRIMARY KEY (actorId, showId),
	CONSTRAINT FOREIGN KEY fk_actorFeature (actorId) REFERENCES actors (actorId)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	CONSTRAINT FOREIGN KEY fk_showFeature (showId) REFERENCES shows (showId)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

DROP TABLE IF EXISTS show_genre;
CREATE TABLE IF NOT EXISTS show_genre (
    genreId INT UNSIGNED NOT NULL,
    showId INT NOT NULL,
    PRIMARY KEY (genreId, showId),
    CONSTRAINT fk_show_genre_genre FOREIGN KEY (genreId) REFERENCES genre (genreId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_show_genre_show FOREIGN KEY (showId) REFERENCES shows (showId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS favorited_prod;
CREATE TABLE IF NOT EXISTS favorited_prod(
    favoritedId INT NOT NULL,
    showId INT NOT NULL,
    PRIMARY KEY (favoritedId, showId),
    CONSTRAINT fk_favoritedFavorites FOREIGN KEY (favoritedId) REFERENCES favorites (favoriteId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_favoritedShow FOREIGN KEY (showId) REFERENCES shows (showId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS comp_lists;
CREATE TABLE IF NOT EXISTS comp_lists(
    toWatchId INT NOT NULL,
    showId INT NOT NULL,
    PRIMARY KEY (toWatchId, showId),
    CONSTRAINT fk_compWatchlist FOREIGN KEY (toWatchId) REFERENCES watchlist (toWatchId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_watchListShow FOREIGN KEY (showId) REFERENCES shows (showId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS watched_prod;
CREATE TABLE IF NOT EXISTS watched_prod(
    userId INT NOT NULL,
    showId INT NOT NULL,
    PRIMARY KEY (userId, showId),
    CONSTRAINT fk_watchedUser FOREIGN KEY (userId) REFERENCES users (userId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_watchedShow FOREIGN KEY (showId) REFERENCES shows (showId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS article_genre;
CREATE TABLE IF NOT EXISTS article_genre (
    genreId INT UNSIGNED NOT NULL,
    articleId INT NOT NULL,
    PRIMARY KEY (genreId, articleId),
    CONSTRAINT fk_articleGenreGenre FOREIGN KEY (genreId) REFERENCES genre (genreId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_articleGenreArticle FOREIGN KEY (articleId) REFERENCES articles (articleId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS com_reviews;
CREATE TABLE IF NOT EXISTS com_reviews (
    commentId INT NOT NULL,
    reviewId INT NOT NULL,
    PRIMARY KEY (commentId, reviewId),
    CONSTRAINT fk_comrev FOREIGN KEY (commentId) REFERENCES comments (commentId)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    CONSTRAINT fk_comrevRev FOREIGN KEY (reviewId) REFERENCES reviews (writtenrevId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

INSERT INTO users (userId, userName, name, email, age)
VALUES (1, 'cinemalover99', 'Alex Turner', 'alex.t@example.com', 28),
      (2, 'tvaddict88', 'Sophie Miller', 'sophie.m@example.com', 34),
      (3, 'streamqueen', 'Lena Diaz', 'lena.d@example.com', 22),
     (14, 'cinemalover99', 'Alex Turner', 'alex.t@example.com', 28),
      (410, 'tvaddict88', 'Sophie Miller', 'sophie.m@example.com', 34),
      (412, 'streamqueen', 'Lena Diaz', 'lena.d@example.com', 22);


INSERT INTO recommendations (userId, rating)
VALUES (1, 4.5),
      (2, 3.8),
      (14, 4.0);


INSERT INTO shows (showID, title, rating, releaseDate, season, ageRating, streamingPlatform)
VALUES
  (10, 'Ted Lasso', 4.5, '2020-08-14', 3, 'TV-14', 'Apple TV+'),
  (11, 'Stranger Things', 4.8, '2016-07-15', 4, 'TV-14', 'Netflix'),
  (14, 'The Witcher', 4.3, '2019-12-20', 2, 'TV-MA', 'Netflix'),
  (15, 'Breaking Bad', 4.9, '2008-01-20', 5, 'TV-MA', 'AMC'),
  (16, 'Friends', 4.7, '1994-09-22', 10, 'TV-14', 'Netflix'),
  (17, 'The Crown', 4.6, '2016-11-04', 5, 'TV-MA', 'Netflix'),
  (18, 'Black Mirror', 4.5, '2011-12-04', 5, 'TV-MA', 'Netflix'),
  (19, 'Westworld', 4.4, '2016-10-02', 3, 'TV-MA', 'HBO'),
  (20, 'The Mandalorian', 4.7, '2019-11-12', 3, 'TV-14', 'Disney+'),
  (21, 'Ozark', 4.3, '2017-07-21', 4, 'TV-MA', 'Netflix'),
  (22, 'House of Cards', 4.4, '2013-02-01', 6, 'TV-MA', 'Netflix'),
  (23, 'Sherlock', 4.6, '2010-07-25', 4, 'TV-14', 'BBC'),
  (24, 'The Boys', 4.6, '2019-07-26', 3, 'TV-MA', 'Amazon Prime'),
  (25, 'Better Call Saul', 4.8, '2015-02-08', 6, 'TV-MA', 'AMC'),
  (26, 'Narcos', 4.5, '2015-08-28', 3, 'TV-MA', 'Netflix'),
  (27, 'Mindhunter', 4.5, '2017-10-13', 2, 'TV-MA', 'Netflix'),
  (28, 'Fargo', 4.7, '2014-04-15', 4, 'TV-MA', 'FX'),
  (29, 'Dark', 4.6, '2017-12-01', 3, 'TV-MA', 'Netflix');

INSERT INTO reviews (writtenrevID, userId, showID, createdAt, rating, content)
VALUES
  (200, 1, 17, NOW(), 4.5, 'Great sci-fi thriller!'),
  (201, 2, 15, NOW(), 4.8, 'Emotional and beautifully shot.');

INSERT INTO comments (commentId, reviewId, userId, createdAt, content)
VALUES (300, 200, 14, NOW(), 'Totally agree! It was intense.'),
(301, 201, 14, NOW(), 'Totally agree! It was intense.');

INSERT INTO favorites (userId, showId)
VALUES
   (1, 13),
   (2, 45),
   (400, 34),
   (410, 43);

INSERT INTO watchlist (toWatchId, userId, numberOfElements, createdAt, name, showId)
VALUES (400, 1, 2, NOW(), 'Must Watch', 18),
      (401, 2, 1, NOW(), 'Next Up', 20);

INSERT INTO directors (directorId, firstName, lastName, filmsMade, bio, socialMedia)
VALUES (100, 'Bong', 'Joon-ho', 12, 'South Korean director known for Parasite.', '@bongjoonho'),
      (101, 'Sam', 'Levinson', 5, 'Director and writer of Euphoria.', '@samlevinson');

INSERT INTO userFeedback (feedbackId, title, content, createdAt, userId)
VALUES (500, 'App suggestion', 'Would love a dark mode.', NOW(), 1),
      (501, 'Bug report', 'Show page crashes sometimes.', NOW(), 2);

INSERT INTO watches (watchId, watchDate, showId, userId)
VALUES (1, '2023-10-10', 14, 1),
      (2, '2023-11-05', 15, 2);

INSERT INTO forum (forumId, topic, content, name)
VALUES (600, 'Best Sci-Fi Shows', 'Let''s discuss your favorites!', 'Alex T'),
      (601, 'Teen Drama Highlights', 'Euphoria deep dive.', 'Sophie M');

INSERT INTO genre (genreId, title, description)
VALUES (700, 'Sci-Fi', 'Futuristic, space-related content.'),
      (701, 'Drama', 'Character-driven narratives.');

INSERT INTO articles (articleID, title, createdAt, rating, content, directorID, showrunnerID)
VALUES (800, 'Why Euphoria Matters', '2022-02-01', 4.6, 'An in-depth look at its social impact.', 101, NULL),
      (801, 'The Future of Sci-Fi', '2023-01-12', 4.2, 'Exploring modern sci-fi.', 100, NULL);

INSERT INTO actors (actorID, lastName, firstName, bio, socialMedia)
VALUES (900, 'Page', 'Hunter', 'Star of The Silent Sea.', '@hunterp'),
      (901, 'Zendaya', 'Coleman', 'Lead in Euphoria.', '@zendaya');

INSERT INTO featured_films (actorId, featuredFilms)
VALUES (900, 'The Silent Sea'),
      (901, 'Euphoria');

INSERT INTO films_made (directorId, filmsMade)
VALUES (100, 12),
      (101, 5);

INSERT INTO streaming_pltfm (showId, platform)
VALUES (10, 'Netflix'),
      (11, 'HBO');

INSERT INTO coworkers (directorId, actorId)
VALUES (100, 900),
      (101, 901);

INSERT INTO keyword (showId, keyword)
VALUES (15, 'space'),
      (16, 'high school');

INSERT INTO user_forums (userId, forumId)
VALUES (1, 600),
      (2, 601);

INSERT INTO follows (followerId, followeeId)
VALUES (1, 2),
      (2, 1);

INSERT INTO featuredIn (actorId, showId)
VALUES (900, 15),
      (901, 16);

INSERT INTO show_genre (genreId, showId)
VALUES (700, 10),
      (701, 11);

INSERT INTO favorited_prod (favoritedId, showId)
VALUES (1, 10),
      (2, 11);

INSERT INTO comp_lists (toWatchId, showId)
VALUES (400, 18),
      (401, 29);

INSERT INTO watched_prod (userId, showId)
VALUES (1, 10),
      (2, 11);

INSERT INTO article_genre (genreId, articleId)
VALUES (701, 800),
      (700, 801);

INSERT INTO com_reviews (commentId, reviewId)
VALUES (300, 200),
      (301, 201);


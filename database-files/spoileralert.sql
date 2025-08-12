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
CREATE TABLE IF NOT EXISTS userFeedback (
    feedbackId INTEGER AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    userId INT,
    CONSTRAINT feedback_writtenBy FOREIGN KEY (userId) REFERENCES users(userId) ON DELETE RESTRICT
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


INSERT INTO shows (showID, title, rating, releaseDate, season, ageRating, streamingPlatform) VALUES
    (1, 'Breaking Bad', 2.0, '1981-01-27', 8, 'R', 'Yakitri'),
    (2, 'Game of Thrones', 0.8, '2012-10-09', 17, 'PG-13', 'Kazio'),
    (3, 'Friends', 3.4, '1942-08-12', 13, 'NC-17', 'Babbleset'),
    (4, 'The Office', 2.1, '1942-09-14', 18, 'PG', 'Mycat'),
    (5, 'Stranger Things', 0.1, '1943-12-03', 11, 'PG', 'Shuffletag'),
    (6, 'The Crown', 2.4, '1920-05-06', 2, 'NC-17', 'Thoughtstorm'),
    (7, 'The Simpsons', 0.3, '1959-11-25', 1, 'PG', 'Mynte'),
    (8, 'The Mandalorian', 2.6, '1961-02-16', 4, 'PG-13', 'Demizz'),
    (9, 'Better Call Saul', 4.9, '1948-04-06', 20, 'NC-17', 'Dynabox'),
    (10, 'Seinfeld', 2.7, '1945-12-01', 16, 'G', 'Thoughtbridge'),
    (11, 'The Sopranos', 3.3, '1981-10-26', 12, 'PG-13', 'Browsecat'),
    (12, 'The Witcher', 2.5, '1968-12-05', 15, 'NC-17', 'Wordtune'),
    (13, 'Lost', 1.9, '1995-07-13', 6, 'R', 'Quaxo'),
    (14, 'House of Cards', 1.1, '1921-01-27', 15, 'PG-13', 'Skilith'),
    (15, 'The Boys', 0.2, '1993-08-11', 18, 'PG-13', 'Yodel'),
    (16, 'Mad Men', 0.5, '1902-06-03', 18, 'R', 'Ainyx'),
    (17, 'Parks and Recreation', 1.3, '1970-03-08', 20, 'G', 'Fatz'),
    (18, 'Sherlock', 4.6, '1951-11-06', 1, 'G', 'Zoombeat'),
    (19, 'House', 1.3, '1937-07-30', 9, 'G', 'Mynte'),
    (20, 'True Detective', 2.6, '1987-06-12', 8, 'G', 'Rhybox'),
    (21, 'Narcos', 1.4, '1953-03-21', 13, 'R', 'Plambee'),
    (22, 'Westworld', 2.0, '2004-04-12', 13, 'PG', 'Miboo'),
    (23, 'The Walking Dead', 1.7, '1953-02-06', 3, 'R', 'Oba'),
    (24, 'The Big Bang Theory', 0.9, '2018-03-14', 7, 'G', 'Roomm'),
    (25, 'Vikings', 0.8, '1941-06-20', 9, 'R', 'Meevee'),
    (26, 'Peaky Blinders', 0.1, '1998-06-14', 12, 'PG', 'Edgeclub'),
    (27, 'Succession', 1.3, '1943-12-11', 20, 'R', 'Mydo'),
    (28, 'Dexter', 3.2, '1906-06-17', 18, 'R', 'Agivu'),
    (29, 'Community', 0.5, '1980-06-13', 2, 'G', 'Thoughtsphere'),
    (30, 'The X-Files', 3.3, '1991-06-05', 7, 'PG-13', 'Jabbertype'),
    (31, 'Black Mirror', 1.3, '1923-05-19', 20, 'PG', 'Ozu'),
    (32, 'Fargo', 3.8, '2022-07-13', 10, 'R', 'Roomm'),
    (33, 'Brooklyn Nine-Nine', 2.5, '1947-05-27', 19, 'PG-13', 'Centimia'),
    (34, 'Ozark', 0.2, '1999-02-09', 20, 'R', 'Zazio'),
    (35, 'The Handmaid''s Tale', 4.3, '1995-03-16', 19, 'NC-17', 'Skimia'),
    (36, 'Arrested Development', 4.3, '1934-12-14', 6, 'PG-13', 'Yodo'),
    (37, 'Boardwalk Empire', 4.9, '1929-09-04', 8, 'PG', 'Photofeed'),
    (38, 'Mindhunter', 3.9, '1929-12-19', 4, 'NC-17', 'Fadeo'),
    (39, 'Chernobyl', 1.9, '1930-11-03', 11, 'NC-17', 'Twinder'),
    (40, 'The Americans', 4.5, '1963-07-17', 15, 'PG-13', 'Twimm');

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

INSERT INTO genre (genreId, title) 
VALUES
    (1, 'Comedy|Drama'),
    (2, 'Action|Thriller'),
    (3, 'Drama|Thriller'),
    (4, 'Documentary'),
    (5, 'Comedy'),
    (6, 'Comedy|Drama|Romance'),
    (7, 'Drama|Romance'),
    (8, 'Horror'),
    (9, 'Adventure|Animation|Children|Comedy|Fantasy|Romance'),
    (10, 'Comedy|Horror'),
    (11, 'Drama|Mystery'),
    (12, 'Crime|Drama|Thriller'),
    (13, 'Drama|Mystery'),
    (14, 'Action|Drama|War'),
    (15, 'Comedy'),
    (16, 'Children|Comedy'),
    (17, 'Horror'),
    (18, 'Comedy|Drama'),
    (19, 'Comedy|Horror'),
    (20, 'Drama'),
    (21, 'Drama|Western'),
    (22, 'Comedy|Romance'),
    (23, 'Action|Drama'),
    (24, 'Sci-Fi|Thriller'),
    (25, 'Documentary'),
    (26, 'Comedy'),
    (27, 'Comedy'),
    (28, 'Drama|Thriller'),
    (29, 'Adventure|Animation|Horror|Sci-Fi|Thriller'),
    (30, 'Documentary'),
    (31, 'Action|Adventure|Drama|War'),
    (32, 'Documentary'),
    (33, 'Drama'),
    (34, 'Comedy|Fantasy'),
    (35, 'Comedy'),
    (36, 'Action|Horror'),
    (37, 'Documentary'),
    (38, 'Comedy|Drama'),
    (39, 'Crime|Drama|Romance'),
    (40, 'Adventure|Fantasy');


INSERT INTO articles (articleID, title, createdAt, rating, content, directorID)
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


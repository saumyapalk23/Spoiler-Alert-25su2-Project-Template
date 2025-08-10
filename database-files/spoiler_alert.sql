DROP DATABASE IF EXISTS SpoilerAlert;
CREATE DATABASE SpoilerAlert;

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
   showId      INT NOT NULL,
   favoritedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
   FOREIGN KEY (userId) REFERENCES users (userId)
       ON DELETE CASCADE ON UPDATE CASCADE,
   FOREIGN KEY (showId) REFERENCES shows (showID)
       ON DELETE CASCADE ON UPDATE CASCADE
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
    CONSTRAINT fk_watchesUsers FOREIGN KEY (watchId) REFERENCES users(userId)
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
    CONSTRAINT fk_comrevComment FOREIGN KEY (commentId) REFERENCES comments (commentId)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_comrevRev FOREIGN KEY (reviewId) REFERENCES reviews (writtenrevId)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

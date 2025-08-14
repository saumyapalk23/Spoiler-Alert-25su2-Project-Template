# Spoiler Alert

We are building ‘Spoiler Alert’, an app dedicated to appreciating content such as TV shows and onstage performances. Unlike platforms like Letterboxd, which cater primarily to film enthusiasts, ‘Spoiler Alert’ is designed for a broader community. From theatregoers and casual fans to performance artists and professionals in the field, this app offers a dedicated space for users to rate, review, and discuss television, plays, and musicals: mediums that are often overlooked on mainstream review platforms and relegated to non-dedicated forums such as Twitter or Reddit. 

Through collecting such user data, we hope to create personalized platforms for discussion and analysis, as well as tailored recommendations for users. Now, lovers of episodic storytelling and live performance no longer have to struggle to find personalized recommendations or to share their niche interests with others. Key features include the ability to log live performances, create watchlists, and connect with others through a built-in forum. ‘Spoiler Alert’ builds upon the best aspects of Letterboxd, further building community.

The database is built in MySQL with the application built using python, streamlit, and flask. 


## How to run the app
The app is run using app, api, and database containers in docker desktop. To start the app, use `docker compose up -d`, and shut off the containers using `docker compose down -v`. In order to run everything properly, you need to make a copy of the `.env.template` file, change the password and set the database so that it says `DB_NAME=spoileralert`, and save as just `.env`. 


## Users
The users are accessed by buttons on the home page, and each user profile has access to different features based on their hypothetical role in the apps userbase. We have Amanda, who is a system administrator, Sally, an aspiring filmmaker, John, a (not very) casual binger (roll credits), and Alex, who is a data analyst. 
### Amanda
As a system administrator, Amanda wants to know what and who is trending on the app. As such, her routes pertain to seeing the most popular shows (by which one has the most reviews), filtering by recent articles and their genres, as well as being able to create lists of favorites for shows, directors, and actors.
### Sally
Sally, as an aspiring filmmaker, wants to take inspiration from other shows to know what to emulate in her own work. As such, her pages include watchlists, which allow the user to create, update, and delete watchlists of shows. She alwo wants to follow other users, as well as write, edit, and delete her reviews. 
### John
As a TV enthusiast, John always wants something new to watch. As such, he wants to be able to filter shows by parameters such as genre or release date. He also can be more specific and search for specific shows by certain keywords. He also has access to write, edit, and delete comments on other peoples reviews.
### Alex
Alex, as a data analyst, wants to be able to filter shows by parameters as well. His home page has a slider that displays shows based on a min and max amount of seasons. He also wants to filter shows by star rating, in order to see what is trending. He can also filter comments on shows by most recent to see current opinion.

## Navigating the app
The buttons controlling the login direct to each users home page, as well as granting the role's dedicated sessionstate, which grants different functionalities. Most basically, it changes what each user sees based on their user stories, but also gives each user access to different nav bars on the left side, which would be most practical for an admin who would have greater permissions than an ordinary user. 

## The Database
The routes in the backend are all SQL commands, which make it easy for keywords to narrow down the list of shows as in the search by keywords or as in adding data in the form of reviews or comments on those reviews. The SQL database, `spoileralert.sql` automatically runs with the db container, and contains data viewed and updated using the commands in each users routes.

Project by: Saumya Palakodety, Constanza Perusquia Ruiz, Jahnavi Bulusu, and Hannah Chapman

Link to pitch/demo: https://drive.google.com/file/d/1Iv0rxnEZ5VwsFq7teIGGoPTi8p7O3kaE/view?usp=sharing

-- multiple SQL files to fulfill the parts of Pset7 "Movies"
-- Part 1
SELECT title FROM movies WHERE year = "2008";
-- Part 2
SELECT birth FROM people WHERE name = "Emma Stone";
-- Part 3
SELECT title FROM movies WHERE year >= "2018" ORDER BY title;
-- Part 4
SELECT COUNT(movie_id) FROM ratings WHERE rating = "10.0";
-- Part 5
SELECT title, year FROM movies WHERE title LIKE "Harry Potter%" ORDER BY year;
-- Part 6
SELECT AVG(rating) FROM ratings JOIN movies ON ratings.movie_id = movies.id WHERE year = "2012";
-- Part 7
SELECT title, rating from RATINGS JOIN movies ON ratings.movie_id = movies.id WHERE year = "2010" ORDER BY rating DESC, title;
-- Part 8
SELECT name FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON stars.movie_id = movies.id WHERE title = "Toy Story";
-- Part 9
SELECT name FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON stars.movie_id = movies.id WHERE year = "2004" ORDER BY birth;
-- Part 10
SELECT DISTINCT(name) FROM people JOIN directors ON people.id = directors.person_id JOIN movies ON directors.movie_id = movies.id JOIN ratings ON movies.id = ratings.movie_id WHERE rating >= "9.0";
-- Part 11
SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id
JOIN people ON stars.person_id = people.id JOIN ratings ON movies.id = ratings.movie_id WHERE name = "Chadwick Boseman" ORDER BY rating DESC LIMIT 5;
-- Part 12
SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id JOIN people ON stars.person_id = people.id WHERE name = "Johnny Depp" INTERSECT
SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id JOIN people ON stars.person_id = people.id WHERE name = "Helena Bonham Carter";
-- Part 13
SELECT DISTINCT(name) FROM people JOIN stars ON people.id = stars.person_id JOIN movies ON stars.movie_id = movies.id
WHERE title IN (SELECT title FROM movies JOIN stars ON movies.id = stars.movie_id JOIN people ON stars.person_id = people.id
WHERE name = "Kevin Bacon" AND birth = "1958") EXCEPT SELECT name FROM people WHERE name = "Kevin Bacon"; 

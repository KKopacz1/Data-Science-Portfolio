Use sakila;

-- List all actors. Display first and last name.
SELECT first_name,last_name FROM actor
Where first_name IS NOT NULL and last_name IS NOT NULL;

-- Display first and last name of each actor in single column, uppercase.
SELECT CONCAT(ucase(first_name), ' ', ucase(last_name)) as 'Actor Name' FROM actor;

-- Display all actors with the first name "Joe"
SELECT actor_id, first_name, last_name FROM actor 
WHERE first_name = "Joe" and last_name IS NOT NULL;

-- Display all last names with "GEN"
SELECT * FROM actor
WHERE last_name LIKE "%gen%";

-- Display all last names with "LI"
SELECT first_name, last_name FROM actor
WHERE last_name LIKE "%LI%";

-- Display all instances of Afghanistan, Bangladesh, or China with corresponding ID.
SELECT country_id, country FROM country
WHERE country in ("Afghanistan", "Bangladesh", "China");

-- Alter table to include middle_name column
ALTER TABLE actor ADD COLUMN middle_name VARCHAR(20) AFTER first_name;

-- Alter middle_name column to BLOB data type
ALTER TABLE actor MODIFY COLUMN middle_name BLOB;

-- Delete middle_name column
ALTER TABLE actor DROP COLUMN middle_name;
SELECT * FROM actor;

-- List the names of actors and the actor name count
SELECT last_name, COUNT(*) as COUNT FROM actor GROUP BY last_name;

-- List names of actors shared name (>= 2)
SELECT last_name, COUNT(*) as COUNT FROM actor GROUP BY last_name HAVING COUNT>1;

-- Write a query to fix Harpo.
SELECT * FROM actor WHERE first_name="GROUCHO" AND last_name="WILLIAMS";
UPDATE actor SET first_name="HARPO" WHERE first_name = "GROUCHO" AND last_name="WILLIAMS";

-- If the first name of the actor is currently HARPO, change it to GROUCHO.
SELECT * FROM actor WHERE first_name="HARPO" AND last_name="WILLIAMS";

UPDATE actor SET first_name=(
	CASE WHEN first_name="HARPO" THEN "GROUCHO"
    ELSE "MUCHO GROUCHO"
    END)
WHERE actor_id=172 AND last_name="WILLIAMS";

-- Locate the schema of address table
SELECT  *
FROM    INFORMATION_SCHEMA.TABLES
where   TABLES.TABLE_NAME="address";

-- Create the database if it doesnot exist
CREATE database IF NOT EXISTS sakila;

--  Display first & last names
SELECT staff.first_name,staff.last_name, address.address,address.district 
FROM staff
INNER JOIN address ON STAFF.ADDRESS_ID=ADDRESS.ADDRESS_ID; 

-- Use JOIN to display the total amount rung up by each staff member in August of 2005.
SELECT staff.first_name,staff.last_name, SUM(payment.amount) as `Total Sum`
FROM payment 
INNER JOIN STAFF ON PAYMENT.STAFF_ID=STAFF.STAFF_ID
WHERE payment_date BETWEEN "2005-08-01" AND "2005-08-31" 
GROUP BY staff.STAFF_ID;

-- List films & associated actors.
SELECT FILM.TITLE, COUNT(FILM_ACTOR.FILM_ID) AS `COUNT OF ACTORS`
FROM FILM
INNER JOIN FILM_ACTOR ON FILM.FILM_ID=FILM_ACTOR.FILM_ID
GROUP BY FILM.TITLE;

-- Count number of Hunchback Impossible instances.
SELECT FILM.TITLE, COUNT(INVENTORY.FILM_ID) AS `COUNT`
FROM FILM
INNER JOIN INVENTORY ON FILM.FILM_ID=INVENTORY.FILM_ID
WHERE FILM.TITLE="Hunchback Impossible";

-- List total played by customers & sort customers by last name ascending.
SELECT CUSTOMER.FIRST_NAME, CUSTOMER.LAST_NAME, SUM(PAYMENT.AMOUNT) AS `TOTAL AMOUNT PAID`
FROM CUSTOMER
LEFT JOIN PAYMENT ON CUSTOMER.CUSTOMER_ID=PAYMENT.CUSTOMER_ID
GROUP BY CUSTOMER.CUSTOMER_ID
ORDER BY CUSTOMER.LAST_NAME ASC;


-- Movies starting with K and Q
SELECT * FROM FILM
WHERE (TITLE LIKE "K%" OR TITLE LIKE"Q%") 
AND  LANGUAGE_ID=(SELECT LANGUAGE_ID FROM LANGUAGE WHERE NAME="ENGLISH");

-- Display actors in alone trip
SELECT FIRST_NAME, LAST_NAME FROM ACTOR
WHERE ACTOR_ID IN (SELECT ACTOR_ID FROM FILM_ACTOR 
					WHERE FILM_ID=(SELECT FILM_ID FROM FILM WHERE TITLE="Alone Trip"));

-- Display Canadian customers
SELECT first_name AS `FIRST NAME`, last_name AS `LAST NAME`,email AS `E-MAIL` FROM customer
LEFT JOIN address ON customer.address_id=address.address_id
LEFT JOIN city ON address.city_id=city.city_id
LEFT JOIN country ON city.country_id=country.country_id
WHERE country="Canada";

-- Identify family films
SELECT TITLE FROM FILM 
WHERE FILM_ID IN (SELECT FILM_ID FROM FILM_CATEGORY
				WHERE CATEGORY_ID=(SELECT CATEGORY_ID FROM CATEGORY 
									WHERE NAME="FAMILY")
				);

-- Most rented movies, descending order
SELECT film.title,COUNT(film.film_id) as `Count`FROM rental
LEFT JOIN inventory ON rental.inventory_id=inventory.inventory_id
LEFT JOIN film ON inventory.film_id=film.film_id
GROUP BY film.film_id
ORDER BY `Count` DESC;

-- Revenue per business in dollars, descending order
SELECT CONCAT(city.city,",",country.country) as `Store`,SUM(payment.amount) AS `Total Sales` FROM payment
LEFT JOIN rental on payment.rental_id=rental.rental_id
LEFT JOIN inventory ON rental.inventory_id=inventory.inventory_id
LEFT JOIN store ON inventory.store_id=store.store_id
LEFT JOIN address ON store.address_id=address.address_id
LEFT JOIN city ON address.city_id=city.city_id
LEFT JOIN country ON city.country_id=country.country_id
WHERE store.store_id IS NOT NULL
GROUP BY store.store_id
ORDER BY `Total Sales` DESC;

-- Display store ID, city, and country.
SELECT store.store_id, city.city,country.country FROM store
LEFT JOIN address ON store.address_id=address.address_id
LEFT JOIN city ON address.city_id=city.city_id
LEFT JOIN country ON city.country_id=country.country_id;

-- Dop five genres in gross revenue in descending order.
SELECT category.name AS `Category`, SUM(payment.amount) as `Total Sales` FROM category
LEFT JOIN film_category ON category.category_id=film_category.category_id
LEFT JOIN inventory ON film_category.film_id=inventory.film_id
LEFT JOIN rental ON inventory.inventory_id=rental.inventory_id
LEFT JOIN payment ON rental.rental_id= payment.rental_id
GROUP BY category.category_id
ORDER BY `Total Sales` DESC LIMIT 5;

-- Create View for Top Five Genres
CREATE VIEW top_5_genres AS(
	SELECT category.name AS `Category`, SUM(payment.amount) as `Total Sales` FROM category
	LEFT JOIN film_category ON category.category_id=film_category.category_id
	LEFT JOIN inventory ON film_category.film_id=inventory.film_id
	LEFT JOIN rental ON inventory.inventory_id=rental.inventory_id
	LEFT JOIN payment ON rental.rental_id= payment.rental_id
	GROUP BY category.category_id
	ORDER BY `Total Sales` DESC LIMIT 5
	);

-- Display the View created in previous code 
SELECT * FROM top_5_genres;

-- Query to delete the view top_5_genres
DROP VIEW top_5_genres;
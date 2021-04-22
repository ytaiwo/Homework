--1.	Create a new column called “status” in the rental table that uses a case statement to indicate if a film was returned late, early, or on time. 

SELECT title, rental_id, rental_date, rental.inventory_id, rental.customer_id, rental.return_date, rental.staff_id, rental.last_update,
	CASE
		WHEN DATE_PART('day', return_date - rental_date) < rental_duration THEN 'Returned Early'
		WHEN DATE_Part('day', return_date - rental_date) = rental_duration THEN 'Returned on Time'
		ELSE 'Returned Late' END AS status
FROM rental
JOIN inventory ON rental.inventory_id = inventory.inventory_id
JOIN FILM ON film.film_id = inventory.film_id;

--2.	Show the total payment amounts for people who live in Kansas City or Saint Louis. 

SELECT CONCAT(first_name,' ', last_name) AS cust_name, SUM(amount) AS cust_amt, city
FROM payment
INNER JOIN customer
ON payment.customer_id = customer.customer_id
INNER JOIN address
ON customer.address_id = address.address_id
INNER JOIN city
ON address.city_id = city.city_id
WHERE city = 'Kansas City' OR city = 'Saint Louis'
GROUP BY cust_name, city.city;

--3.	How many film categories are in each category? Why do you think there is a table for category and a table for film category?
-- The table category allows us to see all the distinct categories. If it was joined with the film, then it would be hard to differentiate the number of distinct categoies since it would all be jumbled up.

SELECT name, COUNT(film_category)
FROM film_category
INNER JOIN category
ON film_category.category_id = category.category_id
GROUP BY name;

--4.	Show a roster for the staff that includes their email, address, city, and country (not ids)

SELECT first_name, last_name, email, address, country, city
FROM staff
JOIN address
ON staff.address_id = address.address_id
JOIN city
ON city.city_id = address.city_id
JOIN country
ON country.country_id = city.country_id;

--5.	Show the film_id, title, and length for the movies that were returned from May 15 to 31, 2005
SELECT film_id, title, length
FROM film
WHERE film_id IN
	(SELECT film_id
	 FROM rental
	 JOIN inventory
	 ON rental.inventory_id = inventory.inventory_id
	 WHERE return_date BETWEEN '2005-05-15' AND '2005-05-31'
	);

--6.	Write a subquery to show which movies are rented below the average price for all movies. 

SELECT f.title, f.rental_rate
FROM film f
WHERE f.rental_rate < (SELECT AVG(rental_rate) FROM film)
ORDER BY rental_rate;


--7.	Write a join statement to show which moves are rented below the average price for all movies.

SELECT title, rental_rate
FROM film f
JOIN 
(SELECT AVG(rental_rate) avg_rental_rate 
FROM film)
AS f2 ON f.rental_rate < f2.avg_rental_rate
ORDER BY rental_rate;


--8.	Perform an explain plan on 6 and 7, and describe what you’re seeing and important ways they differ.
--For number 6, it does the aggregation first and then is filtered and removes the rows that restricted by the filter. The total execution time 
--is 9.085 ms.
-- For number 7, the nested loop is done first, after sorting, then it's aggregated and then joins the filter, where rows are removed...
--based on that filter. It is then aggregated again. The total execution time is 1.262 milliseconds. This shows that for the subquery, it takes longer
--to process than when using JOINS. This is expected since we know wthat although subqueries avoid the limits of joins, it has a high processing time.

--9.	With a window function, write a query that shows the film, its duration, and what percentile the duration fits into. This may help https://mode.com/sql-tutorial/sql-window-functions/#rank-and-dense_rank 
SELECT title, length,
	NTILE(100) OVER (ORDER BY length)
	AS percentile
FROM film;

--10.	In under 100 words, explain what the difference is between set-based and procedural programming. Be sure to specify which sql and python are. 
-- Set based languages are declarative; the user is telling the program WHAT they want to happen. In procedural programming, the program is being told HOW to process them.
--SQL is set based, Python is procedural.

--Bonus: Find the relationship that is wrong in the data model. Explain why it’s wrong. 

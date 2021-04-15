SELECT film_id, title, A.replacement_cost, B.AVG(replacement_cost)
JOIN 
WHERE replacement_cost > (SELECT AVG(replacement_cost) FROM film);

SELECT CONCAT(first_name, ' ', last_name) AS name, 

-- select c.first_name || ' ' || c.last_name as name, c.activebool, co country, a.district
-- from customer c, address a, city ci, country co
-- where c.address_id = a.address_id
-- and a.city_id = ci.city_id 
-- and ci.country_id = co.country_id
-- and country like '%United States%'
-- and activebool = 'true'
-- order by district

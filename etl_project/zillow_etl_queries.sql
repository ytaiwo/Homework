--Zillow_ETL Queries

/* Query 1: Combine indicator and category table*/ 
select * from zindicator as i -- get all values from indicator table
inner join category as c --join category table
on c. category_id = i.category_id --join on common key

/* Query 2:
Get region id for UT state*/

select d.zregion_id from region as r
inner join zdata as d
on d.zind_id = r.region_num
where trim(state) = 'UT'

/* Query 3:
Display all the avalibale rentals with their prices: */

select zindicator.indicator_name,
zdata.zdate, zdata.zvalue,
category.category_name,
reg.state --select indicator_name, date, rental value, state, and category name
from zindicator
left join zdata
on zindicator.zind_id = zdata.zind_id
left join category
on category.category_id = zindicator.category_id
left join region reg
ON reg.region_num = zdata.zregion_id --join tables together
where indicator_name = 'RSNA' --indicator name for rentals
and trim(state) = 'IN' --Indiana state


/* Query 4:
Display all the indicators for Inventory and sales category */
select c.category_id,c.category_name, i.zind_id, i.indicator_name, i.indicator from category as c --selection of columns needed
inner join zindicator as i
on c.category_id=i.category_id --join tables together to get the right info
where category_name='Inventory and sales' 

/* Query 5:
sum of all values by state */
SELECT r.state, sum(z.zvalue) --select state and sum of housing values
from region as r 
inner join zdata as z
on z.zind_id = r.region_num --join tables on zillow indicator value and region number
group by r.state --group by state
order by sum DESC --order it in descending form


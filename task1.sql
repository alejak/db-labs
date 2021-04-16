#1
SELECT last_name, first_name FROM authors WHERE author_id = (SELECT author_id FROM books WHERE title = 'The Shining');
100%
#2
SELECT title FROM books WHERE author_id = (SELECT author_id FROM authors WHERE first_name = 'Paulette' and last_name = 'Bourgeois' );
100%
#3
SELECT last_name , first_name
FROM customers c
INNER JOIN shipments s on c.customer_id = s.customer_id
INNER JOIN editions e on s.isbn = e.isbn
INNER JOIN books b on b.book_id=e.book_id
INNER JOIN subjects su on b.subject_id = su.subject_id
WHERE subject = 'Horror';
100%
#4
SELECT title
FROM books b
INNER JOIN editions e on e.book_id = b.book_id
INNER JOIN stock s on s.isbn = e.isbn
WHERE stock = (SELECT MAX(stock) FROM stock);
100%
#5
SELECT SUM(retail_price)
FROM stock s
RIGHT JOIN shipments sh ON s.isbn = sh.isbn
RIGHT JOIN editions e on sh.isbn = e.isbn
RIGHT JOIN books b on b.book_id = e.book_id
RIGHT JOIN subjects su on su.subject_id = b.subject_id
WHERE subject = 'Science Fiction';
100%
#6
SELECT title
FROM books b
INNER JOIN editions e on e.book_id = b.book_id
INNER JOIN shipments s on s.isbn = e.isbn
GROUP BY title
HAVING COUNT(DISTINCT customer_id)=2;
100%
#7
SELECT * FROM(
SELECT p.name, sum(st.cost * (st.stock + s.books_sold)) AS total_sold
FROM stock st
JOIN (
  SELECT isbn, count(isbn) AS books_sold FROM shipments GROUP BY isbn
) AS s ON s.isbn = st.isbn
JOIN editions ed ON ed.isbn = st.isbn
JOIN publishers p USING (publisher_id)
GROUP BY p.name
) x
ORDER BY x.total_sold DESC
LIMIT 1;
100%
#8
SELECT SUM (sh.isbn * (s.retail_price - s.cost))
FROM shipments sh
JOIN stock s on s.isbn = sh.isbn;
#9
select last_name, first_name
from customers
WHERE customer_id in (select customer_id
FROM (SELECT shipment_id, customer_id, subject_id FROM shipments
join(SELECT isbn, title, subject_id from editions
join books on editions.book_id = books.book_id) as a on a.isbn = shipments.isbn
ORDER by customer_id)as a)
group by customer_id having count (subject_id)>=3);
#10
select subject
from subjects
where subject_id not in (
			select s.subject_id from (
					select distinct shipments.shipment_id, a.subject_id
					from shipments

					join (
						select subject_id, a.isbn1, a.isbn2 
						from books
						join (select distinct e1.isbn as isbn1,  e2.isbn as isbn2, e1.book_id 
						from editions as e1, editions as e2 
						where e1.book_id = e2.book_id) as a

						on a.book_id = books.book_id) as a
			on shipments.isbn = a.isbn1 or shipments.isbn = a.isbn2) as s);








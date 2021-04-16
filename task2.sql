#task 2
#1
create view isbntitle as
SELECT isbn, title
FROM books b
join editions e on e.book_id = b.book_id;
drop view isbntitle # it might be nice to have this view in order to quickly access the isbns of all titles
#2
Insert into editions values ('5555', 12345, 1, 59, '2012-12-02');
output -> Key (book_id)=(12345) is not present in table "books".
#3
insert into editions values (isbn='5555');
we get an error because it violates the integrity contstraint saying that "integrity" CHECK (book_id IS NOT NULL AND edition IS NOT NULL)
#4
insert into books values (12345,'How I Insert');
works because book id and title not NULL
insert into editions values ('5555', 12345, 1, 59, '2012-12-02');
this works because we now have a book with the corresponding book id thereby fulfilling the integrity contraint
#5
UPDATE books
 set subject_id = 10 
 where book_id = '12345';
#6
Delete  FROM books where book_id = '12345';
doesnt work because dependency on editions already established
#7
Delete FROM editions where book_id = '12345';
delete from books where book_id = '12345';
#8
insert into books values (12345, 'How I Insert', 3443);
doesnt work because Key (author_id)=(3443) is not present in table "authors".
#9
ALTER TABLE books add constraint hasSubject check(subject_id is not NULL);
ALTER TABLE books DROP constraint hasSubject;
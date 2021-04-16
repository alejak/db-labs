DROP FUNCTION decstock() CASCADE;
CREATE FUNCTION decstock() RETURNS trigger AS $pname$
      BEGIN
             IF (select stock from stock where isbn = NEW.isbn) = 0
                then raise exception 'There is no stock to ship';
             ELSE update stock set stock = stock.stock -1 where isbn = NEW.isbn;
             END IF;
             RETURN NEW;
      END;
$pname$ LANGUAGE plpgsql;
CREATE TRIGGER newShipment
      BEFORE insert on shipments
      FOR EACH ROW
             EXECUTE PROCEDURE decstock();
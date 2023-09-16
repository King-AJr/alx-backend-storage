-- trigger that decreases the quantity of an item after adding a new order.
-- Quantity in the table items can be negative.
DELIMITER //
CREATE TRIGGER decrease_item_quantity
AFTER INSERT
ON orders
FOR EACH ROW
BEGIN
    -- Decrease the quantity of the associated item in the items table
    UPDATE items
    SET quantity = quantity - NEW.number
    WHERE name = NEW.item_name;
END;
//
DELIMITER ;

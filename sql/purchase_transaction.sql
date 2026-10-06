USE EVENT_TICKETING;

DELIMITER $$

CREATE PROCEDURE TransactionalLogicSucceed()
BEGIN
    -- Declare a handler that triggers if ANY SQL error occurs
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- If an error is caught, roll back all changes made in this block
        ROLLBACK;
        SELECT 'Transaction failed and was rolled back.' AS Status;
    END;

    -- Start the transaction
    START TRANSACTION;
	INSERT INTO ORDERS (USER_ID) VALUES (2);
	SELECT ORDER_ID INTO @ORDER_ID FROM ORDERS WHERE USER_ID = 2 ORDER BY ORDER_CREATED DESC LIMIT 1;
	INSERT INTO ORDER_ITEMS(ORDER_ID, EVENT_ID, TICKET_PRICE) VALUES
	(@ORDER_ID, 4, 650),
	(@ORDER_ID, 4, 650),
	(@ORDER_ID, 4, 650),
	(@ORDER_ID, 4, 650),
	(@ORDER_ID, 4, 650);
	INSERT INTO PAYMENTS(ORDER_ID, PAYMENT_AMT) VALUES (6, 3.50);
    COMMIT;
    SELECT 'Transaction completed successfully.' AS Status;
END $$

CREATE PROCEDURE TransactionalLogicFail()
BEGIN
    -- Declare a handler that triggers if ANY SQL error occurs
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        -- If an error is caught, roll back all changes made in this block
        ROLLBACK;
        SELECT 'Transaction failed and was rolled back.' AS Status;
    END;

    -- Start the transaction
    START TRANSACTION;
	INSERT INTO ORDERS (USER_ID) VALUES (2);
	SELECT ORDER_ID INTO @ORDER_ID FROM ORDERS WHERE USER_ID = 2 ORDER BY ORDER_CREATED DESC LIMIT 1;
	INSERT INTO ORDER_ITEMS(ORDER_ID, EVENT_ID, TICKET_PRICE) VALUES
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50), (@ORDER_ID, 1, 50),
	(@ORDER_ID, 1, 50);
	INSERT INTO PAYMENTS(ORDER_ID, PAYMENT_AMT) VALUES (6, 3.50);
    COMMIT;
    SELECT 'Transaction completed successfully.' AS Status;
END $$

DELIMITER ;

#CALL TransactionalLogicSucceed();
#CALL TransactionalLogicFail();

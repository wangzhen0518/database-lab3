drop trigger update_account_on_insert;
delimiter //
CREATE 
    TRIGGER  update_account_on_insert
 AFTER INSERT ON loan_record FOR EACH ROW 
    BEGIN 
		update cheque_account 
        set recent_visited=NOW(),overdraft=overdraft+new.loanRecord_amount
        where account_id=(
        select customer_account.cheque_account as temp_id
        from customer_account
        where customer_account.customer_id=new.customer_id and customer_account.subbank_name=new.subbank_name
        LIMIT 1);
    END//
delimiter ;

drop trigger update_account_on_delete;
delimiter //
CREATE 
    TRIGGER  update_account_on_delete
 BEFORE DELETE ON loan_record FOR EACH ROW 
    BEGIN 
		update cheque_account 
        set recent_visited=NOW(),overdraft=overdraft-old.loanRecord_amount
        where account_id=(
        select customer_account.cheque_account as temp_id
        from customer_account
        where customer_account.customer_id=old.customer_id and customer_account.subbank_name=old.subbank_name
        LIMIT 1  );
    END//
delimiter ;

alter table loan_record
modify loanRecord_date timestamp;

delimiter //
CREATE PROCEDURE count_loan (IN id char(20),OUT release_amount float, OUT tol_amount float) 
BEGIN
	select SUM(loan_record.loanRecord_amount), loan_record.total_amount into release_amount, tol_amount
    FROM loan_record
    where loan_record.loan_id=id
    group by loan_record.loan_id,loan_record.total_amount;
END //
delimiter ;

select loan_record.total_amount , SUM(loan_record.loanRecord_amount) as _sum,loan_record.loan_id
    FROM loan_record
    where loan_record.loan_id='123412'
    group by loan_record.loan_id;

call count_loan('123412',@release_amount,@tol_amount);
select @release_amount,@tol_amount;

drop trigger insert_loan_record;

delimiter //
CREATE 
    TRIGGER  insert_loan_record
 BEFORE INSERT ON loan_record FOR EACH ROW 
    BEGIN 
		update cheque_account 
        set recent_visited=NOW(),overdraft=overdraft-old.loanRecord_amount
        where account_id=(
        select customer_account.cheque_account as temp_id
        from customer_account, loan_record
        where customer_account.customer_id=loan_record.customer_id and customer_account.subbank_name=loan_record.subbank_name
        );
    END//
delimiter ;

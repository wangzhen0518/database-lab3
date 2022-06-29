/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2022/06/09 17:08:31                          */
/*==============================================================*/


drop table if exists cheque_account;

drop table if exists customer;

drop table if exists customer_account;

drop table if exists customer_staff;

drop table if exists department;

drop table if exists deposit_account;



drop table if exists staff;

/*==============================================================*/
/* Table: cheque_account                                        */
/*==============================================================*/
create table cheque_account
(
   account_id       char(20) not null,
   balance              float,
   start_date           date,
   bank                 char(20) not null,
   recent_visited       date,
   overdraft            float,
   primary key (account_id)
);

/*==============================================================*/
/* Table: customer                                              */
/*==============================================================*/
create table customer
(
   customer_id          char(18) not null,
   customer_name        char(10) not null,
   customer_phone       char(11) not null,
   customer_address     char(50),
   ex_id                char(18) not null,
   ex_name              char(10) not null,
   ex_phone             char(11) not null,
   ex_address           char(50),
   ex_email             char(30),
   relationship         char(5) not null,
   primary key (customer_id)
);

/*==============================================================*/
/* Table: customer_account                                      */
/*==============================================================*/
create table customer_account
(
   customer_id          char(18) not null,
   subbank_name         char(10) not null,
   deposit_account      char(20),
   cheque_account       char(20),
   primary key (customer_id, subbank_name)
);

/*==============================================================*/
/* Table: customer_staff                                        */
/*==============================================================*/
create table customer_staff
(
   customer_id          char(18) not null,
   subbank_name         char(10) not null,
   account_staff        char(18),
   staff_id             char(18),
   primary key (customer_id, subbank_name)
);

/*==============================================================*/
/* Table: department                                            */
/*==============================================================*/
create table department
(
   department_id        char(8) not null,
   subbank_name         char(10) not null,
   staff_id             char(18),
   department_type      char(5) not null,
   department_name      char(10) not null,
   primary key (department_id, subbank_name)
);

/*==============================================================*/
/* Table: deposit_account                                       */
/*==============================================================*/
create table deposit_account
(
   account_id      char(20) not null,
   balance              float,
   start_date           date,
   bank                 char(20) not null,
   recent_visited       date,
   rate                 float not null,
   currency_type        char(5) not null,
   primary key (account_id)
);

/*==============================================================*/
/* Table: loan_record                                           */
/*==============================================================*/
drop table if exists loan_record;
create table loan_record
(
   loan_id              char(20) not null,
   customer_id          char(18) not null,
   subbank_name         char(10) not null,
   loanRecord_date      timestamp DEFAULT CURRENT_TIMESTAMP not null,
   loanRecord_amount   float not null,
   total_amount         float,
   sequence             integer  not null AUTO_INCREMENT,
   primary key (sequence,subbank_name, customer_id, loan_id)
);

/*==============================================================*/
/* Table: staff                                                 */
/*==============================================================*/
create table staff
(
   staff_id             char(18) not null,
   staff_name           char(10) not null,
   staff_address        char(50),
   staff_phone          char(11) not null,
   department_id        char(8) not null,
   staff_start_date     date not null,
   staff_type           char not null,
   primary key (staff_id)
);

alter table customer_account add constraint FK_account2customer foreign key (customer_id)
      references customer (customer_id) on delete cascade on update cascade;

alter table customer_account add constraint FK_customerChequeAccount foreign key (cheque_account)
      references cheque_account (account_id) on delete set null on update cascade;

alter table customer_account add constraint FK_customerDepositAccount foreign key (deposit_account)
      references deposit_account (account_id) on delete set null on update cascade;

alter table customer_staff add constraint FK_account_staff foreign key (account_staff)
      references staff (staff_id) on delete set null on update cascade;

alter table customer_staff add constraint FK_customer_staff foreign key (customer_id)
      references customer (customer_id) on delete cascade on update cascade;

alter table customer_staff add constraint FK_loan_staff foreign key (staff_id)
      references staff (staff_id) on delete set null on update cascade;

alter table department add constraint FK_departmentManager foreign key (staff_id)
      references staff (staff_id) on delete cascade on update cascade;

alter table loan_record add constraint FK_loanRecord2customer foreign key (customer_id)
      references customer (customer_id) on delete restrict on update cascade;

alter table staff add constraint FK_department2staff foreign key (department_id)
      references department (department_id) on delete cascade on update cascade;


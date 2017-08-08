
select * from user_interaction limit 100

# Create a row number
create table user_interaction_rank
SELECT t.*, 
       @rownum := @rownum + 1 AS rank
  FROM user_interaction t, 
       (SELECT @rownum := 0) r

# Create a row number - 1 , to be able to join the "next" interaction to the current interaction
create table user_interaction_pre_row
select *
,(rank - 1) as pre_row 
from user_interaction_rank

# Check
select * from user_interaction_pre_row limit 100

# Add indexs

ALTER TABLE `user_interaction_pre_row` ADD INDEX rank_index (`rank`);

ALTER TABLE `user_interaction_pre_row` ADD INDEX pre_row_index (`pre_row`);

ALTER TABLE `user_interaction_pre_row` ADD INDEX userID_index (`userID`);


# join table to get "next" interaction to the current interaction
create table user_interaction_next_interaction
select a.* 
,b.targetID as next_targetID
,b.interaction as next_interaction
from user_interaction_pre_row as a
left join user_interaction_pre_row as b
on a.userID = b.userID
and a.rank = b.pre_row;

select * from user_interaction_next_interaction limit 1000

# Creating distinct user id table to be able to split the data by users
create table users
select distinct userID from user_interaction;

select count(*) , count(distinct userID) from user_interaction;
select count(*) , count(distinct userID) from user_interaction_next_interaction;
select count(*) , count(distinct userID) from users;


# Create smaller tables of 50 000 users each , because of RAM restrictions 

create table users1
select * from users
limit 50000

create table users2
select * from users
limit 50000 OFFSET 50000

create table users3
select * from users
limit 50000 OFFSET 100000

select count(distinct userID) as cc from users1
union all
select count(distinct userID) as cc from users2
union all 
select count(distinct userID) as cc from users3

select * from user_interaction_next_interaction limit 10 ;
select * from users1 limit 10 ;

ALTER TABLE `user_interaction_next_interaction` ADD INDEX userID_index (`userID`);
ALTER TABLE `users1` ADD INDEX userID_index (`userID`);
ALTER TABLE `users2` ADD INDEX userID_index (`userID`);
ALTER TABLE `users3` ADD INDEX userID_index (`userID`);


create table user_interaction_next_interaction1
select a.* from user_interaction_next_interaction as a
inner join users1 as b
on a.userID = b.userID;

select count(*) , count(distinct userID) from user_interaction_next_interaction1;

delete from user_interaction_next_interaction1 where next_interaction is null

create table user_interaction_next_interaction2
select a.* from user_interaction_next_interaction as a
inner join users2 as b
on a.userID = b.userID;

create table user_interaction_next_interaction3
select a.* from user_interaction_next_interaction as a
inner join users3 as b
on a.userID = b.userID;


select * from user_interaction_next_interaction1
limit 1000
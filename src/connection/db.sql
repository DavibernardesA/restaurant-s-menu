drop if exists restaurant_db
create database restaurant_db

create table menu (
    id serial primary key,
    name varchar(255) not null
);

alter table menu
add column description text,
add column price decimal(10, 2),
add column available boolean default true;

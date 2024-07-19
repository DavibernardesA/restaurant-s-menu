drop if exists restaurant_db
create database restaurant_db

create table menu (
    id serial primary key,
    name varchar(255) not null
    description text,
    price decimal(10, 2),
    available boolean default true;
);
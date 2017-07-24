
drop database if exists demo;
create database demo;
use demo;

-- New Scripts
drop table if exists countries;
CREATE TABLE `countries` (
  `country_id` int(11) NOT NULL AUTO_INCREMENT,
  `country_name` varchar(500) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `last_updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`country_id`)
)

drop table if exists states_provs;
CREATE TABLE `states_provs` (
 `state_prov_id` int(11) NOT NULL AUTO_INCREMENT,
 `state_name` varchar(500) DEFAULT NULL,
 `country_id` int(11) DEFAULT NULL,
 `created_date` datetime DEFAULT NULL,
 `last_updated_date` datetime DEFAULT NULL,
 PRIMARY KEY (`state_prov_id`),
 KEY `country_id` (`country_id`),
 CONSTRAINT `states_provs_ibfk_1` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`)
)

drop table if exists customer;
CREATE TABLE `customer` (
  `customer_id` int(11) NOT NULL AUTO_INCREMENT,
  `customer_name` varchar(500) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL,
  `city` varchar(100) DEFAULT NULL,
  `state_prov_id` int(11) DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `postal_code` varchar(20) DEFAULT NULL,
  `ship_to` int(11) DEFAULT NULL,
  `sold_to` int(11) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `last_updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  KEY `state_prov_id` (`state_prov_id`),
  KEY `country_id` (`country_id`),
  CONSTRAINT `customer_ibfk_1` FOREIGN KEY (`state_prov_id`) REFERENCES `states_provs` (`state_prov_id`),
  CONSTRAINT `customer_ibfk_2` FOREIGN KEY (`country_id`) REFERENCES `countries` (`country_id`)
)

drop table if exists products;
CREATE TABLE `products` (
 `product_id` int(11) NOT NULL AUTO_INCREMENT,
 `product_number` varchar(100) DEFAULT NULL,
 `product_name` varchar(500) DEFAULT NULL,
 `description` varchar(2000) DEFAULT NULL,
 `uom` varchar(20) DEFAULT NULL,
 `manufacturer_id` int(11) DEFAULT NULL,
 `family_id` int(11) DEFAULT NULL,
 `subfamily_id` int(11) DEFAULT NULL,
 PRIMARY KEY (`product_id`),
 KEY `family_id` (`family_id`),
 KEY `subfamily_id` (`subfamily_id`),
 CONSTRAINT `products_ibfk_1` FOREIGN KEY (`family_id`) REFERENCES `product_subfamily` (`family_id`),
 CONSTRAINT `products_ibfk_2` FOREIGN KEY (`subfamily_id`) REFERENCES `product_subfamily` (`subfamily_id`)
)

drop table if exists product_family;
CREATE TABLE `product_family` (
 `family_id` int(11) NOT NULL AUTO_INCREMENT,
 `product_family_name` varchar(5000) DEFAULT NULL,
 PRIMARY KEY (`family_id`)
)

drop table if exists product_subfamily;
CREATE TABLE `product_subfamily` (
 `subfamily_id` int(11) NOT NULL AUTO_INCREMENT,
 `product_subfamily_name` varchar(500) DEFAULT NULL,
 `family_id` int(11) DEFAULT NULL,
 PRIMARY KEY (`subfamily_id`),
 KEY `family_id` (`family_id`),
 CONSTRAINT `product_subfamily_ibfk_1` FOREIGN KEY (`family_id`) REFERENCES `product_family` (`family_id`)
)

drop table if exists product_costs;
CREATE TABLE `product_costs` (
 `cost_id` int(11) NOT NULL AUTO_INCREMENT,
 `product_id` int(11) DEFAULT NULL,
 `mtl_cost` decimal(10,0) DEFAULT NULL,
 `labor_cost` decimal(10,0) DEFAULT NULL,
 `burden_cost` decimal(10,0) DEFAULT NULL,
 PRIMARY KEY (`cost_id`)
)

drop table if exists products_prices;
CREATE TABLE `products_prices` (
 `price_id` int(11) NOT NULL AUTO_INCREMENT,
 `price_list_id` int(11) DEFAULT NULL,
 `product_id` int(11) DEFAULT NULL,
 `list_price` decimal(10,0) DEFAULT NULL,
 PRIMARY KEY (`price_id`),
 KEY `price_list_id` (`price_list_id`),
 KEY `product_id` (`product_id`),
 CONSTRAINT `products_prices_ibfk_1` FOREIGN KEY (`price_list_id`) REFERENCES `price_lists` (`price_list_id`),
 CONSTRAINT `products_prices_ibfk_2` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
)

drop table if exists price_lists;
CREATE TABLE `price_lists` (
  `price_list_id` int(11) NOT NULL AUTO_INCREMENT,
  `active` tinyint(1) DEFAULT NULL,
  `list_start_date` date DEFAULT NULL,
  `list_end_date` date DEFAULT NULL,
  PRIMARY KEY (`price_list_id`)
)

drop table if exists shipping_types;
CREATE TABLE `shipping_types` (
 `shipping_type_id` int(11) NOT NULL AUTO_INCREMENT,
 `description` varchar(100) DEFAULT NULL,
 `cost` int(11) DEFAULT NULL,
 `created_date` datetime DEFAULT NULL,
 `last_updated_date` datetime DEFAULT NULL,
 PRIMARY KEY (`shipping_type_id`)
)

drop table if exists order_headers;
CREATE TABLE `order_header` (
  `header_id` int(11) NOT NULL AUTO_INCREMENT,
  `order_number` varchar(20) DEFAULT NULL,
  `sold_to_id` varchar(20) DEFAULT NULL,
  `po_id` varchar(20) DEFAULT NULL,
  `currency` varchar(5) DEFAULT NULL,
  `created_date` datetime DEFAULT NULL,
  `last_updated_date` datetime DEFAULT NULL,
  PRIMARY KEY (`header_id`)
)

drop table if exists order_line;
CREATE TABLE `order_line` (
 `line_id` int(11) NOT NULL AUTO_INCREMENT,
 `header_id` int(11) DEFAULT NULL,
 `shipping_type_id` int(11) DEFAULT NULL,
 `line_number` int(11) DEFAULT NULL,
 `schedule_ship_date` datetime DEFAULT NULL,
 `quantity` int(11) DEFAULT NULL,
 `product_id` int(11) DEFAULT NULL,
 `price_list_id` int(11) DEFAULT NULL,
 `discount` float DEFAULT NULL,
 `net_price` float DEFAULT NULL,
 `created_date` datetime DEFAULT NULL,
 `last_updated_date` datetime DEFAULT NULL,
 PRIMARY KEY (`line_id`),
 KEY `header_id` (`header_id`),
 KEY `shipping_type_id` (`shipping_type_id`),
 KEY `product_id` (`product_id`),
 CONSTRAINT `order_line_ibfk_1` FOREIGN KEY (`header_id`) REFERENCES `order_header` (`header_id`),
 CONSTRAINT `order_line_ibfk_2` FOREIGN KEY (`shipping_type_id`) REFERENCES `shipping_types` (`shipping_type_id`),
 CONSTRAINT `order_line_ibfk_3` FOREIGN KEY (`product_id`) REFERENCES `products` (`product_id`)
)



create or replace view current_product_prices as
select pp.product_id, pp.list_price, pl.price_list_id
from products_prices pp
inner join price_lists pl
on pp.price_list_id = pl.price_list_id
where pl.price_list_id = true
;

create or replace view current_product_costs as
 select pc.product_id, pc.mtl_cost, pc.labor_cost, pc.burden_cost, pc.cost_id, pc.created_date
 from product_costs pc
 inner join (
   select max(cost_id) as cost_id, product_id
   from product_costs
   group by 2
   ) most_recent
 on pc.cost_id = most_recent.cost_id
;

-- drop database if exists test_electronics;
-- create database test_electronics;
-- use test_electronics;
--
--
-- drop table if exists order_headers;
--
-- create table order_headers (
--  header_id int not null,
--  order_number varchar(20) not null,
--  sold_to_id int not null,
--  ship_to_id int not null ,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  po_id varchar(10),
--  currency varchar(5),
--  primary key (header_id),
--  Foreign key (sold_to_id) references customers(customer_id),
--  Foreign key (ship_to_id) references customers(customer_id)
-- );
--
--
-- drop table if exists order_lines;
--
-- create table order_lines (
--  line_id int not null,
--  header_id int not null,
--  line_number int not null,
--  schedule_ship_date date,
--  quantity int,
--  product_id int ,
--  price_list_id int,
--  discount decimal(2,2),
--  net_price decimal(6,2),
--  shipping_type_id int,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (line_id),
--  Foreign key (header_id) references order_headers(header_id),
--  Foreign key (product_id) references products(product_id),
--  Foreign key (price_list_id) references price_lists(price_list_id),
--  Foreign key (shipping_type_id) references shipping_types(shipping_type_id)
-- );
--
--
-- drop table if exists shipping_types;
--
-- create table shipping_types (
--  shipping_type_id int not null,
--  description varchar(100),
--  cost decimal(5,2),
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (shipping_type_id)
-- );
--
--
-- drop table if exists customers;
--
-- create table customers (
--  customer_id int not null,
--  name varchar(500),
--  address_1 varchar(100),
--  address_2 varchar(100),
--  city varchar(100),
--  state_prov_id int references state_prov(state_prov_id),
--  country_id int references state_prov(country_id),
--  postal_code varchar(20),
--  ship_to boolean,
--  sold_to boolean,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (customer_id)
-- );
--
--
--
-- drop table if exists states_provs;
--
-- create table states_provs (
--  state_prov_id int not null,
--  name varchar(500),
--  country_id int not null,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (state_prov_id),
--  Foreign key (country_id) references countries(country_id)
-- );
--
--
-- drop table if exists countries;
--
-- create table countries (
--  country_id int not null,
--  name varchar(500) not null,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (country_id)
-- );
--
-- -- products
-- drop table if exists products;
--
-- create table products (
--  product_id int not null auto_increment,
--  product_number varchar(100) not null,
--  name varchar(500),
--  description varchar(2000),
--  uom varchar(20) not null,
--  manufacturer_id int,
--  family_id int not null,
--  subfamily_id int not null,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (product_id) ,
--  Foreign Key (family_id) references product_family(family_id),
--  Foreign Key (subfamily_id) references product_subfamily(subfamily_id)
-- );
--
--
-- drop table if exists product_subfamily;
--
-- create table product_subfamily (
--  subfamily_id int not null auto_increment,
--  name varchar(500),
--  family_id int not null,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (subfamily_id),
--  Foreign key (family_id) references product_family(family_id)
-- );
--
--
-- drop table if exists product_family;
--
-- create table product_family (
--  family_id int not null auto_increment,
--  name varchar(500),
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (family_id)
-- );
--
--
-- drop table if exists product_costs;
--
-- create table product_costs (
--  cost_id int not null auto_increment,
--  product_id int not null,
--  mtl_cost decimal(6, 2),
--  labor_cost decimal(6,2),
--  burden_cost decimal(6,2),
--  created_date timestamp default current_timestamp,
--  primary key (cost_id),
--  Foreign key (product_id) references products(product_id)
-- );
--
--
--
-- create or replace view current_product_costs as
--  select pc.product_id, pc.mtl_cost, pc.labor_cost, pc.burden_cost, pc.cost_id, pc.created_date
--  from product_costs pc
--  inner join (
--    select max(cost_id) as cost_id, product_id
--    from product_costs
--    group by 2
--    ) most_recent
--  on pc.cost_id = most_recent.cost_id
-- ;
--
-- drop table if exists products_prices;
--
-- create table products_prices (
--    price_list_id int not null,
--    product_id int not null,
--    list_price decimal(6,2),
--    created_date timestamp default current_timestamp,
--  Foreign Key (price_list_id) references price_lists(price_list_id),
--    Foreign Key (product_id) references products(product_id)
-- );
--
-- drop table if exists price_lists;
--
-- create table price_lists (
--  price_list_id int not null auto_increment,
--  active boolean,
--  list_start_date date,
--  list_end_date date,
--  created_date timestamp default current_timestamp,
--  last_updated_date timestamp default current_timestamp,
--  primary key (price_list_id)
-- );

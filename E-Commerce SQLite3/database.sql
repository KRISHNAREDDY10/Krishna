CREATE TABLE IF NOT EXISTS products ('
        product_id integer PRIMARY KEY, 
        product_name text,
        selling_price integer not null,
        inventory integer not null,
        ');



CREATE TABLE If NOT EXISTS customers ('
        customers_id integer not null PRIMARY KEY,
        customer_name text not null,
        address text not null,
        phone integer not null,
        email text not null,
        ');


CREATE TABLE If NOT EXISTS orders ('
        order_id integer not null PRIMARY KEY,
        product_id integer not null,
        product_name text not null,
        customer_id integer not null,
        quantity integer not null,
        FOREIGN KEY (product_id) REFERENCES products(product_id),
        '); 
#! /usr/bin/env python3
# coding: utf-8


"""
This script collect the data from the Openfoodfacts file in CSV format.

Then, the script will create the database of the application and will
insert the data collected into the table.

Author: Alix VOINOT

"""

import pymysql
from constant import *

def csv_reader():
    pass


# Create an acces to the database
def db_connect():
    
    conn = pymysql.connect(host="localhost",\
                                user="root",\
                                password="")
    return conn


# Create all the table of the database
def create_db(cursor):

    cursor.execute(""" DROP DATABASE IF EXISTS purbeurre; """)
    cursor.execute(""" CREATE DATABASE purbeurre; """)
    cursor.execute(""" USE purbeurre; """)
    
    cursor.execute("""SET NAMES utf8;""")
    cursor.execute("""SET CHARACTER SET utf8;""")
    cursor.execute("""SET character_set_connection=utf8;""")

    # Delete all the previous table from the database
    cursor.execute(""" DROP TABLE IF EXISTS saved_substitute; """) 
    cursor.execute(""" DROP TABLE IF EXISTS product; """)
    cursor.execute(""" DROP TABLE IF EXISTS category; """)
    cursor.execute(""" DROP TABLE IF EXISTS nutriscore; """)
    cursor.execute(""" DROP TABLE IF EXISTS brand; """)
    cursor.execute(""" DROP TABLE IF EXISTS store; """)
    
    
    

    # Create the table category
    cursor.execute(""" CREATE TABLE category (
                        id_category TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        PRIMARY KEY(id_category)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)

    # Create the table nutriscore
    cursor.execute(""" CREATE TABLE nutriscore (
                        id_nutriscore TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        value VARCHAR(1) NOT NULL,
                        PRIMARY KEY(id_nutriscore)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)
    

    # Create the table brand
    cursor.execute(""" CREATE TABLE brand (
                        id_brand MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        PRIMARY KEY(id_brand)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)

    # Create the table store
    cursor.execute(""" CREATE TABLE store (
                        id_store MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        PRIMARY KEY(id_store)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)
    
    # Create the table product
    cursor.execute(""" CREATE TABLE product (
                        id_product BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        id_category TINYINT UNSIGNED NOT NULL,
                        id_brand MEDIUMINT UNSIGNED NOT NULL,
                        id_store MEDIUMINT UNSIGNED NOT NULL,
                        id_nutriscore TINYINT UNSIGNED NOT NULL,
                        url VARCHAR(100) NOT NULL,
                        PRIMARY KEY(id_product),
                        CONSTRAINT fk_category
                            FOREIGN KEY(id_category)
                            REFERENCES category(id_category),
                        CONSTRAINT fk_brand
                            FOREIGN KEY(id_brand)
                            REFERENCES brand(id_brand),
                        CONSTRAINT fk_nutriscore
                            FOREIGN KEY(id_nutriscore)
                            REFERENCES nutriscore(id_nutriscore),
                        CONSTRAINT fk_store
                            FOREIGN KEY(id_store)
                            REFERENCES store(id_store)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)
    
    # Create the table savedsubstitute
    cursor.execute(""" CREATE TABLE saved_substitute (
                        id_saved_substitute INT UNSIGNED NOT NULL AUTO_INCREMENT,
                        id_product BIGINT UNSIGNED NOT NULL,
                        id_substitute BIGINT UNSIGNED NOT NULL,
                        PRIMARY KEY(id_saved_substitute),
                        CONSTRAINT fk_prod
                            FOREIGN KEY(id_product)
                            REFERENCES product(id_product),
                        CONSTRAINT fk_sub
                            FOREIGN KEY(id_substitute)
                            REFERENCES product(id_product)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)

# Insert data in the table nutriscore                        
def insert_nutriscore(cursor, nutri):
    
    cursor.execute("""
                    INSERT INTO nutriscore(value)
                    VALUES("{}");""" .format(nutri))

# Insert data in the table brand
def insert_brand(cursor, brand):

    cursor.execute("""
                    INSERT INTO brand(name)
                    VALUES("{}");""" .format(brand))

# Insert data in the table store
def insert_store(cursor, store):

    cursor.execute("""
                    INSERT INTO store(name)
                    VALUES("{}");""" .format(store))

# Insert data in the table category
def insert_category(cursor, categ):

    cursor.execute("""
                    INSERT INTO category(name)
                    VALUES("{}");""" .format(categ))
                        

    

def main():
        conn = db_connect()
        cursor = conn.cursor()
        create_db(cursor)
        for x in nutriscore:
            insert_nutriscore(cursor, x)
        conn.commit()
        conn.close()
    
if __name__ == "__main__":
    main()

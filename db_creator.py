#! /usr/bin/env python3
# coding: utf-8


"""
This script collect the data from the Openfoodfacts file in CSV format.

Then, the script will create the database of the application and will
insert the data collected into the table.

Author: Alix VOINOT

"""

import pymysql
import sys
from constant import *
import csv

def csv_reader(file, conn):

    cursor = conn.cursor()
    csv.field_size_limit(sys.maxsize)
    file =  open(file, newline='', encoding ="utf8") 
    reader = csv.reader(file, delimiter = '	')
    for row in reader:
        brand = str(row[12])
        category = str(row[16])
        store = str(row[30])
        cursor.execute("""
                    INSERT INTO category(name)
                    SELECT %s
                    WHERE
                    NOT EXISTS (
                    	SELECT name FROM category WHERE name = %s
                    	)""",  (category, category))
        cursor.execute("""
                    INSERT INTO brand(name)
                    SELECT %s
                    WHERE
                    NOT EXISTS (
                    	SELECT name FROM brand WHERE name = %s
                    	)""",  (brand, brand))
        cursor.execute("""
                    INSERT INTO store(name)
                    SELECT %s
                    WHERE
                    NOT EXISTS (
                    	SELECT name FROM store WHERE name = %s
                    	)""",  (store, store))
        



# Create an acces to the database
def db_connect():
    
    conn = pymysql.connect(host="localhost",\
                                user="root",\
                                password="",\
                                charset="utf8")
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
                        id_category MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(1000) NOT NULL,
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
                        name VARCHAR(200) NOT NULL,
                        PRIMARY KEY(id_brand)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)

    # Create the table store
    cursor.execute(""" CREATE TABLE store (
                        id_store MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(200) NOT NULL,
                        PRIMARY KEY(id_store)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)
    
    # Create the table product
    cursor.execute(""" CREATE TABLE product (
                        id_product BIGINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(40) NOT NULL,
                        id_category MEDIUMINT UNSIGNED NOT NULL,
                        id_brand MEDIUMINT UNSIGNED NOT NULL,
                        id_store MEDIUMINT UNSIGNED NOT NULL,
                        id_nutriscore TINYINT UNSIGNED NOT NULL,
                        url VARCHAR(1000) NOT NULL,
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

                        
def main():
        conn = db_connect()
        cursor = conn.cursor()
        create_db(cursor)
        #csv_reader(file1, conn)
        conn.commit()
        conn.close()
    
if __name__ == "__main__":
    main()

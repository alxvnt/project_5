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
                                password="",\
                                database="purbeurre")
    return conn



def create_db(conn):
    
    cursor = conn.cursor()
    cursor.execute("""SET NAMES utf8;""")
    cursor.execute("""SET CHARACTER SET utf8;""")
    cursor.execute("""SET character_set_connection=utf8;""")

    # Delete all the previous table from the database
    cursor.execute(""" DROP TABLE IF EXISTS saved_substitute; """) 
    cursor.execute(""" DROP TABLE IF EXISTS product; """)
    cursor.execute(""" DROP TABLE IF EXISTS category; """)
    #cursor.execute(""" DROP TABLE IF EXISTS nutriscore; """)
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
##    cursor.execute(""" CREATE TABLE nutriscore (
##                        id_nutriscore TINYINT UNSIGNED NOT NULL AUTO_INCREMENT,
##                        value VARCHAR(1) NOT NULL,
##                        PRIMARY KEY(id_nutriscore)
##                        )
##                        ENGINE = InnoDB
##                        DEFAULT CHARSET = utf8; """)
##    

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
                        url VARCHAR(100) NOT NULL,
                        PRIMARY KEY(id_product),
                        CONSTRAINT fk_category
                            FOREIGN KEY(id_category)
                            REFERENCES category(id_category),
                        CONSTRAINT fk_brand
                            FOREIGN KEY(id_brand)
                            REFERENCES brand(id_brand),
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
                        
def insert_nutriscore(conn, category):
    
    cursor = conn.cursor()
    cursor.execute("""
                    INSERT INTO category(name)
                    VALUES("{}");""" .format(category))

    
                        

    

def main():
        conn = db_connect()
        create_db(conn)
        for x in nutriscore:
            insert_nutriscore(conn, x)
        conn.commit()
        conn.close()
    
if __name__ == "__main__":
    main()

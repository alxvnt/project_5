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
    header = next(reader)
    for row in reader:
        try:
            url = str(row[1])
            name = str(row[7])
            brand = str(row[12])
            category = categ_pars(row[16])
            store = str(row[30])
            nutriscore = str(row[164])
            list1 = []
            list1.append([str(row[7]), categ_pars(row[16]), str(row[12]), str(row[30]), str(row[164]), str(row[1])])
            if ( (0 < len(list1[0][0]) < 30) and (list1[0][1]) and (0 < len(list1[0][2]) < 25) and (0 < len(list1[0][3]) < 25) and (list1[0][4]) and (0 < len(list1[0][5]) < 100)):
                print(list1)
                cursor.execute("""
                    INSERT INTO category(name)
                    SELECT %s
                    WHERE
                    NOT EXISTS (
                    	SELECT name FROM category WHERE name = %s
                    	)""",  (list1[0][1], list1[0][1]))
                cursor.execute("""
                    INSERT INTO brand(name)
                    SELECT %s
                    WHERE
                    NOT EXISTS (
                    	SELECT name FROM brand WHERE name = %s
                    	)""",  (list1[0][2], list1[0][2]))
                cursor.execute("""
                    INSERT INTO store(name)
                    SELECT %s
                    WHERE
                    NOT EXISTS (
                    	SELECT name FROM store WHERE name = %s
                    	)""",  (list1[0][3], list1[0][3]))
                cursor.execute("""
                    INSERT INTO product
                    SET name = %s, id_category = (SELECT id_category FROM category WHERE name = %s), 
                        id_brand = (SELECT id_brand FROM brand WHERE name = %s),
                        id_store = (SELECT id_store FROM store WHERE name = %s),
                        nutriscore = %s,
                        url = %s
                        """, (list1[0][0], list1[0][1], list1[0][2], list1[0][3], list1[0][4], list1[0][5]))
        except IndexError:
            pass
        except UnicodeEncodeError:
            pass
        

def categ_pars(var):

    new_categ = ""
    for categories in pb_categories:
        if categories in var:
            new_categ = categories
    return new_categ



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
    cursor.execute(""" DROP TABLE IF EXISTS brand; """)
    cursor.execute(""" DROP TABLE IF EXISTS store; """)
    
    
    

    # Create the table category
    cursor.execute(""" CREATE TABLE category (
                        id_category MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(50) NOT NULL,
                        PRIMARY KEY(id_category)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)
    

    # Create the table brand
    cursor.execute(""" CREATE TABLE brand (
                        id_brand MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(50) NOT NULL,
                        PRIMARY KEY(id_brand)
                        )
                        ENGINE = InnoDB
                        DEFAULT CHARSET = utf8; """)

    # Create the table store
    cursor.execute(""" CREATE TABLE store (
                        id_store MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
                        name VARCHAR(50) NOT NULL,
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
                        nutriscore TINYINT NOT NULL,
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

                        
def main():
        conn = db_connect()
        cursor = conn.cursor()
        create_db(cursor)
        csv_reader(file1, conn)
        conn.commit()
        conn.close()
    
if __name__ == "__main__":
    main()

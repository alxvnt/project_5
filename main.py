#! /usr/bin/env python3
# coding: utf-8


"""
This script contains the main function of the PurBeurre Project.

Author: Alix VOINOT

"""

import pymysql
from classes import *

# Create an access to the database

def db_connect():
    conn = pymysql.connect(host="localhost",\
                                    user="root",\
                                    password="",\
                                    database="purbeurre",\
                                    charset="utf8")
    return conn

# Print the list of categories
def display_categories(conn):

    cursor = conn.cursor()
    cursor.execute("""SELECT name FROM category""")
    row = cursor.fetchone()
    x = 0
    while row is not None:
        x+=1
        print( str(x) + ")" + row[0])
        row = cursor.fetchone()

        

# Print the list of the product in the select category
def list_product(conn, id_category):

    cursor = conn.cursor()
    cursor.execute(""" SELECT name FROM product WHERE id_category = %s """,(id_category))
    row = cursor.fetchone()
    x = 0
    while row is not None:
        x+=1
        print( str(x) + ")" + row[0])
        row = cursor.fetchone()



# Print the chosen product and all the information about him
def display_product(conn, id_product):
    
    cursor = conn.cursor()
    cursor.execute(""" SELECT p.id_product, p.name, c.name, b.name, s.name, n.value, p.url FROM product p
                        JOIN category c ON c.id_category = p.id_category
                        JOIN brand b ON b.id_brand = p.id_brand
                        JOIN store s ON s.id_store = p.id_store
                        JOIN nutriscore n ON n.id_nutriscore = p.id_nutriscore
                        WHERE id_product = %s""", (id_product))
    row = cursor.fetchone()
    id_prod = row[0]
    name = row[1]
    categ = row[2]
    brand = row[3]
    store = row[4]
    nutriscore = row[5]
    url = row[6]
    prod = Product(id_prod, name, categ, brand, store, nutriscore, url)
    prod.display()
    

def save_sub(prod1, prod2, conn):

    cursor = conn.cursor()
    cursor.execute(""" INSERT INTO saved_substitute(id_product, id_substitute
                    """, (prod1.id_prod, prod2.id_prod))

def find_sub(conn):

    cursor = conn.cursor()
    cursor.execute("""SELECT p.name, s.id_product FROM product p
                      JOIN saved_substitute s ON s.id_product = p.id_product
                        """)

def main():
    
    conn = db_connect()
    
    
    loop = True
    
    while loop:
        
        print("1) Remplacer un aliment")
        print("2) Retrouver un aliment substitué")
        
        choice = input(" Choix : ")

        if choice == '1':
            print("Vous avez choisi de remplacer un aliment")
            
            #Nouvel boucle
            display_categories(conn)
            choice_categ =  int(input("Entrez la catégorie choisi : "))
            list_product(conn, choice_categ)
            choice_product = int(input("Entrez le produit choisi : "))
            display_product(conn, choice_product)
            # Entrez votre categories :
            #choice_categ = l'id du produit
            # display_product(cursor, choice_categ)
            # Entrez votre produit
            


          

        elif choice == '2':
            print("Vous avez choisi de retrouver un aliment substitué")
            loop = False

        elif choice == 'q':
            loop = False

        else:
            print("Veuillez entrer un des chiffres proposés")
            
    
                 

if __name__ == "__main__":
    main()

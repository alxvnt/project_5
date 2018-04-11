#! /usr/bin/env python3
# coding: utf-8


"""
This script contains the main function of the PurBeurre Project.

Author: Alix VOINOT

"""

import pymysql
from classes import *

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
    cursor.execute(""" SELECT p.name, c.name, b.name, s.name, n.value, p.url FROM product p
                        JOIN category c ON c.id_category = p.id_category
                        JOIN brand b ON b.id_brand = p.id_brand
                        JOIN store s ON s.id_store = p.id_store
                        JOIN nutriscore n ON n.id_nutriscore = p.id_nutriscore
                        WHERE id_product = %s""", (id_product))
    row = cursor.fetchone()
    name = row[0]
    categ = row[1]
    brand = row[2]
    store = row[3]
    nutriscore = row[4]
    url = row[5]
    prod = Product(name, categ, brand, store, nutriscore, url)
    prod.display()
    

def main():
    
    conn = pymysql.connect(host="localhost",\
                                user="root",\
                                password="",\
                                database="purbeurre",\
                                charset="utf8")
    
    
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

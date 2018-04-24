#! /usr/bin/env python3
# coding: utf-8


"""
This script contains the main function of the PurBeurre Project.

Author: Alix VOINOT

"""

import pymysql
from classes import *
from constant import *

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
    list1 = []
    while row is not None:
        list1.append(row[0])
        row = cursor.fetchone()
    return list1

        

# Print the list of the product in the select category
def list_product(conn, id_category):

    cursor = conn.cursor()
    cursor.execute(""" SELECT name FROM product WHERE id_category = %s """,(id_category))
    row = cursor.fetchone()
    list1 = []
    while row is not None:
        list1.append(row[0])
        row = cursor.fetchone()
    return list1

# Display the list of the potential sub
def list_sub(conn, nutriscore, categ):

    cursor = conn.cursor()
    cursor.execute(""" SELECT name FROM Product WHERE nutriscore < {0} AND id_category = {1}""".format(nutriscore, categ))
    row = cursor.fetchone()
    list1 = []
    while row is not None:
        list1.append(row[0])
        row = cursor.fetchone()
    return list1
    

# Print the chosen product and all the information about him
def get_product(conn, id_product):
    
    cursor = conn.cursor()
    cursor.execute(""" SELECT p.id_product, p.name, c.name, b.name, s.name, p.nutriscore, p.url FROM product p
                        JOIN category c ON c.id_category = p.id_category
                        JOIN brand b ON b.id_brand = p.id_brand
                        JOIN store s ON s.id_store = p.id_store
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
    return prod
   
def get_product_by_name(conn, prod_name):

    cursor = conn.cursor()
    cursor.execute(""" SELECT p.id_product, p.name, c.name, b.name, s.name, p.nutriscore, p.url FROM product p
                        JOIN category c ON c.id_category = p.id_category
                        JOIN brand b ON b.id_brand = p.id_brand
                        JOIN store s ON s.id_store = p.id_store
                        WHERE p.name = %s""", (prod_name))
    row = cursor.fetchone()
    id_prod = row[0]
    name = row[1]
    categ = row[2]
    brand = row[3]
    store = row[4]
    nutriscore = row[5]
    url = row[6]
    prod = Product(id_prod, name, categ, brand, store, nutriscore, url)
    return prod

def save_sub(prod1, prod2, conn):

    cursor = conn.cursor()
    id1 = int(prod1.id_prod)
    id2 = int(prod2.id_prod)
    cursor.execute(""" INSERT INTO saved_substitute(id_product, id_substitute)
                        VALUES({0}, {1})
                    """ .format(id1, id2))
    conn.commit()

# Find in the DB all the previous product which have been substitute
def find_sub(conn):

    print("Voici la liste des précédents substitut effectué: ")
    cursor = conn.cursor()
    cursor.execute("""SELECT s.id_product, p.name  FROM product p
                      JOIN saved_substitute s ON s.id_product = p.id_product
                      ORDER BY s.id_saved_substitute
                        """)
    row = cursor.fetchone()
    list1 = []
    while row is not None:
        list1.append(row[1])
        row = cursor.fetchone()
    return list1

def get_sub_data(conn, id_save_sub):

    cursor = conn.cursor()
    cursor.execute("""SELECT id_product, id_substitute FROM saved_substitute
                        WHERE id_saved_substitute = {0} """ .format(id_save_sub))
    list1 = []
    row = cursor.fetchone()
    list1.append(row[0])
    list1.append(row[1])
    return list1

def get_prod_name(conn, id_prod):

    cursor = conn.cursor()
    cursor.execute(""" SELECT name FROM product
                        WHERE id_product = {0}""" .format(id_prod))

    row = cursor.fetchone()
    name = row[0]
    return name
                   

def pick_choice(op1, op2):

    print()
    print("1)" + op1)
    print("2)" + op2)
    choice = input("Votre choix : ")
    if choice not in ["1", "2"]:
        print("Veuillez entrer un chiffre disponible \n")
        choice = pick_choice(op1, op2)
    return int(choice)

def display_list(list1):
    y = 1
    for x in list1:
        print(y, x)
        y+=1
    print()


def pick_line(list1):
    
    choice = input("Choix :")
    try:
        int(choice)
        if not (1 <= int(choice) <= len(list1)):
            print("Veuillez entrer un nombre disponible")
            choice = pick_line(list1)
    except ValueError:
        print("Veuillez entrer un nombre")
        choice = pick_line(list1)
        
    return int(choice)

def main():
    
    conn = db_connect()
    
    
    loop = True
    
    while loop:

        print("----------------------------------")
        print("MENU PRINCIPAL")
        ch1 = pick_choice(op1, op2)
        print(ch1)
        if ch1 == 1:
            print("Vous avez choisi de remplacer un aliment")

            # Display all the categorie and choose one
            list_categ = display_categories(conn)
            display_list(list_categ)
            print("Choisissez une catégorie")
            choice_categ = pick_line(list_categ)

            # Display all the product in the choosen categorie and choose one
            list_prod = list_product(conn, choice_categ)
            display_list(list_prod)
            print("Choisissez un produit")
            choice_product = pick_line(list_prod)
            

            # Display the product information
            prod1 = get_product_by_name(conn, list_prod[choice_product-1])
            prod1.display()

            ch3 = pick_choice(op6, op3)

            if ch3 == 1:
                print("Voici les aliments pouvant être un substitut plus diététique à votre choix :")
                listSub = list_sub(conn, prod1.nutriscore, choice_categ)
                if not listSub:
                    print("Nous n'avons pas trouvé d'alternative plus saine à cette aliment")
                else:
                    display_list(listSub)
                    print("Choisissez un produit")
                    choice_sub = pick_line(listSub)

                    prod2 = get_product_by_name(conn, listSub[choice_sub-1])
                    prod2.display()
                    ch3 = pick_choice(op5, op3)
                    if ch3 == 1:
                        save_sub(prod1, prod2, conn)
                        print(" Le substitut a bien été enregistré ")    
                    ch4 = pick_choice(op3, op4)
                    if ch4 == 2:
                        loop = False
        else:
            listSub = find_sub(conn)
            if listSub:
                display_list(listSub)

                print("Choisissez le substitut voulu")
                id_sub = pick_line(listSub)
                list2 = get_sub_data(conn, id_sub)
            
                name1 = get_prod_name(conn, list2[0])
                name2 = get_prod_name(conn, list2[1])
                p1 = get_product_by_name(conn, name1)
                p2 = get_product_by_name(conn, name2)

                p1.display()
                print()
                print("---------------------------------------")
                p2.display()

            else:
                print("Aucun substitut n'a été enregistré")

            ch5 = pick_choice(op3, op4)
            if ch5 == 2:
                loop = False
                


    conn.commit()
    conn.close()
    
                 

if __name__ == "__main__":
    main()

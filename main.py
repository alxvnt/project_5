#! /usr/bin/env python3
# coding: utf-8


"""
This script contains the main function of the PurBeurre Project.

Author: Alix VOINOT

"""

# Print the list of categories
def display_categories(cursor):
    
    cursor.execute("""SELECT name FROM category""")
    row = cursor.fetchone()
    x = 0
    while row is not None:
        x+=1
        print( str(x) + ")" + row[0])
        row = cursor.fetchone()

# Print the list of the product in the select category
def display_product(cursor, id_category):

    cursor.execute(""" SELECT name FROM product WHERE id_category = %d """, (id_category))
    row = cursor.fetchone()
    x = 0
    while row is not None:
        x+=1
        print( str(x) + ")" + row[0])
        row = cursor.fetchone()

def main():

    loop = True
    
    while loop:
        
        print("1) Remplacer un aliment")
        print("2) Retrouver un aliment substitué")
        
        choice = input(" Choix : ")

        if choice == '1':
            print("Vous avez choisi de remplacer un aliment")
            loop = False
            #Nouvel boucle
            #display_categories
            # Entrez votre categories :
            #choice_categ = l'id du produit
            # display_product(cursor, choice_categ)
            # Entrez votre produit
            


          

        elif choice == '2':
            print("Vous avez choisi de retrouver un aliment substitué")
            loop = False

        else:
            print("Veuillez entrer un des chiffres proposés")
            
    
                 

if __name__ == "__main__":
    main()

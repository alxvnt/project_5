#! /usr/bin/env python3
# coding: utf-8


"""
This script contains all the class of the PurBeurre Project.

Author: Alix VOINOT

"""

class Product():

    def __init__(self, id_prod, name, category, brand, store, nutriscore, url):
        self.id_prod = id_prod
        self.name = name
        self.category = category
        self.brand = brand
        self.store = store
        self.nutriscore = nutriscore
        self.url = url

    def display(self):
        print()
        print("Nom : " + self.name)
        print("Catégorie : " + self.category)
        print("Marque : " + self.brand)
        print("Magasin : " + self.store)
        print("Nutriscore : ", self.nutriscore)
        print("Plus d'infos : " + self.url)
        print()
        

class SaveSub():

    def __init__(self, id_SaveSub, id_product, id_substitute):
        self.id_SaveSub = id_SaveSub
        self.id_product = id_product
        self.id_substitute = id_substitute


        

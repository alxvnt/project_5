#! /usr/bin/env python3
# coding: utf-8


"""
This script contains all the class of the PurBeurre Project.

Author: Alix VOINOT

"""

class Product():

    def __init__(self,id_product, name, category, brand, store, nutriscore, url):
        self.id_product = id_product
        self.name = name
        self.category = category
        self.brand = brand
        self.store = store
        self.nutriscore = nutriscore
        self.url = url

    def display_product():
        print("Nom : " + name)
        print("Catégorie : " + category)
        print("Marque : " + 
        

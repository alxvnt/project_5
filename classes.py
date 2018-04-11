#! /usr/bin/env python3
# coding: utf-8


"""
This script contains all the class of the PurBeurre Project.

Author: Alix VOINOT

"""

class Product():

    def __init__(self, name, category, brand, store, nutriscore, url):
        self.name = name
        self.category = category
        self.brand = brand
        self.store = store
        self.nutriscore = nutriscore
        self.url = url

    def display(self):
        print("Nom : " + self.name)
        print("Catégorie : " + self.category)
        print("Marque : " + self.brand)
        print("Magasin : " + self.store)
        print("Nutriscore : " + self.nutriscore)
        print("Plus d'infos : " + self.url)
        

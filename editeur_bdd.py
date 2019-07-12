#! /usr/bin/python3
# coding: utf8

import mysql.connector 
import os
import sys
from CaglioEbddModule import *




""" Script me permettant de mettre à jour mes tables sql contenant des urls d'integration  """


#DATA
tables= ['hiphop','trancegoa','folk','hardteck','hardcore','chansons', 'bluejazz', 'classique', 'electro', 'wtf', 'punk' , 'zeul' , 'darkwave', 'rockpsy', 'raggae']
gamma=[]
show=[]
tron= False
arbre= False

print("---------------")
print("- atfield2501 -")
print("- BDD Editeur -")
print("---------------")




## Connexion à la bdd
session=Connection()



# Lecture des arguments
if len(sys.argv) < 2:
   print("-Veuillez spécifier un argument-")
   sys.exit(1)
if len(sys.argv) == 3:
    cibleA=sys.argv[2]
    tron= True
if len(sys.argv) == 4:
    cibleA=sys.argv[2]
    cibleB=sys.argv[3]
    arbre= True



action = sys.argv[1]


####### Prompt d'aide
if action == '-h':
    session.aide()

##### Mode total des Entrées
if action == '-tt':
    session.total()

##### Mode Lecture
if action == '-l':
    if tron == True:
        session.lecture(cibleA)
    else:
        session.affiche()

##### Mode Ajout avec Découpe
if action == '-f':
    session.ajout()

####### MODE VERIFICATION
if action == '-e':
    if arbre == True:
        session.edition_uni(cibleA,cibleB)    
    else:
        try:
            session.edition_all(cibleA)
        except NameError:
            print("* Vous devez spécifiez une table *")

###### Decoonexion
session.deconn()

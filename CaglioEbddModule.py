#! /usr/bin/python3
# -*- coding: utf8 -*-

import mysql.connector 
import os
from ebddCaglioIdentifiant import *

""" Module de fonctions et de class diverses pour l'usage de l'editeur_bdd"""




class Connection():
    """ Class se connectant à la bdd et effectuant un certains nombres d'opérations sur celle-ci"""
    cursor = None
    conn = None
    spirale = ""
    def __init__(self):
        ## Connexion à la bdd
        try:
            Connection.conn = mysql.connector.connect(host=localisation,user=utilisateur,password=mdp, database=baseDonnees)
            Connection.cursor = Connection.conn.cursor()
            print("Connexion à la base de données     OK \n")
        except Exception as e:
            print("connexion impossible . . . Cause: "+str(e))

    def aide(self):
        """ Prompt d'aide """
        print("Editeur de bdd")
        print("- - - - - - - - - - - - - - - - - - - - - -  - - - - -  - - - - - - - - - -")
        print("fonctions: (-f) Mode fuck off , accepte un code d'integration iframe \net la decoupe pour inserer adresse dans la table")
        print("fonctions: (-v) Verification des url")
        print("fonctions: (-e <table> <id>) Renseignement du champ titre de toutes les entrées de la table spécifiée si id non reseignée")
        print("fonctions: (-tt) conpte le total d'entrées du juke-box, toutes catégories confondues")
        print("fonctions: (-l <table>) lecture des tables appelé sans option liste les tables présentes")
        print("- - - - - - - - - - - - - - - - - - - - - -  - - - - -  - - - - - - - - - -")
        print("exemple: editeur_bdd.py -a https://www.youtube.com/embed/A4F414LFY6I?rel=0")

    def total(self):
        """ Méthode affichant le total des entrées, toutes tables musicales confondus """
        try:
            Connection.cursor.execute("""SELECT SUM(somme) 
                                         FROM (SELECT COUNT(*) somme FROM hiphop
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM trancegoa
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM folk
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM hardcore
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM hardteck
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM classique
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM electro
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM wtf
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM punk
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM zeul
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM chansons
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM darkwave
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM rockpsy
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM raggae
                                               UNION ALL
                                               SELECT COUNT(*) somme FROM bluejazz
                                               ) table_temp;""")

            Copte = Connection.cursor.fetchall()
            nb= Copte[0]
            nb= str(nb[0])
            print(nb+" - Entrées")
        except Exception as e:
            print("Lecture Impossible. Cause: "+str(e))

    def lecture(self, cibleA):
        """ Methode qui lit le contenue d'une table si le paramètre cibleA lui est passé sinon affiche le contenue de la bdd """
        try:
            id=1
            ff=0
            # compte le nombre d'entrées
            Connection.cursor.execute("""select count(*) from """+cibleA+""" """)
            Copte = Connection.cursor.fetchall()
            nb= Copte[0]
            nb= str(nb[0])
            print(nb+" - Entrées")
            nb1= int(nb)
            while ff != nb1:
                idd=str(id)
                Connection.cursor.execute("""SELECT id, titre FROM """+cibleA+""" WHERE id="""+idd+""" """)
                rows = Connection.cursor.fetchall()
                for row in rows:
                    print('{0} : {1}'.format(row[0], row[1]))
                    id += 1
                    ff += 1
        except Exception as e:
            print("Lecture Impossible. Cause:"+str(e))

    def affiche(self):
        try:
            # Lecture bdd
            Connection.cursor.execute("""SHOW TABLES""")
            darius = Connection.cursor.fetchall()
            print("Lecture de la bdd \n")
            for i in darius:
                print(i[0])
        except Exception as e:
            print("Lecture Impossible. Cause:"+str(e))

    def ajout(self):
        """ Methode qui ajoute une entrée à une table musicale, elle attend en paramètre un code d'intégration iframe qu'elle va découpé avant de la transformé en entrée """
        code= input("Code d'integration d'iframe: "+"\n")
        try:
            abra= code.split('src="')
            cada= abra[1]
            bra= cada.split('"')
            url= bra[0]
        except IndexError:
            print("Cette entrée n'est pas valable")
            return
        print("\n"+"url= {0}".format(url))

        vrac= os.system('curl '+url+' 2>/dev/null | grep '"title"' > .tmp_recherche.txt ' )
        with open(".tmp_recherche.txt", "r") as f:  # Fonction d'analyse du titre de l'url
            try:
                for line in f.readlines():
                    if '<title>' in line:
                        iioonnn = line.split('<title>')
                        iii= iioonnn[1]
                        ii= iii.split('</title>')                       
                        folio=str(ii[0]) 
                        spirale= folio.replace('&quot;' , '"')
                        spirale= folio.replace('&#39;' , "'")
                        Connection.spirale = spirale
                        print("* titre: {0} *".format(spirale)+"\n")
            except Exception as e:
                print("Découpe Impossible. Cause: "+str(e))

            tableU= input("Table d'écriture: "+"\n")
            ## A partir d'ici, il faudrait enclenché une sequence de verification de présence d'url ou de titre de la valeur dans la bdd
            obj2= Verif()
            verif_url= obj2.verif(url, tableU)
            if verif_url== True:
                print("l'url {0} est déjà présente dans la table {1}".format(url, tableU))
            else:
                try:
                    # Ecriture dans la bdd
                    Connection.cursor.execute( """INSERT INTO """+tableU+""" (url , titre) VALUES ('"""+url+ """','"""+Connection.spirale+"""')""")
                    print("-- ECRITURE      --  OK")
                except Exception as e:
                    print("Ecriture Impossible. Cause: "+str(e))

    def edition_uni(self, cibleA ,cibleB):
        """ Méthode utilisée pour renseigner le champ titre d'une table du juke-box grâce à son id """
        try:
            Connection.cursor.execute("""SELECT id, url, titre FROM """+cibleA+""" WHERE id="""+cibleB+""" """)
            rows = Connection.cursor.fetchall()
            for row in rows:
                print('{0} : {1} - {2}'.format(row[0], row[1], row[2]))
                cible=row[1]
                vrac= os.system('curl '+cible+' 2>/dev/null | grep '"title"' > .tmp_recherche.txt ' )

                with open(".tmp_recherche.txt", "r") as f:  # Fonction d'analyse du titre de l'url
                    try:
                        for line in f.readlines():
                            if '<title>' in line:
                                iioonnn = line.split('<title>')
                                iii= iioonnn[1]
                                ii= iii.split('</title>')
                           
                                folio=str(ii[0]) 
                                spirale= folio.replace("'" , " ")
                                print(folio)
                                print("* titre: {0}".format(spirale)) 

                                try:
                                    # Ecriture dans la bdd
                                    Connection.cursor.execute( """UPDATE """+cibleA+""" SET titre='"""+spirale+"""' WHERE id='"""+cibleB+"""' """)
                                    print("-- ECRITURE      --  OK")
                                except:
                                    pass
                    except:
                        pass
        except Exception as e:
            print("Ecriture Impossible. Cause:"+str(e))

    def edition_all(self,cibleA):  
        """  Méthode utilisée pour renseigner tous les champs titre d'une table du juke-box  """
        try:
            id=1
            ff=0
            # compte le nombre d'entrées
            Connection.cursor.execute("""select count(*) from """+cibleA+""" """)
            Copte = Connection.cursor.fetchall()
            nb= Copte[0]
            nb= str(nb[0])
            nb1= int(nb)
            while ff != nb1:
                idd=str(id)
                try:
                    Connection.cursor.execute("""SELECT id, url, titre FROM """+cibleA+""" WHERE id="""+idd+""" """)
                    rows = Connection.cursor.fetchall()
                    for row in rows:
                        print('{0} : {1} - {2}'.format(row[0], row[1], row[2]))
                        cible=row[1]
                        vrac= os.system('curl '+cible+' 2>/dev/null | grep '"title"' > .tmp_recherche.txt ' )

                        with open(".tmp_recherche.txt", "r") as f:  # Fonction d'analyse du titre de l'url
                            try:
                                for line in f.readlines():
                                    if '<title>' in line:
                                        iioonnn = line.split('<title>')
                                        iii= iioonnn[1]
                                        ii= iii.split('</title>')
                           
                                        folio=str(ii[0]) 
                                        spirale= folio.replace("♫ " , " ")
                                        spirale= folio.replace("'" , " ")
                                        print("* titre: {0}".format(spirale)) 

                                        try:
                                            # Ecriture dans la bdd
                                            Connection.cursor.execute( """UPDATE """+cibleA+""" SET titre='"""+spirale+"""' WHERE id='"""+idd+"""' """)
                                            print("-- ECRITURE      --  OK")
                                        except Exception as e:
                                            print("Ecriture Impossible. Cause:"+str(e))
                                        id += 1
                                        ff += 1
                                        break
                            except:
                                pass
                except:
                    pass
        except Exception as e:
            print(str(e))

    def deconn(self):
        """ Méthode apelée pour fermer la connexion avec la base de données """
        Connection.conn.close()


class Verif(Connection):
    """  Class servant à la véification """

    def __init__(self):
        """ Fonction permettant de vérifier la présence d'une entrée avant de l'enregistrer """
    def verif(self, url , tableU):
        Connection.cursor.execute("""SELECT url FROM """+tableU+""" WHERE url='"""+url+"""'""")
        rows = Connection.cursor.fetchall()
        if rows:
            verif_url = True
        else:
            verif_url = False   
        return verif_url

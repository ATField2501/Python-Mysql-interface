#! /usr/bin/python3
# -*- coding: utf8 -*-

import mysql.connector 
import os
import sys

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


#Verification de présence
def verif(url):
    cible = []
    id= 1
    idd=str(id)
    cursor.execute("""SELECT url FROM hiphop WHERE id='"""+ idd +"""'""")
    rows = cursor.fetchall()
    for cibi in rows:
        cible = str(cibi[0])
        print(url)
        print(cible)
        if cible == url:
            verif_url = True
        else:
            verif_url = False   
        return verif_url


## Connexion à la bdd
try:
    conn = mysql.connector.connect(host=localisation,user=utilisateur,password=mdp, database=baseDonnees)
    cursor = conn.cursor()
    print("Connexion à la base de données     OK \n")
except:
    print("Connexion impossible")




# Lecture des arguments
if len(sys.argv) < 2:
   print("-Veuillez spécifier un argument-")
   sys.exit(1)
if len(sys.argv) == 3:
    cibleA=sys.argv[2]
    tron= True
    print(cibleA)

action = sys.argv[1]


####### Prompt d'aide
if action == '-h':
    print("Editeur de bdd")
    print("- - - - - - - - - - - - - - - - - - - - - -  - - - - -  - - - - - - - - - -")
    print("fonctions: (-f) Mode fuck off , identique à a mais accepte un code d'integration iframe \net la decoupe pour inserer adresse dans la table")
    print("fonctions: (-v) Verification des url")
    print("fonctions: (-e <table>) Renseignement du champ titre de toutes les entrées de la table renseignée")
    print("fonctions: (-i) initialisation des variables d'environement")
    print("fonctions: (-tt) conpte le total d'entrées du juke-box, toutes catégories confondues")
    print("fonctions: (-l <table>) lecture des tables appelé sans option liste les tables présentes")
    print("- - - - - - - - - - - - - - - - - - - - - -  - - - - -  - - - - - - - - - -")
    print("exemple: editeur_bdd.py -a https://www.youtube.com/embed/A4F414LFY6I?rel=0")
else:
    pass


##### Mode total des Entrées
if action == '-tt':
    try:
        cursor.execute("""SELECT SUM(somme) 
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
        Copte = cursor.fetchall()
        nb= Copte[0]
        nb= str(nb[0])
        print(nb+" - Entrées")
    except Exception as e:
        print("Lecture Impossible. Cause:"+str(e))


##### Mode Lecture
if action == '-l':
    if tron == True:
        try:
            id=1
            ff=0
            # compte le nombre d'entrées
            cursor.execute("""select count(*) from """+cibleA+""" """)
            Copte = cursor.fetchall()
            nb= Copte[0]
            nb= str(nb[0])
            print(nb+" - Entrées")
            nb1= int(nb)
            while ff != nb1:
                idd=str(id)
                cursor.execute("""SELECT id, titre FROM """+cibleA+""" WHERE id="""+idd+""" """)
                rows = cursor.fetchall()
                for row in rows:
                    print('{0} : {1}'.format(row[0], row[1]))
                    id += 1
                    ff += 1
        except Exception as e:
            print("Lecture Impossible. Cause:"+str(e))

    else:
         # Lecture bdd
         cursor.execute("""SHOW TABLES""")
         darius = cursor.fetchall()
         print("Lecture de la bdd \n")
         for i in darius:
             print(i[0])

else:
    pass





##### Mode Ajout avec Découpe
if action == '-f':
    code= input("Code d'integration d'iframe: "+"\n")
    abra= code.split('src="')
    cada= abra[1]
    bra= cada.split('"')
    url= bra[0]
    print("\n"+"url= {0}".format(url))
    ## A partir d'ici, il faudrait enclenché une sequence de verification de présence d'url ou de titre de la valeur dans la bdd
    verif_url= verif(url)
    if verif_url == True:
        print("l'url {0} est déjà présente dans la bdd".format(url))
    else:
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
                        print("* titre: {0} *".format(spirale)+"\n")
            except:
                pass

        tableU= input("Table d'écriture: "+"\n")
        try:
            # Ecriture dans la bdd
            cursor.execute( """INSERT INTO """+tableU+""" (url , titre) VALUES ('"""+url+ """','"""+spirale+"""')""")
            print("-- ECRITURE      --  OK")
        except Exception as e:
            print("Ecriture Impossible. Cause:"+str(e))
else:
    pass



####### MODE VERIFICATION
if action == '-e':
    if arbre == True:
        try:
            cursor.execute("""SELECT id, url, titre FROM """+cibleA+""" WHERE id="""+cibleB+""" """)
            rows = cursor.fetchall()
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
                                    #       spirale= folio.decode('utf8', errors='replace')
                                    cursor.execute( """UPDATE """+cibleA+""" SET titre='"""+spirale+"""' WHERE id='"""+cibleB+"""' """)
                                    print("-- ECRITURE      --  OK")
                                except Exception as e:
                                    print("Ecriture Impossible. Cause:"+str(e))
                                    break
                    except:
                        pass

        except:
            pass        


    else:
        ## Lecture d'une url à partir de la bdd
        try:
            id=1
            ff=0
            # compte le nombre d'entrées
            cursor.execute("""select count(*) from """+cibleA+""" """)
            Copte = cursor.fetchall()
            nb= Copte[0]
            nb= str(nb[0])
            nb1= int(nb)

            while ff != nb1:
                idd=str(id)
                try:
                    cursor.execute("""SELECT id, url, titre FROM """+cibleA+""" WHERE id="""+idd+""" """)
                    rows = cursor.fetchall()
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
                                     #       spirale= folio.decode('utf8', errors='replace')
                                            cursor.execute( """UPDATE """+cibleA+""" SET titre='"""+spirale+"""' WHERE id='"""+idd+"""' """)
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


    conn.close()
sys.exit(1)

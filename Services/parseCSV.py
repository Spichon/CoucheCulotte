from Projet.Model import Product, Feature
import csv


def get_product_and_features(pathProduct, pathPoids):

    try:
        with open(pathProduct):
            pass
    except IOError:
        print("Erreur! Le fichier contenant les produits n'a pas pu être ouvert")
        return

    try:
        with open(pathPoids):
            pass
    except IOError:
        print("Erreur! Le fichier contenant les poids n'a pas pu être ouvert")
        return

    #Parse les fichiers
    with open(pathProduct, 'r') as csvfile:
        with open(pathPoids, 'r') as csvfilePoids:

            #On initialise ici nos csv readers
            reader = csv.DictReader(csvfile)
            readerPoids = csv.DictReader(csvfilePoids)

            #On initialise ici nos dictionnaires permettant d'avoir autant de caractéristiques que nous le souhaitons.
            #En fonction des caractéristiques on initialise également un dictonnaire de poids
            dict_features = reader.fieldnames[:]
            dict_features.remove("Nom")
            dict_features.remove("Score")
            dict_poids = {}
            for p in readerPoids:
                dict_poids[p["Critere"]] = p["Poids"]


            #On initialise la liste finale de nos produits
            list_product = []
            for row in reader:
                if(row):
                    #On créé notre produit
                    product = Product.Product(row['Nom'], row['Score'])

                    #Si le fichier source possède des caractéristiques à rajouter pour chaque produit
                    if(dict_features):

                        # On initialise la liste des features à rajouter au produit
                        list_features = []
                        for f in dict_features:
                            #On créé la feature avec son nom, sa note et non poids(venant du dictionnaire de poids)
                            list_features.append(Feature.Feature(f, row[f], dict_poids[f]))

                        #On rajoute ici les caractéristiques au produit
                        product.add_feature(list_features)

                    #On rajoute le produit créé à la liste finale des produits créés
                    list_product.append(product)

            return list_product

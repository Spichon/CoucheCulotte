from Model import Product, Feature
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
            dict_features.remove("Classement")
            dict_poids = {}
            for p in readerPoids:
                dict_poids[p["Critere"]] = p["Poids"]


            #On initialise la liste finale de nos produits
            list_product = []
            for row in reader:
                if(row):
                    #On créé notre produit
                    product = Product.Product(row['Nom'], row['Classement'], row['Score'])

                    #Si le fichier source possède des caractéristiques à rajouter pour chaque produit
                    if(dict_features):

                        # On initialise la liste des features à rajouter au produit
                        list_features = []
                        for f in dict_features:
                            #On créé la feature avec son nom, sa note et non poids(venant du dictionnaire de poids)
                            list_features.append(Feature.Feature(f, row[f], dict_poids[f]))

                        #On rajoute ici les caractéristiques au produit
                        product.features=list_features[:]

                    #On rajoute le produit créé à la liste finale des produits créés
                    list_product.append(product)

            return list_product

def get_product_and_features_notations(pathProduct, pathPoids):

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
            dict_features.remove("Classement")
            dict_poids = {}
            for p in readerPoids:
                dict_poids[p["Critere"]] = p["Poids"]


            #On initialise la liste finale de nos produits
            list_product = []
            for row in reader:
                if(row):
                    #On créé notre produit
                    product = Product.Product(row['Nom'], row['Classement'], row['Score'])

                    #Si le fichier source possède des caractéristiques à rajouter pour chaque produit
                    if(dict_features):
                        # On initialise la liste des features à rajouter au produit
                        list_features = []
                        for f in dict_features:
                            #On créé la feature avec son nom, sa note et son poids(venant du dictionnaire de poids)
                            temp_poids=convertNotationToInt(row[f])
                            list_features.append(Feature.Feature(f, temp_poids, dict_poids[f]))

                        #On rajoute ici les caractéristiques au produit
                        product.features=list_features[:]

                    #On rajoute le produit créé à la liste finale des produits créés
                    list_product.append(product)

            return list_product

def get_profiles(pathProfiles,pathPoids):

    try:
        with open(pathProfiles):
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
    with open(pathProfiles, 'r') as csvfile:
        with open(pathPoids, 'r') as csvfilePoids:
            
            readerPoids = csv.DictReader(csvfilePoids)

            #On initialise ici nos csv readers
            reader = csv.DictReader(csvfile)

            #On initialise ici nos dictionnaires permettant d'avoir autant de caractéristiques que nous le souhaitons.
            #En fonction des caractéristiques on initialise également un dictonnaire de poids
            dict_features = reader.fieldnames[:]
            dict_features.remove("Profils")
            dict_poids = {}
            for p in readerPoids:
                dict_poids[p["Critere"]] = p["Poids"]

            #On initialise la liste finale de nos produits
            list_profiles = []
            for row in reader:
                if(row):
                    #On créé notre produit
                    product = Product.Product(row['Profils'])

                    #Si le fichier source possède des caractéristiques à rajouter pour chaque produit
                    if(dict_features):

                        # On initialise la liste des features à rajouter au produit
                        list_features = []
                        for f in dict_features:
                            #On créé la feature avec son nom, sa note modifiée et non poids(venant du dictionnaire de poids)
                            temp_poids=convertNotationToInt(row[f])
                            list_features.append(Feature.Feature(f, temp_poids, dict_poids[f]))
                            
                        #On rajoute ici les caractéristiques au produit
                        product.features=list_features[:]

                    #On rajoute le produit créé à la liste finale des produits créés
                    list_profiles.append(product)

            return list_profiles
        
        
def convertNotationToInt(poids):
    if poids=='++++':
        return 6
    elif poids=="+++":
        return 5
    elif poids=="++":
        return 4
    elif poids=="+":
        return 3
    elif poids=="-":
        return 2
    elif poids=="--":
        return 1
    elif poids=="---":
        return 0
        
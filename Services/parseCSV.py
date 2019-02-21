from CoucheCulotte.Model import Product, Feature
import csv

# Récupère les bornes inférieurse et supérieures
def get_interval():
    with open('./Data//Conf/interval.csv', 'r') as csvfile:
        # On initialise ici nos csv readers
        reader = csv.DictReader(csvfile)
        dict_interval = {}
        for p in reader:
            ss_json = {}
            ss_json["lb"] = p["lb"]
            ss_json["ub"] = p["ub"]
            dict_interval[p["Notation"]] = ss_json
        return dict_interval

# Remplace la notation en un entier
def convertNotationToInt(poids):
    if poids == '++++':
        return 6
    elif poids == "+++":
        return 5
    elif poids == "++":
        return 4
    elif poids == "+":
        return 3
    elif poids == "-":
        return 2
    elif poids == "--":
        return 1
    elif poids == "---":
        return 0

# Fonction parsant le csv et créant les entiés Products et features, es retournant au main.js
def get_product_and_features(pathProduct, pathPoids, note="yes", numberNotation="no", profil="no"):

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
            if "Nom" in dict_features:
                dict_features.remove("Nom")
            if "Score" in dict_features:
                dict_features.remove("Score")
            if "Categorie" in dict_features:
                dict_features.remove("Categorie")
            if "Classement" in dict_features:
                dict_features.remove("Classement")
            if "Profils" in dict_features:
                dict_features.remove("Profils")
            dict_poids = {}
            for p in readerPoids:
                dict_poids[p["Critere"]] = p["Poids"]

            #On initialise la liste finale de nos produits
            list_product = []
            for row in reader:
                if(row):
                    #Si on n'a pas à faire à des profils (produits types)
                    if (profil == "no"):
                        #On créé notre produit avec score
                        if "Score" in row.keys() or note == "yes":
                            if "Classement" in row.keys():
                                product = Product.Product(row['Nom'], row['Categorie'], row['Score'], row['Classement'])
                            if "Classement" not in row.keys():
                                product = Product.Product(row['Nom'], row['Categorie'], row['Score'], 0)
                        # On créé notre produit sans score
                        if "Score" not in row.keys() or note == "no":
                            if "Classement" in row.keys():
                                product = Product.Product(row['Nom'], row['Categorie'], 0, row['Classement'])
                            if "Classement" not in row.keys():
                                product = Product.Product(row['Nom'], row['Categorie'], 0, 0)
                    else :
                        product = Product.Product(row['Profils'])
                    #Si le fichier source possède des caractéristiques à rajouter pour chaque produit
                    if(dict_features):
                        # On initialise la liste des features à rajouter au produit
                        list_features = []
                        for f in dict_features:
                            #On créé la feature avec son nom, sa note et non poids(venant du dictionnaire de poids)
                            temp_weight = row[f]
                            if numberNotation == "yes" : temp_weight = convertNotationToInt(row[f])
                            list_features.append(Feature.Feature(f, temp_weight, dict_poids[f]))

                        #On rajoute ici les caractéristiques au produit
                        product.features=list_features[:]

                    #On rajoute le produit créé à la liste finale des produits créés
                    list_product.append(product)

            return list_product
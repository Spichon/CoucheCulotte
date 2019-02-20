from Services import parseCSV
from Services import mathFunctions, electreTri

pathProduct = "./Data/couche.csv"
pathPoids = "./Data/poids.csv"
pathProfiles = "./Data/profil.csv"
pathCuisine = "./Data/cuisine.csv"
pathPoidsCuisine= "./Data/poidscuisine.csv"
pathProfilesCuisines = "./Data/profilCuisines.csv"

list_product = parseCSV.get_product_and_features(pathProduct, pathPoids, note="no")
to_release = {}
to_maximise = {}


def afficher_detail_produit(list_product):
    for product in list_product:
        print("-Produit : ", product)
        print("-Features: ")
        for feature in product.features:
            print("     ", feature, feature.notation, feature.poids)
        print("-Score : ", product.score)
        print("-Categorie : ", product.categorie)
        print("-Classement : ", product.classement)
        print("\n\n")
        print("\n\n")

def afficher_list_produit(list_product):
    for product in list_product:
        print("-Produit : ", product)

def execution_PL(list_product):
    entree_valide = False
    while entree_valide != True:
        saisie = input("Voulez vous récupérer les produits avec leurs notes ? Y/N ")
        if saisie == "Y" or saisie == "y":
            entree_valide = True
            list_product = parseCSV.get_product_and_features(pathProduct, pathPoids, note="yes")
        if saisie == "N" or saisie == "n":
            entree_valide = True
    print("Voici la liste des produits disponibles :")
    afficher_list_produit(list_product)
    print("\n")
    saisie = input("Voulez vous afficher les détails de chaque produit ? Y/N : ")
    if saisie == "Y" or saisie == "y":
        afficher_detail_produit(list_product)
    print(
        "Nous nous apprêtons à vérifier si les notes des produits cités si-dessus sont explicables à l'aide d'une somme pondéré. Pour ce"
        " faire, nous utilisons un programme d'optimisation linéaire. Il s'agit d'un ensemble de variables (les notes des produits), "
        "soumisent à des contraintes ")
    saisie = input("Voulez vous relacher des contraintes sur un produit en particulier ? Y/N : ")
    if saisie == "Y" or saisie == "y":
        while saisie != "stop":
            saisie = input("Ecrire le nom du produit ou stop pour arrêter la saisie: ")
            entree_valide = False
            for product in list_product:
                if product.name == saisie:
                    entree_valide = True
                    nomproduit = saisie
                    features = product.features
            if entree_valide == True:
                to_release[nomproduit] = {}
                while saisie != "N" or saisie != "n":
                    saisie = input(
                        "Souhaitez vous appliquer la notion de classement pour le produit " + nomproduit + " Y/N : ")
                    if saisie == "Y" or saisie == "y":
                        to_release[nomproduit]["classement"] = True
                    if saisie == "N" or saisie == "n":
                        to_release[nomproduit]["classement"] = False
                    saisie = input(
                        "Souhaitez vous modifier la borne inférieure ou supérieure d'un des critère du produit " + nomproduit + " Y/N : ")
                    if saisie == "Y" or saisie == "y":
                        while saisie != "stop":
                            saisie = input("Rentrer le nom du critère à modifier ou stop pour terminer la saisie :")
                            entree_valide = False
                            for feature in features:
                                if feature.name == saisie:
                                    entree_valide = True
                                    nomfeature = saisie
                            if entree_valide == True:
                                to_release[nomproduit][nomfeature] = {}
                                saisie = input("Saisir la borne inférieure de " + nomproduit + "_" + nomfeature)
                                to_release[nomproduit][nomfeature]["lb"] = saisie
                                saisie = input("Saisir la borne supérieure de " + nomproduit + "_" + nomfeature)
                                to_release[nomproduit][nomfeature]["ub"] = saisie
                    else:
                        break
    print("Choix des critères d'optimisation")

    entree_valide = False
    nomproduit = "Joone"
    while entree_valide != True:
        saisie = input("Ecrire le nom du produit: ")
        for product in list_product:
            if product.name == saisie:
                entree_valide = True
                nomproduit = saisie
                features = product.features
        if entree_valide == True:
            to_maximise["product"] = nomproduit

    entree_valide = False
    while entree_valide != True:
        saisie = input("Ecrire le type d'optimisation : min/max ")
        if saisie == "min" or saisie == "max":
            entree_valide = True
            to_maximise["sens"] = saisie

    entree_valide = False
    while entree_valide != True:
        saisie = input(
            "Voulez-vous optimiser la note finale du produit " + nomproduit + " ou un de ses critères ? : result/criteria")
        to_maximise["result"] = False
        if saisie == "result":
            entree_valide = True
            to_maximise["result"] = True
        if saisie == "criteria":
            while entree_valide != True:
                saisie = input("Rentrer le nom du critère à optimiser: ")
                for feature in features:
                    if feature.name == saisie:
                        entree_valide = True
                        nomfeature = saisie
                if entree_valide == True:
                    to_maximise["feature"] = nomfeature

    # Question 1
    # Questions 2.1 : Programme impossible quand les notes sont fixées. Il y a donc un biais dans les notes du magasine.
    # Question2
    # Question 2.3 : Même le categorie n'est pas possible indépendament des notes finales
    # Question3
    # Question3.1 : MAX -> status OK, MIN -> status OK. Joone obtient 20 dans le meilleur des cas et 17 dans le pire des cas
    #               Love & green est passé au dessus de la moyenne (9.5 à 10.6)
    # Question 3.2 : Max -> status OK,, MIN - status OK, les 4 dernières passent au dessus de 10 quand on tente de maximiser la pire note,
    #               Or elles repassent en dessous de 10 quand on minimise la pire note (Sauf Love & green)
    # Question 3.3 : Les notes sont relatives et sensible à l'ajustement des paramètres de la fonction d'optimisation.
    #               Des notes peuvent se trouver en dessous ou au dessus de la moyenne si on maximise ou minimise le "plus mauvais" produit
    model_PL = mathFunctions.CheckAdditiveModel(list_product, to_maximze=to_maximise, release_constraint=to_release)
    if model_PL.status == "infeasible":
        print("\n")
        print("Le status du modèle est : ", model_PL.status)
        print("Votre modèle n'a pas de solution réalisable")
    else:
        print("Le status du modèle est : ", model_PL.status)
        print("objective value:", model_PL.objective.value)
        print("----------")
        for var_name, var in model_PL.variables.items():
            print(var_name, "=", var.primal)


def execution_electre():
    # ELECTRE TRI COUCHES CULOTTES
    list_product_electre = parseCSV.get_product_and_features_notations(pathProduct, pathPoids)
    list_profiles = parseCSV.get_profiles(pathProfiles,pathPoids)

    print("QUESTION 6 - ELECTRE TRI - LAMBDA = 0.55")
    print("   OPTIMISTE : ")
    for cle,valeur in electreTri.optimistic_evaluation(list_product_electre, list_profiles,0.55):
        print(cle, ": categorie C", valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_product_electre, list_profiles, electreTri.optimistic_evaluation, 0.55),"%")
    print()

    print("   PESSIMISTE : ")
    for cle,valeur in electreTri.pessimistic_evaluation(list_product_electre, list_profiles, 0.55):
        print(cle, ": categorie C", valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_product_electre, list_profiles, electreTri.pessimistic_evaluation, 0.55),"%")
    print()
    print()

    print("QUESTION 6 - ELECTRE TRI - LAMBDA = 0.75")
    print("   OPTIMISTE : ")
    for cle,valeur in electreTri.optimistic_evaluation(list_product_electre, list_profiles,0.75):
        print(cle, ": categorie C", valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_product_electre, list_profiles, electreTri.optimistic_evaluation, 0.75),"%")
    print()

    print("   PESSIMISTE : ")
    for cle,valeur in electreTri.pessimistic_evaluation(list_product_electre, list_profiles, 0.75):
        print(cle,": categorie C",valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_product_electre, list_profiles, electreTri.pessimistic_evaluation, 0.75),"%")

    print()
    print()
    print()
    # QUESTION 9 - ELECTRE TRI CUISINES
    list_cuisine_electre = parseCSV.get_product_and_features_notations(pathCuisine, pathPoidsCuisine)
    list_profiles_cuisines = parseCSV.get_profiles(pathProfilesCuisines,pathPoidsCuisine)

    print("QUESTION 9 - ELECTRE TRI - LAMBDA = 0.55")
    print("   OPTIMISTE : ")
    for cle,valeur in electreTri.optimistic_evaluation(list_cuisine_electre, list_profiles_cuisines,0.55):
        print(cle, ": categorie C", valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_cuisine_electre, list_profiles_cuisines, electreTri.optimistic_evaluation, 0.55),"%")
    print()

    print("   PESSIMISTE : ")
    for cle,valeur in electreTri.pessimistic_evaluation(list_cuisine_electre, list_profiles_cuisines, 0.55):
        print(cle, ": categorie C", valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_cuisine_electre, list_profiles_cuisines, electreTri.pessimistic_evaluation, 0.55),"%")
    print()
    print()

    print("QUESTION 9 - ELECTRE TRI - LAMBDA = 0.75")
    print("   OPTIMISTE : ")
    for cle,valeur in electreTri.optimistic_evaluation(list_cuisine_electre, list_profiles_cuisines,0.75):
        print(cle, ": categorie C", valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_cuisine_electre, list_profiles_cuisines, electreTri.optimistic_evaluation, 0.75),"%")
    print()

    print("   PESSIMISTE : ")
    for cle,valeur in electreTri.pessimistic_evaluation(list_cuisine_electre, list_profiles_cuisines, 0.75):
        print(cle,": categorie C",valeur)

    print("Taux de mauvaise classification :",electreTri.compare_classification(list_cuisine_electre, list_profiles_cuisines, electreTri.pessimistic_evaluation, 0.75),"%")


def main(list_product):
    entree_valide = ""
    while entree_valide != "stop":
        saisie = input("tapez 'pl' ou 'electre' pour accéder aux fonctions sous jacentes ou stop pour quitter le programme: ")
        if saisie == "pl":
            execution_PL(list_product)
        if saisie == "electre":
            execution_electre()
        if saisie == "stop":
            entree_valide = "stop"


main(list_product)






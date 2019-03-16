#GROUPE M2 ID APP : JAMMES PICHON PERRIN LEJEUNE
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Services import parseCSV
from Services import mathFunctions, electreTri, arbrePourClassement60
from Model import Product


# Configuration des liens vers les fichiers de classements de produits, ainsi que la configuration des features et du poids
# associé à chaque features
NAPPIES_PATH = "./Data/Couche/Data/couche.csv"
NAPPIES_WEIGHT_PATH = "./Data/Couche/Conf/poids.csv"
NAPPIES_PROFILES_PATH = "./Data/Couche/Conf/profil.csv"
ROBOTS_PATH = "./Data/Cuisine/Data/cuisine.csv"
ROBOTS_WEIGHT_PATH= "./Data/Cuisine/Conf/poidscuisine.csv"
ROBOTS_PROFILES_PATH = "./Data/Cuisine/Conf/profilCuisines.csv"

# Cette variablee est utilisée dans le cadre de la programmation linéaire pour relacher des contraintes sur des produits (Par exemple
# redefinir les bornes inférieures et supérieures d'une caractéristique d'un produit, ou par exemple ne pas utiliser la notion
# de classement pour un produit donné).
to_release = {}
# Cette variable sert à choisir quel projet on souhaite optimiser, si on désire minimiser ou maximiser, et si c'est sa note finale
# ou une de ses caractéristiques que l'on souhaite optimiser.
to_maximise = {}

# Affiche la liste des produits détaillée que l'on vient de parser
def show_products_details(product_list):
    for product in product_list:
        print("-Produit : ", product)
        print("-Features: ")
        for feature in product.features:
            print("     ", feature, feature.notation, feature.poids)
        print("-Score : ", product.score)
        print("-Categorie : ", product.categorie)
        print("-Classement : ", product.classement)
        print("\n\n")

# Affiche le nom des produit que l'on vient de parser
def show_product_list(product_list):
    for product in product_list:
        print("-Produit : ", product)

# Menu contextuel permettant d'intialiser les variables to_release et to_maximise, et d'apeller la fonction se chargeant d'exécuter
# le programe linéaire.
def execution_PL(product_path, weight_path):
    is_next_step_ok = False
    while is_next_step_ok != True:
        user_input = input("Voulez-vous récupérer les produits avec leurs notes ? Y/N ")
        if user_input == "Y" or user_input == "y":
            is_next_step_ok = True
            product_list = parseCSV.get_product_and_features(product_path, weight_path, note="yes")
        if user_input == "N" or user_input == "n":
            is_next_step_ok = True
            product_list = parseCSV.get_product_and_features(product_path, weight_path, note="no")
            
    print("Voici la liste des produits disponibles :")
    show_product_list(product_list)
    print("\n")
    user_input = input("Voulez-vous afficher les détails de chaque produit ? Y/N : ")
    if user_input == "Y" or user_input == "y":
        show_products_details(product_list)
    print(
        "Nous nous apprêtons à vérifier si les notes des produits cités si-dessus sont explicables à l'aide d'une somme pondéré. \nPour ce"
        "faire, nous utilisons un programme d'optimisation linéaire. Il s'agit d'un ensemble de variables (les notes des produits), "
        "soumisent à des contraintes ")
    print("_" * 100, "\n")
    user_input = input("Voulez-vous relâcher des contraintes sur un produit en particulier ? Y/N : ")
    if user_input == "Y" or user_input == "y":
        while user_input != "stop":
            print("_" * 100, "\n")
            user_input = input("Ecrire le nom du produit ou stop pour arrêter la user_input : ")
            is_next_step_ok = False
            for product in product_list:
                if product.name == user_input:
                    is_next_step_ok = True
                    nomproduit = user_input
                    features = product.features
            if is_next_step_ok == True:
                to_release[nomproduit] = {}
                while user_input != "N" or user_input != "n":
                    print("_" * 100, "\n")
                    user_input = input(
                        "Souhaitez-vous appliquer la notion de classement pour le produit " + nomproduit + " ? Y/N : ")
                    if user_input == "Y" or user_input == "y":
                        to_release[nomproduit]["classement"] = True
                    elif user_input == "N" or user_input == "n":
                        to_release[nomproduit]["classement"] = False
                    print("_" * 100, "\n")
                    user_input = input(
                        "Souhaitez-vous modifier la borne inférieure ou supérieure d'un des critères du produit " + nomproduit + " ? Y/N : ")
                    if user_input == "Y" or user_input == "y":
                        while user_input != "stop":
                            print("_" * 100, "\n")
                            user_input = input("Entrer le nom du critère à modifier ou stop pour terminer la user_input : ")
                            is_next_step_ok = False
                            for feature in features:
                                if feature.name == user_input:
                                    is_next_step_ok = True
                                    nomfeature = user_input
                            if is_next_step_ok == True:
                                to_release[nomproduit][nomfeature] = {}
                                print("_" * 100, "\n")
                                user_input = input("Saisir la borne inférieure de " + nomproduit + "_" + nomfeature + " : ")
                                to_release[nomproduit][nomfeature]["lb"] = user_input
                                print("_" * 100, "\n")
                                user_input = input("Saisir la borne supérieure de " + nomproduit + "_" + nomfeature + " : ")
                                to_release[nomproduit][nomfeature]["ub"] = user_input
                    else:
                        break
                
    print("_"*100,"\n")
    print("Choix des critères d'optimisation")

    is_next_step_ok = False
    nomproduit = "Joone"
    while is_next_step_ok != True:
        user_input = input("Ecrire le nom du produit : ")
        for product in product_list:
            if product.name == user_input:
                is_next_step_ok = True
                nomproduit = user_input
                features = product.features
        if is_next_step_ok == True:
            to_maximise["product"] = nomproduit

    print("_"*100,"\n")
    
    is_next_step_ok = False
    while is_next_step_ok != True:
        user_input = input("Ecrire le type d'optimisation : min/max ")
        if user_input == "min" or user_input == "max":
            is_next_step_ok = True
            to_maximise["sens"] = user_input

    print("_"*100,"\n")

    is_next_step_ok = False
    while is_next_step_ok != True:
        user_input = input(
            "Voulez-vous optimiser la note finale du produit " + nomproduit + " ou un de ses critères ? : result/criteria ")
        to_maximise["result"] = False
        if user_input == "result":
            is_next_step_ok = True
            to_maximise["result"] = True
        elif user_input == "criteria":
            while is_next_step_ok != True:
                user_input = input("Rentrer le nom du critère à optimiser: ")
                for feature in features:
                    if feature.name == user_input:
                        is_next_step_ok = True
                        nomfeature = user_input
                if is_next_step_ok == True:
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
    model_PL = mathFunctions.CheckAdditiveModel(product_list, to_maximze=to_maximise, release_constraint=to_release)
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
    print("_"*100,"\n")

# Menu contextuel permettant d'executer electre tri
def execution_electre(product_path, weight_path, profiles_path):
    
    print("--- Classification des produits avec la méthode ELECTRE TRI ---")
    product = parseCSV.get_product_and_features(product_path, weight_path, numberNotation="yes")
    profiles = parseCSV.get_product_and_features(profiles_path, weight_path, numberNotation="yes", profil="yes")
    affectation_type="optimistic"
    _lambda=0.55
    
    is_next_step_ok = False
    while is_next_step_ok != True:
        user_input = input("Voulez-vous une affectation optimiste (1) ou pessimiste (2) des catégories ? 1/2 : ")
        if user_input == "1":
            affectation_type="optimistic"
            is_next_step_ok = True
        if user_input == "2":
            affectation_type="pessimistic"
            is_next_step_ok = True
        else :
            print("Erreur. Veuillez reformuler votre requête.")
            
    print("_"*100,"\n")
    
    is_next_step_ok = False
    while is_next_step_ok != True:
        print("Quelle est la valeur du lambda pour cette affectation ? Il est par défaut à 0.55.")
        user_input = input("Indiquer un autre lambda (entre 0.00 et 1.00) ou taper entrée : ")
        if user_input == "" :
            is_next_step_ok = True
        elif float(user_input) > 0 and float(user_input) <= 1 :
            _lambda=float(user_input)
            is_next_step_ok = True
        else :
            print("Erreur. Veuillez reformuler votre requête.")
            
    print("_"*100,"\n")
    
    print("ELECTRE TRI CLASSIFICATION - AFFECTATION "+affectation_type+" - LAMBDA = "+str(_lambda))
    for cle,valeur in electreTri.affectation(product, profiles, affectation_type, _lambda):
        print(cle, ": categorie C", valeur)

    print("\nTaux de mauvaise classification :", electreTri.compare_classification(product, profiles, affectation_type, _lambda),"%")
    
    print("\n--- Arbre de décision des catégories du magazine ---")
    arbrePourClassement60.construst_and_print_decision_tree(product)
    
    for cle,valeur in electreTri.affectation(product, profiles, affectation_type, _lambda):
        for prod in product:
            if cle==prod: prod.categorie=valeur
            
    print("\n--- Arbre de décision des catégories de la méthode ELECTRE TRI ---")
    arbrePourClassement60.construst_and_print_decision_tree(product)
    print("_"*100,"\n")

def menu():
    step=""
    product=""
    weight=""
    profiles=""
    is_next_step_ok=False
    while is_next_step_ok != True:
        
        print("\n--------- MENU PRINCIPAL ---------")
        print("--- Analyse des classements de produits : Le cas du magazine 60 millions de consommateurs ---")
        print()
        print("Les analyses des produits suivants sont disponibles :")
        print(" 1) les couche-culottes : Taper 1")
        print(" 2) les robots de cuisine : Taper 2")
        print("\n Quitter :  Taper 'stop'")
        
        user_input = input("Quels produits voulez-vous analyser ? Taper 1 ou 2 : ")
        if user_input == "1":
            is_next_step_ok=True
            product=NAPPIES_PATH
            weight=NAPPIES_WEIGHT_PATH
            profiles=NAPPIES_PROFILES_PATH
        elif user_input == "2":
            is_next_step_ok=True
            product=ROBOTS_PATH
            weight=ROBOTS_WEIGHT_PATH
            profiles=ROBOTS_PROFILES_PATH
        elif user_input == "stop":
            step="stop"
            is_next_step_ok=True
        else :
            print("Erreur. Reformuler la requête.")
    return(product, weight, profiles, step)

# Initialise quel produit on souhaite analyser et quelle anaylyse on souhaite opérer
def main():
    (product, weight, profiles, step) = menu()
        
    print("_"*100,"\n")
    while step != "stop":
        print("Choix d'analyse : ")
        print("   1) Test de validité par programmation linéaire")
        print("   2) Classification avec la méthode ELECTRE TRI")
        print("\nRetour au choix des produits :  Taper 'retour'")
        print("Quitter :  Taper 'stop'")
        user_input = input("Quelle analyse voulez-vous effectuer ? Taper 1,2 ou une commande de navigation ci-dessus : ")
        print("_"*100,"\n")
        if user_input == "1":
            execution_PL(product, weight)
        elif user_input == "2":
            execution_electre(product, weight, profiles)
        elif user_input == "retour":
            print("Retour au menu princiapl")
            (product, weight, profiles, step) = menu()
        elif user_input == "stop":
            step = "stop"
        else :
            print("Erreur. Reformuler la requête.")
    print(" --------- END --------- ")
    print("_"*100,"\n")

main()

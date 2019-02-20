# partial_concordance : méthode générant l'indice de concordance partielle selon un critère donné entre deux produits
def partial_concordance(product1, product2, criteria):
    # Product1 est au moins aussi bon que product2 si sa note est supérieure ou égale car on est dans un cas de maximisation
    if int(product1.features[criteria].notation) >= int(product2.features[criteria].notation) :
        return 1 #retourne 1 si product1 est au moins aussi bon que product2
    return 0

# total_concordance : méthode générant l'indice de concordance totale entre deux produits
def total_concordance(product1, product2):
    result = 0
    divisor = 0
    # Pour chaque critère
    for c in range(len(product1.features)):
        # On multiplie le poids du critère et la concordance partielle sur le critère c, et on l'ajoute à la somme
        result += float(product1.features[c].poids) * partial_concordance(product1, product2, c)
        
        # On somme le poids de tous les critères
        divisor += float(product1.features[c].poids)
    result = result/divisor
    return result

# out_ranking : méthode de surclassement entre deux produits avec un lambda donné
def out_ranking(product1, product2, _lambda):
    if total_concordance(product1, product2) >= _lambda:
        return 1 # retourne 1 si le product1 surclasse le product2
    return 0

# opstimistic_evaluation : méthode d'affectation optimiste qui assigne à chaque produit une catégorie
    # un lambda par défaut est mis à 0.5
def optimistic_evaluation(list_products, list_profiles, _lambda):
    result={}
    # Pour chaque produit
    for product in list_products:
        # Pour chaque profil, qui sont les produits bornant les catégories
        for profile in list_profiles:
            # Si ce profil surclasse le produit mais le produit ne surclasse pas le profil
            if (out_ranking(profile,product,_lambda) and not out_ranking(product,profile,_lambda)):
                # La catégorie du produit est donc celle dont le profil est la borne supérieure
                result[product] = list_profiles.index(profile)
                break
    return sorted(result.items(), key=lambda t: t[1], reverse=True)

# pessimistic_evaluation : méthode d'affectation pessimiste qui assigne à chaque produit une catégorie
    # un lambda par défaut est mis à 0.5
def pessimistic_evaluation(list_products, list_profiles, _lambda):
    result={}
    # Pour chaque produit
    for product in list_products:
        # Pour chaque profil, qui sont les produits bornant les catégories, dans l'ordre inverse
        for profile in reversed(list_profiles):
            # Si ce produit surclasse le profil
            if (out_ranking(product,profile,_lambda)):
                # La catégorie du produit est donc celle dont le profil est la borne inférieure
                result[product] = len(list_profiles)-list_profiles[::-1].index(profile)
                break
    return sorted(result.items(), key=lambda t: t[1], reverse=True)

#  compare_classification : méthode calculant la matrice de confusion et retournant le taux de mauvaise classification
def compare_classification(list_products,list_profiles, function_evaluation, _lambda=0.5):
    # matrice de confusion vide
    confusion=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    # pour chaque produit
    for product in list_products:
        # on parcourt les résultats de l'affectation
        for cle,valeur in function_evaluation(list_products, list_profiles,_lambda):
            # on récupère la catégorie du produit
            if cle==product:
                value=valeur
        # on incrémente de 1 la case de la matrice de confusion telle que la colonne soit la catégorie prédite et la colonne est la catégorie du magazine
        confusion[int(value)-1][int(product.classement)-1]+=1
    print(confusion)
    result=0
    divisor=0
    # Calcul du taux de bonne classification
    for i in range(5):
        # on additionne les chiffres sur la diagonales (bonne classification)
        result+= confusion[i][i]
        for j in range(5):
            # on additionne tous les chiffres de la matrices
            divisor+=confusion[i][j]
    # on retourne le taux de mauvaise classification en pourcentage
    return 100*(1-(result/divisor))
    
    
    
    
    
    
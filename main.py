from CoucheCulotte.Services import parseCSV
from CoucheCulotte.Services import mathFunctions

pathProduct = "./Data/couche.csv"
pathPoids = "./Data/poids.csv"

list_product = parseCSV.get_product_and_features(pathProduct, pathPoids)

"""for product in list_product:
    print("-Produit : ", product)
    print("-Features: ")
    for feature in product.features:
        print("     ",feature, feature.notation, feature.poids)
    print("-Score : ", product.score)
    print("\n\n")"""


#Question 1
#Questions 2.1 : Programme impossible quand les notes sont fixées. Il y a donc un biais dans les notes du magasine.
model_PL= mathFunctions.CheckAdditiveModelQ1(list_product, "Joone")
print("status", model_PL.status)
print("objective value:", model_PL.objective.value)
print("----------")
for var_name, var in model_PL.variables.items():
    print(var_name, "=", var.primal)

#Question2
#Question 2.3 : Même le classement n'est pas possible indépendament des notes finales
"""model_PL2= mathFunctions.CheckAdditiveModelQ2(list_product)
print("status", model_PL2.status)
print("objective value:", model_PL2.objective.value)
print("----------")
for var_name, var in model_PL2.variables.items():
    print(var_name, "=", var.primal)"""

#Question3
#Question3.1 : MAX -> status OK, MIN -> status OK. Joone obtient 20 dans le meilleur des cas et 17 dans le pire des cas
#               Love & green est passé au dessus de la moyenne (9.5 à 10.6)
#Question 3.2 : Max -> status OK,, MIN - status OK, les 4 dernières passent au dessus de 10 quand on tente de maximiser la pire note,
#               Or elles repassent en dessous de 10 quand on minimise la pire note (Sauf Love & green)
#Question 3.3 : Les notes sont relatives et sensible à l'ajustement des paramètres de la fonction d'optimisation.
#               Des notes peuvent se trouver en dessous ou au dessus de la moyenne si on maximise ou minimise le "plus mauvais" produit
"""model_PL3= mathFunctions.CheckAdditiveModelQ3(list_product)
print("status", model_PL3.status)
print("objective value:", model_PL3.objective.value)
print("----------")
for var_name, var in model_PL3.variables.items():
    print(var_name, "=", var.primal)"""


#Question4
"""model_PL4= mathFunctions.CheckAdditiveModelQ3(list_product)
print("status", model_PL4.status)
print("objective value:", model_PL4.objective.value)
print("----------")
for var_name, var in model_PL4.variables.items():
    print(var_name, "=", var.primal)


with open('./Data/resultf12.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for var_name, var in model_PL4.variables.items():
        spamwriter.writerow([var_name, var.primal])"""





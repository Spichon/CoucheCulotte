from Services import parseCSV
from Services import electreTri


pathProduct = "./Data/couche.csv"
pathPoids = "./Data/poids.csv"
pathProfiles = "./Data/profil.csv"

list_product = parseCSV.get_product_and_features(pathProduct, pathPoids)

for product in list_product:
    print("-Produit : ", product)
    print("-Features: ")
    for feature in product.features:
        print("     ",feature, feature.notation, feature.poids)
    print("-Score : ", product.score)
    print("-Classement : ", product.classement)
    print("\n\n")

# ELECTRE TRI 
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

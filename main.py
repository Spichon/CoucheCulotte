from Projet.Services import parseCSV

pathProduct = "/Users/simonpichon/Desktop/En cours/Language de Script/Projet/Data/couche.csv"
pathPoids = "/Users/simonpichon/Desktop/En cours/Language de Script/Projet/Data/poids.csv"

list_product = parseCSV.get_product_and_features(pathProduct, pathPoids)

for product in list_product:
    print("-Produit : ", product)
    for features in product.features:
        print("-Features: ")
        for feature in features:
            print("     ",feature, feature.notation, feature.poids)
    print("-Score : ", product.score)
    print("\n\n")



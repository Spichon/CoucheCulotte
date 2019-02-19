def partial_concordance(product1, product2, criteria):
    if int(product1.features[criteria].notation) >= int(product2.features[criteria].notation) :
        return 1
    return 0

def total_concordance(product1, product2):
    result = 0
    divisor = 0
    for i in range(len(product1.features)):
        result += float(product1.features[i].poids) * partial_concordance(product1, product2, i)
        divisor += float(product1.features[i].poids)
    result = result/divisor
    return result

def out_ranking(product1, product2, _lambda):
    if total_concordance(product1, product2) >= _lambda:
        return 1
    return 0

def optimistic_evaluation(list_products, list_profiles, _lambda=0.5):
    result={}
    for product in list_products:
        for profile in list_profiles:
            #print(product, profile)
            if (out_ranking(profile,product,_lambda) and not out_ranking(product,profile,_lambda)):
                result[product] = list_profiles.index(profile)
                #print("categorie :", list_profiles.index(profile))
                break
    return sorted(result.items(), key=lambda t: t[1], reverse=True)

def pessimistic_evaluation(list_products, list_profiles, _lambda=0.5):
    result={}
    for product in list_products:
        for profile in reversed(list_profiles):
            #print(product, profile)
            if (out_ranking(product,profile,_lambda)):
                result[product] = len(list_profiles)-list_profiles[::-1].index(profile)
                #print("categorie :", result[product])
                break
    return sorted(result.items(), key=lambda t: t[1], reverse=True)

def compare_classification(list_products,list_profiles, function_evaluation, _lambda=0.5):
    confusion=[[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0]]
    for product in list_products:
        for cle,valeur in function_evaluation(list_products, list_profiles,_lambda):
            if cle==product:
                value=valeur
        confusion[int(value)-1][int(product.classement)-1]+=1
    print(confusion)
    result=0
    divisor=0
    for i in range(5):
        result+= confusion[i][i]
        for j in range(5):
            divisor+=confusion[i][j]
    return 100*(1-(result/divisor))
    
    
    
    
    
    
# -*- coding: utf-8 -*-

from math import log

class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None):
        
        #indique l’indice de colonne du critère à tester
        self.col=col
        
        #précise la valeur de la colonne qui correspond à un résultat vrai
        self.value=value
        
        #contient un dictionnaire des résultats de la branche en cours.
        #Sa valeur est None excepté lorsque le noeud est une feuille
        self.results=results
        
        #noeuds suivants de l’arbre
        self.tb=tb
        self.fb=fb

mes_donnees=[['slashdot', 'USA', 'oui', 18, 'Aucun'],
             ['google', 'France', 'oui', 23, 'Premium'],
             ['digg', 'USA', 'oui', 24, 'Basique'] ,
             ['kiwitobes','France', 'oui', 23, 'Basique'] ,
             ['google', 'Angleterre', 'non', 21, 'Premium'],
             ['(direct)', 'Allemagne', 'non',12, 'Aucun'],
             ['(direct)', 'Angleterre', 'non',21, 'Basique'],
             ['google', 'USA', 'non', 24, 'Premium'],
             ['slashdot', 'France', 'oui',19, 'Aucun'],
             ['digg', 'USA', 'non', 18, 'Aucun'] ,
             ['google','Angleterre', 'non', 18, 'Aucun'], 
             ['kiwitobes', 'Angleterre', 'non', 19, 'Aucun'] ,
             ['digg', 'Allemagne', 'oui', 12, 'Basique'] ,
             ['slashdot', 'Angleterre', 'non',21, 'Aucun'],
             ['google','Angleterre', 'oui', 18, 'Basique'] ,
             ['kiwitobes', 'France', 'oui', 19, 'Basique']]

def diviserjeu(lignes,colonne,valeur):
    fonction_diviser=None
    if isinstance(valeur,int) or isinstance(valeur,float):
        fonction_diviser=lambda ligne:ligne[colonne]>=valeur
    else:
        fonction_diviser=lambda ligne:ligne[colonne]==valeur
    jeu1=[ligne for ligne in lignes if fonction_diviser(ligne)]
    jeu2=[ligne for ligne in lignes if not fonction_diviser(ligne)]
    return (jeu1,jeu2)

(jeu1,jeu2)=diviserjeu(mes_donnees, 2, 'oui')

def compteursuniques(lignes):
    resultats={}
    for ligne in lignes:
        r=ligne[len(ligne)-1]
        if r not in resultats:
            resultats[r]=0
        resultats[r]+=1
    return resultats

print("Compteur unique :", compteursuniques(mes_donnees))
print()

def entropie(lignes):
    log2 = lambda x:log(x)/log(2)
    resultats=compteursuniques(lignes)
    entropie=0
    for r in resultats.keys():
        p=float(resultats[r]/len(lignes))
        entropie = entropie - p * log2(p)
    return entropie

def buildtree(rows,scoref=entropie):
    if len(rows)==0:
        return decisionnode()
    current_score=scoref(rows)
    
    # Variables de suivi du meilleur critère.
    best_gain=0.0
    best_criteria=None
    best_sets=None
    
    column_count=len(rows[0])-1
    for col in range(0,column_count):
        
        # Générer la liste des différentes valeurs de la colonne
        column_values={}
        for row in rows:
            column_values[row[col]]=1
            
        # Effectuer une division des lignes sur chaque valeur de la colonne
        for value in column_values.keys():
            (set1,set2) = diviserjeu(rows,col,value)
            
            # Gain d’information
            p=float(len(set1))/len(rows)
            gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
            if gain>best_gain and len(set1)>0 and len(set2)>0:
                best_gain=gain
                best_criteria=(col,value)
                best_sets=(set1,set2)
                
    # Créer les sous branches
    if best_gain>0:
        trueBranch=buildtree(best_sets[0])
        falseBranch=buildtree(best_sets[1])
        return decisionnode(col=best_criteria[0],value=best_criteria[1],tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=compteursuniques(rows))

def printtree(tree,indent=''):
    # Is this a leaf node?
    if tree.results!=None:
        print(str(tree.results))
    else:
        # Print the criteria
        print(str(tree.col)+':'+str(tree.value)+'? ')
        # Print the branches
        print(indent+'V->',printtree(tree.tb,indent+'  '))
        print(indent+'F->',printtree(tree.fb,indent+'  '))
        
printtree(buildtree(mes_donnees))

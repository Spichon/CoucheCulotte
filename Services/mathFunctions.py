import numpy as np
import scipy as sp
from CoucheCulotte.Services import parseCSV
from optlang import Model, Variable, Constraint, Objective
import json

#Construction des Variables
def build_variables(list_product, release_constraint):
    intervals = parseCSV.get_interval()
    variables = {}
    results = {}
    for product in list_product:
        variables[product.name]= {}
        if product.score != 0:
            results[product.name] = Variable(name="{}_result".format(product.name), lb=product.score, ub=product.score)
        else:
            results[product.name] = Variable(name="{}_result".format(product.name), lb=0, ub=20)
        for feature in product.features:
            ub = intervals[feature.notation]["ub"]
            lb = intervals[feature.notation]["lb"]
            if product.name in release_constraint.keys():
                if feature.name in release_constraint[product.name]:
                    if "ub" in release_constraint[product.name][feature.name]:
                        ub = release_constraint[product.name][feature.name]["ub"]
                    if "lb" in release_constraint[product.name][feature.name]:
                        lb = release_constraint[product.name][feature.name]["lb"]
            var = Variable(name="{}_{}".format(product.name, feature.name), lb=lb, ub=ub)
            variables[product.name][feature.name] = var
    return variables,results

#Construction des contraintes
def build_constraints_products(variables, results, list_product, release_constraint):
    constraints = []
    for product in list_product:
        const = Constraint(
            sum(variables[product.name][feature.name]*float(feature.poids) for feature in product.features) - results[product.name],
            lb=0,
            ub=0,
            name="{}_product".format(product.name)
        )
        constraints.append(const)
        if list_product.index(product) < len(list_product) - 1:
            classement=True
            if product.name in release_constraint.keys():
                if "classement" in release_constraint[product.name]:
                    classement = release_constraint[product.name]["classement"]
            if classement==True:
                if list(list_product)[list_product.index(product)].classement == list(list_product)[list_product.index(product)+1].classement:
                    const2 = Constraint(
                        (list(results.values())[list_product.index(product)] - list(results.values())[list_product.index(product)+1]),
                        lb=0,
                        ub=0,
                        name="{}_constraint_result".format(product.name)
                    )
                if list(list_product)[list_product.index(product)].classement != list(list_product)[list_product.index(product)+1].classement:
                    const2 = Constraint(
                        (list(results.values())[list_product.index(product)] - list(results.values())[list_product.index(product)+1]),
                        lb=0.1,
                        name="{}_classement_constraint".format(product.name)
                    )
                constraints.append(const2)
    return constraints

#Lancement du programme linéaire
def CheckAdditiveModel(list_product,to_maximze=None,release_constraint=None):
    variables = build_variables(list_product, release_constraint)[0]
    results = build_variables(list_product, release_constraint)[1]
    constraints = build_constraints_products(variables, results, list_product, release_constraint)
    if to_maximze["result"] == True:
        obj = Objective(results[to_maximze["product"]], direction=to_maximze["sens"])
    if to_maximze["result"] == False:
        obj = Objective(variables[to_maximze["product"]][to_maximze["feature"]], direction=to_maximze["sens"])
    model = Model(name='Simple model static')
    model.objective = obj
    model.add(constraints)
    model.optimize()
    return model

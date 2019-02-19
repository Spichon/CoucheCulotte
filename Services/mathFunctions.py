import numpy as np
import scipy as sp
from CoucheCulotte.Services import parseCSV
from optlang import Model, Variable, Constraint, Objective

def build_variables(list_product):
    intervals = parseCSV.get_interval()
    variables = {}
    for product in list_product:
        variables[product.name]= {}
        for feature in product.features:
            var = Variable(name="{}_{}".format(product.name, feature.name), lb=intervals[feature.notation]["lb"], ub=intervals[feature.notation]["ub"])
            variables[product.name][feature.name] = var
    return variables

def build_constraints_products(variables, list_product):
    constraints = []
    for product in list_product:
        const = Constraint(
            sum(variables[product.name][feature.name]*float(feature.poids) for feature in product.features),
            lb=product.score,
            ub=product.score,
            name="{}_product".format(product.name)
        )
        constraints.append(const)
    return constraints

def delete_product_in_variables(nomProduit):
    return

def delete_product_in_constraints():
    return



def CheckAdditiveModelQ1(list_product, objName):
    variables = build_variables(list_product)
    constraints = build_constraints_products(variables, list_product)
    obj = Objective(variables[objName]["Performance"], direction='max')
    model = Model(name='Simple model static')
    model.objective = obj
    model.add(constraints)
    status = model.optimize()
    return model


def CheckAdditiveModelQ2(list_product, objName):
    variables = build_variables(list_product)

    x11 = Variable('x11', lb=17, ub=20)
    x21 = Variable('x21', lb=17, ub=20)
    x12 = Variable('x12', lb=13, ub=16.5)
    x22 = Variable('x22', lb=13, ub=16.5)
    x13 = Variable('x13', lb=10, ub=12.5)
    x23 = Variable('x23', lb=17, ub=20)
    x14 = Variable('x14', lb=10, ub=12.5)
    x24 = Variable('x24', lb=17, ub=20)
    x15 = Variable('x15', lb=10, ub=12.5)
    x25 = Variable('x25', lb=10, ub=12.5)
    x16 = Variable('x16', lb=13, ub=16.5)
    x26 = Variable('x26', lb=10, ub=12.5)
    x17 = Variable('x17', lb=13, ub=16.5)
    x27 = Variable('x27', lb=7, ub=9.5)
    x18 = Variable('x18', lb=10, ub=12.5)
    x28 = Variable('x28', lb=7, ub=9.5)
    x19 = Variable('x19', lb=13, ub=16.5)
    x29 = Variable('x29', lb=7, ub=9.5)
    x110 = Variable('x110', lb=13, ub=16.5)
    x210 = Variable('x210', lb=0, ub=6.5)
    x111 = Variable('x111', lb=13, ub=16.5)
    x211 = Variable('x211', lb=0, ub=6.5)
    x112 = Variable('x112', lb=10, ub=12.5)
    x212 = Variable('x212', lb=0, ub=6.5)

    f1 = Variable('f1', lb=0, ub=20)
    f2 = Variable('f2', lb=0, ub=20)
    f3 = Variable('f3', lb=0, ub=20)
    f4 = Variable('f4', lb=0, ub=20)
    f5 = Variable('f5', lb=0, ub=20)
    f6 = Variable('f6', lb=0, ub=20)
    f7 = Variable('f7', lb=0, ub=20)
    f8 = Variable('f8', lb=0, ub=20)
    f9 = Variable('f9', lb=0, ub=20)
    f10 = Variable('f10', lb=0, ub=20)
    f11 = Variable('f11', lb=0, ub=20)
    f12 = Variable('f12', lb=0, ub=20)

    c1 = Constraint((0.6 * x11 + 0.4 * x21)-f1, lb=0, ub=0)
    c2 = Constraint((0.6 * x12 + 0.4 * x22)-f2, lb=0, ub=0)
    c3 = Constraint((0.6 * x13 + 0.4 * x23)-f3, lb=0, ub=0)
    c4 = Constraint((0.6 * x14 + 0.4 * x24)-f4, lb=0, ub=0)
    c5 = Constraint((0.6 * x15 + 0.4 * x25)-f5, lb=0, ub=0)
    c6 = Constraint((0.6 * x16 + 0.4 * x26)-f6, lb=0, ub=0)
    c7 = Constraint((0.6 * x17 + 0.4 * x27)-f7, lb=0, ub=0)
    c8 = Constraint((0.6 * x18 + 0.4 * x28)-f8, lb=0, ub=0)
    c9 = Constraint((0.6 * x19 + 0.4 * x29)-f9, lb=0, ub=0)
    c10 = Constraint((0.6 * x110 + 0.4 * x210)-f10, lb=0, ub=0)
    c11 = Constraint((0.6 * x111 + 0.4 * x211)-f11, lb=0, ub=0)
    c12 = Constraint((0.6 * x112 + 0.4 * x212)-f12, lb=0, ub=0)
    c13 = Constraint(f1 - f2, lb=0.1)
    c14 = Constraint(f2 - f3, lb=0.1)
    c15 = Constraint(f3 - f4, lb=0, ub=0)
    c16 = Constraint(f4 - f5, lb=0, ub=0)
    c17 = Constraint(f5 - f6, lb=0, ub=0)
    c18 = Constraint(f6 - f7, lb=0.1)
    c19 = Constraint(f7 - f8, lb=0, ub=0)
    c20 = Constraint(f8 - f9, lb=0.1)
    c21 = Constraint(f9 - f10, lb=0, ub=0)
    c22 = Constraint(f10 - f11, lb=0, ub=0)
    c23 = Constraint(f11 - f12, lb=0.1)



    obj = Objective(x11, direction='max')

    model = Model(name='Simple model static')
    model.objective = obj
    model.add([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16, c17, c18, c19, c20, c21, c22, c23])
    status = model.optimize()
    return model


def CheckAdditiveModelQ3(list_product):
    x11 = Variable('x11', lb=17, ub=20)
    x21 = Variable('x21', lb=17, ub=20)
    x12 = Variable('x12', lb=13, ub=16.5)
    x22 = Variable('x22', lb=13, ub=16.5)
    x13 = Variable('x13', lb=10, ub=12.5)
    x23 = Variable('x23', lb=0, ub=20)
    x14 = Variable('x14', lb=10, ub=12.5)
    x24 = Variable('x24', lb=17, ub=20)
    x15 = Variable('x15', lb=10, ub=12.5)
    x25 = Variable('x25', lb=10, ub=12.5)
    x16 = Variable('x16', lb=13, ub=16.5)
    x26 = Variable('x26', lb=10, ub=12.5)
    x17 = Variable('x17', lb=13, ub=16.5)
    x27 = Variable('x27', lb=7, ub=9.5)
    x18 = Variable('x18', lb=10, ub=12.5)
    x28 = Variable('x28', lb=7, ub=9.5)
    x19 = Variable('x19', lb=13, ub=16.5)
    x29 = Variable('x29', lb=7, ub=9.5)
    x110 = Variable('x110', lb=13, ub=16.5)
    x210 = Variable('x210', lb=0, ub=6.5)
    x111 = Variable('x111', lb=13, ub=16.5)
    x211 = Variable('x211', lb=0, ub=6.5)
    x112 = Variable('x112', lb=10, ub=12.5)
    x212 = Variable('x212', lb=0, ub=6.5)

    f1 = Variable('f1', lb=0, ub=20)
    f2 = Variable('f2', lb=0, ub=20)
    f3 = Variable('f3', lb=0, ub=20)
    f4 = Variable('f4', lb=0, ub=20)
    f5 = Variable('f5', lb=0, ub=20)
    f6 = Variable('f6', lb=0, ub=20)
    f7 = Variable('f7', lb=0, ub=20)
    f8 = Variable('f8', lb=0, ub=20)
    f9 = Variable('f9', lb=0, ub=20)
    f10 = Variable('f10', lb=0, ub=20)
    f11 = Variable('f11', lb=0, ub=20)
    f12 = Variable('f12', lb=0, ub=20)

    c1 = Constraint((0.6 * x11 + 0.4 * x21)-f1, lb=0, ub=0)
    c2 = Constraint((0.6 * x12 + 0.4 * x22)-f2, lb=0, ub=0)
    c3 = Constraint((0.6 * x13 + 0.4 * x23)-f3, lb=0, ub=0)
    c4 = Constraint((0.6 * x14 + 0.4 * x24)-f4, lb=0, ub=0)
    c5 = Constraint((0.6 * x15 + 0.4 * x25)-f5, lb=0, ub=0)
    c6 = Constraint((0.6 * x16 + 0.4 * x26)-f6, lb=0, ub=0)
    c7 = Constraint((0.6 * x17 + 0.4 * x27)-f7, lb=0, ub=0)
    c8 = Constraint((0.6 * x18 + 0.4 * x28)-f8, lb=0, ub=0)
    c9 = Constraint((0.6 * x19 + 0.4 * x29)-f9, lb=0, ub=0)
    c10 = Constraint((0.6 * x110 + 0.4 * x210)-f10, lb=0, ub=0)
    c11 = Constraint((0.6 * x111 + 0.4 * x211)-f11, lb=0, ub=0)
    c12 = Constraint((0.6 * x112 + 0.4 * x212)-f12, lb=0, ub=0)
    c13 = Constraint(f1 - f2, lb=0.1)
    c14 = Constraint(f2 - f3, lb=0.1)
    c15 = Constraint(f3 - f4, lb=0, ub=0)
    c17 = Constraint(f5 - f6, lb=0, ub=0)
    c18 = Constraint(f6 - f7, lb=0.1)
    c19 = Constraint(f7 - f8, lb=0, ub=0)
    c20 = Constraint(f8 - f9, lb=0.1)
    c22 = Constraint(f10 - f11, lb=0, ub=0)
    c23 = Constraint(f11 - f12, lb=0.1)



    obj = Objective(f12, direction='min')

    model = Model(name='Simple model static')
    model.objective = obj
    model.add([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c17, c18, c19, c20, c22, c23])
    status = model.optimize()
    return model

def CheckAdditiveModelQ4(list_product):
    x11 = Variable('x11', lb=17, ub=20)
    x21 = Variable('x21', lb=17, ub=20)
    x12 = Variable('x12', lb=13, ub=16.5)
    x22 = Variable('x22', lb=13, ub=16.5)
    x13 = Variable('x13', lb=10, ub=12.5)
    x23 = Variable('x23', lb=0, ub=20)
    x14 = Variable('x14', lb=10, ub=12.5)
    x24 = Variable('x24', lb=17, ub=20)
    x15 = Variable('x15', lb=10, ub=12.5)
    x25 = Variable('x25', lb=10, ub=12.5)
    x16 = Variable('x16', lb=13, ub=16.5)
    x26 = Variable('x26', lb=10, ub=12.5)
    x17 = Variable('x17', lb=13, ub=16.5)
    x27 = Variable('x27', lb=7, ub=9.5)
    x18 = Variable('x18', lb=10, ub=12.5)
    x28 = Variable('x28', lb=7, ub=9.5)
    x19 = Variable('x19', lb=13, ub=16.5)
    x29 = Variable('x29', lb=7, ub=9.5)
    x110 = Variable('x110', lb=13, ub=16.5)
    x210 = Variable('x210', lb=0, ub=6.5)
    x111 = Variable('x111', lb=13, ub=16.5)
    x211 = Variable('x211', lb=0, ub=6.5)
    x112 = Variable('x112', lb=10, ub=12.5)
    x212 = Variable('x212', lb=0, ub=6.5)

    f1 = Variable('f1', lb=0, ub=20)
    f2 = Variable('f2', lb=0, ub=20)
    f3 = Variable('f3', lb=0, ub=20)
    f4 = Variable('f4', lb=0, ub=20)
    f5 = Variable('f5', lb=0, ub=20)
    f6 = Variable('f6', lb=0, ub=20)
    f7 = Variable('f7', lb=0, ub=20)
    f8 = Variable('f8', lb=0, ub=20)
    f9 = Variable('f9', lb=0, ub=20)
    f10 = Variable('f10', lb=0, ub=20)
    f11 = Variable('f11', lb=0, ub=20)
    f12 = Variable('f12', lb=0, ub=20)

    c1 = Constraint((0.6 * x11 + 0.4 * x21)-f1, lb=0, ub=0)
    c2 = Constraint((0.6 * x12 + 0.4 * x22)-f2, lb=0, ub=0)
    c3 = Constraint((0.6 * x13 + 0.4 * x23)-f3, lb=0, ub=0)
    c4 = Constraint((0.6 * x14 + 0.4 * x24)-f4, lb=0, ub=0)
    c5 = Constraint((0.6 * x15 + 0.4 * x25)-f5, lb=0, ub=0)
    c6 = Constraint((0.6 * x16 + 0.4 * x26)-f6, lb=0, ub=0)
    c7 = Constraint((0.6 * x17 + 0.4 * x27)-f7, lb=0, ub=0)
    c8 = Constraint((0.6 * x18 + 0.4 * x28)-f8, lb=0, ub=0)
    c9 = Constraint((0.6 * x19 + 0.4 * x29)-f9, lb=0, ub=0)
    c10 = Constraint((0.6 * x110 + 0.4 * x210)-f10, lb=0, ub=0)
    c11 = Constraint((0.6 * x111 + 0.4 * x211)-f11, lb=0, ub=0)
    c12 = Constraint((0.6 * x112 + 0.4 * x212)-f12, lb=0, ub=0)




    obj = Objective(f1, direction='max')

    model = Model(name='Simple model static')
    model.objective = obj
    model.add([c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12])
    status = model.optimize()
    return model

from math import log
from CoucheCulotte.Services import parseCSV

class decisionnode:
    def __init__(self,col=-1,value=None,results=None,tb=None,fb=None): # __init__ methods can take any number of arguments, and just like functions, the arguments can be defined with default values, making them optional to the caller.
        self.col=col
        self.value=value
        self.results=results
        self.tb=tb    # tb= True Branch / Right Branch 
        self.fb=fb    # fb = False Branch / Left B 

def transform(category):
    if (category==1): return 'Très insuffisant'
    if (category==2): return 'Insuffisant'
    if (category==3): return 'Acceptable'
    if (category==4): return 'Bon'
    if (category==5): return 'Très bon'
    
def construst_and_print_decision_tree(products):
    my_data=[]
    for product in products:
        row=[]
        for feature in product.features:
            row=row+[feature.notation]
        row=row+[float(product.score), transform(int(product.categorie))]
        my_data.append(row)

# Divides a set on a specific column. Can handle numeric or nominal values
def divideset(rows,column,value):
    # Make a function that tells us if a row is in 
    # the first group (true) or the second group (false)
    split_function=None
    if isinstance(value,int) or isinstance(value,float):
        if isinstance(rows[0],str): split_function=lambda row: parseCSV.convertNotationToInt(row[column]) >= value
        else: split_function=lambda row:row[column] >= value
    else: split_function=lambda row:row[column]==value
   
    # Divide the rows into two sets and return them
    set1=[row for row in rows if split_function(row)]
    set2=[row for row in rows if not split_function(row)]
    return (set1,set2)

# Create counts of possible results (the last column of each row is the result)
def uniquecounts(rows):
    results={}
    for row in rows:
        # The result is the last column
        rr=row[len(row)-1]
        if rr not in results: results[rr]=0
        results[rr]+=1
    return results

#
def entropy(rows):
    log2=lambda x:log(x)/log(2)  
    results=uniquecounts(rows)
    # Now calculate the entropy
    ent=0.0
    for r in results.keys():
        p=float(results[r])/len(rows)
        ent=ent-p*log2(p)
    return ent

def buildtree(rows,scoref=entropy):
    if len(rows)==0: return decisionnode()
    current_score=scoref(rows)

    # Set up some variables to track the best criteria
    best_gain=0.0
    best_criteria=None
    best_sets=None
  
    column_count=len(rows[0])-1
    for col in range(0,column_count):
        # Generate the list of different values in this column
        column_values={}
        for row in rows:
            column_values[row[col]]=1
            # Now try dividing the rows up for each value in this column
            for value in column_values.keys():
                (set1,set2)=divideset(rows,col,value)
                
                # Information gain
                p=float(len(set1))/len(rows)
                gain=current_score-p*scoref(set1)-(1-p)*scoref(set2)
                if gain>best_gain and len(set1)>0 and len(set2)>0:
                    best_gain=gain
                    best_criteria=(col,value)
                    best_sets=(set1,set2)
    # Create the sub branches   
    if best_gain>0:
        trueBranch=buildtree(best_sets[0]) # Right Branch 
        falseBranch=buildtree(best_sets[1]) # Left Branch 
        return decisionnode(col=best_criteria[0],value=best_criteria[1], tb=trueBranch,fb=falseBranch)
    else:
        return decisionnode(results=uniquecounts(rows))

#
def printtree(tree,indent='  '):
    # Is this a leaf node?
    if tree.results!=None:
        print (str(tree.results))
    else:
        # Print the criteria
        print ('Critère '+str(tree.col+1)+' = '+str(tree.value)+' ? ')

        # Print the branches
        print (indent+'T->', end="")
        printtree(tree.tb,indent+'  ')
        print (indent+'F->', end="")
        printtree(tree.fb,indent+'  ')

def construst_and_print_decision_tree(product_list):
    my_data=[]
    for product in product_list:
        row=[]
        for feature in product.features:
            row=row+[feature.notation]
        row=row+[float(product.score), transform(int(product.categorie))]
        my_data.append(row)
    printtree(buildtree(my_data))
import pandas as pd
import numpy as np 
from sklearn.tree import DecisionTreeClassifier
import graphviz
from random import * 
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score,GridSearchCV,cross_val_predict


data = pd.read_csv("iris.data", names = ["comprimento_septala","largura_septala","comprimento_petala","largura_petala","classe"])
data =data.apply(lambda x: x.replace("Iris-setosa", 0))
data =data.apply(lambda x: x.replace("Iris-versicolor", 1))
data =data.apply(lambda x: x.replace("Iris-virginica", 2))

j = 0
lista_indice = []
while True:
	num = randint(0,len(data) - 1)
	add =True
	for element in lista_indice:
		if num == element:
			add = False
	if add:
		lista_indice.append(num)
	if len(lista_indice) == 50:
		break

print(lista_indice)

val = pd.DataFrame(columns = ["comprimento_septala","largura_septala","comprimento_petala","largura_petala","classe"])
j = 0
for element in lista_indice:
	val.loc[j] = data.loc[element]
	data.drop([element],inplace=True)
	j += 1
data.reset_index(drop=True, inplace =True)

################# data train and test_x #################################################

features = list(data.columns[0:-1])
target = data.columns[-1:]
train_x = data[features]	# train data
train_y = data[target] 		# train data
test_x = val[features] 		# test data 
test_y = val[target]		# test data

########################################### tree ########################################
clf_tree = DecisionTreeClassifier()
#clf_tree.fit(train_x,train_y)

grid_tree = GridSearchCV(clf_tree, {}, cv=10)
grid_tree.fit(train_x, train_y)
tree = DecisionTreeClassifier().fit(train_x,train_y)
tree_cross = grid_tree.best_estimator_

print(tree_cross.score(test_x,test_y), tree.score(test_x,test_y))



#result = tree.predict(test_x)

def transforma(classe):
	if classe == 0:
		return "Iris-setosa"
	elif classe == 1:
		return "Iris-versicolor"
	elif classe == 2:
		return "Iris-virginica"
	else:
		return "erro"

###################################### forest #########################################
clf_forest = RandomForestClassifier()
train_y = np.reshape(train_y.to_numpy(),-1)

param_grid = {
                 'n_estimators': [5, 10, 15, 20],
  				 'max_depth': [2, 5, 7, 9]
  			}

grid_forest = GridSearchCV(clf_forest, param_grid, cv=10)
grid_forest.fit(train_x, train_y)
forest = RandomForestClassifier().fit(train_x,train_y)
forest_cross = grid_forest.best_estimator_
print(forest_cross.score(test_x.values, test_y.values), forest.score(test_x.values, test_y.values))



#forest = RandomForestClassifier(n_estimators=100, max_depth=4,random_state=0)
#forest.fit(train_x, train_y)
#print(forest.predict_proba(test_x.values),forest.predict([[0.3,0.6,0.7,0.5]]))










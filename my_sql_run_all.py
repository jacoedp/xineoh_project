
import mysql.connector
import pandas as pd

cnx = mysql.connector.connect(user='test_user_01', password='',
                              host='173.45.91.18',
                              database='user_interaction_01')

df = pd.read_sql("""select * from user_interaction_next_interaction1 """, con=cnx)

cnx.close()
#11:14 to 11:25

#%%
# Creating row nr per unique user

df['user_rn'] = df.groupby(['userID']).cumcount()+1

#%%

# Counting nr of interactions cumulatively per interaction per unique user

df['user_interact_rn'] = df.groupby(['userID', 'interaction']).cumcount()+1

#%%

# Creating a column for each interaction type and cumulatively counting each interaction at any given point

df['c_maybe'] = 0
df.loc[df['interaction'] == 'maybe', 'c_maybe'] = 1
df['c_maybe'] = df.groupby(['userID']).c_maybe.cumsum()


#%%
df['c_yes'] = 0
df.loc[df['interaction'] == 'yes', 'c_yes'] = 1
df['c_yes'] = df.groupby(['userID']).c_yes.cumsum()

#%%
df['c_no'] = 0
df.loc[df['interaction'] == 'no', 'c_no'] = 1
df['c_no'] = df.groupby(['userID']).c_no.cumsum()

#%%
df['c_never'] = 0
df.loc[df['interaction'] == 'never', 'c_never'] = 1
df['c_never'] = df.groupby(['userID']).c_never.cumsum()




#%%

# Normilizing interactive counts per user

df['action_position'] = df['user_interact_rn']/df['user_rn']

df['c_maybe'] = df['c_maybe']/df['user_rn']

df['c_yes'] = df['c_yes']/df['user_rn']

df['c_no'] = df['c_no']/df['user_rn']

df['c_never'] = df['c_never']/df['user_rn']
#%%

# creating dummy variable: for predicting the next interaction as 0 or 1 classinfication for TEST2

list(df)


df_2 = df[['targetID','interaction','action_position','next_interaction','c_maybe','c_yes','c_no','c_never']]


df_2.interaction.unique()

title_mapping = {"maybe": 1, "yes": 2, "no": 3, "never": 4}

df_2['interaction'] = df_2['interaction'].map(title_mapping)
df_2['next_interaction'] = df_2['next_interaction'].map(title_mapping)

df_2.head()



df_2['y_1'] = 0
df_2.loc[df_2['next_interaction'] == 1, 'y_1'] = 1


df_2['y_2'] = 0
df_2.loc[df_2['next_interaction'] == 2, 'y_2'] = 1

df_2['y_3'] = 0
df_2.loc[df_2['next_interaction'] == 3, 'y_3'] = 1

df_2['y_4'] = 0
df_2.loc[df_2['next_interaction'] == 4, 'y_4'] = 1



#%%

#keeping 20% for testing

from sklearn.model_selection import train_test_split

train, test = train_test_split(df_2, test_size = 0.2)


#%%
#TEST1: y=next_interaction   1 model predicting 1,2,3 or 4
#TEST2: y=y_1/y_2/y_3/y_4    4 models | 1 predicting y_1 | 2 predicting y_2 | etc

X_train = train[['c_maybe','c_yes','c_no','c_never']]
Y_train = train["next_interaction"]

X_test = test[['c_maybe','c_yes','c_no','c_never']]
Y_test = test["next_interaction"]


# machine learning

from sklearn.ensemble import RandomForestClassifier
#from sklearn.linear_model import LogisticRegression




X_train = X_train.as_matrix()
Y_train = Y_train.as_matrix()
X_test = X_test.as_matrix()
#%%


#%%
random_forest = RandomForestClassifier(n_estimators=10)

random_forest.fit(X_train, Y_train)

#Logistic_regression = LogisticRegression()
#Logistic_regression.fit(X_train, Y_train)


#%%

# Predicting on test sample
test['Y_pred'] = random_forest.predict(X_test)
#test['Y_pred'] = Logistic_regression.predict(X_test)

#%%
print(type(X_train))
print(type(Y_train))
print(X_train.shape)
print(Y_train.shape)
#%%

test['correct'] = 0
test.loc[test.next_interaction == test.Y_pred, 'correct'] = 1
#%%
test.groupby('Y_pred').targetID.count()
#%%
test.groupby('next_interaction').targetID.count()
#%%

# Majority of "next_interactions" are "1 = maybe"
# Does this skew the result to favor 1 ?

test.groupby([ 'next_interaction','correct']).targetID.count().reset_index()
#test.groupby('correct').targetID.count()
#%%
list(test)
train.groupby('next_interaction').targetID.count()
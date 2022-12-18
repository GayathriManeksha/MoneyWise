import pandas as pd
df = pd.read_csv('resultdata.csv')
print(df.head())

df_filtered = df[df['Type'] !='Others']
df=df_filtered
print(df_filtered.head())

df['category_id'] = df['Type'].factorize()[0]
from io import StringIO
category_id_df = df[['Type', 'category_id']].drop_duplicates().sort_values('category_id')
category_to_id = dict(category_id_df.values)
id_to_category = dict(category_id_df[['category_id', 'Type']].values)

# from imblearn.under_sampling import RandomUnderSampler
from collections import Counter

# import library
from imblearn.over_sampling import RandomOverSampler

ros = RandomOverSampler(random_state=42)

# fit predictor and target variable
x_ros, y_ros = ros.fit_resample(df, df.category_id)
print('Original dataset shape', Counter(df.category_id))
print('Resample dataset shape', Counter(y_ros))
print(id_to_category)


import matplotlib.pyplot as plt
fig = plt.figure(figsize=(8,6))
df.groupby('Type').Name.count().plot.bar(ylim=0)
plt.show()

from sklearn.feature_selection import chi2
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

tfidf = TfidfVectorizer(sublinear_tf=True, min_df=5, norm='l2', encoding='latin-1', ngram_range=(1, 2), stop_words='english')
features = tfidf.fit_transform(x_ros.Name).toarray()
labels = y_ros
print(labels)
print(features.shape)

N=2
for Product, category_id in sorted(category_to_id.items()):
  features_chi2 = chi2(features, labels == category_id)
  indices = np.argsort(features_chi2[0])
  feature_names = np.array(tfidf.get_feature_names_out())[indices]
  unigrams = [v for v in feature_names if len(v.split(' ')) == 1]
  bigrams = [v for v in feature_names if len(v.split(' ')) == 2]
  print("# '{}':".format(Product))
  print("  . Most correlated unigrams:\n. {}".format('\n. '.join(unigrams[-N:])))
  print("  . Most correlated bigrams:\n. {}".format('\n. '.join(bigrams[-N:])))

from sklearn.model_selection import train_test_split  
from sklearn.linear_model import LogisticRegression 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import pickle

X_train, X_test, y_train, y_test = train_test_split(x_ros['Name'], x_ros['Type'], random_state = 0)
count_vect = CountVectorizer()
X_train_counts = count_vect.fit_transform(X_train)
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
model=LogisticRegression()
clf = model.fit(X_train_tfidf, y_train) 
pickle.dump(clf, open('model.pkl','wb'))
pickle.dump(count_vect, open("vectorizer.pickle", "wb"))

y=clf.predict(count_vect.transform(['Vi']))
print(y)
# for x in X_test:
#   print(x)
#   p=clf.predict(count_vect.transform([x]))
#   print(p)

# score=model.score(count_vect.transform(X_test),y_test)
# print(score)
# from sklearn.metrics import r2_score

# X_test_counts=count_vect.fit_transform(list(X_test[0]))

# r2=r2_score(y_test,X_test_counts)
# print(r2)
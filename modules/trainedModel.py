import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv('modules/doj_queries.csv', encoding='ISO-8859-1')

df.head(5000)

def get_number(x):
    if x == 'Divisions': return 0
    elif x == 'Judges Appointed': return 1
    elif x == 'Judges Vacancy': return 2
    elif x == 'Case pendency': return 3
    elif x == 'Live Stream': return 4
    elif x == 'Welcome': return 5

    else: return 6

df['type'] = df['Category'].apply(get_number)

df.head(5000)

#Modle Training

X_train, X_test, y_train, y_test = train_test_split(df.Query, df.type, test_size=0.4)

v = CountVectorizer()

X_train_cv = v.fit_transform(X_train.values)

model = MultinomialNB()

model.fit(X_train_cv, y_train)

X_test_cv = v.transform(X_test)

y_pred = model.predict(X_test_cv)

def threshold(query, model, vectorizer, threshold=0.5):
    queries_count = vectorizer.transform([query])
    probability = model.predict_proba(queries_count) 
    max_prob = max(probability[0])    
    if max_prob < threshold:
        return 6 #change when categories are added
    else:
        return model.predict(queries_count)[0]

# query = ['live streame delhi high court']

# prediction = threshold(query[0], model, v, threshold=0.4)

# print(prediction)
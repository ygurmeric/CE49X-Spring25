import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from sklearn.impute import SimpleImputer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, FeatureUnion
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import nltk
import re
nltk.download('stopwords')
from nltk.corpus import stopwords




# 1. Load Dataset
df = pd.read_json('../../labs/lab6/construction_documents.json')

# I just wanted to see the columns in the dataframe
print(df.columns)

# 2. Handle Missing Metadata
meta_columns = ['project_phase', 'author_role']
imputer = SimpleImputer(strategy='most_frequent')
df[meta_columns] = imputer.fit_transform(df[meta_columns])

# 3. One-hot Encode Metadata
dict_vectorizer = DictVectorizer(sparse=False)
meta_features = dict_vectorizer.fit_transform(df[meta_columns].to_dict(orient='records'))

# 4. Text Preprocessing Function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'\b(?:rfi|cmu|sf|lf|psi|sqft|typ|w\/|n\/a|tbd)\b', '', text)  # remove construction abbreviations
    text = re.sub(r'[\d]+(?:[\./][\d]+)*\s*(mm|cm|m|ft|in|kg|lb|psi|sqm|sqft|sf|lf)', '', text)  # remove units
    text = re.sub(r'[^a-z\s]', '', text)
    text = ' '.join([word for word in text.split() if word not in stopwords.words('english')])
    return text

df['clean_text'] = df['content'].apply(preprocess_text)

# 5. Text Vectorization
vectorizer = TfidfVectorizer(max_features=5000)
text_features = vectorizer.fit_transform(df['clean_text'])

# 6. Combine Text and Metadata Features
from scipy.sparse import hstack
X_combined = hstack([text_features, meta_features])
y = df['document_type']

# 7. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X_combined, y, test_size=0.2, random_state=42)

# 8. Train Naive Bayes Classifier
clf = MultinomialNB()
clf.fit(X_train, y_train)

# 9. Evaluate Model
y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred, labels=clf.classes_)
sns.heatmap(cm, annot=True, fmt='d', xticklabels=clf.classes_, yticklabels=clf.classes_)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# 10. Key Terms Visualization
import numpy as np

feature_names = vectorizer.get_feature_names_out()

for i, label in enumerate(clf.classes_):

    class_feature_log_probs = clf.feature_log_prob_[i]
    n_features = len(feature_names)
    top10 = np.argsort(class_feature_log_probs)[-10:]


    top10 = [j for j in top10 if j < n_features]
    terms = [feature_names[j] for j in top10]

    print(f"Top terms for {label}: {', '.join(terms)}")


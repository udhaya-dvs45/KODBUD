import pandas as pd
import numpy as np
import nltk
import string
import streamlit as st
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from sklearn.metrics import accuracy_score
#Data loding
data=pd.read_csv(r"C:\Users\Udhaya kiran\OneDrive\Desktop\KODBUD\TASK-1\spam.csv")
df=pd.DataFrame(data)
print(df.head())
print(df.shape)
#Data preprocessing
df.drop_duplicates(inplace=True)
df.dropna(inplace=True)
print(df.shape)
nltk.download('stopwords')
df['Category']=df['Category'].map({"ham":0,"spam":1})
steammer=PorterStemmer()
stop_words=set(stopwords.words('english'))
def clean_text (text):
    text=text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words=text.split()
    words=[steammer.stem(word) for word in words if word not in stop_words]
    return " ".join(words)
df['Message']=df['Message'].apply(clean_text)
tf=TfidfVectorizer(max_features=3000)
x=tf.fit_transform(df['Message'])
y=df['Category']
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
#Model initilazation
model=MultinomialNB(alpha=1.0)
model.fit(x_train,y_train)
y_pred = model.predict(x_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
#streamlit part
st.title("SPAM FOLDER CLASSIFICATION")
raw_input=st.text_input("ENTER YOUR TEXT HERE")
if st.button("VALIATED"):
  user_input= clean_text(raw_input)
  vector=tf.transform([user_input])
  prediction=model.predict(vector)
  if prediction[0]==1:
     st.error("SPAM")
     st.image(r"C:\Users\Udhaya kiran\OneDrive\Desktop\KODBUD\TASK-1\spam.png",width=300)
     
  else:
     st.success("NOT A SPAM")
     st.image(r"C:\Users\Udhaya kiran\OneDrive\Desktop\KODBUD\TASK-1\NOT_A_SPAM.png.png",width=300)
from BD_conn import conection 

# import the necessary libraries 
import json 
import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.decomposition import PCA 
from sklearn.cluster import KMeans 
# import matplotlib.pyplot as plt 

# reccuperation de la vue postgres
connect = conection()

print(connect)

try:
    query = """ select course_message_view."course_id", course_message_view."course", course_message_view."message_id", course_message_view."body"  from course_message_view """
    connect.execute(query)
    records = connect.fetchall()
except:
    print ("Query not possible")
    records = None

connect.close()

df = pd.DataFrame(records, columns=["course_id", "course", "message_id", "body"])

print(df)
"""
# Dataset link:  
# https://github.com/PawanKrGunjan/Natural-Language-Processing/blob/main/Sarcasm%20Detection/sarcasm.json 
df=pd.read_json('sarcasm.json') 
  
# Extract the sentence only 
sentence = df.headline 
  
# create vectorizer 
vectorizer = TfidfVectorizer(stop_words='english') 
  
# vectorizer the text documents 
vectorized_documents = vectorizer.fit_transform(sentence) 
  
# reduce the dimensionality of the data using PCA 
pca = PCA(n_components=2) 
reduced_data = pca.fit_transform(vectorized_documents.toarray()) 
  
  
# cluster the documents using k-means 
num_clusters = 2
kmeans = KMeans(n_clusters=num_clusters, n_init=5, 
                max_iter=500, random_state=42) 
kmeans.fit(vectorized_documents) 
  
  
# create a dataframe to store the results 
results = pd.DataFrame() 
results['document'] = sentence 
results['cluster'] = kmeans.labels_ 
  
# print the results 
print(results.sample(5)) 
  
# plot the results 
colors = ['red', 'green'] 
cluster = ['Not Sarcastic','Sarcastic'] 
for i in range(num_clusters): 
    plt.scatter(reduced_data[kmeans.labels_ == i, 0], 
                reduced_data[kmeans.labels_ == i, 1],  
                s=10, color=colors[i],  
                label=f' {cluster[i]}') 
plt.legend() 
plt.show()
"""
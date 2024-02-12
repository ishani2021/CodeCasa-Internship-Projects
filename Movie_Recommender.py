import pandas as pd
credits_df = pd.read_csv("C:\\Users\\ishan\\OneDrive\\Desktop\\credits.csv")
movies_df = pd.read_csv("C:\\Users\\ishan\\OneDrive\\Desktop\\movies.csv")
movies_df= movies_df.merge(credits_df, on='title')
movies_df = movies_df[['movie_id','title','overview','genres','keywords','cast','crew']]
movies_df.dropna(inplace=True)

import ast
def convert(obj):
    L=[]
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L

def convert3(obj):
    L=[]
    counter=0
    for i in ast.literal_eval(obj):
        if counter!=3:
            L.append(i['name'])
            counter+=1
        else:
            break
    return L

movies_df['genres']=movies_df['genres'].apply(convert)
movies_df['keywords']=movies_df['keywords'].apply(convert)
movies_df['cast']=movies_df['cast'].apply(convert3)

def fetch_director(obj):
    L=[]
    for i in ast.literal_eval(obj):
        if i['job']=='Director':
            L.append(i['name'])
    return L

movies_df['crew']=movies_df['crew'].apply(fetch_director)
movies_df['overview']=movies_df['overview'].apply(lambda x:x.split())
movies_df['genres']=movies_df['genres'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['keywords']=movies_df['keywords'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['cast']=movies_df['cast'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['crew']=movies_df['crew'].apply(lambda x:[i.replace(" ","") for i in x])
movies_df['tags']=movies_df['overview']+movies_df['genres']+movies_df['keywords']+movies_df['cast']+movies_df['crew']
new_df=movies_df[['movie_id','title','tags']]
new_df['tags']=new_df['tags'].apply(lambda x:' '.join(x))
new_df['tags']=new_df['tags'].apply(lambda x:x.lower())

from sklearn.feature_extraction.text import CountVectorizer as ctv
cv= ctv(max_features=5000, stop_words='english')
vectors=cv.fit_transform(new_df['tags']).toarray()

from nltk.stem.porter import PorterStemmer
ps = PorterStemmer()
def stem(text):
    y=[]
    for i in text.split():
        y.append(ps.stem(i))
    return " ".join(y)

new_df['tags']=new_df['tags'].apply(stem)

from sklearn.metrics.pairwise import cosine_similarity as cs
similarity = cs(vectors)

def recommend():
    movie=entry.get()
    movie_index=new_df[new_df['title']==movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse = True, key = lambda x:x[1])[1:6]
    for i in movies_list:
        recommendation=Label(text=new_df.iloc[i[0]].title)
        recommendation.pack()
        
import tkinter as tk

root = tk.Tk()
root.title("MovieClick.com")
root.geometry("500x400")
root.minsize(200,200)
entry_message=Label(text="Enter name of the movie you watched:")
entry_message.pack(pady=10)

entry = tk.Entry(root)
entry.pack(pady=10)

display_button = tk.Button(root, text="Recommend next movies to watch...", command=recommend)
display_button.pack(pady=10)  

display_label = tk.Label(root, text="")
display_label.pack(pady=10)  
    
root.mainloop()

#Small Soldiers, Avatar, Tangled, Avengers: Age of Ultron, The Avengers, Titanic, Iron Man 3, 
#Up, Iron Man, Frozen, Thor, Hulk, Kung Fu Panda, Cinderella, Toy Story 3, Enchanted 
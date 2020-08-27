from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import requests
# Create your views here.
def home(request):
	return render(request,'index.html')

def get_title_from_index(index):
	df = pd.read_csv("movie_dataset1.csv",encoding='latin-1')
	df['title']=df['title'].str.upper()
	return df[df.index == index]["title"].values[0]

def get_index_from_title(title):
	df = pd.read_csv("movie_dataset1.csv",encoding='latin-1')
	df['title']=df['title'].str.upper()
	try:
		return df[df.title == title]["index"].values[0]
	except:
		print("Movie not found")
		
def search(request):
	df = pd.read_csv("movie_dataset1.csv",encoding='latin-1')
	df['title']=df['title'].str.upper()
	list1=list(df['title'])
	features = ['keywords','cast','genres','director']
	for feature in features:
		df[feature] = df[feature].fillna('')

	def combine_features(row):
		try:
			return row['keywords'] +" "+row['cast']+" "+row["genres"]+" "+row["director"]
		except:
			print("Error:", row)

	df["combined_features"] = df.apply(combine_features,axis=1)

	cv = CountVectorizer()

	count_matrix = cv.fit_transform(df["combined_features"])
	
	cosine_sim = cosine_similarity(count_matrix)
	num1=request.GET['message']
	movie_caps=num1.upper()
	for lists in list1:
		if movie_caps in lists:
			movie_user_likes=lists
			break
		
	try:	
		movie_index= get_index_from_title(movie_user_likes)
	except:
		return HttpResponse("<h1>Movie not found</h1><br> Please look at the 'Movies' Section for a sample movie")
	similar_movies =  list(enumerate(cosine_sim[movie_index]))
	sorted_similar_movies = sorted(similar_movies,key=lambda x:x[1],reverse=True)

	i=0
	title1=[]
	for element in sorted_similar_movies:
			title1+=[get_title_from_index(element[0])]
			i=i+1
			if i>10:
				break
	print(title1)

	

	return render(request,'result.html',{'title':title1,'movie_user_likes':movie_user_likes})

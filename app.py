import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    api_key = "a2ce9bdbadaa0b91f1ef6a40fddbe613" 
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a2ce9bdbadaa0b91f1ef6a40fddbe613&language=en-US"
    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        data = response.json()
        
        if 'poster_path' in data and data['poster_path']:  
            return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"  # Fallback image
    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return "https://via.placeholder.com/500x750?text=No+Poster+Available"


new_df = pickle.load(open('movies.pkl', 'rb'))  
similarity = pickle.load(open('similarity.pkl', 'rb'))  

st.title('Movie Recommender')

# Recommendation function
def recommend(selected_movie_name):
    try:
        movie_index = new_df[new_df['original_title'] == selected_movie_name].index[0]
    except IndexError:
        st.error("Movie not found in dataset!")
        return [], []
    
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_posters = []
    
    for i in movies_list:
        movie_id = new_df.iloc[i[0]].id 
        recommended_movies.append(new_df.iloc[i[0]].original_title)
        recommended_movie_posters.append(fetch_poster(movie_id))  

    return recommended_movies, recommended_movie_posters

movies_list = new_df['original_title'].values
selected_movie_name = st.selectbox('Select a movie:', movies_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)

    if names:
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])

        col4, col5 = st.columns(2)
        
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])


import joblib
import streamlit as st
import requests

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=15c1fe1e09cc77173404bf460e06845c&language=en-US'.format(movie_id))
    data = response.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

cv = joblib.load('counter_vectorizer.pkl')
similarity = joblib.load('cosine_similarity.pkl')

new_df = joblib.load('new_df.csv')

def recommendation(movie):
    movie_index = new_df[new_df['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movieslist = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movieslist:
        movie_id = new_df.iloc[i[0]].id
        recommended_movies.append(new_df.iloc[i[0]].original_title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters

user_input = st.selectbox("How would you like to be contacted?", new_df['original_title'].values)

if st.button("Get Recommendations"):
    recommendations,posters = recommendation(user_input)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommendations[0])
        st.image(posters[0])
    with col2:
        st.text(recommendations[1])
        st.image(posters[1])
    with col3:
        st.text(recommendations[2])
        st.image(posters[2])
    with col4:
        st.text(recommendations[3])
        st.image(posters[3])
    with col5:
        st.text(recommendations[4])
        st.image(posters[4])
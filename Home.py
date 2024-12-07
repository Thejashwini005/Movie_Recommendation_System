import streamlit as st
import pickle
import pandas as pd
import requests
import random

TMDB_API_KEY = "c297c43d34d05fcfdcd03d10f634813a"  # Replace with your TMDb API key
TMDB_BASE_URL = "https://api.themoviedb.org/3"

# Load movie data
movies = pickle.load(open("moviesList.pkl", 'rb'))
similarity = pickle.load(open("similar.pkl", 'rb'))
similarity1 = pickle.load(open("Title_similar.pkl", 'rb'))
similarity2 = pickle.load(open("Des_similar.pkl", 'rb'))
movies_list = movies['Title'].values

# Function to fetch movie poster from TMDB API
def fetch_movie_poster(movie_name):
    search_url = f"{TMDB_BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={movie_name}"
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json().get("results")
        if results:
            poster_path = results[0].get("poster_path")
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    return None

# Function to display recommendations
def display_recommendations(similarity_data, header):
    st.subheader(header)
    index = movies[movies['Title'] == movie_input].index[0]
    similar_movies = sorted(list(enumerate(similarity_data[index])), key=lambda x: x[1], reverse=True)[1:6]
    
    # Display posters and titles side by side
    cols = st.columns(len(similar_movies))
    for idx, col in zip(similar_movies, cols):
        rec_title = movies.iloc[idx[0]]['Title']
        rec_poster_url = fetch_movie_poster(rec_title)
        with col:
            if rec_poster_url:
                st.image(rec_poster_url, use_container_width=True)
            st.markdown(f"<div style='text-align: center; color: white;'>{rec_title}</div>", unsafe_allow_html=True)

# HTML and CSS for Background, Header, and Menu
st.markdown("""
    <style>
        /* Full-page background targeting Streamlit container */
        .stApp {
            background-image: url('https://images.unsplash.com/photo-1489599849927-2ee91cede3ba?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D'); /* Replace with your image URL */
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
            color: gray;
            font-family: 'Arial', sans-serif;
        }

        /* Animated Background Pattern (Moving circles) */
        .circle-animation {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            animation: circleAnimation 10s ease infinite;
        }

        /* Animation for circles */
        @keyframes circleAnimation {
            0% {
                width: 50px;
                height: 50px;
                top: 20%;
                left: 20%;
                opacity: 0;
            }
            25% {
                width: 100px;
                height: 100px;
                top: 40%;
                left: 40%;
                opacity: 1;
            }
            50% {
                width: 150px;
                height: 150px;
                top: 60%;
                left: 60%;
                opacity: 0.5;
            }
            75% {
                width: 100px;
                height: 100px;
                top: 80%;
                left: 80%;
                opacity: 1;
            }
            100% {
                width: 50px;
                height: 50px;
                top: 20%;
                left: 20%;
                opacity: 0;
            }
        }

        /* Header Styling */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(97, 11, 11, 0.3); /* Transparent black background */
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(118, 71, 89, 0.5);
            z-index: 1;
        }

        .menu-button {
            font-size: 35px;
            cursor: pointer;
        }

        .header-title {
            font-size: 30px;
            font-weight: 900;
            color: white;
        }
    </style>
    
    <!-- Floating Circles Animation for added dynamic effect -->
    <div class="circle-animation" style="top: 10%; left: 15%; animation-delay: 2s;"></div>
    <div class="circle-animation" style="top: 40%; left: 50%; animation-delay: 4s;"></div>
    <div class="circle-animation" style="top: 70%; left: 80%; animation-delay: 6s;"></div>
    <div class="header-container">
        <div class="menu-button" onclick="menuClick()"></div>
        <div class="header-title">Movie Recommender System</div>
    </div>
    <script>
        function menuClick() {
            const btn = document.querySelector('button[aria-label="Menu Button"]');
            if (btn) {
                btn.click();
            }
        }
    </script>
""", unsafe_allow_html=True)

# Initialize sidebar visibility state
menu_options = ["Home", "Recommend", "About"]
selected_option = st.sidebar.selectbox("Menu", menu_options)

# Pages
if selected_option == "Home":
    st.header("Search or Select a Movie")

    # Create a searchable dropdown box
    movie_input = st.selectbox("Type or select a movie from the dropdown:", ["Select a Movie"] + list(movies_list))

    # Show details button appears only if a valid movie is selected
    if movie_input != "Select a Movie":
        if st.button("Show Details"):
            # Check if the movie exists
            movie_details = movies[movies['Title'] == movie_input]
            if not movie_details.empty:
                movie_details = movie_details.iloc[0]
                title = movie_details['Title']
                year = movie_details['Year of Release']
                rate = movie_details['Rating']
                review = movie_details['Number of Reviews']
                cast = movie_details.get('Movie Cast', 'N/A')
                director = movie_details.get('Director', 'N/A')
                description = movie_details.get('Description', 'N/A')

                poster_url = fetch_movie_poster(title)

                # Display movie details
                if poster_url:
                    st.image(poster_url, width=300, caption=f"Poster for {title}")
                st.markdown(f"**Title:** {title}")
                st.markdown(f"**Year of Release:** {year}")
                st.markdown(f"**Rating:** {rate}")
                st.markdown(f"**Number of Reviews:** {review}")
                st.markdown(f"**Cast:** {cast}")
                st.markdown(f"**Director:** {director}")
                st.markdown(f"**Description:** {description}")
               
                # Recommendations
                display_recommendations(similarity, "Recommended Movies Based on Cast")
                display_recommendations(similarity1, "Recommended Movies Based on Title")
                display_recommendations(similarity2, "Recommended Movies Based on Description")
            else:
                # Movie not found
                st.error("No details found for the selected movie. Please try another movie.")

    else:
        st.info("Please select or type a movie to proceed.")

elif selected_option == "Recommend":
    st.header("Random Movie Recommendations")
    random_movies = random.sample(list(movies_list), 10)

    selected_movie = None
    cols = st.columns(len(random_movies))
    for col, movie_title in zip(cols, random_movies):
        poster_url = fetch_movie_poster(movie_title)
        with col:
            if st.button(movie_title):
                selected_movie = movie_title
            st.image(poster_url, width=150)
            st.caption(movie_title)

    # If a movie is clicked, show its details
    if selected_movie:
        st.header(f"Details for {selected_movie}")
        movie_details = movies[movies['Title'] == selected_movie]
        if not movie_details.empty:
            movie_details = movie_details.iloc[0]
            title = movie_details['Title']
            year = movie_details['Year of Release']
            rate = movie_details['Rating']
            review = movie_details['Number of Reviews']
            cast = movie_details.get('Movie Cast', 'N/A')
            director = movie_details.get('Director', 'N/A')
            description = movie_details.get('Description', 'N/A')
            poster_url = fetch_movie_poster(title)

            # Display movie details
            if poster_url:
                st.image(poster_url, width=300, caption=f"Poster for {title}")
            st.markdown(f"**Title:** {title}")
            st.markdown(f"**Year of Release:** {year}")
            st.markdown(f"**Rating:** {rate}")
            st.markdown(f"**Number of Reviews:** {review}")
            st.markdown(f"**Cast:** {cast}")
            st.markdown(f"**Director:** {director}")
            st.markdown(f"**Description:** {description}")
        else:
            st.error("No details found for the selected movie.")
elif selected_option == "About":
    st.header("About")
    st.markdown("""
        Welcome to the **Movie Recommender System**! 🎥  
        This website allows users to explore movies, view details about each movie.  
        ### Features:
        - Explore and learn more about your favorite movies.
        - Upload your own dataset and view its contents.
        - Built with ❤️ using Streamlit.
    """)

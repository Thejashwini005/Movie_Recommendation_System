import streamlit as st
import pickle
import pandas as pd

# Load movie data
movies = pickle.load(open("moviesList.pkl", 'rb'))
similarity = pickle.load(open("similar.pkl", 'rb'))
movies_list = movies['Title'].values

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

        /* Header Styling */
        .header-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px;
            background: rgba(97, 11, 11, 0.3); /* Semi-transparent black */
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
            color:white;
        }

        .header-title {
            font-size: 30px;
            font-weight: 900;
            color: white;
        }
    </style>

    <!-- Header -->
    <div class="header-container">
        <div class="header-title">Movie Recommendation System</div>
    </div>
""", unsafe_allow_html=True)

# Initialize sidebar visibility state
menu_options = ["Home", "Upload CSV File", "Recommend", "About"]
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

                

                # Display movie details
                st.markdown(f"**Title:** <span style='color: white;'>{title}</span>", unsafe_allow_html=True)
                st.markdown(f"**Year Of Release:** <span style='color: white;'>{year}</span>", unsafe_allow_html=True)
                st.markdown(f"**Rating:** <span style='color: white;'>{rate}</span>", unsafe_allow_html=True)
                st.markdown(f"**No Of Reviews:** <span style='color: white;'>{review}</span>", unsafe_allow_html=True)
                st.markdown(f"**Cast:** <span style='color: white;'>{cast}</span>", unsafe_allow_html=True)
                st.markdown(f"**Director:** <span style='color: white;'>{director}</span>", unsafe_allow_html=True)
                st.markdown(f"**Description:** <span style='color: white;'>{description}</span>", unsafe_allow_html=True)

                index = movies[movies['Title'] == movie_input].index[0]
                similar_movies = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)[1:6]
                st.subheader("Recommended Movies:")
                for i, (idx, score) in enumerate(similar_movies, 1):
                    st.write(f"{i}. {movies.iloc[idx]['Title']}")
            else:
                # Movie not found
                st.error("No details found for the selected movie. Please try another movie.")

    else:
        st.info("Please select or type a movie to proceed.")

elif selected_option == "Upload CSV File":
    st.header("Upload Your Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    if uploaded_file is not None:
        try:
            data = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully!")
            st.dataframe(data.head())  # Display the first few rows of the uploaded dataset
        except Exception as e:
            st.error(f"An error occurred: {e}")

elif selected_option == "About":
    st.header("About")
    st.markdown("""
        Welcome to the **Movie Recommender System**! 🎥  
        This website allows users to explore movies, view details about each movie, and even upload custom datasets for analysis.  
        ### Features:
        - Explore and learn more about your favorite movies.
        - Upload your own dataset and view its contents.
        - Built with ❤️ using Streamlit.
    """)

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

        /* Floating Circles for Animation */
        .circle-animation {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.2);
            animation: circleAnimation 10s ease infinite;
        }
        @keyframes circleAnimation {
            0% { width: 50px; height: 50px; top: 10%; left: 10%; opacity: 0; }
            25% { width: 100px; height: 100px; top: 20%; left: 30%; opacity: 1; }
            50% { width: 150px; height: 150px; top: 50%; left: 50%; opacity: 0.5; }
            75% { width: 100px; height: 100px; top: 80%; left: 70%; opacity: 1; }
            100% { width: 50px; height: 50px; top: 10%; left: 10%; opacity: 0; }
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

        .menu-button {
            font-size: 35px;
            cursor: pointer;
            border: none;
            background-color: rgba(0,0,0,1);
        }

        .header-title {
            font-size: 30px;
            font-weight: 900;
            color: white;
        }
        .sidebar .sidebar-content {
            background-color: rgba(0, 0, 0, 1); /* Transparent black */
            border-radius: 10px;
        }
        .stSelectbox > div {
            color: gray; /* Text color in the dropdown */
        }
    </style>

    <!-- Animated Circles -->
    <div class="circle-animation" style="top: 10%; left: 10%; animation-delay: 2s;"></div>
    <div class="circle-animation" style="top: 30%; left: 40%; animation-delay: 4s;"></div>
    <div class="circle-animation" style="top: 60%; left: 70%; animation-delay: 6s;"></div>

    <!-- Header with Menu Button -->
    <div class="header-container">
        <div class="menu-button" onclick="menuClick()"></div>
        <div class="header-title">Movie Recommendation System</div>
    </div>

    <!-- Script to Trigger Sidebar -->
    <script>
        function menuClick() {
            const menuButton = document.querySelector('button[aria-label="Menu Button"]');
            if (menuButton) {
                menuButton.click();
            }
        }
    </script>
""", unsafe_allow_html=True)

# Initialize sidebar visibility state
menu_options = ["Home", "Upload CSV File","Recommend","About"]
selected_option = st.sidebar.selectbox("Menu", menu_options)

# Pages
if selected_option == "Home":
    st.header("Select movie from dropdown")
    selectvalue = st.selectbox("Choose a Movie", ["Select a Movie"] + list(movies_list))

    if selectvalue != "Select a Movie":
        try:
            movie_details = movies[movies['Title'] == selectvalue].iloc[0]
            title = movie_details['Title']
            year = movie_details['Year of Release']
            rate = movie_details['Rating']
            review = movie_details['Number of Reviews']
            cast = movie_details.get('Movie Cast', 'N/A')
            director = movie_details.get('Director','N/A')
            description = movie_details.get('Description','N/A')

            st.markdown(f"**Title:** <span style='color: white;'>{title}</span>", unsafe_allow_html=True)
            st.markdown(f"**Year Of Release:** <span style='color: white;'>{year}</span>", unsafe_allow_html=True)
            st.markdown(f"**Rating:** <span style='color: white;'>{rate}</span>", unsafe_allow_html=True)
            st.markdown(f"**No Of Reviews:** <span style='color: white;'>{review}</span>", unsafe_allow_html=True)
            st.markdown(f"**Cast:** <span style='color: white;'>{cast}</span>", unsafe_allow_html=True)
            st.markdown(f"**Director:** <span style='color: white;'>{director}</span>", unsafe_allow_html=True)
            st.markdown(f"**Description:** <span style='color: white;'>{description}</span>", unsafe_allow_html=True)

        except IndexError:
            st.error("Movie details could not be found. Please try another selection.")
    else:
        st.markdown("**Please select a movie to see its details.**", unsafe_allow_html=True)

elif selected_option == "Upload Dataset":
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
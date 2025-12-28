import streamlit as st
import pandas as pd
import requests
#from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import difflib

# Page configuration
st.set_page_config(
    page_title="movie is recommended hereee",
    page_icon="🍿",
    layout="wide",
    initial_sidebar_state="expanded"
   
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
        padding: 0.5rem;
        border-radius: 0.5rem;
    }
    .movie-card {
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin: 0.5rem 0;
    }
    </style>
""", unsafe_allow_html=True)

# Cache the data loading and processing
@st.cache_data
def load_and_process_data():
    """Load the movies data and compute similarity matrix"""
    try:
        # Load the data
        movies_data = pd.read_csv('movies.csv')
        
        # Select relevant features
        selected_features = ['genres', 'keywords', 'tagline', 'cast', 'director']
        
        # Replace null values with empty string
        for feature in selected_features:
            movies_data[feature] = movies_data[feature].fillna('')
        
        # Combine all features
        combined_features = (
            movies_data['genres'] + ' ' + 
            movies_data['keywords'] + ' ' + 
            movies_data['tagline'] + ' ' + 
            movies_data['cast'] + ' ' + 
            movies_data['director']
        )
        
        # Convert text to feature vectors
        vectorizer = TfidfVectorizer()
        feature_vectors = vectorizer.fit_transform(combined_features)
        
        # Compute similarity matrix
        similarity = cosine_similarity(feature_vectors)
        
        return movies_data, similarity
    except FileNotFoundError:
        st.error("❌ movies.csv file not found. Please upload the dataset.")
        return None, None

def fetch_poster(movie_title):
    """Fetch movie poster from TMDB API"""
    try:
        # Search for the movie
        search_url = f"https://api.themoviedb.org/3/search/movie?api_key=0b78123bc2f438d6b6d11c94f882d34b&query={movie_title}"
        response = requests.get(search_url, timeout=5)
        data = response.json()
        
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=No+Poster"

def get_recommendations(movie_name, movies_data, similarity, num_recommendations=10):
    """Get movie recommendations based on similarity"""
    try:
        # Get list of all movie titles
        list_of_all_titles = movies_data['title'].tolist()
        
        # Find close match
        find_close_match = difflib.get_close_matches(movie_name, list_of_all_titles, n=1, cutoff=0.6)
        
        if not find_close_match:
            return None, "Sorry to say this, we couldn’t find any movies related to the selected movie. Please try another one."
        
        close_match = find_close_match[0]
        
        # Find index of the movie
        index_of_the_movie = movies_data[movies_data['title'] == close_match].index[0]
        
        # Get similarity scores
        similarity_score = list(enumerate(similarity[index_of_the_movie]))
        
        # Sort movies by similarity
        sorted_similar_movies = sorted(similarity_score, key=lambda x: x[1], reverse=True)
        
        # Get top recommendations (excluding the input movie itself)
        recommendations = []
        for i, movie in enumerate(sorted_similar_movies[1:num_recommendations+1]):
            index = movie[0]
            title = movies_data.iloc[index]['title']
            score = movie[1]
            recommendations.append({
                'title': title,
                'similarity_score': score,
                'rank': i + 1
            })
        
        return recommendations, close_match
    except Exception as e:
        return None, f"Error: {str(e)}"

# Main app
def main():
    # Header
    st.title("🍿🍿CineMatch, Come and Check it out!!🍿🍿")
    st.markdown("### Discover movies similar to your favorites!")
    st.markdown("---")
    
    # Load data
    with st.spinner("Loading movie database..."):
        movies_data, similarity = load_and_process_data()
    
    if movies_data is None or similarity is None:
        st.stop()
    
    st.success(f"✅ Loaded {len(movies_data)} movies")
    
    # Input section
    col1, col2 = st.columns([3, 1])
    
    with col1:
        movie_input = st.text_input(
            
            "Enter your favorite movie name:",
            placeholder="e.g., The Dark Knight, Inception, Avatar...",
            help="Type a movie name and we'll find similar recommendations"
        )
    
    with col2:
        num_recommendations = st.slider(
            "Number of recommendations:",
            min_value=5,
            max_value=20,
            value=10,
            step=5
        )
    
    # Search button
    if st.button("🔍 Get Recommendations", type="primary"):
        if movie_input:
            with st.spinner("Finding similar movies..."):
                recommendations, result = get_recommendations(
                    movie_input, 
                    movies_data, 
                    similarity, 
                    num_recommendations
                )
            
            if recommendations:
                st.success(f"😺 Movies similar to **{result}**")
                st.markdown("---")
                
                # Display recommendations in a grid
                cols_per_row = 5
                for i in range(0, len(recommendations), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(recommendations):
                            rec = recommendations[i + j]
                            with col:
                                with st.container():
                                    # Fetch and display poster
                                    poster_url = fetch_poster(rec['title'])
                                    st.image(poster_url, use_container_width=True)
                                    
                                    # Display movie info
                                    st.markdown(f"**{rec['rank']}. {rec['title']}**")
                                    st.caption(f"Similarity: {rec['similarity_score']:.2%}")
            else:
                st.error(f"❌ {result}")
        else:
            st.warning("⚠️ Please enter a movie name")
    
    # Sidebar with info
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("""
    **How it works (the simple version):**
    
    We look at each movie's important details - genres, cast, director, keywords, and tagline.
    Then we convert all that info into numbers using something called TF-IDF.
    
    After that, we use cosine similarity to compare movies and find which ones are most similar 
    to the one you picked.
    
    Think of it like this: if two movies share a lot of the same features (same genre, similar 
    cast, etc.), they'll probably have a similar vibe - so you might enjoy both! 🎬
    """)
        
        st.header("📊 Statistics")
        if movies_data is not None:
            st.metric("Total Movies", len(movies_data))
            st.metric("Features Used", 5)
        
        st.header("💡 Tips")
        st.markdown("""
        - Try popular movie titles for best results
        - The system finds close matches if spelling isn't exact
        - Recommendations are based on content similarity
        """)

if __name__ == "__main__":
    main()
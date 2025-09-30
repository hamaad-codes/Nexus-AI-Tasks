Product Recommendation System – Task 5
📌 Project Overview

The goal of this project is to build a content-based recommendation system that suggests movies to users based on the movies they have previously liked.
The system uses text data (movie descriptions, genres, and keywords) to find similar movies and recommend the top 5 most relevant ones.

⚙️ Steps Performed

Data Preparation

Loaded the TMDB 5000 Movies Dataset.

Selected important columns such as title, overview, genres, and keywords.

Cleaned the text data by converting it to lowercase and removing punctuation.

Feature Extraction

Used TF-IDF Vectorizer to convert movie overviews into a numerical matrix that represents the importance of each word.

Similarity Calculation

Calculated the similarity between movies using Cosine Similarity on the TF-IDF matrix.

Recommendation Function

Created a Python function that takes a movie title as input and returns the top 5 most similar movies.

Testing

Tested the system with example movie titles (e.g., The Dark Knight, Avatar, Inception) to verify that the recommendations are relevant.

How to Run

Install the required libraries:

pip install pandas scikit-learn


Run the notebook or script:

Open Jupyter Notebook or a Python script and execute the code to build the recommendation system.

Expected Output

A Python function (e.g., recommend_movie('The Dark Knight')) that returns the top 5 most similar movies.

Recommendations should be logically related to the input movie (e.g., similar genre, theme, or keywords).
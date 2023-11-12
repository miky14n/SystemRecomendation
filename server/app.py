from flask import Flask, render_template, request, jsonify
from flask_cors import CORS 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

app = Flask(__name__)
CORS(app)

# Load the dataset and perform data preprocessing
df = pd.read_csv('titles.csv')

# Data preprocessing (filling missing values, creating features, TF-IDF)
df['description'].fillna('Sin descripción', inplace=True)
df['age_certification'].fillna('Desconocido', inplace=True)
df['seasons'].fillna(0, inplace=True)
df.drop(['imdb_id', 'imdb_score', 'imdb_votes', 'tmdb_popularity', 'tmdb_score'], axis=1, inplace=True)

df['genres'] = df['genres'].str.replace("[", "").str.replace("]", "").str.replace("'", "").str.split(", ")

unique_genres = set(x for _list in df['genres'] for x in _list)
for genre in unique_genres:
    df[genre] = df['genres'].apply(lambda x: 1 if genre in x else 0)

tfidf = TfidfVectorizer(stop_words='english')
df['description'] = df['description'].fillna('')
tfidf_matrix = tfidf.fit_transform(df['description'])
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# Reverse mapping of indices and anime titles
indices = pd.Series(df.index, index=df['title']).drop_duplicates()

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    anime_indices = [i[0] for i in sim_scores]
    recommended_animes = df['title'].iloc[anime_indices].tolist()
    return recommended_animes
# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendations', methods=['GET', 'POST'])
def recommendations():
    if request.method == 'GET':
        print('entramos a get')
        anime_name = request.args.get('anime_name')
        recommended_animes = get_recommendations(anime_name)
        return jsonify({'recommendations': recommended_animes})
    else:
        return jsonify({'message': 'Send a GET request with anime_name parameter'})



if __name__ == '__main__':
    app.run(debug=True)
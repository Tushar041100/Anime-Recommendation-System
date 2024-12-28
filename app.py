# from flask import Flask, render_template, request
# import pickle
# import numpy as np

# popular_anime = pickle.load(open('model/popular_anime.pkl', 'rb'))
# pivot_table = pickle.load(open('model/pivot_table.pkl', 'rb'))
# recommended_animes = pickle.load(open('model/animes.pkl', 'rb'))
# cosine_sim = pickle.load(open('model/cosine_sim.pkl', 'rb'))
# linear_sim = pickle.load(open('model/linear_sim.pkl', 'rb'))

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('index.html',
#                            Name = list(popular_anime['Name'].values),
#                            Rating = list(popular_anime['Rating'].values),
#                            Genres = list(popular_anime['Genres'].values),
#                            Synopsis = list(popular_anime['Synopsis'].values)
#                            )

# @app.route('/recommend')
# def recommend():
#     return render_template('recommend.html')

# @app.route('/recommend_animes', methods=['POST'])
# def recommend_animes():
#     user_input = request.form.get('user_input')
#     return render_template('recommend.html', user_input = user_input)

# @app.route('/content_based_recommendation', methods=['POST'])
# def content_based_recommendation():
#     input = request.get_json()
#     user_input = input.get('user_input')
#     idx = recommended_animes[recommended_animes['Name'] == user_input].index[0]
#     sim_scores = list(enumerate(linear_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:11]

#     data = []
#     for i in sim_scores:
#         item = []
#         temp_data = recommended_animes[recommended_animes['Name'] == recommended_animes.iloc[i[0]]['Name']]
#         item.append(temp_data['Name'].values[0])
#         item.append(temp_data['Genres'].values[0])
#         item.append(temp_data['Synopsis'].values[0])

#         data.append(item)
#     print(data)
#     return render_template('recommend.html', data = data)

# @app.route('/collaborative_based_recommendation', methods=['POST'])
# def collaborative_based_recommendation():
#     input = request.get_json()
#     user_input = input.get('user_input')
#     anime_id = get_anime_id(user_input)
#     idx = np.where(pivot_table.index == anime_id)[0][0]
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:11]

#     data = []
#     for i in sim_scores:
#         item = []
#         temp_data = recommended_animes[recommended_animes['Anime ID'] == pivot_table.index[i[0]]]
#         item.append(temp_data['Name'].values[0])
#         item.append(temp_data['Genres'].values[0])
#         item.append(temp_data['Synopsis'].values[0])

#         data.append(item)

#     return render_template('recommend.html', data = data)

# @app.route('/hybrid_based_recommendation', methods=['POST'])
# def hybrid_based_recommendation():
#     input = request.get_json()
#     user_input = input.get('user_input')
#     ## Content Based
#     idx = recommended_animes[recommended_animes['Name'] == user_input].index[0]
#     sim_scores = list(enumerate(linear_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:6]

#     data = []
#     for i in sim_scores:
#         content_based_recommend_animeitem = []
#         temp_data = recommended_animes[recommended_animes['Name'] == recommended_animes.iloc[i[0]]['Name']]
#         content_based_recommend_animeitem.append(temp_data['Name'].values[0])
#         content_based_recommend_animeitem.append(temp_data['Genres'].values[0])
#         content_based_recommend_animeitem.append(temp_data['Synopsis'].values[0])

#         data.append(content_based_recommend_animeitem)
            
#     ## Collaborative Based
#     anime_id = get_anime_id(user_input)
#     idx = np.where(pivot_table.index == anime_id)[0][0]
#     sim_scores = list(enumerate(cosine_sim[idx]))
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
#     sim_scores = sim_scores[1:6]

#     for i in sim_scores:
#         collaborative_based_recommend_anime = []
#         temp_data = recommended_animes[recommended_animes['Anime ID'] == pivot_table.index[i[0]]]
#         collaborative_based_recommend_anime.append(temp_data['Name'].values[0])
#         collaborative_based_recommend_anime.append(temp_data['Genres'].values[0])
#         collaborative_based_recommend_anime.append(temp_data['Synopsis'].values[0])

#         data.append(collaborative_based_recommend_anime)

#     return render_template('recommend.html', data = data)

# def get_anime_id(name):
#     return recommended_animes[recommended_animes['Name']==name]['Anime ID'].values[0]

# if __name__ == '__main__':
#     app.run(debug= True)

import logging
from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO)

popular_anime = pickle.load(open('model/popular_anime.pkl', 'rb'))
pivot_table = pickle.load(open('model/pivot_table.pkl', 'rb'))
recommended_animes = pickle.load(open('model/animes.pkl', 'rb'))
cosine_sim = pickle.load(open('model/cosine_sim.pkl', 'rb'))
linear_sim = pickle.load(open('model/linear_sim.pkl', 'rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                           Name=list(popular_anime['Name'].values),
                           Rating=list(popular_anime['Rating'].values),
                           Genres=list(popular_anime['Genres'].values),
                           Synopsis=list(popular_anime['Synopsis'].values)
                           )

@app.route('/recommend')
def recommend():
    return render_template('recommend.html')

@app.route('/recommend_animes', methods=['POST'])
def recommend_animes():
    user_input = request.form.get('user_input')
    return render_template('recommend.html', user_input=user_input)

@app.route('/content_based_recommendation', methods=['POST'])
def content_based_recommendation():
    input = request.get_json()
    user_input = input.get('user_input')
    
    if user_input not in recommended_animes['Name'].values:
        logging.error(f"Anime '{user_input}' not found in recommended_animes.")
        return jsonify({"error": "Anime not found"}), 404
    
    try:
        idx = recommended_animes[recommended_animes['Name'] == user_input].index[0]
        sim_scores = list(enumerate(linear_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
    except IndexError as e:
        logging.error(f"Index error: {e}")
        return jsonify({"error": "Index error"}), 500

    data = []
    for i in sim_scores:
        item = []
        temp_data = recommended_animes[recommended_animes['Name'] == recommended_animes.iloc[i[0]]['Name']]
        item.append(temp_data['Name'].values[0])
        item.append(temp_data['Genres'].values[0])
        item.append(temp_data['Synopsis'].values[0])
        data.append(item)
    
    logging.info(f"Recommended animes for '{user_input}': {data}")
    return render_template('recommend.html', data=data)

@app.route('/collaborative_based_recommendation', methods=['POST'])
def collaborative_based_recommendation():
    input = request.get_json()
    user_input = input.get('user_input')
    
    try:
        anime_id = get_anime_id(user_input)
        idx = np.where(pivot_table.index == anime_id)[0][0]
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        sim_scores = sim_scores[1:11]
    except IndexError as e:
        logging.error(f"Index error: {e}")
        return jsonify({"error": "Index error"}), 500

    data = []
    for i in sim_scores:
        item = []
        temp_data = recommended_animes[recommended_animes['Anime ID'] == pivot_table.index[i[0]]]
        item.append(temp_data['Name'].values[0])
        item.append(temp_data['Genres'].values[0])
        item.append(temp_data['Synopsis'].values[0])
        data.append(item)
    
    logging.info(f"Collaborative recommended animes for '{user_input}': {data}")
    return render_template('recommend.html', data=data)

@app.route('/hybrid_based_recommendation', methods=['POST'])
def hybrid_based_recommendation():
    input = request.get_json()
    user_input = input.get('user_input')
    
    if user_input not in recommended_animes['Name'].values:
        logging.error(f"Anime '{user_input}' not found in recommended_animes.")
        return jsonify({"error": "Anime not found"}), 404
    
    try:
        # Content-based recommendation
        idx_content = recommended_animes[recommended_animes['Name'] == user_input].index[0]
        sim_scores_content = list(enumerate(linear_sim[idx_content]))
        sim_scores_content = sorted(sim_scores_content, key=lambda x: x[1], reverse=True)
        sim_scores_content = sim_scores_content[1:6]
        
        # Collaborative-based recommendation
        anime_id = get_anime_id(user_input)
        idx_collab = np.where(pivot_table.index == anime_id)[0][0]
        sim_scores_collab = list(enumerate(cosine_sim[idx_collab]))
        sim_scores_collab = sorted(sim_scores_collab, key=lambda x: x[1], reverse=True)
        sim_scores_collab = sim_scores_collab[1:6]
    except IndexError as e:
        logging.error(f"Index error: {e}")
        return jsonify({"error": "Index error"}), 500

    data = []
    for i in sim_scores_content:
        item = []
        temp_data = recommended_animes[recommended_animes['Name'] == recommended_animes.iloc[i[0]]['Name']]
        item.append(temp_data['Name'].values[0])
        item.append(temp_data['Genres'].values[0])
        item.append(temp_data['Synopsis'].values[0])
        data.append(item)

    for i in sim_scores_collab:
        item = []
        temp_data = recommended_animes[recommended_animes['Anime ID'] == pivot_table.index[i[0]]]
        item.append(temp_data['Name'].values[0])
        item.append(temp_data['Genres'].values[0])
        item.append(temp_data['Synopsis'].values[0])
        data.append(item)
    
    logging.info(f"Hybrid recommended animes for '{user_input}': {data}")
    return render_template('recommend.html', data=data)

def get_anime_id(anime_name):
    try:
        anime_id = recommended_animes[recommended_animes['Name'] == anime_name]['Anime ID'].values[0]
        return anime_id
    except IndexError:
        logging.error(f"Anime ID for '{anime_name}' not found.")
        raise

if __name__ == '__main__':
    app.run(debug=True)
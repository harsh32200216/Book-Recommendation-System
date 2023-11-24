from flask import Flask, render_template, request
import pickle
from difflib import SequenceMatcher

popular = pickle.load(open('popular.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
sim_score = pickle.load(open('similarity_scores.pkl', 'rb'))

def recommend(book_name):
    ratio = 0
    index = -1
    for x,i in enumerate(pt.index):
        if(SequenceMatcher(None, book_name, i).ratio() > ratio):
            ratio = SequenceMatcher(None, book_name, i).ratio()
            index = x
    similar_items = sorted(list(enumerate(sim_score[index])), key = lambda x: x[1], reverse = True)[:8]
    data = []
    for i in similar_items:
        items = []
        temp = books[books['Book-Title'] == pt.index[i[0]]]
        temp = temp.drop_duplicates('Book-Title')
        items.append(temp['Book-Title'].values[0])
        items.append(temp['Book-Author'].values[0])
        items.append(temp['Image-URL-M'].values[0])
        data.append(items)
    return data

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',
                           book_name = list(popular['Book-Title'].values),
                           author = list(popular['Book-Author'].values),
                           image = list(popular['Image-URL-M'].values),
                           votes = list(popular['num-ratings'].values),
                           ratings = list(popular['avg-ratings'].values))

@app.route("/recommend")
def recommend_ui():
    return render_template('recommend.html')

@app.route("/recommend_books", methods = ['POST'])
def recommend_book():
    user_input = request.form.get('user_input')
    data = recommend(user_input)
    return render_template('recommend.html', data = data)

if __name__ == ('__main__'):
    app.run(debug = True)
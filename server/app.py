from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
CORS(app)

# Configuration for SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define your Movie model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    year = db.Column(db.Integer)

    def to_dict(self):
        return {'id': self.id, 'title': self.title, 'year': self.year}

# Define your routes
@app.route('/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movies_list = [movie.to_dict() for movie in movies]
    return jsonify(movies_list)

@app.route('/movies/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)
    if not movie:
        return jsonify({'error': 'Movie not found'}), 404
    return jsonify(movie.to_dict())

if __name__ == '__main__':
    app.run(port=5555)

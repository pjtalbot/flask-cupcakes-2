"""Flask app for Cupcakes"""


# Part Zero: Set Up
# Make a virtual environment and install the dependencies.

# Make your project a Git repo.

# Part One: Cupcake Model
# Create Cupcake model in models.py.

# It should have the following columns:

# id: a unique primary key that is an auto-incrementing integer
# flavor: a not-nullable text column
# size: a not-nullable text column
# rating: a not-nullable column that is a float
# image: a non-nullable text column. If an image is not given, default to https://tinyurl.com/demo-cupcake
# Make a database called cupcakes.

# Once you’ve made this, you can run our seed.py file to add a few sample cupcakes to your database.

from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "oh-so-secret"

    with app.app_context():
        connect_db(app)

    return app

app = Flask(__name__)





@app.route('/')
def root():
    """homepage"""

    return render_template("index.html")

@app.route('/api/cupcakes')
def list_cupcakes():

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=list_cupcakes)

@app.route('/api/cupcakes', methods=['POST'])
def create():
    data = request.json
    cupcake = Cupcake(
        flavor=data['flavor'],
        rating=data['rating'],
        size=data['size'],
        image=data['image'] or None
    )

    db.session.add(cupcake)
    db.session.commit()

    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):

    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data('flavor')
    cupcake.rating = data('rating')
    cupcake.size = data('size')
    cupcake.image = data('image')

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())

@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(id):

    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message=f"Deleted Cupcake id:{id}")

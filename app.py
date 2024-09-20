"""Flask app for Cupcakes"""
from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake
from flask_debugtoolbar import DebugToolbarExtension
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "oh-so-secret"

debug = DebugToolbarExtension(app)

connect_db(app)

@app.route('/')
def list_cupcakes():
    """Shows homepage - a list of cupcakes"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes = cupcakes )

@app.route('/api/cupcakes', methods = ["GET"])
def get_all_cupcakes():
    """returns JSON with all cupcakes in database"""
    cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes/<int:id>', methods = ["GET"])
def get_cupcake(id):
    """Returns JSON for one cupcake at a time """
    cupcake = Cupcake.query.get_or_404(id)
    return jsonify(cupcake=cupcake.serialize())

@app.route("/api/cupcakes/", methods = ["POST"])
def create_cupcake():
    """Create a new cupcake, return JSON, and add to DB """
    image = request.json.get('image') or 'https://tinyurl.com/demo-cupcake'   #This should ensure we always get an image, even if user doesnt add one we get the default. dont need to use .get() for the others cuz they are all required (not nullable) and cant be defaulted (cuz that doesnt logically make sense here)

    new_cupcake = Cupcake(flavor=request.json['flavor'], 
                          size=request.json['size'], 
                          rating=request.json['rating'], 
                          image=image)
    db.session.add(new_cupcake)
    db.session.commit()
    response_json = jsonify(cupcake = new_cupcake.serialize())
    return (response_json, 201)


@app.route('/api/cupcakes/<int:id>', methods = ["PATCH"])
def update_cupcake(id):
    """Updates a cupcake based on ID and respones with JSON of that update"""
    cupcake = Cupcake.query.get_or_404(id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    db.session.commit()
    return jsonify(cupcake = cupcake.serialize())

@app.route('/api/cupcakes/<int:id>', methods = ["DELETE"])
def delete_cupcake(id):
    """Deletes cupcake from the DB """
    cupcake = Cupcake.query.get_or_404(id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message = 'DELETED')

# app.py
from flask import Flask, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, validators

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)

# Step 1: Create Database & Model
class Pet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String)
    age = db.Column(db.Integer)
    notes = db.Column(db.String)
    available = db.Column(db.Boolean, nullable=False, default=True)

# Step 3: Create Add Pet Form
class AddPetForm(FlaskForm):
    name = StringField('Name', [validators.InputRequired()])
    species = StringField('Species', [validators.InputRequired(), validators.AnyOf(['cat', 'dog', 'porcupine'], message="Invalid species")])
    photo_url = StringField('Photo URL', [validators.Optional(), validators.URL()])
    age = IntegerField('Age', [validators.Optional(), validators.NumberRange(min=0, max=30)])
    notes = StringField('Notes')

# Step 2: Make Homepage Listing Pets
@app.route('/')
def index():
    pets = Pet.query.all()
    return render_template('index.html', pets=pets)

# Step 4: Create Handler for Add Pet Form
@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    form = AddPetForm()
    if form.validate_on_submit():
        pet = Pet(
            name=form.name.data,
            species=form.species.data,
            photo_url=form.photo_url.data,
            age=form.age.data,
            notes=form.notes.data
        )
        db.session.add(pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_pet.html', form=form)

# Step 6: Add Display/Edit Form
@app.route('/<int:pet_id>', methods=['GET', 'POST'])
def pet_detail(pet_id):
    pet = Pet.query.get_or_404(pet_id)
    form = AddPetForm(obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('pet_detail.html', pet=pet, form=form)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

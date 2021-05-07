from flask import Flask, request, render_template, flash, redirect
from models import db, connect_db, Pet
from flask_debugtoolbar import DebugToolbarExtension
from forms import AddPetForm, EditPetForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.drop_all()
db.create_all()

app.config['SECRET_KEY'] = 'passkey'
debug = DebugToolbarExtension(app)

#######
#routes
#######
@app.route('/')
def main():
    """main page redirects to /pets"""

    return redirect('/pets')

@app.route('/pets')
def pets():
    """displays as homepage"""

    pets = Pet.query.all()

    return render_template('home.html', pets=pets)

@app.route('/pets/add', methods=['GET', 'POST'])
def add():
    """Add pets form"""

    form = AddPetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data
        
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
        db.session.add(pet)
        db.session.commit()

        flash(f'Added {name}')
        return redirect('/pets')



    else:
        return render_template('add_form.html', form=form)

@app.route('/pets/<int:pet_id>')
def pet_page(pet_id):
    """pet infor page"""

    pet = Pet.query.get_or_404(pet_id)

    return render_template('pet_info.html', pet=pet)

@app.route('/pets/<int:pet_id>/edit', methods=['GET', 'POST'])
def pet_edit(pet_id):
    """edit pets form"""

    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)

    if form.validate_on_submit():
        
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()

        return redirect(f'/pets/{pet_id}')

    else:
        return render_template('add_form.html', form=form)
# Copyright 2024 <Votre nom et code permanent>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, session
from flask import render_template
from flask import g
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from werkzeug.utils import secure_filename
from .database import Database
from .utils.card_data import card_index_dict
from .utils import helpers
import os

# Thank you : https://flask.palletsprojects.com/en/stable/patterns/fileuploads/

UPLOAD_FOLDER = 'static\images\photo_animaux'


app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SECRET_KEY'] = 'ourbigsecret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        g._database = Database()
    return g._database


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.disconnect()


@app.route('/')
def index():
    animaux_dict = get_db()
    random_list_animaux = helpers.shuffle_animaux(animaux_dict)
    carousel = helpers.get_animals_carousel(random_list_animaux)
    session['random_list_animaux'] = random_list_animaux
    session['carousel'] = carousel
    return render_template('index.html', cards=card_index_dict, carousel=carousel)


@app.route('/api/get_animal_carousel')
def get_next_animal_carousel():
    animaux_db = get_db()
    random_list_animaux = session.get('random_list_animaux', [])
    carousel = session.get('carousel', [])
    recently_shown_ids = []
    
    if carousel:
        removed_item = carousel.pop(0)
        recently_shown_ids.append(removed_item["id"])

    session['carousel'] = carousel
    carousel_ids = [animal["id"] for animal in carousel]


    available = [
        animal["id"]
        for animal in random_list_animaux
        if animal["id"] not in recently_shown_ids and animal["id"] not in carousel_ids
    ]
    
    
    if available:
        next_animal = animaux_db.get_animal(available[0])
        carousel.append(next_animal)
    else:
        shuffle = helpers.shuffle_animaux(animaux_db)
        new_list_of_random_animals = get_next_animal_carousel(shuffle)
        session['random_list_animaux'] = new_list_of_random_animals
    
    session['carousel'] = carousel
    session['recently_shown'] = recently_shown_ids
    

    return carousel


@app.route("/adoption")
def page_adoption():


    animaux_db = get_db()
    animaux_une_race = animaux_db.get_race("chat")
    nb_animaux_by_race = len(animaux_une_race)

    print(nb_animaux_by_race)

    return render_template("page_adoption.html", pets=animaux_une_race, nbr=nb_animaux_by_race, race='chat')



@app.route("/adoption/<animal_type>")
def page_adoption_by_race(animal_type):

    animaux_db = get_db()
    animaux_une_race = animaux_db.get_race(animal_type)
    print(animaux_une_race)
    nb_animaux_by_race = len(animaux_une_race)
    print(nb_animaux_by_race)


    return render_template(f"adoption_{animal_type}.html", pets=animaux_une_race, nbr=nb_animaux_by_race, race=animal_type)

@app.route("/adoption/autre")
def page_adoption_autre():

    animaux_db = get_db()
    animaux_une_race = animaux_db.get_uncommon()
    print(animaux_une_race)
    nb_animaux_by_race = len(animaux_une_race)
    print(nb_animaux_by_race)
    
    return render_template(f"adoption_autre.html", pets=animaux_une_race, nbr=nb_animaux_by_race, race="autre")


    
@app.route("/reloger_un_animal")
def page_reloger():
    return render_template("formulaire_adoption.html")


@app.route("/animal_descr_page/<pet_id>")
def page_descr_animal(pet_id):
    animaux_db = get_db()
    pet = animaux_db.get_animal(pet_id)
    print("testing pet")
    print(pet)
    return render_template(f"animal_descr_page.html", fiche_animal = pet)


@app.route('/register_animal', methods=['POST'])
def register_animal():
        
        if request.method == 'POST':

            # Do I have my file?
            if 'photo' not in request.files:
                flash('No file part')
                return redirect('error_page_html')
            
            file = request.files['photo']

        if file and helpers.allowed_file(file.filename):
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                animal_db = get_db()
                petName = request.form.get('name')
                petAge = request.form.get('age')
                petPhoto = filename
                petRace = request.form.get('race')
                petEspece = request.form.get('espece')
                petDescription = request.form.get('description')
                ownerEmail = request.form.get('email')
                ownerAddress = request.form.get('address')
                ownerCity = request.form.get('city')
                ownerCp = request.form.get('cp')

                information_list = [petName, petAge, petPhoto, petRace, petEspece, petDescription, ownerEmail, ownerAddress, ownerCity, ownerCp]

                # Did I get all my pet data ?
                if any(information is None for information in information_list):
                    return render_template('error_page.html')
                else:
                    animal_db.add_animal(petName, petEspece, petRace, petAge, petDescription, ownerEmail, ownerAddress, ownerCity, ownerCp, petPhoto)

                    lastAnimalId = animal_db.get_last_animal()['id']
                return redirect(url_for('page_descr_animal', pet_id=lastAnimalId))
            except Exception as e:
                print(f"there's an error {e}")
                return render_template('error_page.html')

            

    



#         return redirect( url_for('page_descr_animal'))



    


    

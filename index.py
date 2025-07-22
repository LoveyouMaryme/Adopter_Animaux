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
from .database import Database
from .utils.card_data import card_index_dict
from .utils import helpers

app = Flask(__name__, static_url_path="", static_folder="static")
app.config['SECRET_KEY'] = 'ourbigsecret'



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

    
    


# class Animal: 
#     def __init__(self, id, nom, espece, race, age, description, courriel, adresse, ville, cp):
#         self.id = id
#         self.nom = nom
#         self.espece = espece
#         self.race = race
#         self.age = age
#         self.description = description
#         self.courriel = courriel
#         self.adresse = adresse
#         self.ville = ville
#         self.cp = cp
    
    # def __str__(self):
    #      card_pet_dict_element = {
        
    #     }

    #     return  card_pet_dict_element
    


    

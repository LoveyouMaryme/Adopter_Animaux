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

from flask import Flask
from flask import render_template
from flask import g
from .database import Database
from .utils.card_data import card_index_dict
from .utils import helpers

app = Flask(__name__, static_url_path="", static_folder="static")



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
    carousel = helpers.get_animals_carousel(animaux_dict)
    print(carousel)
    return render_template('index.html', cards=card_index_dict, carousel=carousel)



class Animal: 
    def __init__(self, id, nom, espece, race, age, description, courriel, adresse, ville, cp):
        self.id = id
        self.nom = nom
        self.espece = espece
        self.race = race
        self.age = age
        self.description = description
        self.courriel = courriel
        self.adresse = adresse
        self.ville = ville
        self.cp = cp
    
    # def __str__(self):
    #      card_pet_dict_element = {
        
    #     }

    #     return  card_pet_dict_element
    


    

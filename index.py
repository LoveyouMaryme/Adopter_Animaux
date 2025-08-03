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
import re
from flask import jsonify


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
    ANIMAUX_DB = get_db()
    random_list_animaux = helpers.shuffle_animaux(ANIMAUX_DB)
    carousel = helpers.get_animals_carousel(random_list_animaux)
    session['random_list_animaux'] = random_list_animaux
    session['carousel'] = carousel
    return render_template(
        'index.html',
        cards=card_index_dict,
        carousel=carousel
    )


@app.route('/api/get_animal_carousel')
def get_next_animal_carousel():
    ANIMAUX_DB = get_db()
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
        if (
            animal["id"] not in recently_shown_ids and
            animal["id"] not in carousel_ids)
    ]
    if available:
        next_animal = ANIMAUX_DB.get_animal(available[0])
        carousel.append(next_animal)
    else:
        shuffle = helpers.shuffle_animaux(ANIMAUX_DB)
        new_list_of_random_animals = get_next_animal_carousel(shuffle)
        session['random_list_animaux'] = new_list_of_random_animals
    session['carousel'] = carousel
    session['recently_shown'] = recently_shown_ids
    return carousel


@app.route("/adoption")
def page_adoption():
    ANIMAUX_DB = get_db()
    animaux_une_race = ANIMAUX_DB.get_espece("chat")
    nb_animaux_by_race = len(animaux_une_race)
    return render_template(
        "page_adoption.html",
        pets=animaux_une_race,
        nbr=nb_animaux_by_race, race='chat')


@app.route("/adoption/<animal_type>")
def page_adoption_by_race(animal_type):
    ANIMAUX_DB = get_db()
    animaux_une_race = ANIMAUX_DB.get_espece(animal_type)
    nb_animaux_by_race = len(animaux_une_race)
    return render_template(
        f"adoption_{animal_type}.html",
        pets=animaux_une_race,
        nbr=nb_animaux_by_race,
        race=animal_type)


@app.route("/adoption/autre")
def page_adoption_autre():
    ANIMAUX_DB = get_db()
    animaux_une_race = ANIMAUX_DB.get_uncommon()
    nb_animaux_by_race = len(animaux_une_race)
    return render_template(
        f"adoption_autre.html",
        pets=animaux_une_race,
        nbr=nb_animaux_by_race,
        race="autre")


@app.route("/reloger_un_animal")
def page_reloger():
    return render_template("formulaire_adoption.html")


@app.route("/animal_descr_page/<pet_id>")
def page_descr_animal(pet_id):
    ANIMAUX_DB = get_db()
    pet = ANIMAUX_DB.get_animal(pet_id)
    return render_template(
        f"animal_descr_page.html",
        fiche_animal=pet)


@app.route("/contactez_nous")
def page_contact():
    return render_template("contactez_nous.html")


@app.route("/recherche_avance")
def page_recherche_avance():
    ANIMAUX_DB = get_db()
    five_common_espece = ANIMAUX_DB.get_five_most_common_espece()
    list_espece = [espece[0] for espece in five_common_espece]
    print(list_espece)
    return render_template(
        "recherche_avance.html",
        especes=list_espece)


@app.route("/api/races", methods=["GET"])
def get_races_per_espece():
    ANIMAUX_DB = get_db()
    especes = request.args.getlist('especes')
    five_common_race = ANIMAUX_DB.get_five_most_common_race(especes)
    return jsonify(five_common_race)


@app.route("/api/results", methods=['GET'])
def get_results():
    ANIMAUX_DB = get_db()
    especes = request.args.getlist('especes')
    races = request.args.getlist('races')
    results = []

    if especes or races:
        results = ANIMAUX_DB.get_result_research(especes, races)
    return jsonify(results)


@app.route("/api/results_searchbar", methods=['GET'])
def get_results_from_searchbar():
    ANIMAUX_DB = get_db()
    filters = request.args.getlist('filters')

    results = ANIMAUX_DB.get_data_everywhere(filters)
    return jsonify(results)


@app.route('/register_animal', methods=['POST'])
def register_animal():
    ANIMAUX_DB = get_db()
    EMAIL_RX = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    CP_RX = r'^[A-Z]\d[A-Z]\s?\d[A-Z]\d$'
    ADDRESS_RX = r'^[0-9]+\s+[A-Za-zÀ-Ö\' -]+$'
    CITY_RX = r'^[A-Za-zÀ-Ö\' -]+$'

    try:
        pet_name = request.form.get('name')
        pet_age = int(request.form.get('age'))
        pet_race = request.form.get('race')
        pet_espece = request.form.get('espece')
        pet_description = request.form.get('description')
        owner_email = request.form.get('email')
        owner_address = request.form.get('address')
        owner_city = request.form.get('city')
        owner_cp = request.form.get('cp')
        information_list = [
            pet_name,
            pet_age,
            pet_race,
            pet_espece,
            pet_description,
            owner_email,
            owner_address,
            owner_city,
            owner_cp
        ]

        # Est-ce que j'ai reçu toutes les données de mon formulaire?
        if any(information is None for information in information_list):
            return redirect(url_for('error_page'))
        # Les vérifications des règles business
        valid = (
            pet_age >= 0 and pet_age <= 20 and
            len(pet_name) >= 3 and len(pet_name) <= 20 and
            re.fullmatch(EMAIL_RX, owner_email) and
            re.fullmatch(CP_RX, owner_cp) and
            re.fullmatch(ADDRESS_RX, owner_address) and
            re.fullmatch(CITY_RX, owner_city)
        )
        if not valid:
            return redirect(url_for('error_page'))
        ANIMAUX_DB.add_animal(
            pet_name,
            pet_espece,
            pet_race,
            pet_age,
            pet_description,
            owner_email,
            owner_address,
            owner_city,
            owner_cp)
        last_animal_id = ANIMAUX_DB.get_last_animal()['id']
        return redirect(url_for('page_descr_animal', pet_id=last_animal_id))
    except Exception as e:
        print(f"there's an error {e}")
        return redirect(url_for('error_page'))

@app.route('/error')
def error_page():
    return render_template('error_page.html')

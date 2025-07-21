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

    card_index_dict = card_index = [
        {
        "image_link" : "images/icons/finding-pet.png",
        "text" :  """Parmi tous ces regards, 
        il y a peut-être celui qui changera votre vie. 
        Parcourez nos compagnons à la recherche d’un foyer 
        et trouvez votre futur ami.""",
        "text_button" : "Trouvez votre ami"
    },
    {
        "image_link" : "images/icons/house-pet.png",
        "text" :  """Votre compagnon mérite un foyer aimant.
             Mettez-le en adoption dès aujourd’hui
            et permettez à une famille de le rencontrer.""",
        "text_button" : "Trouvez une maison"
    },
    {
        "image_link" : "images/icons/team.png",
        "text" :  """Rencontrez les humains au grand cœur qui veillent sur chaque compagnon.
Découvrez notre mission, nos valeurs, et les visages de ceux qui rendent tout cela possible.""",
        "text_button" : "Rencontrez-nous"
    }
    ]
    animaux_db = get_db()
    print(animaux_db.get_animaux())
    return render_template('index.html', card_index=card_index_dict)

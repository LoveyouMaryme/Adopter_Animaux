# Copyright 2022 Jacques Berger
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


import sqlite3


def _build_animal(result_set_item):
    animal = {}
    animal["id"] = result_set_item[0]
    animal["nom"] = result_set_item[1]
    animal["espece"] = result_set_item[2]
    animal["race"] = result_set_item[3]
    animal["age"] = result_set_item[4]
    animal["description"] = result_set_item[5]
    animal["courriel"] = result_set_item[6]
    animal["adresse"] = result_set_item[7]
    animal["ville"] = result_set_item[8]
    animal["cp"] = result_set_item[9]
    return animal


class Database:
    def __init__(self):
        self.connection = None

    def get_connection(self):
        if self.connection is None:
            self.connection = sqlite3.connect('db/animaux.db')
        return self.connection

    def disconnect(self):
        if self.connection is not None:
            self.connection.close()

    def get_animaux(self):
        cursor = self.get_connection().cursor()
        query = ("select id, nom, espece, race, age, description, "
                 "courriel, adresse, ville, cp from animaux")
        cursor.execute(query)
        all_data = cursor.fetchall()
        return [_build_animal(item) for item in all_data]
    
    def get_espece(self, animal_espece):
        cursor = self.get_connection().cursor()
        query = ("select id, nom, espece, race, age, description, "
                 "courriel, adresse, ville, cp from animaux where lower(espece) = ?" )
        cursor.execute(query, (animal_espece,))
        all_data = cursor.fetchall()
        if all_data is None:
            return all_data
        else:
            return [_build_animal(item) for item in all_data]
        
    def get_last_animal(self):
        cursor = self.get_connection().cursor()
        query = ("select  id, nom, espece, race, age, description, courriel, "
                 "adresse, ville, cp from animaux order by id desc limit 1")
        cursor.execute(query)
        item = cursor.fetchone()
        if item is None:
            return item
        else:
            return _build_animal(item)
        

    def get_five_most_common_espece(self):
        cursor = self.get_connection().cursor()
        query = ("""SELECT espece 
                    FROM (
                        SELECT espece, COUNT(*) AS cnt 
                        FROM animaux 
                        GROUP BY espece
                    ) AS subquery
                    ORDER BY cnt DESC 
                    LIMIT 5;""" )

        cursor.execute(query)
        all_data = cursor.fetchall()
        return all_data
    
    def get_five_most_common_race(self, especes):
        cursor = self.get_connection().cursor()

        placeholders = ','.join(['?'] * len(especes))

        if( '*' in especes):
            query = (f"""SELECT race 
                    FROM (
                        SELECT race, espece, COUNT(*) AS cnt 
                        FROM animaux
                        GROUP BY race, espece
                    ) AS subquery
                    ORDER BY cnt DESC
                    LIMIT 5""" )
            cursor.execute(query)
        else:
            query = (f"""SELECT race 
                    FROM (
                        SELECT race, espece, COUNT(*) AS cnt 
                        FROM animaux
                        WHERE lower(espece) IN ({placeholders})
                        GROUP BY race, espece
                    ) AS subquery
                    ORDER BY cnt DESC
                    LIMIT 5""" )

            especesList = [espece for espece in especes]
            cursor.execute(query, especesList)
        all_data = cursor.fetchall()
        return all_data


    def get_result_research(self, especes, races):
        cursor = self.get_connection().cursor()

        print("this is race")
        print(races)

        where_clauses = []
        parameters = []

    
        if("*" not in especes and especes):
            placeholders_espece = ','.join(['?'] * len(especes)) if especes else ''
            where_clauses.append(f"lower(espece) IN ({placeholders_espece})")
            parameters.extend(especes)

        if("*" not in races and races):
            placeholders_race = ','.join(['?'] * len(races)) if especes else ''
            where_clauses.append(f"lower(race) IN ({placeholders_race})")
            parameters.extend(races)

        where_statement = ""
        if where_clauses and len(where_clauses )>= 1:
            where_statement = "WHERE " + " AND ".join(where_clauses)
        else:
            where_statement= "WHERE ".join(where_clauses)

        print("this is where statement") 
        print(where_clauses)

        query = f"""
            SELECT nom, espece, race, ville
            FROM animaux
            {where_statement};
        """


        cursor.execute(query, parameters)
        all_data = cursor.fetchall()
        return all_data
    

    def get_data_everywhere(self, filters):
        cursor = self.get_connection().cursor()

        columns = ['nom', 'espece', 'race', 'description']
        clauses = []
        params  = []
        
        for f in filters:
            filter = f"%{f.lower()}%"
  
            for col in columns:
                clauses.append(f"lower({col}) LIKE ?")
                params.append(filter)


        where_sql = " OR ".join(clauses)
        query = f"""
            SELECT nom, espece, race, ville
            FROM animaux
         WHERE {where_sql}
            """
        
        cursor.execute(query, params)
        all_data = cursor.fetchall()
        return all_data


    def get_uncommon(self):
        cursor = self.get_connection().cursor()
        query = ("select id, nom, espece, race, age, description, "
                 "courriel, adresse, ville, cp from animaux "
                 "where lower(espece) NOT IN (?, ?, ?, ?, ?)")
        cursor.execute(query, ("chat", "chien", "rat", "souris", "hamster"))
        all_data = cursor.fetchall()
        if all_data is None:
            return all_data
        else:
            return [_build_animal(item) for item in all_data]

    def get_animal(self, animal_id):
        cursor = self.get_connection().cursor()
        query = ("select id, nom, espece, race, age, description, courriel, "
                 "adresse, ville, cp from animaux where id = ?")
        cursor.execute(query, (animal_id,))
        item = cursor.fetchone()
        if item is None:
            return item
        else:
            return _build_animal(item)

    def add_animal(self, nom, espece, race, age, description, courriel,
                   adresse, ville, cp):
        connection = self.get_connection()
        query = ("insert into animaux(nom, espece, race, age, description, "
                 "courriel, adresse, ville, cp) "
                 "values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")
        connection.execute(query, (nom, espece, race, age, description,
                                   courriel, adresse, ville, cp))
        cursor = connection.cursor()
        cursor.execute("select last_insert_rowid()")
        lastId = cursor.fetchone()[0]
        connection.commit()
        return lastId

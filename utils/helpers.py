from flask import Flask
from flask import render_template
from flask import g
from ..database import Database
from ..utils.card_data import card_index_dict
import math
import random



def get_animals_carousel(db):
    
    """
    Description : Select the animals that will start the  in the index page

    """
    
    list_animaux = db.get_animaux()
    num_animaux = len(list_animaux)
    num_carousel = random.randrange(num_animaux - 1)
    num_picked = 0
    picked_animals = []

    
    while num_picked < 5:
        animal = list_animaux[num_carousel]
        picked_animals.append(animal)
  

        num_carousel += 1
        num_picked += 1

        if (num_carousel >= len(list_animaux)):
            num_carousel = 0
            
        
    return picked_animals
        
        




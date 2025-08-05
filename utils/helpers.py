from flask import Flask
from flask import render_template
from flask import g
from ..database import Database
from ..utils.card_data import card_index_dict
import random


def shuffle_animaux(db):
    list_animaux = db.get_animaux()
    random_list_animaux = random.sample(list_animaux, len(list_animaux))
    return random_list_animaux


def get_animals_carousel(shuffle_animaux):
    picked_animals = shuffle_animaux[0: 5]
    return picked_animals


def next_animal_in_carousel(animal_dict, recently_shown_animals):
    next_animal_id = [
        animal["id"]
        for animal
        in animal_dict
        if animal not in recently_shown_animals][0]
    return next_animal_id


def history_picked_animals(picked_animals):
    animal_id = []
    for id in picked_animals:
        animal_id.append(id["id"])
    return animal_id


def get_animals_carousel_from_index(animals_list, start_index):
    carousel = []
    num_animals = len(animals_list)
    for i in range(5):
        index = (start_index + i) % num_animals
        carousel.append(animals_list[index])
    return carousel

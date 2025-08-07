from flask import Flask
from flask import render_template
from flask import g
from ..database import Database
from ..utils.card_data import card_index_dict
import random
import re


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


def are_informations_valid(
        pet_age,
        pet_name,
        owner_email,
        owner_cp,
        owner_address,
        owner_city):
    EMAIL_RX = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    CP_RX = r"^[A-Z]\d[A-Z]\s?\d[A-Z]\d$"
    ADDRESS_RX = r"^[0-9]+\s+[A-Za-zÀ-Ö\' -]+$"
    CITY_RX = r"^[A-Za-zÀ-Ö\' -]+$"

    valid = (
            pet_age >= 0
            and pet_age <= 20
            and len(pet_name) >= 3
            and len(pet_name) <= 20
            and re.fullmatch(EMAIL_RX, owner_email)
            and re.fullmatch(CP_RX, owner_cp)
            and re.fullmatch(ADDRESS_RX, owner_address)
            and re.fullmatch(CITY_RX, owner_city)
        )
    return valid

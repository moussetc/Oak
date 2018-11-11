#!/usr/bin/env python3

import re
from names import POKEMON
import db
from utils import logger

from typing import List, Optional
from google.cloud import vision
from google.cloud.vision import types
from fuzzywuzzy import process

time_pattern = re.compile('[0-9]+:[0-9]+:[0-9]+')

def build_image_url(image_url):
    source = types.ImageSource(image_uri=image_url)
    image = types.Image(source=source)
    return image


def build_image_file(image_file):
    with open(file_name, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    return image


def detect_text(image_url) -> List[str]:
    image = build_image_url(image_url)
    client = vision.ImageAnnotatorClient()
    response = client.text_detection(image=image)
    return response.text_annotations[0].description.split('\n')


def find_raid_fields(elements: List[str]):
    """
    Tries to find raid boss, raid time and raid gym in given string elements
    """
    boss = None
    time = None
    gym = None
    for e in elements:
        if len(e) < 3:
            # Ignore small text fragments to avoid false-positive matches
            continue
        if time_pattern.search(e) is not None:
            time = e
            break
        pokemon_match = find_pokemon(e)
        if pokemon_match is not None:
            boss = pokemon_match
            continue
        gym_match = find_fuzzy(e, db.all_gyms, 90)
        if gym_match is not None:
            gym = gym_match
    return {'boss': boss, 'time': time, 'gym': gym}

def find_fuzzy(text: str, text_options: List[str], score_cutoff: int) -> Optional[str]:
    """
    Find the best approximate match for a string in a list of strings.
    """
     # First, try to find exact match
    if text in text_options:
        return text
    else:
        # Then, try to find a close match 
        match = process.extractOne(text, text_options, score_cutoff=score_cutoff)
        #logger.debug('searching for "%s", finding "%s"', str(text), str(match))
        if match is not None:
            return match[0]
        return None
    

def find_pokestop(elements: List[str])-> Optional[str]:
    """
    Return the name of the 1st pokestop that matches one of the input strings in elements.
    """
    for e in elements:
        match = find_fuzzy(e, db.all_pokestops, 90)
        if match is not None:
            return match
    return None

def find_pokemon(text: str)-> Optional[str]:
    """
    Return the name of the 1st pokemon that matches a given string.
    """
    for language in POKEMON:
        pokemon_match = find_fuzzy(text, POKEMON[language].values(), 80) 
        if pokemon_match is not None:
            return pokemon_match
    return None

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Process text recognition')
    parser.add_argument('--image', '-i', help='Input image')
    args = parser.parse_args()

    run_quickstart(args.image)


if __name__ == '__main__':
    main()

